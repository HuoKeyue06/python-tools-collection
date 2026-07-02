import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

class ZhipuClient:
    def __init__(self):
        self.api_key = os.getenv("zhipu_api_key")
        self.url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    def chat(self, messages: list, model: str = "glm-4-flash"):
        headers = {
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json"  
        }
        data = {"model": model, "messages": messages} 
        try:
            r = requests.post(self.url, headers=headers, json=data)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            else:
                print(f"请求失败，状态码: {r.status_code}, 错误信息: {r.text}")    
                return f"请求失败,错误信息: {r.text}"
        except Exception as e:
            print(f"请求失败，异常信息: {e}")
            return "请求失败，发生异常"
    def chat_with_tools(self, messages: list, tools:list,model: str = "glm-4-flash"):
        """
        发送带工具定义的请求
        Args:
            messages (list): 聊天消息列表
            tools (list): 工具列表,格式为[{"type":"function":{...}},...]
            model (str, optional): 模型名称. Defaults to "glm-4-flash".
            Returns:
                str: 模型返回的答案
        """
        headers = {
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json"  
        }
        data = {"model": model, "messages": messages, "tools": tools}
        try: 
            r = requests.post(self.url, headers=headers, json=data)
            if r.status_code == 200:
                return r.json()
            else:
                print(f"请求失败，状态码: {r.status_code}, 错误信息: {r.text}")    
                return f"请求失败,错误信息: {r.text}"
        except Exception as e:
            print(f"请求失败，异常信息: {e}")
            return "请求失败，发生异常"
        

