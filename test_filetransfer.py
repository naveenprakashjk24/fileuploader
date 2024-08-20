import unittest
from unittest.mock import MagicMock, patch

from file_transfer import FileTransfer


class TestFileTransfer(unittest.TestCase):

    @patch('FileTransfer.boto3.client')
    @patch('FileTransfer.storage.Client')
    def setUp(self, mock_s3Client, mock_gcsClient):
        self.mock_s3Client = MagicMock()
        self.mock_gcsClient = MagicMock()
        mock_s3Client.return_value = self.mock_s3Client
        mock_gcsClient.return_value = self.mock_gcsClient

        self.uploader = FileTransfer(
            s3BucketName='test_s3_bucket',
            gcsBucketName='test_gcp_bucket'
        )

    def test_uploadToawsS3(self):
        with patch('FileTransfer.os.path.basename', return_value='test.jpg'):
            self.uploader.uploadToawsS3('test.jpg')
            self.mock_s3Client.upload_file.assert_called_with('test.jpg', 'test_s3_bucket', 'test.jpg')

    def test_uploadToGCS(self):
        mock_blob = MagicMock()
        self.mock_gcsClient.bucket.return_value.blob.return_value = mock_blob

        with patch('FileTransfer.os.path.basename', return_value='test.pdf'):
            self.uploader.uploadToGCS('test.pdf')
            mock_blob.upload_from_filename.assert_called_with('test.pdf')

    @patch('FileTransfer.os.walk')
    def test_storeFileData(self, mock_walk):
        mock_walk.return_value = [
            ('root', ('subdir',), ('file1.jpg', 'file2.pdf'))
        ]

        with patch.object(self.uploader, 'upload_file') as mock_upload_file:
            self.uploader.storeFileData('root')
            mock_upload_file.assert_any_call('root/file1.jpg')
            mock_upload_file.assert_any_call('root/file2.pdf')

if __name__ == '__main__':
    unittest.main()
