import os

import boto3
from google.cloud import storage


class FileTransfer:
    def __init__(self, s3BucketName, gcsBucketName,
        imageExts=None, mediaExts=None, docExts=None):


        self.s3Client = boto3.client('s3')
        self.s3BucketName = s3BucketName

        self.gcsClient = storage.Client()
        self.gcsBucketName = gcsBucketName

        self.imageExts = imageExts or ['jpg', 'png', 'svg', 'webp']
        self.mediaExts = mediaExts or ['mp3', 'mp4', 'mpeg4', 'wmv', '3gp', 'webm']
        self.docExts = docExts or ['doc', 'docx', 'csv', 'pdf']

    def uploadToawsS3(self, filePath, fileName):

        try:
            self.s3Client.upload_file(filePath, self.s3BucketName, fileName)
            print(f"Uploaded {fileName} to S3 bucket {self.s3BucketName}.")
        except Exception as e:
            print(f"Failed to upload {fileName} to AWS S3: {e}")

    def uploadToGCS(self, filePath, fileName):

        try:
            bucket = self.gcsClient.get_bucket(self.gcsBucketName)
            blob = bucket.blob(fileName)
            blob.upload_from_filename(filePath)
            print(f"Uploaded {fileName} to GCS bucket {self.gcsBucketName}.")
        except Exception as e:
            print(f"Failed to upload {fileName} to GCS: {e}")

    def fileUploadToStorage(self, filePath):
        formatData = filePath.split('.')[-1].lower()
        if formatData in self.imageExts + self.mediaExts:
            self.uploadToawsS3(filePath)
        elif formatData in self.docExts:
            self.uploadToGCS(filePath)

    def storeFileData(self, directory):
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                self.fileUploadToStorage(file_path)

if __name__ == "__main__":

    s3BucketName = 'Bucket Name'
    gcsBucketName = 'Bucket Name'
    directory = 'path'

    file_transfer = FileTransfer(s3BucketName, gcsBucketName)
    file_transfer.transfer_files(directory)
