"""
Asyncio Crawler Support
"""

import asyncio
from asyncio.queues import Queue
from collections import deque
import queue
import random
import re
import os
import sys
import traceback
from typing import Dict, Any, Callable
import yaml
import time
from pprint import pformat
import aiohttp


from agptools.helpers import expandpath, I, parse_uri, build_uri
from agptools.progress import Progress
from agptools.containers import (
    walk,
    myassign,
    rebuild,
    SEP,
    list_of,
    overlap,
    soft,
    build_paths,
)

from syncmodels.syncmodels import SyncModel, COPY

# ---------------------------------------------------------
# Loggers
# ---------------------------------------------------------
from agptools.logs import logger

log = logger(__name__)


DEFAULT = "__default__"
UNKNOWN = "__unknown__"


SINGLE = "single"  # single stream subtype element, not a list
REG_KIND = r"(?P<parent>[^-]*)(-(?P<sub>.*))?$"


# ---------------------------------------------------------
# Agent
# ---------------------------------------------------------
class iAgent:
    "the minimal interface for an agent in crawler module"

    def __init__(self, config_path=None, name="", include=None, exclude=None):
        name = name or f"uid:{random.randint(1, 1000)}"
        self.name = name
        # tasks to be included or excluded
        self.include = include or [".*"]
        self.exclude = exclude or []

        self.progress = Progress(label=self.name)

        if not config_path:
            config_path = "config.yaml"
        config_path = expandpath(config_path)
        self.root = os.path.dirname(config_path)
        self.stats_path = os.path.join(self.root, "stats.yaml")

        if not config_path:
            config_path = "config.yaml"
        config_path = expandpath(config_path)

        try:
            with open(config_path, "rt", encoding="utf-8") as f:
                self.cfg = yaml.load(f, Loader=yaml.Loader)
        except Exception:
            self.cfg = {}

    def __str__(self):
        return f"<{self.__class__.__name__}>:{self.name}"

    def __repr__(self):
        return str(self)

    async def run(self):
        "agent's initial setup"
        await self._create_resources()
        await self.bootstrap()

    async def bootstrap(self):
        "Add the initial tasks to be executed by crawler"
        log.info(">> [%s] entering bootstrap()", self.name)

        for func, args, kwargs in self._bootstrap():
            log.info("+ [%s] %s(%s, %s)", self.name, func, args, kwargs)
            self.add_task(func, *args, **kwargs)
        log.info("<< [%s] exit bootstrap()", self.name)

    # async def bootstrap(self):
    # "Add the initial tasks to be executed by crawler"

    def _bootstrap(self):
        "Provide the initial tasks to ignite the process"
        return []

    def add_task(self, func, *args, **kw):
        "add a new pending task to be executed by this iAgent"
        raise NotImplementedError()

    async def _create_resources(self):
        "create/start the agent's resources needed before starting"

    async def _stop_resources(self):
        "stop/release the agent's resources on exit"


# ---------------------------------------------------------
# iPlugin
# ---------------------------------------------------------
class iPlugin:
    "A pluging that manipulate received data before giving to main crawler"
    SPECS = {}

    def __init__(self, bot=None, specs=None):
        self.bot = bot
        specs = {} if specs is None else specs
        self.specs = overlap(specs, self.SPECS, overwrite=True)
        self.stats = {}

    def handle(self, data, **context):
        return data, context

    @classmethod
    def matches(self, serie, *patterns):
        for string in serie:
            string = str(string)
            for pattern in patterns:
                if re.match(pattern, string):
                    yield string


class iPostPlugin(iPlugin):
    """Plugins that must be executed at the end of process just once"""

    SPECS = {
        **iPlugin.SPECS,
    }


class iEachPlugin(iPlugin):
    """Plugins that must be executed for each data received"""

    SPECS = {
        **iPlugin.SPECS,
    }


