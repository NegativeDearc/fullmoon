# coding:utf-8
from __future__ import print_function

try:
    from security import MailConfig
except ImportError:
    print("failed load security file, you'll not be able to use some modules")

from datetime import datetime
from pprint import pprint
import requests
import urllib
import hmac
import hashlib
import base64
import uuid


def local_to_utc():
    # turn local time to UTC
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    return datetime.utcnow().strftime(format=UTC_FORMAT)


def HMAC_SHA1(key, string_to_sign=None):
    # generate HMAC_SHA1 token
    # print(key)
    # print(string_to_sign)
    signature = base64.b64encode(
        hmac.new(key, string_to_sign, hashlib.sha1).digest()
    )
    return signature


def unique_id():
    return uuid.uuid4().__str__()


def single_mail_api(recipients="", subject="", text="", html="", method="GET"):
    # https://help.aliyun.com/document_detail/29442.html?spm=5176.doc29441.6.567.kBMXeE
    # paras must be encode with utf-8
    # base URL
    base_http_url = " http://dm.aliyuncs.com/"
    base_https_url = " https://dm.aliyuncs.com/"
    # private_params
    private_params = dict(Action="SingleSendMail", AccountName=MailConfig.MAIL_USERNAME, ReplyToAddress="true",
                          AddressType="1", ToAddress=recipients, Subject=subject, HtmlBody=html,
                          TextBody=text)
    # sign HMC-SHA1 with Access Key Secret
    public_params = dict(Format="JSON", Version="2015-11-23", AccessKeyId=MailConfig.ACCESS_KEY_ID,
                         SignatureMethod="HMAC-SHA1", SignatureNonce=unique_id(), SignatureVersion="1.0",
                         Timestamp=local_to_utc())
    # signature
    public_params.update(private_params)
    params_string = urllib.urlencode(public_params)
    print(params_string)
    string_to_sign = "{HTTPMethod}&%2F&{PARAMS}".format(HTTPMethod=method, PARAMS=params_string)
    print(string_to_sign)
    signature = HMAC_SHA1(key=MailConfig.ACCESS_KEY_SECRET + "&", string_to_sign=string_to_sign)
    pprint(signature)
    # update GET parameters
    public_params.update({"Signature": signature})
    #
    pprint(public_params)
    r = requests.get(base_https_url, params=public_params)

    print(r.url)
    print(r.text)


if __name__ == "__main__":
    single_mail_api()
