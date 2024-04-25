from typing import Any
import requests
from pydantic import HttpUrl
from app.exception.client_exception import ApiServiceError, CantCreateApplication, CantCreateDialogWithApp
from app.config import JAY_COPILOT_API_KEY
from app.schemas import AppType


class JayCopilot():

    HEADERS = {
        "X-API-KEY": JAY_COPILOT_API_KEY,
        "Content-Type": "application/json",
    }

    BASE_URL = HttpUrl(
        "https://app.jaycopilot.com/api/appsAdapter/")

    TIMEOUT = (120, 300)

    def __init__(self, app_template: AppType = AppType.OPENAI_GPT,
                 modelName: str = 'gpt-3.5-turbo-1106',
                 system_prompt: str = "",
                 proxies: dict = None,
                 timeout: tuple = TIMEOUT,
                 **model_kwargs) -> None:
        self.TIMEOUT = timeout
        self.proxies = proxies
        self.app_template = app_template
        self.LLM_PARAMS = {
            "modelName": modelName,
            # "modelName": 'gpt-4-1106-preview',
            "systemPrompt": system_prompt,
            **model_kwargs
        }

    def _request_to_client(self, method: str, endpoint: str, **kwargs) -> Any:
        """Общий метод для выполнения HTTP-запросов к API."""
        url = self.BASE_URL.unicode_string() + endpoint
        try:
            with requests.Session() as session:
                session.headers.update(self.HEADERS)
                if self.proxies:
                    session.proxies.update(self.proxies)

                session.timeout = self.TIMEOUT

                # Выбор метода запроса Get, Post, Delete
                request_method = getattr(session, method.lower(), None)
                if request_method is None:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                response = request_method(url, **kwargs)
                response.raise_for_status()  # Проверка на HTTP ошибки

                if method.lower() != 'delete':
                    return response.json()
                else:
                    return None
        except requests.exceptions.RequestException as exc:
            raise ApiServiceError from exc

    def get_app_templates(self):
        """Получить шаблоны для Jay Copilot

        Returns:
            dict: dict with template params and describe 
        """
        endpoint = "/templates"
        response = self._request_to_client(method='get', endpoint=endpoint)

        return response

    def get_dialogs(self, hasUnreadChanges: bool = False):
        """Получение списка диалогов
        https://help.jaycopilot.com/api/#tag/Conversations/operation/createConversation

        Returns:
            list: Список диалогов (response)
        """
        endpoint = "conversations/"
        payload = {'hasUnreadChanges': str(hasUnreadChanges).lower()}
        response = self._request_to_client(
            method='get', endpoint=endpoint, params=payload)

        return response

    def get_dialog(self, dialog_id: str):
        """Получение диалога по идентификатору со всей информацией и историей сообщений 
        https://help.jaycopilot.com/api/#tag/Conversations/operation/findConversations

        Args:
            dialog_id (str): идентификатор диалога

        Returns:
            dict: response
        """
        endpoint = f"conversations/{dialog_id}"
        response = self._request_to_client(
            method='get', endpoint=endpoint)

        return response

    def delete_dialog(self, dialog_id: str):
        """Удаление диалога по идентификатору
        https://help.jaycopilot.com/api/#tag/Conversations/operation/deleteConversation

        Args:
            dialog_id (str): идентификатор диалога

        Returns:
            dict: response
        """
        endpoint = f"conversations/{dialog_id}"
        self._request_to_client(
            method='delete', endpoint=endpoint)

        return 1

    def delete_dialog_history(self, dialog_id: str):
        """Удаление истории сообщений диалога (очистка контекста).
        https://help.jaycopilot.com/api/#tag/Conversations/operation/updateConversation

        Args:
            dialog_id (str): идентификатор диалога
        """
        endpoint = f"conversations/{dialog_id}/clear"
        response = self._request_to_client(
            method='post', endpoint=endpoint)

        return response

    def _create_dialog_with_app(self, app_id: str) -> str:
        endpoint = "conversations/"
        json_data = {"app": {"id": app_id}}
        response = self._request_to_client(
            method='post', endpoint=endpoint, json=json_data)

        if response["status"] != "READY":
            raise CantCreateDialogWithApp

        return response["id"]

    def _create_app(self) -> str:
        endpoint = "apps/"
        json_data = {"template": self.app_template, "params": self.LLM_PARAMS}
        response = self._request_to_client(
            method='post', endpoint=endpoint, json=json_data)

        if response["status"] == "FAILED":
            raise CantCreateApplication

        return response["id"]

    def create_chat(self) -> str:
        """Create new chat with LLM params

        Returns:
            str: dialog_id
        """
        app_id = self._create_app()
        dialog_id = self._create_dialog_with_app(app_id=app_id)

        return dialog_id

    def generate_text(self, prompt: str, dialog_id: str | None = None) -> str:
        """Send message to LLM. if dialog_id is None, than created new chat.
        https://help.jaycopilot.com/api/#tag/Conversations/operation/getConversationHistory

        Args:
            prompt (str): message from user to llm
            dialog_id (str | None, optional): if dialog_id is None, than created new chat. Defaults to None.

        Returns:
            dict: response отправленного сообщения, со всей инфой 
        """
        if dialog_id is None:
            dialog_id = self.create_chat()

        endpoint = f"conversations/{dialog_id}/message"
        json_data = {"text": prompt}

        response = self._request_to_client(
            method='post', endpoint=endpoint, json=json_data)

        return response
