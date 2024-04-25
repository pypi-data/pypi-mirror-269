import os
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

JAY_COPILOT_API_KEY = os.getenv("JAY_COPILOT_API_KEY")
JAY_COPILOT_USERNAME = os.getenv("JAY_COPILOT_USERNAME")
JAY_COPILOT_USER_PASSWORD = quote(os.getenv("JAY_COPILOT_USER_PASSWORD"))
# USE_PROXY = bool(os.getenv("USE_PROXY"))
# HTTPS_PROXY = os.getenv("HTTPS_PROXY")

# PROXIES = {
#     "https": (
#         f"http://sovcombank%5C{JAY_COPILOT_USERNAME}:{JAY_COPILOT_USER_PASSWORD}"
#         f"@uhq-mcafee.sovcombank.group:9090"
#     ),
# }
