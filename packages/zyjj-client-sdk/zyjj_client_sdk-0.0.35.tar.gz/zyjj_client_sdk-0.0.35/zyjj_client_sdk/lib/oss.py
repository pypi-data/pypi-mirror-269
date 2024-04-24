import logging

from zyjj_client_sdk.base.api import ApiService
from zyjj_client_sdk.base import Base
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from typing import Callable


def _callback(i: float):
    logging.info(f"[storage] current progress {i}")


class OSSService:
    def __init__(self, base: Base, api: ApiService):
        self.__base = base
        self.__api = api
        self.__auth = None

    def __get_auth(self):
        if self.__auth is None:
            self.__auth = self.__api.could_get_tencent_cos()
        return self.__auth

    def __tencent_get_client(self) -> CosS3Client:
        auth = self.__get_auth()
        token = auth["token"]
        config = CosConfig(
            Region=auth["region"],
            SecretId=token["TmpSecretId"],
            SecretKey=token["TmpSecretKey"],
            Token=token["Token"],
            Scheme="https",
        )
        return CosS3Client(config)

    # 下载腾讯存储文件
    def tencent_download_file_by_key(self, key: str) -> str:
        client = self.__tencent_get_client()
        path = self.__base.generate_file_with_path(key)
        client.download_file(
            Bucket=self.__auth["bucket"],
            Key=key,
            DestFilePath=path,
            # progress_callback=lambda finish, total: callback((finish / total) * 100),
        )
        return path

    # 本地路径上传文件
    def tencent_upload_by_local_path(self, uid: str, path: str) -> str:
        client = self.__tencent_get_client()
        key = f"tmp/{uid}/{self.__base.generate_filename(path.split('.')[-1])}"
        client.upload_file(
            Bucket=self.__auth["bucket"],
            Key=key,
            LocalFilePath=path,
            # progress_callback=lambda finish, total: callback((finish / total) * 100),
        )
        return key

    # 上传二进制数据
    def tencent_upload_by_bytes(self, uid: str, data: bytes, ext: str) -> str:
        client = self.__tencent_get_client()
        key = f"tmp/{uid}/{self.__base.generate_filename(ext)}"

        class TmpBody:
            def __init__(self, _data: bytes):
                self.__data = _data

            def read(self, n: int) -> bytes:
                if n >= len(self.__data):
                    _data = self.__data
                    self.__data = bytes()
                    return _data
                else:
                    _data = self.__data[:n]
                    self.__data = self.__data[n - 1:]
                    return _data

        client.upload_file_from_buffer(
            Bucket=self.__auth["bucket"],
            Key=key,
            Body=TmpBody(data),
        )
        return key

    def tencent_get_url_by_key(self, key: str, expired=180) -> str:
        client = self.__tencent_get_client()
        bucket = self.__auth["bucket"]
        url = client.get_presigned_download_url(
            Bucket=bucket,
            Key=key,
            Expired=expired,
            SignHost=False,
            Params={
                "x-cos-security-token": self.__auth["token"]["Token"]
            }
        )
        return str(url).replace(f'{bucket}.cos.{self.__auth["region"]}.myqcloud.com', 'cos-origin.zyjj.cc')
