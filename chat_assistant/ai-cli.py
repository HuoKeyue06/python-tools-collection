from src.llm_client import ZhipuClient
import json
import argparse
import datetime
from src.tool import GetCurrentTimeTool, CalculatorTool,ToolRegistry


history_file = "chat_history.json"
def load_history():
    try:
        with open('D:\\VScode\\my-first-project\\chat_history.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        pass
    return [
        {"role": "system", "content": "你是我的人工智能助手，协助我解答问题。"}
    ]
def save_history(history):
    try:
        with open('D:\\VScode\\my-first-project\\chat_history.json', 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
            print("保存聊天记录成功")
    except IOError as e:
        print(f"保存聊天记录失败: {e}")
def export_history(output_file):
    messages = load_history()
    if output_file is True:
        output_file = f"chat_history_export_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
    elif isinstance(output_file, str): #检查output_file变量是不是字符串类型
        output_file = output_file
        if not output_file.endswith('.md'): #判断是否以.md结尾
            output_file += '.md'
        else:
            print("导出失败，输出文件名必须以 .md 为后缀")
            return
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 智谱聊天记录\n\n")
        for msg in messages:
            if msg['role'] == 'user':
                f.write(f"**用户:** {msg['content']}\n\n")
            elif msg['role'] == 'assistant':
                f.write(f"**智谱:** {msg['content']}\n\n")
    print(f"聊天记录已导出到 {output_file}")   
          

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", help="请输入问题：")
    parser.add_argument("--load", action="store_true", help="继续对话")
    parser.add_argument("--export",nargs='?', const=True, default=None, help="导出聊天记录")
    parser.add_argument("--clear", action="store_true", help="清除聊天记录")
    args = parser.parse_args()
    tool_registry = ToolRegistry()
    
    tool_registry.register(GetCurrentTimeTool())
    tool_registry.register(CalculatorTool())
   

    if args.export is not None:
        export_history(output_file=args.export)
    if args.clear:
        confirm = input("确定要清除聊天记录吗？(yes/no): ")
        if confirm.lower() == 'yes':
            save_history([{"role": "system", "content": "你是我的人工智能助手，协助我解答问题。"}])
            print("聊天记录已清除")
        else:
            print("取消清除聊天记录")
    if args.question:
        #进行单轮问答
        messages = [{"role": "system", "content": "你是我的人工智能助手，协助我解答问题。"}]

        messages.append({"role": "user", "content": args.question})
        client = ZhipuClient()
        replay = client.chat(messages)
        print(f"智谱回复: {replay}")
        messages.append({"role": "assistant", "content": replay})
        return
    if args.load:
        #进行多轮问答
        messages = load_history()
        print("已加载历史聊天记录，继续对话...")
    else:
        messages = [{"role": "system", "content": "你是我的人工智能助手，协助我解答问题。"}]

    print("进入对话模式，输入 'exit' 退出程序。")
    while True:
        user_input=input("请输入问题（输入 'exit' 退出）：")
        if user_input.lower() == 'exit':
            save_history(messages)
            print("退出程序")
            break
        messages.append({"role":"user","content":user_input})
        print("正在调用智谱API，请稍等...")
        client = ZhipuClient()
        tool_params=list(tool_registry.get_schemas().values())
        replay = client.chat_with_tools(messages,tool_params)
        if "error" in replay:
            print(f"智谱API调用失败: {replay['error']}")
            continue
        choice = replay["choices"][0]
        if choice["finish_reason"] == "tool_calls":
            tool_calls = choice["message"]["tool_calls"]
            messages.append(choice["message"])
            for tool_call in tool_calls:
                tool_name = tool_call['function']['name']
                tool_args = json.loads(tool_call['function']['arguments'])
                print(f"正在调用工具: {tool_name},调用参数: {tool_args}")
                tool_result = tool_registry.execute(tool_name, **tool_args)
                messages.append({"role": "tool", 
                                 "tool_call_id": tool_call['id'],
                                 "content": json.dumps(tool_result,ensure_ascii=False)})
                final_replay = client.chat(messages)
                print(f"智谱回复: {final_replay}")
                messages.append({"role": "assistant", "content": final_replay})
        else:
            print(f"智谱回复: {choice['message']['content']}")
            messages.append({"role": "assistant", "content": choice['message']['content']})


if __name__ == "__main__":
    main()