# ---------------------------------------------------------
# Bot
# ---------------------------------------------------------
class iBot(iAgent):
    "Interface for a bot"
    MAX_QUEUE = 200
    DONE_TASKS = {}  # TODO: review faster method

    def __init__(self, result_queue: Queue, parent=None, context=None, *args, **kw):
        super().__init__(*args, **kw)
        self.result_queue = result_queue
        self.fiber = None
        self.task_queue = asyncio.queues.Queue()
        self._wip = []
        self.plugins = {}
        self.parent = parent

        context = context or {}
        self.context = {
            **context,
            **kw,
        }
        # add plugins
        self.add_plugin(Cleaner())

    def add_plugin(self, plugin: iPlugin):
        for klass in iEachPlugin, iPostPlugin:
            if isinstance(plugin, klass):
                self.plugins.setdefault(klass, []).append(plugin)
        if not plugin.bot:
            plugin.bot = self

    def process(self, klass, data, **context):
        for plugin in self.plugins.get(klass, []):
            data, context = plugin.handle(data, **context)
        return data, context

    def add_task(self, func, *args, **kw):
        "add a new pending task to be executed by this iBot"
        universe = list(kw.values()) + list(args)

        def check():
            for string in universe:
                string = str(string)
                for pattern in self.include:
                    if re.match(pattern, string):
                        return True
                for pattern in self.exclude:
                    if re.match(pattern, string):
                        return False

        if check():
            if isinstance(func, str):
                # must be processed by parent
                if self.parent:
                    self.parent.add_task(func, *args, **kw)
                else:
                    log.warning(
                        "[%s] hasn't parent trying to process: %s(%s, %s)",
                        self.name,
                        func,
                        args,
                        kw,
                    )
            else:
                # process itself
                self.task_queue.put_nowait((func, args, kw))

    async def run(self):
        "the entry point / main loop of a single `fiber` in pool"
        progress = Progress(label=self.name)

        log.info(">> [%s] entering run()", self.name)
        await super().run()

        while True:
            try:
                while (pending := self.result_queue.qsize()) > self.MAX_QUEUE:
                    print(
                        f"Pause worker due too much results pending in queue: {pending}"
                    )
                    await asyncio.sleep(1)
                progress.update(pending=pending)

                # Get a task from the queue
                task = await asyncio.wait_for(self.task_queue.get(), timeout=5)
                if task is None:
                    break  # Break the loop
                try:
                    self._wip.append(1)
                    func, args, kwargs = task
                    # print(f">> Processing task: {args}: {kwargs}")
                    if isinstance(func, str):
                        func = getattr(self, func)
                    assert isinstance(func, Callable)
                    async for data in func(*args, **kwargs):
                        item = task, data
                        await self.result_queue.put(item)
                except Exception as why:
                    log.error(why)
                    log.error("".join(traceback.format_exception(*sys.exc_info())))
                finally:
                    self._wip.pop()
                # print(f"<< Processing task: {func}")
            except queue.Empty:
                pass
            except asyncio.exceptions.TimeoutError:
                pass
            except Exception as why:
                log.error(why)
                log.error("".join(traceback.format_exception(*sys.exc_info())))

        log.info("<< [%s] exit run()", self.name)

    async def dispatch(self, task, data, *args, **kw):
        "do nothing"
        log.info(" - dispatch: %s: %s ; %s, %s", task, data, args, kw)

    def remain_tasks(self):
        "compute how many pending tasks still remains"
        return len(self._wip) + self.task_queue.qsize()


# ---------------------------------------------------------
# Helper Plugins
# ---------------------------------------------------------
class Cleaner(iEachPlugin):
    SPECS = {
        **iEachPlugin.SPECS,
    }

    def handle(self, data, **context):
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = v.strip()
        return data, context


class RegExtractor(iEachPlugin):
    # example for gitLab
    SPECS = {
        **iEachPlugin.SPECS,
    }

    def handle(self, data, **context):
        # TODO: review
        # TODO: create a reveal + regexp + SEP ?

        aux = {**data, **context}
        values = list([aux[x] for x in self.matches(aux, "path")])

        # for key in self.matches(aux, "kind"):
        # kind = aux[key]
        for regexp in self.specs:
            for value in values:
                m = re.match(regexp, value)
                if m:
                    data.update(m.groupdict())
        return data, context


