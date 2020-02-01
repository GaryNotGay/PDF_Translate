# @Author  :  lijishi
# @Contact :  lijishi@emails.bjut.edu.cn
# @Software:  Pycharm
# @EditTime:  Jan 30,2020
# @describe:  Use BaiDu-API to translate
# @LICENSE :  GNU GENERAL PUBLIC LICENSE Version 3

# Based On BaiDu Translation Open Platform official Python3 Demo
# https://fanyiapp.bj.bcebos.com/api/demo/BaiduTransAPI-forPython3.py.zip

# References

import http.client
import hashlib
import urllib
import random
import json
import time
from TencentTrans import tencentLanguageDetect

def baiduTranslate(text, language, Is2language):
    appid = 'ID'  # 填写你的appid
    secretKey = 'Key'  # 填写你的密钥
    httpClient = None
    myurl = '/api/trans/vip/translate'

    fromLang = 'auto'   #原文语种
    if language == 1:
        toLang = 'en'   #译文语种
    else:
        toLang = 'zh'
    salt = random.randint(32768, 65536)
    q= text
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        responsetext = json.dumps(result, ensure_ascii=False)

        length = len(text)
        transtext = ''
        for index in range(64+length, len(responsetext)):
            if responsetext[index] != "\"":
                transtext += responsetext[index]
            else:
                break

        return_text = ''
        if Is2language:
            return_text = text
            return_text += '\n'
        return_text += transtext
        if Is2language:
            return_text += '\n'
        return return_text

    except Exception as e:
        errortext = 'BaiDuError' + str(e)
        return errortext


    finally:
        if httpClient:
            httpClient.close()
