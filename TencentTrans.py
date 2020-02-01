# @Author  :  lijishi
# @Contact :  lijishi@emails.bjut.edu.cn
# @Software:  Pycharm
# @EditTime:  Jan 30,2020
# @describe:  Use Tencent-API to translate
# @LICENSE :  GNU GENERAL PUBLIC LICENSE Version 3

# Based On Tencent Cloud official Python Demo
# https://github.com/TencentCloud/tencentcloud-sdk-python

# References

import time
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

# Temporarily Abandoned
def tencentLanguageDetect(text):
    try:
        cred = credential.Credential("ID", "Key")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile)

        req_language = models.LanguageDetectRequest()
        if text[-1:]=='\n':
            text = text[0:len(text)-1]
        language_params_front = r'{"Text":"'
        language_params_back = r'","ProjectId":0}'
        language_params = language_params_front + text + language_params_back
        req_language.from_json_string(language_params)

        resp_language = client.LanguageDetect(req_language)
        responselanguage = resp_language.to_json_string()
        language = responselanguage[10:12]


    except TencentCloudSDKException as err:
        print(err)

    return language

def tencentTranslate(text, source_language, Is2language):
    try:
        cred = credential.Credential("ID", "Key")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile)

        req_text = models.TextTranslateRequest()
        if text[-1:]=='\n':
            text = text[0:len(text)-1]
        #source_language = tencentLanguageDetect(text)
        text_params_front = '{"SourceText":"'
        if source_language == 1:
            text_params_back = '","Source":"auto","Target":"en","ProjectId":0}'
        else:
            text_params_back = '","Source":"auto","Target":"zh","ProjectId":0}'
        text_params = text_params_front + text + text_params_back
        req_text.from_json_string(text_params)

        resp_text = client.TextTranslate(req_text)
        responsetext = resp_text.to_json_string()
        transtext = ''
        for index in range(16, len(responsetext)):
            if responsetext[index] != "\"":
                transtext += responsetext[index]
            else:
                break

    except TencentCloudSDKException as err:
        errortext = 'TencentCloudError' + str(err)
        return errortext

    return_text = ''
    if Is2language:
        return_text = text
        return_text += '\n'
    return_text += transtext
    if Is2language:
        return_text += '\n'
    return return_text

#text = 'common'
#print(tencentTranslate(text))