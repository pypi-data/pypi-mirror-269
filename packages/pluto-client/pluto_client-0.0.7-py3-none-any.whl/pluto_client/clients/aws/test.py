import os
import sys

sys.path.insert(0, os.path.realpath(os.path.join(__file__, "../../../../")))

print(sys.path)

from pluto_client import Bucket


os.environ["PLUTO_PROJECT_NAME"] = "llama3-sagemaker"
os.environ["PLUTO_STACK_NAME"] = "aws"
os.environ["PLUTO_PLATFORM_TYPE"] = "AWS"

bucket = Bucket.build_client("llama3-rag-bot")


bucket.put("sagemaker", "sagemaker.py")
