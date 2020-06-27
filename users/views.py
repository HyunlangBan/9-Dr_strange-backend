import json
import jwt
import re
import bcrypt

from django.shortcuts import render
from django.views import View
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import (
    JsonResponse,
    HttpResponse
)

from dr_martens.settings import (
    SECRET_KEY,
    ALGORITHM
)
from users.models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            validate_email(data['email'])
            if User.objects.filter(nickname = data['nickname']).exists():
                return HttpResponse(status = 401)

            if re.match("^[0-9A-Za-z]{6,20}$", data['nickname']) == None:
                return HttpResponse(status = 401)

            if re.match("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d$@$!%*#?&]{6,20}$", data['password']) == None:
                return HttpResponse(status = 401)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            User(
                name         = data['name'],
                nickname     = data['nickname'],
                password     = hashed_password.decode('utf-8'),
                birthday     = data['birthday'],
                email        = data ['email'],
                phone_number = data['phone_number'],
            ).save()
            return HttpResponse(status = 200)

        except ValidationError:
            return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)

        except KeyError as e:
            return JsonResponse({'message' : str(e) + ' is right key name.'}, status = 400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(nickname = data['nickname']).exists():
                users = User.objects.get(nickname = data['nickname'])
                if bcrypt.checkpw(data['password'].encode('utf-8'), users.password.encode('utf-8')):
                    token = jwt.encode({'users_id' : users.id}, SECRET_KEY, algorithm = ALGORITHM)
                    return JsonResponse({'access_token':token.decode('utf-8')}, status = 200)

                return HttpResponse(status = 401)
                
        except KeyError as e:
            return JsonResponse({'message' : str(e) + ' is right key name.'}, status = 400)