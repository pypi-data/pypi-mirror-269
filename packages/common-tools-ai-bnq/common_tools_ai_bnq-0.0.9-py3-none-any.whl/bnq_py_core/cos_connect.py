#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @time:2024/4/23 16:33
# Author:Zhang HongTao
# @File:cos_connect.py

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


class CosConnect(object):
    """Cos连接类, 用于连接Cos

    args:
        secret_id: secret_id

        secret_key: secret_key

        region: 地域

        bucket: bucket

    """
    __instance = None  # 单例

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if not cls.__instance:
            cls.__instance = super(CosConnect, cls).__new__(cls)

        return cls.__instance

    def __init__(self, secret_id, secret_key, region="ap-shanghai") -> None:
        """

        :param secret_id: secret_id
        :param secret_key: secret_key
        :param region: 地域
        """
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.region = region

        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
        self.client = CosS3Client(config)


if __name__ == '__main__':
    test_data = {"secret_id": "AKIDd2WngT6aYYOI0fEg93nT0KQM7kGf0DC5",
                 "secret_key": "pV8pbAg0DD0Yu4w2DQeljmndJ0Wv6FLF"}
    file_path = r"D:\BIM\demo\1.png"
    test_cls = CosConnect(**test_data)
    print(test_cls.client.list_buckets())
    buck_of_bim = "bnq-bim-1317585858"
    print(test_cls.client.list_objects(Bucket=buck_of_bim))
    with open(file_path, "rb") as f:
        response = test_cls.client.put_object(Bucket=buck_of_bim, Body=f, Key="1.png")
    print(response)
