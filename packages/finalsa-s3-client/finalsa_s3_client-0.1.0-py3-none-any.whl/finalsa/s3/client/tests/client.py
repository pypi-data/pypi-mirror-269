from finalsa.s3.client.interface import S3Client


class S3ClientTest(S3Client):

    def __init__(self) -> None:
        self.buckets = {}

    def get_object(self, bucket: str, key: str) -> bytes:
        return self.buckets[bucket][key]

    def put_object(self, bucket: str, key: str, data: bytes):
        if bucket not in self.buckets:
            self.buckets[bucket] = {}
        self.buckets[bucket][key] = data

    def delete_object(self, bucket: str, key: str):
        del self.buckets[bucket][key]

    def list_objects(self, bucket: str) -> list:
        return self.buckets[bucket].keys()

    def list_buckets(self) -> list:
        return self.buckets.keys()

    def create_bucket(self, bucket: str):
        self.buckets[bucket] = {}

    def delete_bucket(self, bucket: str):
        del self.buckets[bucket]

    def get_bucket_location(self, bucket: str) -> str:
        return "us-east-1"

    def clear(self):
        self.buckets = {}