class Restructer(iEachPlugin):
    # example for gitLab
    SPECS = {
        **iEachPlugin.SPECS,
    }

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__mask_restruct_data()

    def __mask_restruct_data(self):
        for container in self.specs.values():
            for k in list(container):
                v = container.pop(k)
                k = k.replace("/", SEP)
                v = tuple([v[0].replace("/", SEP), *v[1:]])
                container[k] = v

    def handle(self, data, **context):
        restruct = {}
        kind = context.get("kind", UNKNOWN)
        info = self.specs.get("default", {})
        info.update(self.specs.get(kind, {}))
        reveal = build_paths(data)
        for path, value in reveal.items():
            for pattern, (new_path, new_value) in info.items():
                m = re.match(pattern, path)
                if m:
                    d = m.groupdict()
                    d["value"] = value
                    key = tuple(new_path.format_map(d).split(SEP))
                    _value = value if new_value == COPY else new_value.format_map(d)
                    restruct[key] = _value

        restruct = rebuild(restruct, result={})
        data = {**data, **restruct}

        return data, context


class FQIUD(iEachPlugin):
    SPECS = {
        **iEachPlugin.SPECS,
        "root": ("{url}", I, "url"),
        # 'groups': ("{id}", int, 'id'),
    }

    def handle(self, data, **context):
        patterns = context.get("kind_key", "kind")
        for key in self.matches(data, patterns):
            kind = data[key]
            for specs in self.specs.get(kind, []):
                if not specs:
                    continue
                uid_key, func, id_key = specs
                try:
                    uid = uid_key.format_map(data)
                    fquid = func(uid)
                    data[id_key] = fquid
                    data["_fquid"] = fquid
                    data["_uid"] = uid
                    return data
                except Exception as why:
                    # TODO: remove, just debuging
                    log.error(why)
                    log.error("".join(traceback.format_exception(*sys.exc_info())))
        return data, context


class Tagger(iEachPlugin):
    SPECS = {
        **iEachPlugin.SPECS,
    }

    def handle(self, data, **context):
        return data, context


class DeepSearch(iEachPlugin):
    SPECS = {
        **iEachPlugin.SPECS,
    }

    def handle(self, data, **context):
        aux = {**data, **context}
        patterns = aux.get("kind_key", "kind")

        for key in self.matches(aux, patterns):
            kind = aux.get(key)
            for specs in self.specs.get(kind, []):
                if not specs:
                    continue
                try:
                    sub_kind, sub_url = specs
                    sub_url = sub_url.format_map(aux)
                    aux[key] = sub_kind
                    aux["path"] = sub_url

                    self.bot.add_task(
                        func="get_data",
                        **aux,
                    )
                except Exception as why:
                    # TODO: remove, just debuging
                    log.error(why)
                    log.error("".join(traceback.format_exception(*sys.exc_info())))

        return data, context


class PaginationDisabled:
    "represent no pagination for an item"


class iPaginationPlugin(iPostPlugin):
    PER_PAGE = "per_page"

    MAX_PAGES = "max_pages"
    FIRST_PAGE = "first_page"
    AHEAD_PAGES = "ahead_pages"
    PAGE = "page"

    FIRST_ITEM = "first_item"
    MAX_ITEMS = "max_items"
    OFFSET = "offset"


