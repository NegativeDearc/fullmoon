# coding:utf-8
from __future__ import print_function

try:
    from app.security import MailConfig
except ImportError:
    print("failed load security file, you'll not be able to use some modules")

from datetime import datetime
import requests
import urllib
import hmac
import hashlib
import base64
import uuid
from MyException import HttpMailSendException, HttpMethodException


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


def single_mail_api(recipients=None, subject=None, text=None, html=None, method="GET"):
    # https://help.aliyun.com/document_detail/29442.html?spm=5176.doc29441.6.567.kBMXeE
    # paras must be encode with utf-8
    # base URL
    # issue[fixed]: can't encode html correctly and raise signature don't match error
    base_http_url = " http://dm.aliyuncs.com/"
    base_https_url = " https://dm.aliyuncs.com/"

    if isinstance(recipients, list):
        # ToAddress目标地址，多个Email地址可以逗号分隔
        recipients = ",".join(recipients)
    if isinstance(html, unicode):
        # 中文必须转换成utf-8，否则出错
        html = html.encode("utf-8")
    if isinstance(subject, unicode):
        subject = subject.encode("utf-8")
    # 邮件发送接口参数
    private_params = dict(Action="SingleSendMail", AccountName=MailConfig.MAIL_USERNAME, ReplyToAddress="true",
                          AddressType="1", ToAddress=recipients, Subject=subject, HtmlBody=html)
    # 公共方法参数
    public_params = dict(Format="JSON", Version="2015-11-23", AccessKeyId=MailConfig.ACCESS_KEY_ID,
                         SignatureMethod="HMAC-SHA1", SignatureVersion="1.0", SignatureNonce=unique_id(),
                         Timestamp=local_to_utc())
    # 合并所有参数及其值
    public_params.update(private_params)
    # 阿里文档太垃圾，可参考http://sendcloud.sohu.com/doc/sms/
    # 1. 将实际调用API的参数以字母升序(A-Z)排列, 不包括signature 字段本身
    # 2. 按照排列之后的顺序,对key value进行URL编码, 以&key=value的方式连接所有参数, 得到字符串 param_str
    # 3. 以 "HTTPMethod&/&" 与param_str拼接，这两个部分都需要再次URL编码，得到 string_to_sign
    # 4. 计算 sign_str 的HMAC_SHA1得到 signature
    # 5. 将Signature=signature加入到param_str中，与base_http_url/base_https_url拼接后进行请求
    # 6. 若成功发送则回复如下格式{"EnvId":"9841411220","RequestId":"A8F53EA6-6453-42D6-A11E-B2052E8423A6"}
    params_keys = list(public_params.keys())
    params_keys.sort()
    params_str = ''
    # 对value进行URL编码后拼接为字符串，key原则上需要，但因为全部是英文字母故略去
    # 注意"/"也需要URL编码，使用urllib.quote_plus()会导致空格转换成+而非%20，
    # 而使用urllib.quote需要取消safe，因为"/"不会被编码
    # 如果字符串不符合要求，签名计算无法通过
    for key in params_keys:
        params_str += key + '=' + urllib.quote(str(public_params[key]), safe="") + '&'

    # 别忘记去掉最末的&
    params_str_encoded = urllib.quote(params_str[:-1])
    # 拼接出参与签名计算的字符串，注意若用urllib.quote()，"/"不会被编码成%2F，会导致后续计算错误
    string_to_sign = "{HTTPMethod}&{SLACK}&{PARAMS}".format(
        SLACK=urllib.quote_plus("/"),
        HTTPMethod=method,
        PARAMS=urllib.quote_plus(params_str[:-1])
    )
    # 进行签名计算
    signature = HMAC_SHA1(key=MailConfig.ACCESS_KEY_SECRET + "&", string_to_sign=string_to_sign)
    # update parameters
    public_params.update({"Signature": urllib.quote_plus(signature)})

    if method == "POST":
        # 如果是POST方式需要加上头部信息 headers = {"Content-Type": "application/x-www-form-urlencoded"}
        # 并将请求参数加入到Body中
        pass
    elif method == "GET":
        # 将signature编码后带上参数名Signature加入params_str最后，与base_https_url拼接后生成正确的URL进行请求
        get_url = base_https_url + "?" + params_str + "Signature=%s" % urllib.quote_plus(signature)
        r = requests.get(get_url)
        # 对返回的参数以及HTTP代码进行识别
        if int(r.status_code) == 200:
            return True
        else:
            raise HttpMailSendException(r.text)
    else:
        raise HttpMethodException("HTTP Method Unsupported.")

if __name__ == "__main__":
    html = """
        <html>
        <body>
        <p>测试测试 空格  </p>
        </body>
        </html>
    """
    print(unicode(html, "utf-8"))
    print(type(html))
    single_mail_api(recipients="datingwithme@live.cn",
                    subject="Python发送邮件",
                    html=html)