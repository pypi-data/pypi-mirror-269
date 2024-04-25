class CantCreateApplication(Exception):
    """Program can't create application."""


class ApiServiceError(Exception):
    """Program can't request to Just AI API."""


class CantCreateDialogWithApp(Exception):
    """Program can't create dialog with app from Jay Copilot API."""
