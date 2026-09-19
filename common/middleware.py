import base64
import pickle


class PreferencesMiddleware:
    """Restaure les préférences d'affichage depuis un cookie."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.prefs = {}
        raw = request.COOKIES.get("prefs")
        if raw:
            try:
                request.prefs = pickle.loads(base64.b64decode(raw))
            except Exception:
                request.prefs = {}
        return self.get_response(request)