class GenericPagination(iPaginationPlugin):

    SPECS = {
        **iPostPlugin.SPECS,
        **{
            DEFAULT: {
                iPaginationPlugin.MAX_ITEMS: "count",
                iPaginationPlugin.MAX_PAGES: "max_pages",
                iPaginationPlugin.OFFSET: "offset",
                iPaginationPlugin.PER_PAGE: "limit",
                iPaginationPlugin.FIRST_ITEM: 0,
            },
            "gitlab": {
                iPaginationPlugin.PAGE: "page",
                iPaginationPlugin.PER_PAGE: "per_page",
                iPaginationPlugin.FIRST_PAGE: 1,
                iPaginationPlugin.AHEAD_PAGES: 1,
            },
        },
    }

    def handle(self, data, **context):
        "Request the next pagination (just the next one!)"

        for name, spec in self.specs.items():
            page = int(context.get(spec[self.PAGE], -1))
            per_page = int(context.get(spec[self.PER_PAGE], 50))
            if context.get(spec.get(self.MAX_ITEMS), -1) < page * per_page:
                page = max(page, spec.get(self.FIRST_PAGE, 0))
                for batch in range(spec.get(self.AHEAD_PAGES, 1)):
                    context[spec[self.PAGE]] = page + 1
                    ##log.debug("> request: %s", context)
                    self.bot.add_task(
                        func="get_data",  # TODO: extract from context
                        # **data,
                        **context,
                    )
                break
        return data, context


class SimplePagination(iPaginationPlugin):
    """
    kind: specs_for_this_kind

    used: kind: [] to explicit avoid pagination
    DEFAULT: a default pagination when no other is defined
    """

    SPECS = {
        # **iPostPlugin.SPECS, # don't use base class
        **{
            DEFAULT: {
                iPaginationPlugin.PAGE: "page",
                iPaginationPlugin.PER_PAGE: "per_page",
                iPaginationPlugin.FIRST_PAGE: 1,
                iPaginationPlugin.AHEAD_PAGES: 1,
            },
            # "groups": {},
            # "projects": {},
            # "users": {},
            # "wikis": {},
            # "issues": {},
            # "milestones": {},
            # "notes": {},
        },
    }

    def handle(self, data, **context):
        "Request the next pagination"
        kind = context.get("kind", UNKNOWN)
        spec = self.specs.get(kind, self.specs.get(DEFAULT))

        # poi and poi-single
        d = re.match(REG_KIND, kind).groupdict()
        if spec == PaginationDisabled or d["sub"] in (SINGLE,):
            # single items doesn't use pagination
            ##log.debug("skip pagination for '%s'", kind)
            # remove parent pagination context
            kind = d["parent"]
            spec = self.specs.get(kind, self.specs.get(DEFAULT))
            if spec:
                foo = 1
            for k in spec.values():
                context.pop(k, None)
            foo = 1
        else:
            ##log.debug("for '%s' use pagination: %s", kind, spec)
            ##log.debug("page: %s, per_page: %s", page, per_page)

            # we have 2 options: pagintatin based on pages or based on num items
            per_page = int(context.get(spec.get(self.PER_PAGE), 20))
            max_items = context.get(spec.get(self.MAX_ITEMS))
            page = context.get(spec.get(self.PAGE))
            if max_items is not None:
                offset = int(context.get(spec.get(self.OFFSET), -1))
                offset = max(offset, spec.get(self.FIRST_ITEM, 0))
                if max_items > offset:
                    for batch in range(spec.get(self.AHEAD_PAGES, 1)):
                        context[spec[self.OFFSET]] = offset + per_page
                        ##log.debug("> request page: [%s]:%s", kind, context.get(spec[self.PAGE], -1))
                        self.bot.add_task(
                            func="get_data",  # TODO: extract from context
                            # **data,
                            **context,
                        )

            elif page is not None:
                page = max(offset, spec.get(self.FIRST_PAGE, 0))
                max_pages = max(page, spec.get(self.MAX_PAGES, sys.float_info.max))

                if max_pages >= page:
                    for batch in range(spec.get(self.AHEAD_PAGES, 1)):
                        context[spec[self.PAGE]] = page + per_page
                        ##log.debug("> request page: [%s]:%s", kind, context.get(spec[self.PAGE], -1))
                        self.bot.add_task(
                            func="get_data",  # TODO: extract from context
                            # **data,
                            **context,
                        )

            else:
                log.debug("no pagination info found")

        return data, context


