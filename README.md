# fileuploader

File Upload into AWS S3 and Google cloud storage

required libraries:

    - pip install boto3
    - pip install google-cloud-storage

Set Up Configuration:

    - Ensure your AWS credentials are set up properly in your environment for boto3.
    - Ensure your GCP credentials are set up for the google-cloud-storage library (typically via the GOOGLE_APPLICATION_CREDENTIALS environment variable).

Run the Module:

    - Update the __main__ section with the correct bucket names and directory path
    - Run the script python file_transfer.py
