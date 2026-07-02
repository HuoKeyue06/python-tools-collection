# AI命令助手
## 项目简介
基于智谱API开发的命令行问答工具，支持多轮对话，历史记录
## 技术栈
- Python：3.11
- 智谱API （GLM-4-Flash）
- Python 模块：
- requests，argparse,pyhton-dotenv
## 安装与配置
1. 克隆项目到本地
2. 安装依赖：pip install python-dotenv requests
3. 创建.env文件，并添加智谱API密钥：API_KEY=你的智谱API密钥
## 使用方法
1. 运行ai-cli.py文件
2. 输入命令行，回车
3. 获取答案
4. 加载历史对话
'''bash
python ai-cli.py --load
'''
## 单轮问答
'''bash
python ai-cli.py --question "你的问题"
'''
## 多轮对话
'''bash
python ai-cli.py --load
'''
## 多轮对话示例
'''text
你：你好
AI：你好，我是智谱AI，你可以向我提问任何问题。
你：你是谁
AI：我是智谱AI，一个基于智谱API的命令行工具。
你：你叫什么名字
AI：我叫智谱AI。
你：exit
对话退出，自动保存
'''
## 命令行参数
- question：单轮问答
- load：加载历史对话
- export：导出对话
- clear：清除历史对话