# ---------------------------------------------------------
# Basic Bots
# ---------------------------------------------------------


class HTTPBot(iBot):
    "Basic HTTPBot"
    RESPONSE_META = ["headers", "links", "real_url"]
    MAX_RETRIES = 15
    DEFAULT_PARAMS = {}
    ALLOWED_PARAMS = [".*"]

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        # self.add_plugin(RegExtractor())
        # self.add_plugin(Cleaner())
        # self.add_plugin(FQIUD())
        # self.add_plugin(DeepSearch())
        # self.add_plugin(SimplePagination())
        self.headers = {
            "User-Agent": "python-httpbot/0.1.0",
            "Content-type": "application/json",
            # "Authorization": f"Bearer {personal_access_token}",
        }

    async def get_data(self, **context):
        """
        Example a crawling function for recommender crawler.

        Get data related to the given kind and path.
        May add more tasks to be done by crawler.
        """
        context = {
            # "limit": 50,
            # "offset": 0,
            **context,
        }
        # method to gather the information from 3rd system
        stream, meta = await self._get_data(**context)
        if not stream:
            return

        if isinstance(stream, list):
            ##log.debug("received (%s) items of type '%s'", len(stream), context['kind'])
            pass
        else:
            ##log.debug("received a single items of type: '%s'", context['kind'])
            stream = [stream]

        context.update(meta)
        for _, org in enumerate(stream):
            # data = {**data, **org}
            data = {**org}
            data, ctx = self.process(iEachPlugin, data, **context)

            yield data, (ctx, org)
            # await asyncio.sleep(0)  # to be nice with other fibers
            ##log.debug("[%s]:[%s]#%s: processed", i, context['kind'], data.get('id', '-'))

        # params['offset'] = (page := page + len(result))
        data, context = self.process(iPostPlugin, data, **context)

    def _build_params(self, **context):
        params = {}

        def match(text) -> bool:
            for pattern in self.ALLOWED_PARAMS:
                if re.match(pattern, text):
                    return True
            return False

        for k, v in context.items():
            if match(k) and isinstance(v, (int, str, float)):
                params[k] = v
        return params

    async def _get_data(self, path, **context):
        "A helper method to get the data from external system"

        soft(context, self.DEFAULT_PARAMS)
        params = self._build_params(**context)

        uri = parse_uri(path)
        if not uri["host"]:
            uri2 = self.context["app_url"]  # must exists!
            uri2 = parse_uri(uri2)
            uri["path"] = uri2["path"] = (uri2["path"] or "") + uri["path"]
            uri = overlap(uri2, uri, overwrite=True)
        uri["query_"] = params

        url = build_uri(**uri)
        # print(url)
        if self._is_already(url):
            ##log.info("[%s] SKIPING %s : %s", self.name, url, params)
            foo = 1
        else:
            self._set_already(url)
            try:
                for tries in range(1, self.MAX_RETRIES):
                    try:
                        async with aiohttp.ClientSession() as session:
                            # log.debug(
                            # "[%s][%s/%s] %s : %s", self.name, tries, self.MAX_RETRIES, url, params
                            # )
                            async with session.get(
                                url, headers=self.headers, params=params
                            ) as response:
                                if response.status in (200,):
                                    stream, meta = await self._process_response(
                                        response
                                    )
                                    soft(meta, params)
                                    return stream, meta
                                elif response.status in (400, 404):
                                    ##log.debug("%s: %s: %s", response.status, path, params)
                                    # result = await response.json()
                                    # log.error("server sent: %s", result)
                                    break
                                else:
                                    log.error("Status: %s", response.status)
                    except Exception as why:
                        log.error(why)
                        log.error("".join(traceback.format_exception(*sys.exc_info())))
                    log.warning("retry: %s: %s, %s", tries, path, params)
                    await asyncio.sleep(0.5)
            finally:
                # self._set_already(url)
                pass
        return None, None

    def _is_already(self, url):
        return url in self.DONE_TASKS

    def _set_already(self, url):
        if not self._is_already(url):
            self.DONE_TASKS[url] = time.time()
            return True
        return False

    async def _process_response(self, response):
        def expand(value):
            iterator = getattr(value, "items", None)
            if iterator:
                value = {k: expand(v) for k, v in iterator()}
            return value

        meta = {
            k: expand(getattr(response, k, None))
            for k in self.RESPONSE_META
            if hasattr(response, k)
        }

        # str(meta['links']['next']['url'])
        # first, next, last

        stream = await response.json()
        return stream, meta


