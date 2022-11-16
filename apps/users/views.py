from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import authentication_classes

from apps.users.models import Users, Article
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

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache, caches


# 声明式缓存，通过装饰器缓存请求
# @method_decorator(decorator=cache_page(timeout=600), name='get')
class UsersView(APIView):
    authentication_classes = ()

    def get(self, request):
        # if cache.get('user_data'):
        #     user_data = cache.get('user_data')
        #     return Response({
        #         "code": 200,
        #         'message': 'success',
        #         'data': {
        #             'list': user_data,
        #             "pagination": {
        #                 "total_count": len(user_data),
        #             }
        #         }
        #     })
        email_query = request.GET.get('email', "") # tom
        first_name = request.GET.get('first_name', "")
        offset = request.GET.get('offset', 0)
        limit = request.GET.get('limit', 10)
        # users = Users.objects.filter(
        #     # email__endswith=email_query
        #     gender__in=[0, 2]
        # )

        # users = Users.objects.filter(
        #     email__icontains=email_query
        # )
        # users = Users.objects.filter(
        #     email__icontains=email_query,
        #     first_name__icontains=first_name
        # )

        # users = Users.objects.get_user_by_email(email_query)
        user_query_set = Users.objects.get_queryset()
        users = Users.objects.get_queryset().query_user_by_email(email_query).query_user_by_first_name(first_name)

        total_count = users.count()
        _users = users.get_user_page_info(offset, limit)

        user_data = UserModelSerializer(_users, many=True).data
        # user_data = map(lambda user: {
        #     "id": user.id,
        #     "first_name": user.first_name,
        #     "last_name": user.last_name,
        #     "email": user.email,
        # }, _users)

        # cache.set('user_data', user_data, timeout=600)

        # _data = cache.get('user_data')
        # print(_data)
        # my_cache = caches['session']
        # my_cache.set('user_data', user_data)

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

        cache.delete('user_data')

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


class UserArticleView(APIView):
    authentication_classes = ()

    def get(self, request, user_id):
        user = Users.objects.filter(pk=user_id).first()
        if not user:
            return Response({"code": "404", "message": "user not exists"})

        user_articles = user.user_articles.all()

        # articles = Article.objects.filter(user__id=user_id)

        return Response([
            {
                "article_title": article.title
            } for article in user_articles
        ])


class AticleView(APIView):

    authentication_classes = ()

    def get(self, request):

        articles = Article.objects.all().prefetch_related('user')

        return Response([
            {
                "article_title": article.title,
                "article_user": article.user.email,
            } for article in articles
        ])


class UsersExportView(APIView):
    authentication_classes = ()

    def get(self, request):
        from apps.tasks.async_tasks import export_users
        export_users.delay()
        # start celery: celery -A apps.tasks.task worker -Q default--loglevel=debug
        # export_users()
        return Response({'code': 200})