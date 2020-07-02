import jwt
import json

from django.http import JsonResponse

from users.models import User
from dr_martens.settings import (
    SECRET_KEY,
    ALGORITHM
)

def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get("Authorization", None)
        if access_token is not None:
            try:
                decode_token = jwt.decode(access_token, SECRET_KEY, algorithms = ALGORITHM)
                user_id      = decode_token['user_id']
                if User.objects.get(id = user_id):
                    user         = User.objects.get(id = user_id)
                    request.user = user
                    return func(self, request, *args, **kwargs)

            except jwt.DecodeError:
                return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 400)

            except User.DoesNotExist:
                return JsonResponse({'message' : 'INVALID_USER'}, status = 400)
                
        return JsonResponse({'message' : 'NEED_LOGIN'}, status = 401)

    return wrapper