# ---------------------------------------------------------
# Crawler
# ---------------------------------------------------------
class iCrawler(iAgent):
    "Interface for a crawler"
    bots: Dict[Any, iBot]

    def __init__(self, syncmodel: SyncModel, raw_storage=None, *args, **kw):
        super().__init__(*args, **kw)
        self.bot = {}
        self.round_robin = deque()
        self.result_queue = Queue()

        self.stats = {}
        self.show_stats = True

        self.syncmodel = list_of(syncmodel, SyncModel)
        self.raw_storage = raw_storage

    async def run(self) -> bool:
        """TBD"""
        await super().run()

    def add_task(self, func, *args, **kw):
        "add a new pending task to be executed by a bot that match the profile"
        assert isinstance(func, str), f"'func' must be a function name, not {func}"

        candidates = self.round_robin
        for _ in range(len(candidates)):
            candidates.rotate(-1)
            bot = candidates[-1]
            if call := getattr(bot, func):
                bot.add_task(call, *args, **kw)
                break
        else:
            log.warning("can't find a calleable for `%s` in (%s) bots", len(candidates))

    def remain_tasks(self):
        "compute how many pending tasks still remains"
        n = self.result_queue.qsize()
        for bot in self.bot.values():
            n += bot.remain_tasks()
        return n


