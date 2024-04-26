from finalsa.s3.client.interface.client import S3Client
import boto3
import logging


class S3ClientImpl(S3Client):

    def __init__(
        self,
    ) -> None:
        self.client = boto3.client('s3')
        self.logger = logging.getLogger("finalsa.clients")

    def get_object(self, bucket: str, key: str) -> bytes:
        self.logger.info(f"Getting object from bucket {bucket} with key {key}")
        response = self.client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read()

    def put_object(self, bucket: str, key: str, data: bytes):
        self.logger.info(f"Putting object to bucket {bucket} with key {key}")
        self.client.put_object(Bucket=bucket, Key=key, Body=data)

    def delete_object(self, bucket: str, key: str):
        self.logger.info(f"Deleting object from bucket {bucket} with key {key}")
        self.client.delete_object(Bucket=bucket, Key=key)

    def list_objects(self, bucket: str) -> list:
        self.logger.info(f"Listing objects from bucket {bucket}")
        response = self.client.list_objects(Bucket=bucket)
        return response['Contents']

    def list_buckets(self) -> list:
        self.logger.info(f"Listing buckets")
        response = self.client.list_buckets()
        return response['Buckets']

    def create_bucket(self, bucket: str):
        self.logger.info(f"Creating bucket {bucket}")
        self.client.create_bucket(Bucket=bucket)

    def delete_bucket(self, bucket: str):
        self.logger.info(f"Deleting bucket {bucket}")
        self.client.delete_bucket(Bucket=bucket)

    def get_bucket_location(self, bucket: str) -> str:
        self.logger.info(f"Getting location of bucket {bucket}")
        response = self.client.get_bucket_location(Bucket=bucket)
        return response['LocationConstraint']
