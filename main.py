from openai import OpenAI
import os
import argparse


def get_ai_reply(user_input):
    # 初始化OpenAI客户端
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    is_answering = False  # 判断是否结束思考过程并开始回复

    # 创建聊天完成请求
    completion = client.chat.completions.create(
        model="deepseek-r1",  # 模型名称
        messages=[
            {"role": "user", "content": user_input}
        ],
        stream=True,
        # 在最后一个chunk返回Token使用量
        stream_options={
            "include_usage": True
        }
    )

    for chunk in completion:
        # 如果chunk.choices为空，则打印usage
        if not chunk.choices:
            print("\nUsage:")
            print(chunk.usage)
        else:
            delta = chunk.choices[0].delta
            if hasattr(delta, 'content') and delta.content is not None:
                # 开始回复
                if delta.content != "" and is_answering == False:
                    is_answering = True
                # 打印回复
                print(delta.content, end='', flush=True)

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="传递用户输入的内容")
    parser.add_argument('user_input', type=str, help='用户输入的内容')
    args = parser.parse_args()

    # 调用函数
    get_ai_reply(args.user_input)