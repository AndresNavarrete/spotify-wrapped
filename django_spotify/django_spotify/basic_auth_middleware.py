from django.http import HttpResponse
import base64
import os
class BasicAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        username = os.getenv("DJANGO_ANON_USER")
        password = os.getenv("DJANGO_ANON_PASSWORD")

        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not self._check_credentials(auth_header, username, password):
            return HttpResponse('Unauthorized', status=401)

        response = self.get_response(request)
        return response

    def _check_credentials(self, auth_header, username, password):
        auth_type, encoded_credentials = auth_header.split(' ', 1)
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        provided_username, provided_password = decoded_credentials.split(':', 1)

        return provided_username == username and provided_password == password