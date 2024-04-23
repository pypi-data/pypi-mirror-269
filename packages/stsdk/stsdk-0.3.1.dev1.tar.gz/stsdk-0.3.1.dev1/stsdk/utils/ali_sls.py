import asyncio
import json
import queue
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, wait

from aliyun.log import LogClient
from aliyun.log.logitem import LogItem
from aliyun.log.putlogsrequest import PutLogsRequest
from aliyun.log.getlogsrequest import GetLogsRequest
from aliyun.log.listlogstoresrequest import ListLogstoresRequest
from aliyun.log.index_config import *

from stsdk.utils.config import config
from stsdk.utils.log import log


class SlsData:
    def __init__(self):
        self.project = config.aliyun_sls_project
        self.log_store = config.aliyun_sls_log_store
        self.topic = config.aliyun_sls_topic
        self.source = config.aliyun_sls_source
        self.time_interval = config.aliyun_sls_time_interval
        self.client = self.sls_init()
        self.executor = ThreadPoolExecutor(max_workers=8)
        self.queue = queue.Queue()
        self.time_interval = 15
        self.data_batches = defaultdict(lambda: defaultdict(list))
        threading.Thread(target=self.consume_queue, args=()).start()

    def put_logs(self, log_store, topic, source, flag, contents):
        """
        将日志放入队列
        :param log_store: log_store
        :param topic: topic
        :param source: source
        :param flag: 是否是多个数据，True表示是多个数据，False表示是单个数据
        :param contents: contents
        :return:
        """
        req = {
            "timestamp": time.time(),
            "log_store": log_store,
            "topic": topic,
            "source": source,
            "flag": flag,
            "contents": contents
        }
        self.queue.put(req)

    def consume_queue(self):
        start_time = time.time()
        while True:
            try:
                # 尝试在1秒内从队列中获取数据
                data = self.queue.get(timeout=1)
                log_store = data.get('log_store', {})
                topic = data.get('topic', 'unknown_topic')
                source = data.get('source', 'unknown_source')
                key = (topic, source)  # 使用元组作为键
                if data["flag"]:
                    self.data_batches[log_store][key].extend(data["contents"])
                else:
                    self.data_batches[log_store][key].append(data["contents"])
                self.queue.task_done()
            except queue.Empty:
                continue

            current_time = time.time()
            if (current_time - start_time) >= self.time_interval:
                self.process_and_clear_batches(log_store)
                start_time = current_time

    def process_and_clear_batches(self, log_store):
        for key, batch in self.data_batches[log_store].items():
            topic, source = key
            if len(batch) == 0:
                continue
            log.info(f"Processing {len(batch)} logs for {log_store}/{topic}/{source}")
            self.save_sls_batch(log_store, topic, source, batch)
            self.data_batches[log_store][key] = []

    def get_data(self, num=100):
        data = []
        for _ in range(num):
            # if not self.queue.empty():
            data.append(self.queue.get())
        return data

    # 初始化链接
    def sls_init(self):
        endpoint = config.aliyun_sls_endpoint
        accessKeyId = config.aliyun_sls_access_key_id
        accessKey = config.aliyun_sls_access_key
        client = LogClient(endpoint, accessKeyId, accessKey)
        return client

    def set_project(self, project):
        self.project = project

    # 查询该项目的log_store列表
    def select_log_store(self):
        req1 = ListLogstoresRequest(self.project)
        res1 = self.client.list_logstores(req1)
        res1.log_print()

    # 添加索引
    def create_index(self):
        line_config = IndexLineConfig([" ", "\\t", "\\n", ","], False, ["key_1", "key_2"])
        key_config_list = {"key_1": IndexKeyConfig([",", "\t", ";"], True)}
        index_detail = IndexConfig(30, line_config, key_config_list)
        self.client.create_index(self.project, self.log_store, index_detail)

    # 查看日志
    def read_sls(self, log_store, from_time, to_time, topic, query, line=100, offset=0, reverse=True, **kwargs):
        res_list = []
        req = GetLogsRequest(project=self.project,
                             logstore=log_store,
                             fromTime=from_time,
                             toTime=to_time,
                             topic=topic,
                             query=query,
                             line=line,
                             offset=offset,
                             reverse=reverse,
                             **kwargs)
        res = self.executor.submit(self.client.get_logs, req).result().get_logs()
        for log in res:
            res_list.append(log.get_contents())
        return res_list

    # 写入日志
    def save_sls(self, log_store, topic, source, contents):
        log_item = LogItem(timestamp=int(time.time()), contents=contents)
        req = PutLogsRequest(self.project, log_store, topic, source, [log_item])
        self.executor.submit(self.client.put_logs, req)

    async def save_sls_async(self, log_store, topic, source, contents):
        log_item = LogItem(timestamp=int(time.time()), contents=contents)
        req = PutLogsRequest(self.project, log_store, topic, source, [log_item])
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.client.put_logs, req)

    def save_sls_batch(self, log_store, topic, source, contents_list):
        log_item_list = []
        for i in contents_list:
            log_item = LogItem()
            log_item.set_time(int(time.time()))
            log_item.set_contents(i)
            log_item_list.append(log_item)
        req = PutLogsRequest(self.project, log_store, topic, source, log_item_list)
        try:
            threading.Thread(target=self.client.put_logs, args=(req,)).start()
            log.info(f"Pushed {len(contents_list)} logs to {log_store}/{topic}/{source}")
        except Exception as e:
            log.error(f"Failed to push logs to {log_store}/{topic}/{source}: {e}")


sls_data = SlsData()
