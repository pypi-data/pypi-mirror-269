from prometheus_client import Histogram, start_http_server, Gauge, Counter

from stsdk.utils.config import config
from stsdk.utils.log import log


class MetricUtil:
    def __init__(self):
        self.metrics = {}
        self.add_histogram("processing_time_seconds",
                           "Time spent processing",
                           labelnames=["kind", "operation"])
        self.start_server(config.metric_port)

    def add_gauge(self, name, documentation, labelnames):
        self.metrics[name] = Gauge(name, documentation, labelnames=labelnames)

    def add_counter(self, name, documentation, labelnames):
        self.metrics[name] = Counter(name, documentation, labelnames=labelnames)

    def add_histogram(self, name, documentation, labelnames):
        self.metrics[name] = Histogram(name, documentation, labelnames=labelnames)

    def get_metric(self, name):
        return self.metrics.get(name)

    def guage_set(self, name, labels, value):
        self.get_metric(name).labels(**labels).set(value)

    def start_server(self, port):
        start_http_server(port)
        log.info(f"Prometheus metrics server started on port {port}")

    def metric_time(self, kind, operation, start_time, end_time):
        self.get_metric("processing_time_seconds").labels(kind=kind, operation=operation).observe(
            end_time - start_time
        )

    def metric_guage(self, name, labels, value):
        self.get_metric(name).labels(**labels).set(value)


