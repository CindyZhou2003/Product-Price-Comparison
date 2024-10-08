import json
import logging

import pytz
from django.db.models import Sum
from django.core import serializers
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import make_aware
from django.views.decorators.http import require_http_methods
from backend.models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import jieba  # 引入jieba进行中文分词
from django.contrib.auth import authenticate, login as auth_login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import re
logging.basicConfig(level=logging.DEBUG)  # 设置最低日志级别为 DEBUG


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """
    用户登录函数
    :param request:
    :return:
    """
    response = {}
    try:
        # 获取请求体中的JSON数据
        data = json.loads(request.body.decode('utf-8'))
        check_username = data.get('username')
        # check_email = data.get("email")  # 邮箱
        check_psw = data.get("password")     # 用户输入的密码

        # 使用 Django 提供的 authenticate 方法来验证用户名和密码
        # user = authenticate(request, email=check_email, password=check_psw)
        user = authenticate(request, username=check_username, password=check_psw)

        if user is not None:
            # 用户名和密码正确，将用户标记为已登录状态
            auth_login(request, user)
            response['status'] = 'ok'
            response['message'] = 'Login Successfully.'
            response['user_id'] = user.id  # 返回用户ID以便前端使用
        else:
            # Debugging check
            from backend.models import Account  # Replace with your app name
            try:
                user = Account.objects.get(username=check_username)
                if check_password(check_psw, user.password):
                    response['message'] = 'Password is correct, but authenticate failed.'
                else:
                    response['message'] = 'Password is incorrect.'
            except Account.DoesNotExist:
                response['message'] = 'User does not exist.'

    except json.JSONDecodeError:
        response['status'] = 'error'
        response['message'] = 'Invalid JSON format.'
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    print(response)
    return JsonResponse(response)

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """
    用户注册函数
    :param request:
    :return:
    """
    print(f"Request method: {request.method}")
    response = {}
    try:
        # 解析前端传来的 JSON 数据
        data = json.loads(request.body.decode('utf-8'))
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # 1. 校验必填字段是否为空
        if not username or not email or not password:
            response['status'] = 'error'
            response['message'] = '用户名、邮箱和密码不能为空 Username, email, and password cannot be empty.'
            return JsonResponse(response)

        # 2. 校验用户名和密码长度（用户名要求最短3个字符，密码最短6个字符）
        if len(username) < 3:
            response['status'] = 'error'
            response['message'] = '用户名长度必须至少为3个字符 Username must be at least 3 characters long.'
            return JsonResponse(response)

        if len(password) < 6:
            response['status'] = 'error'
            response['message'] = '密码长度必须至少为6个字符 Password must be at least 6 characters long.'
            return JsonResponse(response)

        # 3. 校验邮箱格式是否正确
        try:
            validate_email(email)  # 使用Django内置的邮箱验证器
        except ValidationError:
            response['status'] = 'error'
            response['message'] = 'Invalid email format.'
            return JsonResponse(response)

        # 4. 校验用户名和邮箱的唯一性
        if Account.objects.filter(username=username).exists():
            response['status'] = 'error'
            response['message'] = 'Username already exists.'
            return JsonResponse(response)

        if Account.objects.filter(email=email).exists():
            response['status'] = 'error'
            response['message'] = '邮箱已存在 Email already exists.'
            return JsonResponse(response)

        # 5. 密码复杂度检查（可选，如果需要，可以加入更多检查规则）
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$', password):
            response['status'] = 'error'
            response['message'] = 'Password must contain at least one letter and one number.'
            return JsonResponse(response)

        # 6. 加密密码
        encrypted_password = make_password(password)

        # 7. 创建并保存用户
        user = Account.objects.create(username=username, email=email, password=encrypted_password)
        user.save()

        # 8. 返回成功信息
        response['status'] = 'ok'
        response['message'] = 'Registration successful.'
        response['user_id'] = user.id  # 返回创建用户的ID

    except json.JSONDecodeError:
        response['status'] = 'error'
        response['message'] = 'Invalid JSON format.'
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)



def update_price(request):
    """
    更新价格函数
    :param request:
    :return:
    """
    response = {}
    return JsonResponse(response)


@require_http_methods(["GET"])
def search_products(request):
    """
    搜索库中的产品，支持分词处理和平台过滤
    :param request:
    :return:
    """
    response = {
        "status": "ok",
        "message": "Search successful.",
        "products": []  # 确保初始化 products 为空列表
    }

    try:
        # 获取请求中的数据
        search = request.GET.get("search")
        # platform = request.GET.get("platform")

        # 如果search为空，直接返回空结果
        if not search:
            response["status"] = "error"
            response["message"] = "搜索关键词为空"
            return JsonResponse(response)

        # logging.debug(f"Search term: {search}")

        # 对搜索关键词进行分词处理
        search_terms = jieba.lcut(search)  # 使用jieba进行分词

        # 创建Q对象来构建查询条件
        query = Q()
        for term in search_terms:
            query |= Q(title__icontains=term)  # 模糊查询title中包含每个分词

        # 平台过滤
        # if platform:
        #     query &= Q(platform=platform)
        #     # 根据条件查询符合的产品
        #     products = Products.objects.filter(query)
        # else:
        #     products = Products.objects.filter(query)

        products = Products.objects.filter(query)

        logging.debug(f"Products found: {products}")  # 打印找到的产品信息
        # 构建返回结果
        for product in products:
            response["products"].append({
                "id": product.id,
                "title": product.title,
                "price": product.price,
                "comments": product.comments,
                "shop": product.shop,
                "img": product.img,
                "link": product.link,
                "platform": product.platform
            })

        # 打印构建的响应数据，检查返回的 JSON 是否包含完整的 products 列表
        # logging.debug(f"Response Data: {response}")

    except json.JSONDecodeError:
        response["status"] = "error"
        response["message"] = "Invalid JSON format"
    except Exception as e:
        response["status"] = "error"
        response["message"] = str(e)


    # 打印最终返回的 JSON 数据
    # print(f"Final JSON response: {response}")

    return JsonResponse(response)

