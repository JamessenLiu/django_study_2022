from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from apps.users.models import Users
from apps.users.serializers import CreateUserSerializer, UserModelSerializer


def get_userinfo(request):
    user = Users.objects.get(id=1)
    print(user)
    result = render(request, 'userinfo.html', context={
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    })
    return result


def get_users(request):
    # users = Users.objects.all()
    # user_data = []
    # for user in users:
    #     user_data.append({
    #         "id": user.id,
    #         "first_name": user.first_name,
    #         "last_name": user.last_name,
    #         "email": user.email,
    #     })

    # print(request)
    # import logging
    # logger = logging.getLogger('errMsg') # 注意日志处理器的级别
    # logger.info('info log')
    # logger.error("error log")

    if request.method == 'GET':
        email_query = request.GET.get('email') # tom
        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10)
        users = Users.objects.filter(
            # email__endswith=email_query
            gender__in=[0, 2]
        )
        total_count = users.count()
        _users = users[offset:offset + limit]
        user_data = list(map(lambda user: {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }, _users))

        return JsonResponse({
            "code": 200,
            'message': 'success',
            'data': {
                'list': user_data,
                "pagination": {
                    "total_count": total_count,
                    'offset': offset,
                    "limit": limit,
                }
            }
        })
    else:
        import json
        user_data = json.loads(request.body)

        # 构建数据模型，save
        # user = Users(
        #     first_name=user_data['first_name'],
        #     last_name=user_data['last_name'],
        #     email=user_data['email'],
        #     gender=user_data['gender']
        # )
        # user.save()

        # create方法
        user = Users.objects.create(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                gender=user_data['gender']
        )

        # 创建用户
        return JsonResponse({'code': 200, 'message': 'success', "data": {
            "userId": user.id
        }})

import json
import time
from rest_framework.views import APIView
from rest_framework.response import Response



class UsersView(APIView):

    def get(self, request):
        email_query = request.GET.get('email') # tom
        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10)
        users = Users.objects.filter(
            # email__endswith=email_query
            gender__in=[0, 2]
        )
        total_count = users.count()
        _users = users[offset:offset + limit]

        user_data = UserModelSerializer(_users, many=True).data
        # user_data = map(lambda user: {
        #     "id": user.id,
        #     "first_name": user.first_name,
        #     "last_name": user.last_name,
        #     "email": user.email,
        # }, _users)

        return Response({
            "code": 200,
            'message': 'success',
            'data': {
                'list': user_data,
                "pagination": {
                    "total_count": total_count,
                    'offset': offset,
                    "limit": limit,
                }
            }
        })

    def post(self, request):
        import json
        user_data = json.loads(request.body)
        serializer = CreateUserSerializer(data={
            "email": user_data.get("email"),
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "gender": user_data.get("gender"),
        })

        if not serializer.is_valid():
            return Response(serializer.errors)

        _user = Users.objects.filter(email=user_data['email']).first()
        if _user:
            return Response({"code": 404})


        user = Users.objects.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            gender=user_data['gender']
        )

        # 创建用户
        return JsonResponse({'code': 200, 'message': 'success', "data": {
            "userId": user.id
        }})


class UserLoginView(APIView):
    authentication_classes = ()

    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        user = Users.objects.filter(email=email).first()
        if not user:
            return Response({
                "code": 404,
                "message": "User does not exist"
            })

        payload = {
            "email": email,
            "exp": int(time.time()) + 30 * 60,
        }
        from django.conf import settings
        import jwt
        secret_key = settings.SECRET_KEY
        token = jwt.encode(payload, secret_key, algorithm='HS256').decode("utf-8")

        return Response({
            'code': 200,
            'message': 'success',
            'data': {
                'token': token
            }
        })
