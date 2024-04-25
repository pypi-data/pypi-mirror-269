from enum import Enum


class AppType(str, Enum):
    """Jay Copilot API GPT Application Templates."""

    OPENAI_GPT = "directLLM"
    JUST_GPT = "justGPT"
    GIGA_CHAT = "gigaChat"
    YA_GPT = "yandexGpt"
