#coding:utf-8

# @Author  :  lijishi
# @Contact :  lijishi@emails.bjut.edu.cn
# @Software:  Pycharm
# @EditTime:  Feb 1,2020
# @describe:  Use Ali-API to translate
# @LICENSE :  GNU GENERAL PUBLIC LICENSE Version 3

# Based On Ali Cloud official Python Demo
# https://help.aliyun.com/document_detail/125187.html?spm=a2c4g.11186623.6.567.31d019da1LovaJ

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.request import CommonRequest
from aliyunsdkalimt.request.v20190107 import TranslateGeneralRequest

def alicloud(line, language, Is2language):
   try:
      client = AcsClient("ID", "Key", "cn-hangzhou")
      request = TranslateGeneralRequest.TranslateGeneralRequest()
      request.set_SourceLanguage("auto")
      request.set_SourceText(line)
      request.set_FormatType("text")
      if language == 1:
         request.set_TargetLanguage("en")
      else:
         request.set_TargetLanguage("zh")
      response = client.do_action_with_exception(request).decode("utf-8")
      transtext = ''
      for index in range(23, len(response)):
         if response[index:index+1] != "\"":
            transtext += response[index]
         else:
            break
      if transtext == 'rom source to target not support':
         return line[:-1]

      return_text = ''
      if Is2language:
         return_text = line
      return_text += transtext[:-2]
      if Is2language:
         return_text += '\n'
      return return_text

   except BaseException as err:
      errortext = 'AliCloudError' + str(err)
      return errortext
