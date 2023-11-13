import json
import requests
import base64
# from aip import AipOcr


def baidu_token(ak, sk, grant_type='client_credentials'):
    """
    获取授权token,expires_in有效期为30天
    :param ak:官网获取的SK
    :param sk:官网获取的AK
    """
    grant_type = grant_type
    # params = {'grant_type': grant_type, 'client_id': ak_, 'client_secret': ak_}
    headers = {'content_type': 'application/json'}
    request_url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type={grant_type}&client_id={ak}&client_secret={sk}'
    response = requests.get(request_url, headers=headers)
    if response:
        return True, response.json()
    if 'error' in response.json():
        return False, response.json()
    return False, None


class BaiduApi:
    def __init__(self, api_key, secret_key, level=1):
        """
        百度ocr api(general_basic:通用文字识别标准版,accurate_basic:通用文字识别高精度版)
        :param api_key: API Key
        :param secret_key:	Secret Key
        # baidu_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"             # 标准版含位置
        # baidu_url = " https://aip.baidubce.com/rest/2.0/ocr/v1/accurate"           # 高精度版含位置
        # baidu_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"       # 标准版
        # baidu_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage"            # 网络图片文字识别
        # baidu_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"   # 高精度版
        """

        basic_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/'
        level_key = 'general_basic'
        if level == 2:
            level_key = 'accurate_basic'
        if level == 3:
            level_key = 'webimage'
        self.baidu_url = basic_url + level_key
        self.api_key = api_key
        self.secret_key = secret_key
        self.level = level

    def get_text(self, file_path=None, file_url=None):
        params = {}
        if file_path:
            # 二进制打开
            with open(file_path, 'rb') as f:
                img = base64.b64encode(f.read())
                params = {'image': img}
        elif file_url:
            # 图片url
            params = {'url': file_url}
        else:
            return False,'图片为空'
        mark, result = baidu_token(self.api_key, self.secret_key)
        if mark:
            baidu_url_ = self.baidu_url + '?access_token=' + result['access_token']
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(baidu_url_, data=params, headers=headers)
            print(response.json())
            if response:
                return True, response.json().get('words_result')[0].get('words')
        else:
            #  {'error_description': 'unknown client id', 'error': 'invalid_client'}
            return False, result.get['error'] if result else 'Api Key或Secret Key错误'

if __name__ == "__main__":
    

# class BaiduSdk:
#     def __init__(self, app_id, api_key, secret_key, level=1):
#         """
#
#         :param app_id:
#         :param api_key:
#         :param secret_key:
#         :param level:识别级别
#         (1:调用通用文字识别（标准版）
#          2:调用通用文字识别（高精度版）
#          3:网络图片文字识别
#         )
#         """
#         self.client = AipOcr(app_id, api_key, secret_key)
#         self.level = level
#
#     def get_text(self, file_path=None, file_url=None):
#         """
#         识别验证码
#         :param file_path:
#         :param file_url:
#         :return: {'words_result': [{'words': '6RS5'}], 'words_result_num': 1, 'log_id': 1581898086821811984}
#         """
#         try:
#             if file_path:
#                 with open(file_path, 'rb') as f:
#                     image = f.read()
#                     if self.level == 2:
#                         res_image = self.client.basicAccurate(image)
#                     elif self.level == 3:
#                         res_image = self.client.webImage(image)
#                     else:
#                         # options 可选参数：CHN_ENG中英混合
#                         res_image = self.client.basicGeneral(image, options={'language_type': 'CHN_ENG'})
#                     print('防护', res_image)
#                     # result = json.loads(res_image)
#                     result = res_image
#                     # return True, result['words_result'][0]['words']
#                     return True, [item.get('words') for item in result['words_result']]
#             elif file_url:
#                 if self.level == 2:
#                     res_url = self.client.basicAccurateUrl(file_url)
#                 elif self.level == 3:
#                     res_url = self.client.webImageUrl(file_url)
#                 else:
#                     res_url = self.client.basicGeneralUrl(file_url, options={'language_type': 'CHN_ENG'})
#                 result = json.loads(res_url)
#                 return True, result['words_result'][0]['words']
#         except Exception as e:
#             return False, str(e)
