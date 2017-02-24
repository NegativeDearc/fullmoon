import hashlib
import hmac
import base64
import sys


def get_sign_string(source, secret):
    h = hmac.new(secret, source, hashlib.sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature


def main():
    print(get_sign_string(
        "POST&%2F&AccessKeyId%3Dtestid%26AccountName%3D%253Ca%2525b%2527%253E%26Action%3DSingleSendMail%26AddressType%3D1%26Format%3DXML%26HtmlBody%3D4%26RegionId%3Dcn-hangzhou%26ReplyToAddress%3Dtrue%26SignatureMethod%3DHMAC-SHA1%26SignatureNonce%3D8ee704e1-152d-4048-9648-8bedd6cbf4f4%26SignatureVersion%3D1.0%26Subject%3D3%26TagName%3D2%26Timestamp%3D2016-09-18T03%253A11%253A44Z%26ToAddress%3D1%2540test.com%26Version%3D2015-11-23",
        "testsecret&"))

if __name__ == "__main__":
    sys.exit(main())
