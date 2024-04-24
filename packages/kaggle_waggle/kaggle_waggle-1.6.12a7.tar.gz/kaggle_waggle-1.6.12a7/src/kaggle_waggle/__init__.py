# coding=utf-8
from __future__ import absolute_import
from kaggle_waggle.api.kaggle_api_extended import KaggleApi
from kaggle_waggle.api_client import ApiClient

api = KaggleApi(ApiClient())
api.authenticate()
