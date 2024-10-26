from uuid import uuid4
from locust import HttpUser, task, between
from prometheus_client import start_http_server,Counter, Gauge
import datetime

# Определяем метрики для Prometheus
REQUESTS_COUNTER = Counter("locust_requests_total", "Total requests executed")
FAILURES_COUNTER = Counter("locust_failures_total", "Total failed requests")
USERS_GAUGE = Gauge("locust_user_count", "Number of active users")

class DemoServiceAPI(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        USERS_GAUGE.inc()
        self.admin_credentials = ("admin", "adminPassword123")
        self.user_credentials = ("user", "superSecretAdminPassword123")

    def on_stop(self):
        USERS_GAUGE.dec()

    @task
    def register_user(self):
        response = self.client.post(
            "/user-register",
            json = {
                "username": str(uuid4()),
                "name": "user",
                "birthdate": datetime.datetime.now().isoformat(),
                "password": "VerySecretPassword123",
            }
        )
        if response.status_code == 200:
            REQUESTS_COUNTER.inc()
        else:
            FAILURES_COUNTER.inc()

start_http_server(9646)