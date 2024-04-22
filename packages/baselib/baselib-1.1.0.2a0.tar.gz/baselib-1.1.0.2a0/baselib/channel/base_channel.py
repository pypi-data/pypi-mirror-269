# -*- coding:utf-8 -*-
import requests
import json
import time
from baselib.log import file_logger

class Channel(object):

    DEBUG = True
    url_tmpl = ""
    app_path = ""
    use_ssl = False
    logger = file_logger()

    @classmethod
    def get(
            cls,
            app_path,
            params=None,
            headers=None,
            cookies=None,
            end_with_slash=True):
        return cls.send(
            app_path,
            params,
            headers,
            cookies,
            "GET",
            end_with_slash)

    @classmethod
    def post(
            cls,
            app_path,
            params=None,
            headers=None,
            cookies=None,
            end_with_slash=True):
        return cls.send(
            app_path,
            params,
            headers,
            cookies,
            "POST",
            end_with_slash)

    @classmethod
    def put(
            cls,
            app_path,
            params=None,
            headers=None,
            cookies=None,
            end_with_slash=True):
        return cls.send(
            app_path,
            params,
            headers,
            cookies,
            "PUT",
            end_with_slash)

    @classmethod
    def send(cls, app_path, params, headers, cookies, method, end_with_slash):
        url, params, headers, cookies = cls.format_input(
            app_path, params, headers, cookies, end_with_slash)
        if method.upper() in ['GET']:
            rsp = requests.get(
                url,
                params=params,
                headers=headers,
                cookies=cookies)
        elif method.upper() in ['POST']:
            rsp = requests.post(
                url,
                json=params,
                headers=headers,
                cookies=cookies)
        elif method.upper() in ['PUT']:
            rsp = requests.put(
                url,
                json=params,
                headers=headers,
                cookies=cookies)
        if not rsp.text:
            return {}
        time.sleep(0.3)
        return cls.format_output(rsp)

    @classmethod
    def common_headers(cls, headers, cookies):
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}
        return headers, cookies

    @classmethod
    def format_input(
            cls,
            app_path,
            params,
            headers=None,
            cookies=None,
            end_with_slash=True):

        if params is None:
            params = {}
        url = cls.format_url(
            url=cls.url_tmpl.format(app_path=app_path),
            end_with_slash=end_with_slash
        )
        headers, cookies = cls.common_headers(headers, cookies)
        if cls.DEBUG:
            cls.logger.debug("[url] {}".format(url))
            cls.logger.debug("[params] {}".format(params))
            cls.logger.debug("[headers] {}".format(headers))
        return url, params, headers, cookies

    @classmethod
    def format_output(cls, rsp):
        data = json.loads(rsp.text)
        if isinstance(data, dict) and data.get("message", ""):
            raise RuntimeError(data)
        if cls.DEBUG:
            cls.logger.debug("[Response] {}".format(data))
        return data

    @classmethod
    def format_url(cls, url, use_ssl=None, end_with_slash=True):
        http = "http://"
        if use_ssl is None:
            use_ssl = cls.use_ssl
        if use_ssl:
            http = "https://"
        url = url.replace("https://", "").replace(
            "http://", "").replace("///", "/").replace("//", "/")
        if url.endswith("/"):
            url = url[:-1]
        if end_with_slash:
            url += "/"
        return http + url
