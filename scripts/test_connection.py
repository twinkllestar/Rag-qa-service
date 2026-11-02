# 一次性的连接测试:确认 endpoint、key、deployment name 都对
# 这个文件只是 debug 用的,不属于应用本身
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # 读取 .env 文件,放进环境变量

client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

response = client.responses.create(
    model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
    input="What is the capital of France? Answer in one word.",
)

print("answer:", response.output_text)