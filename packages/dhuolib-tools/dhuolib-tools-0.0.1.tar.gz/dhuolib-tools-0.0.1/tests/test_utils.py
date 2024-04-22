# import unittest
# from unittest import mock

# from src.oci.utils import OCIUtils


# class TestOCIUtils(unittest.TestCase):
#     def setUp(self):
#         self.namespace = "engdb"
#         self.bucket_name = "dhuodata-mlops"
#         self.file_path = "tests/files/LogisticRegression_best.pickle"

#     def test_upload_file(self):
#         self.utils = OCIUtils()
#         self.utils.upload_file(self.namespace, self.bucket_name, self.file_path)

#     # @mock.patch('src.oci.utils.oci.config.from_file')
#     # @mock.patch('src.oci.utils.oci.object_storage.ObjectStorageClient')
#     # def test_upload_file(self, mock_object_storage_client, mock_from_file):
#     #     mock_config = mock.Mock()
#     #     mock_from_file.return_value = mock_config
#     #     mock_client = mock.Mock()
#     #     mock_object_storage_client.return_value = mock_client

#     #     self.utils = OCIUtils()
#     #     self.utils.upload_file(self.namespace, self.bucket_name, self.file_path)

#     #     mock_from_file.assert_called_once_with('~/.oci/config')
#     #     mock_object_storage_client.assert_called_once_with(mock_config)
#     #     args, _ = mock_object_storage_client.put_object.call_args
#     #     assert args[0] == 'namespace'
#     #     assert args[1] == 'bucket_name'
#     #     assert args[2] == 'file_path'
