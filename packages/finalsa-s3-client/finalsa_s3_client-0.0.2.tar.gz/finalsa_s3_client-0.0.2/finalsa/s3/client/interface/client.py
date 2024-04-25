from abc import ABC, abstractmethod


class S3Client(ABC):

    @abstractmethod
    def get_object(self, bucket: str, key: str) -> bytes:
        pass

    @abstractmethod
    def put_object(self, bucket: str, key: str, data: bytes):
        pass

    @abstractmethod
    def delete_object(self, bucket: str, key: str):
        pass

    @abstractmethod
    def list_objects(self, bucket: str) -> list:
        pass

    @abstractmethod
    def list_buckets(self) -> list:
        pass

    @abstractmethod
    def create_bucket(self, bucket: str):
        pass

    @abstractmethod
    def delete_bucket(self, bucket: str):
        pass

    @abstractmethod
    def get_bucket_location(self, bucket: str) -> str:
        pass
