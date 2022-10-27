from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from apps.users.models import Users


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

    print(request)
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
# Create your views here.
