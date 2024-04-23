import json
import unittest
from unittest.mock import patch

from src.dhuolib import Dhuolib


class TestDhuolibUtils(unittest.TestCase):
    def setUp(self):
        self.dhuolib = Dhuolib(service_endpoint="http://localhost:8000")
        self.namespace = "engdb"
        self.bucket_name = "dhuodata-mlops"
        self.file_path = "tests/files/LogisticRegression_best.pickle"
        self.experiment_id = None

    def tearDown(self):
        pass

    @patch("requests.post")
    def test_create_experiment(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"experiment_id": "1"}

        experiments_params = {
            "experiment_name": "sentiment_analysis_model_1",
            "tags": {"version": "v1", "priority": "P1"},
            "file": {
                "bucket": self.bucket_name,
                "namespace": self.namespace,
                "filepath": self.file_path,
            },
        }
        response = self.dhuolib.create_experiment(experiments_params)

        self.assertEqual(response, mock_response.json.return_value)

        mock_post.assert_called_once_with(
            "http://localhost:8000/api/experiment/save",
            data=json.dumps(experiments_params),
            headers={"Content-Type": "application/json"},
        )

    @patch("requests.post")
    def test_run_experiment(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "current_stage": "Production",
            "last_updated_timestamp": 1713582060414,
            "model_version": "1",
            "run_id": "9434e517ed104958b6f5f47d33c79184",
            "status": "READY",
        }

        run_params = {
            "experiment_id": "2",
            "stage": "Production",
            "file": {
                "bucket": self.bucket_name,
                "namespace": self.namespace,
                "filepath": "LogisticRegression_best.pickle",
            },
        }
        response = self.dhuolib.run_experiment(run_params)

        self.assertEqual(response, mock_response.json.return_value)

        mock_post.assert_called_once_with(
            "http://localhost:8000/api/experiment/run",
            data=json.dumps(run_params),
            headers={"Content-Type": "application/json"},
        )
