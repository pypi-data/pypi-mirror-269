import json
import unittest
from unittest.mock import MagicMock, patch
import sys
import pytest
from pydantic import ValidationError

sys.path.append("src")
from dhuolib.clients import DhuolibClient


class TestDhuolibUtils(unittest.TestCase):
    def setUp(self):
        self.end_point = "http://fake-endpoint"
        self.dhuolib = DhuolibClient(service_endpoint=self.end_point)
        self.namespace = "engdb"
        self.bucket_name = "dhuodata-mlops"
        self.file_path = "tests/files/LogisticRegression_best.pickle"
        self.experiment_id = None

    def test_deve_lancar_excecao_com_valores_run_params_incorretos(self):
        experiments_params = {
            "file": {
                "bucket": self.bucket_name,
                "filepath": self.file_path,
            },
        }

        with pytest.raises(ValidationError):
            self.dhuolib.create_experiment(experiments_params)

    @patch("requests.post")
    @patch('dhuolib.clients.OCIUtils')
    def test_deve_criar_o_experimento_com_run_params_corretos(self, mock_oci_utils, mock_post):
        client = DhuolibClient(service_endpoint="http://fake-endpoint")

        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {"experiment_id": "1"}

        mock_oci = mock_oci_utils.return_value
        mock_oci.upload_file = MagicMock()

        experiment_params = {
            "experiment_name": "test_experiment",
            "experiment_tags": {"version": "v1", "priority": "P1"},
            "file": {
                "bucket": "example_bucket",
                "namespace": "example_namespace",
                "filepath": "tests/files/LogisticRegression_best.pickle"
            }
        }

        response = client.create_experiment(experiment_params)

        mock_oci.upload_file.assert_called_once_with(
            file_path="tests/files/LogisticRegression_best.pickle",
            bucket_name="example_bucket",
            namespace="example_namespace"
        )

        self.assertEqual(response, mock_response.json.return_value)

        mock_post.assert_called_once_with(
            "http://fake-endpoint/api/experiment/save",
            data=json.dumps(experiment_params),
            headers={"Content-Type": "application/json"},
        )

    @patch("requests.post")
    def test_deve_executar_o_experimento_com_run_params_corretos(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "current_stage": "Production",
            "last_updated_timestamp": 1713582060414,
            "model_version": "1",
            "run_id": "9434e517ed104958b6f5f47d33c79184",
            "status": "READY",
        }

        run_params = {
            "experiment_id": 2,
            "stage": "Production",
            "modelname": "nlp_framework",
            "modeltag": "v1",
            "file": {
                "bucket": self.bucket_name,
                "namespace": self.namespace,
                "filepath": "LogisticRegression_best.pickle",
            },
        }
        response = self.dhuolib.run_experiment(run_params)

        self.assertEqual(response, mock_response.json.return_value)

        mock_post.assert_called_once_with(
            "http://fake-endpoint/api/experiment/run",
            data=json.dumps(run_params),
            headers={"Content-Type": "application/json"},
        )
