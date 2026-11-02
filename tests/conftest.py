# pytest 启动时最先加载这个文件。
# 环境变量的优先级高于 .env,所以这里强制 test 用 fake,不会碰真实 Azure
import os

os.environ["LLM_BACKEND"] = "fake"
os.environ["RETRIEVER_BACKEND"] = "fake"