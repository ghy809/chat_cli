import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# 1. 加载 .env 里的密钥
load_dotenv()

# 定义历史记录文件名
HISTORY_FILE = "history.json"

# 2. 配置 DeepSeek 客户端
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

# 3. 写一个最简单的单轮问答函数
def ask_question(question: str) -> str:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": question}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# 4. 主程序入口
if __name__ == "__main__":
    message_history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            loaded_history = json.load(f)
            message_history = loaded_history
        print(f"\U0001f4c2 已加载历史对话，共 {len(message_history)} 条记录。")
    else:
        print("\U0001f4c2 未找到历史记录，开始新对话。")
        print("\U0001f916 聊天助手已启动！输入 'exit' 可退出程序。")

    while True:
        user_input = input("\n你: ")
        if user_input.lower() == "exit":
            print(f"\U0001f4c1 正在保存对话到: {os.path.abspath(HISTORY_FILE)}")
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(message_history, f, ensure_ascii=False, indent=2)
            print("\U0001f44b 再见！")
            break

        if not user_input.strip():
            print("\U0001f916 输入不能为空，请再说一遍。")
            continue

        message_history.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=message_history,
            temperature=0.7
        )
        ai_reply = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": ai_reply})

        print(f"\U0001f916: {ai_reply}")