class iAsyncCrawler(iCrawler):
    """A crawler that uses asyncio"""

    # need to be redefined by subclass
    MODEL = None
    BOTS = [HTTPBot]

    # governance data
    MAPPERS = {}
    RESTRUCT_DATA = {}
    RETAG_DATA = {}
    REFERENCE_MATCHES = []
    KINDS_UID = {}

    def __init__(self, fibers=3, *args, **kw):
        super().__init__(*args, **kw)
        self.fibers = fibers
        self.t0 = 0
        self.t1 = 0
        self.nice = 300
        self.model = self.MODEL()

    async def run(self) -> bool:
        """Execute a full crawling loop"""
        await super().run()

        # Create a worker pool with a specified number of 'fibers'
        self.t0 = time.time()
        self.t1 = self.t0 + self.nice

        # wait until all work is done
        while remain := self.remain_tasks():
            try:
                # result = await asyncio.wait_for(self.result_queue.get(), timeout=2)
                # result = await self.result_queue.get()
                result = await asyncio.wait_for(self.result_queue.get(), timeout=2)
                res = await self.dispatch(*result)
                if not res:
                    log.warning("Can't save item in storage: %s", result[0][2])
                    log.warning("%s", pformat(result[1]))
                    foo = 1
            except queue.Empty:
                pass
            except asyncio.exceptions.TimeoutError:
                pass
            except Exception as why:
                log.error(why)
                log.error("".join(traceback.format_exception(*sys.exc_info())))

            self.progress.update(
                remain=remain,
                stats=self.stats,
                force=False,
            )

        await self._stop_resources()
        result = all([await sync.save(wait=True) for sync in self.syncmodel])
        if result:
            log.info("all storages have been saved")
        else:
            log.error("some storages have NOT been SAVED")

        return result

    async def dispatch(self, task, data, *args, **kw):
        "create an item from data and try to update into storage"
        func, _args, _kw = task
        # _kw: {'kind': 'groups', 'path': '/groups?statistics=true'}
        # data:  {'id': 104, ... }
        kind = _kw["kind"]
        # uid = self.get_uid(kind, data)

        data, (context, org) = data

        # inject item into models
        item = self.new(kind, data)
        if item is None:
            result = False
        else:
            # result = await self.syncmodel.put(item)
            result = all([await sync.put(item) for sync in self.syncmodel])

            # save original item if a raw storage has been specified
            if self.raw_storage:
                fqid = item.id
                await self.raw_storage.put(fqid, org)

            # check if we need to do something from time to time
            t1 = time.time()
            if t1 > self.t1:
                self.t1 = t1 + self.nice
                await self.save(nice=True)

        return result

    async def save(self, nice=False, wait=False):
        log.info("Saving models")
        all([await sync.save(nice=nice, wait=wait) for sync in self.syncmodel])
        if self.raw_storage:
            await self.raw_storage.save(nice=nice, wait=wait)

    async def _create_resources(self):
        BOTS = deque(self.BOTS)

        for n in range(self.fibers):
            BOTS.rotate()
            klass = BOTS[-1]
            name = f"{klass.__name__.lower()}-{n}"
            bot = klass(
                result_queue=self.result_queue,
                name=name,
                parent=self,
                context=self.__dict__,
            )
            self.add_bot(bot)

    def add_bot(self, bot: iBot):
        self.bot[bot.name] = bot
        self.round_robin.append(bot)
        loop = asyncio.get_running_loop()
        bot.fiber = loop.create_task(bot.run())

    async def _stop_resources(self):
        # Add sentinel values to signal worker threads to exit
        for nane, bot in self.bot.items():
            bot.task_queue.put_nowait(None)

        # Wait for all worker threads to complete
        # for worker in self.workers:
        # worker.join()

    def convert_into_references(self, data):
        """Search for nested objects in `value` and convert them into references"""
        if self.REFERENCE_MATCHES:
            id_keys = list(
                walk(
                    data,
                    keys_included=self.REFERENCE_MATCHES,
                    include_struct=False,
                )
            )
            for idkey, idval in id_keys:
                # myassign(value, myget(value, idkey), idkey[:-1])
                myassign(data, idval, idkey[:-1])

        return data

    def new(self, kind, data):
        """Try to create / update an item of `type_` class from raw data

        - convert nested data into references
        - convert data to suit pydantic schema
        - get the pydantic item

        """
        data2 = self.convert_into_references(data)
        d = re.match(REG_KIND, kind).groupdict()
        real_kind = d["parent"]
        klass = self.MAPPERS.get(real_kind)
        if not klass:
            log.warning("missing MAPPERS[%s] class!", kind)  # TODO: remove debug
            return

        item = klass.pydantic(data2)
        return item

    def remain_tasks(self):
        "compute how many pending tasks still remains"
        n = sum([sync.running() for sync in self.syncmodel])
        if self.raw_storage:
            n += self.raw_storage.running()
        n += super().remain_tasks()
        return n

    def _clean(self, kind, data):
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = v.strip()
        return data

    def _restruct(self, kind, data, reveal):
        """Restructure internal data according to `RESTRUCT_DATA` structure info.

        Finally the result is the overlay of the original `data` and the restructured one.
        """
        restruct = {}
        info = self.RESTRUCT_DATA.get("default", {})
        info.update(self.RESTRUCT_DATA.get(kind, {}))
        for path, value in reveal.items():
            for pattern, (new_path, new_value) in info.items():
                m = re.match(pattern, path)
                if m:
                    d = m.groupdict()
                    d["value"] = value
                    key = tuple(new_path.format_map(d).split(SEP))
                    _value = value if new_value == COPY else new_value.format_map(d)
                    restruct[key] = _value

        # build the restructured data
        restruct = rebuild(restruct, result={})
        # create the overlay of both data to be used (possibly) by pydantic
        data = {**data, **restruct}

        return data

    def _transform(self, kind, data):
        return data
