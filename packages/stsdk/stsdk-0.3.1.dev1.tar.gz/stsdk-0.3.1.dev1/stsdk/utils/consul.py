import httpx

from stsdk.utils.log import log


class ConsulClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def register_service(self, service_name, service_address, service_port):
        url = f"http://{self.base_url}/v1/agent/service/register"
        data = {"Name": service_name, "Address": service_address, "Port": service_port}
        response = httpx.put(url, json=data)
        if response.status_code == 200:
            log.info(
                f"Successfully registered {service_name} at {service_address}:{service_port}"
            )
        else:
            log.info(f"Failed to register {service_name}: {response.text}")

    def discover_service(self, service_name):
        url = f"http://{self.base_url}/v1/catalog/service/{service_name}"
        if self.token:
            url += f"?token={self.token}"
        response = httpx.get(url)
        if response.status_code == 200:
            services = response.json()
            if len(services) > 0:
                log.info(
                    f"Discovered {service_name} at {services[0]['ServiceAddress']}:{services[0]['ServicePort']}"
                )
                return f"{services[0]['ServiceAddress']}:{services[0]['ServicePort']}"
            else:
                log.info(f"No service found for {service_name}")
                raise Exception(f"No service found for {service_name}")
        else:
            log.error(f"Failed to discover {service_name}: {response.text}")
            raise Exception(f"Failed to discover {service_name}: {response.text}")

    def get_api_endpoint(self):
        api_endpoint = {
            "http": {
                "dms_base_url": "http://" + self.discover_service("at-dms"),
                "oms_base_url": "http://" + self.discover_service("at-oms"),
                "sms_base_url": "",
            },
            "ws": {
                "dms_base_ws": "ws://" + self.discover_service("at-dms-ws"),
                "oms_base_ws": "ws://" + self.discover_service("at-oms-ws"),
            },
        }
        return api_endpoint
