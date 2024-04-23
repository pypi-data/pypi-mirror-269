'''
Description: Json解析
Version: 0.0.1
Author: aka.zhp
Date: 2024-01-04 11:47:32
LastEditTime: 2024-01-04 11:49:08
'''

import json

class JsonHelper:
    def extract_json_from_text(self, text):
        start_index = text.find('{')
        end_index = text.rfind('}')
        if start_index == -1 or end_index == -1:
            return {}
        json_string = text[start_index:end_index+1]
        try:
            json_data = json.loads(json_string)
            return json_data
        except json.JSONDecodeError:
            print(json_string)
            print("json提取失败")
            return {}
        
    def extract_json_list_from_text(self, text):
        start_index = text.find('[')
        end_index = text.rfind(']')
        json_string = text[start_index:end_index+1]
        try:
            json_data = json.loads(json_string)
            return json_data
        except json.JSONDecodeError:
            print(json_string)
            print("json提取失败")
            return {}
