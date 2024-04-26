import json

import requests


class ServiceAPIML:
    def __init__(self, service_endpoint):

        if not isinstance(service_endpoint, str):
            raise ValueError("service_endpoint must be a string")

        self.service_endpoint = f"{service_endpoint}/api/experiment"
        self.headers = {"Content-Type": "application/json"}

    def create_experiment_by_conf_json(self, experiment_params):
        if experiment_params is None and isinstance(experiment_params, dict):
            raise ValueError("json_data must be a dict")

        response = requests.post(
            f"{self.service_endpoint}/save",
            data=json.dumps(experiment_params),
            headers=self.headers,
        )
        return response

    def run_experiment(self, run_params):
        if run_params is None and isinstance(run_params, str):
            raise ValueError("json_data must be a dict")
        response = requests.post(
            f"{self.service_endpoint}/run",
            data=json.dumps(run_params),
            headers=self.headers,
        )
        return response
