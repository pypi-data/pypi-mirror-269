# import unittest
# from unittest import mock
# import pickle

# from src.services import ServiceAPIML


# class TestServiceAPIML(unittest.TestCase):
#     def setUp(self):
#         self.service_endpoint = "http://localhost:5000"
#         self.service = ServiceAPIML(self.service_endpoint)
#         data = {'key': 'value', 'number': 42}

#         with open('tests/files/data.pickle', 'wb') as file:
#             pickle.dump(data, file)

#     @mock.patch('src.services.requests.post')
#     def test_send_post_with_pickle_and_json(self, mock_post):
#         json_data = {
#             "experiment_name": "test_experiment",
#             "model_name": "test_model",
#             "tag": "1.0.0",
#             "file_path": "data.pickle.pkl"
#         }
#         pickle_path = "tests/files/data.pickle"

#         expected_response = mock.Mock()
#         expected_response.status_code = 201

#         mock_post.return_value = expected_response

#         response = self.service.send_post_with_pickle_and_json(json_data, pickle_path)

#         self.assertEqual(response.status_code, 201)
