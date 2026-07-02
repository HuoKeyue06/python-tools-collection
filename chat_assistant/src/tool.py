class ToolRegistry:
    def __init__(self):
        """初始化一个空字典，为工具注册表"""
        self.tools = {} 

    def register(self, tool):
        """将工具注册到注册表中"""
        self.tools[tool.name] = tool

    def execute(self, tool_name, *args, **kwargs):
        """检查工具是否存在"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found.")
        return self.tools[tool_name].execute(*args, **kwargs)
    def get_schemas(self):
        """返回所有工具的JSON Schema列表，用于传给智谱API"""
        return {name: tool.schema for name, tool in self.tools.items()}
import datetime
class GetCurrentTimeTool:
    def __init__(self):
        self.name = "get_current_time"
        self.description = "获取当前时间"
        self.schema = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }

    def execute(self):
        return {"result": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
class CalculatorTool:
    def __init__(self):
        self.name = "calculator"
        self.description = "一个简单的计算器工具，支持加减乘除运算"
        self.schema = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "要计算的数学表达式，例如 '2 + 2 * 3'"
                        }
                    },
                    "required": ["expression"]
                }
            }
        }

    def execute(self, expression):
        try:
            # 使用 eval 计算表达式，注意安全性问题
            result = eval(expression, {"__builtins__": {}})
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}