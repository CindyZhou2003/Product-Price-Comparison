import json
import logging
import requests
from django.core import mail
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods
from selenium.webdriver.common.devtools.v129.fetch import continue_response

from backend.models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import jieba  # 引入jieba进行中文分词
import jieba.posseg as pseg
from django.contrib.auth import authenticate, login as auth_login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
import re
logging.basicConfig(level=logging.DEBUG)  # 设置最低日志级别为 DEBUG
import random
from django.core.mail import send_mail
from backend.crawler import crawl_tb, crawl_jd,tb_update_price, jd_update_price
import string
from django.core.cache import cache
from django.contrib.auth.hashers import check_password

@csrf_exempt
@require_http_methods(["POST"])
def send_verification_code(request):
    """
    发送验证码到用户邮箱，验证码5分钟内有效
    :param request: POST请求，包含用户邮箱
    :return: JsonResponse
    """
    response = {}

    try:
        # 获取请求数据
        data = json.loads(request.body.decode('utf-8'))
        user_email = data.get('email')
        forget = data.get('forget', False)  # 默认为 False

        if not user_email:
            response = {'status': 'error', 'message': '请提供邮箱地址'}
            return JsonResponse(response)

        # 处理两种情况
        try:
            account = Account.objects.get(email=user_email)
            # 如果找到了账号，且 forget 为 True，发送邮件
            if forget:
                send_verification_email(user_email)
                response['status'] = 'success'
                response['message'] = '验证码已发送到您的邮箱'
                return JsonResponse(response)

            # 找到了账号，但 forget 为 False，返回错误
            response['status'] = 'error'
            response['message'] = '邮箱已被注册过'
            return JsonResponse(response)

        except Account.DoesNotExist:
            # 没找到账号，且 forget 为 False，发送邮件
            if not forget:
                send_verification_email(user_email)
                response['status'] = 'success'
                response['message'] = '验证码已发送到您的邮箱'
                return JsonResponse(response)

            # 没找到账号，且 forget 为 True，返回错误
            response['status'] = 'error'
            response['message'] = '账号不存在'
            return JsonResponse(response)

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)


def send_verification_email(user_email):
    """
    辅助函数：生成验证码并发送邮件
    """
    # 生成6位数字验证码
    verification_code = ''.join(random.choices(string.digits, k=6))

    # 将验证码存入缓存，设置过期时间为5分钟
    cache.set(user_email, verification_code, timeout=300)  # 5分钟过期

    # 准备邮件内容
    subject = "您的验证码"
    message = f"亲爱的用户，\n\n您的验证码是：{verification_code}\n\n验证码有效时间为5分钟，请及时使用。"

    # 发送邮件
    send_mail(
        subject,
        message,
        'cindyzhou6418@gmail.com',  # 替换为发件人地址
        [user_email],
        fail_silently=False,
    )



@csrf_exempt
@require_http_methods(["POST"])
def verify_code(request):
    """
    验证用户输入的验证码是否正确，并检查是否在有效时间内
    :param request: POST请求，包含用户邮箱和验证码
    :return: JsonResponse
    """
    response = {}

    try:
        # 获取请求数据
        data = json.loads(request.body.decode('utf-8'))
        user_email = data.get('email')
        user_code = data.get('verification_code')

        if not user_email or not user_code:
            response['status'] = 'error'
            response['message'] = '请提供邮箱和验证码'
            return JsonResponse(response)

        # 从缓存中获取验证码
        stored_code = cache.get(user_email)

        if not stored_code:
            response['status'] = 'error'
            response['message'] = '验证码已过期或无效，请重新获取'
            return JsonResponse(response)

        # 校验验证码是否正确
        if stored_code == user_code:
            response['status'] = 'success'
            response['message'] = '验证码验证成功'
        else:
            response['status'] = 'error'
            response['message'] = '验证码错误'

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)


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
            response['status'] = 'success'
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
    # print(f"Request method: {request.method}")
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
        response['status'] = 'success'
        response['message'] = 'Registration successful.'
        response['user_id'] = user.id  # 返回创建用户的ID

    except json.JSONDecodeError:
        response['status'] = 'error'
        response['message'] = 'Invalid JSON format.'
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)

@csrf_exempt
@require_http_methods(["POST"])
def change_password(request):
    """
    用户修改密码函数
    :param request:
    :return:
    """
    response = {}
    try:
        # Parse JSON data from the request
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get("user_id")
        old_password = data.get("old_password")
        new_password = data.get("new_password")

        # Validate inputs
        if not user_id or not old_password or not new_password:
            response['status'] = 'error'
            response['message'] = 'User id, old password, and new password are required.'
            return JsonResponse(response)

        # Retrieve user and check old password
        user = Account.objects.get(id=user_id)
        if not check_password(old_password, user.password):
            response['status'] = 'error'
            response['message'] = 'Old password is incorrect.'
            return JsonResponse(response)

        # Set and save the new password
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$', new_password):
            response['status'] = 'error'
            response['message'] = 'Password must contain at least one letter and one number.'
            return JsonResponse(response)

        user.set_password(new_password)
        user.save()

        response['status'] = 'success'
        response['message'] = 'Password changed successfully.'
        return JsonResponse(response)

    except Account.DoesNotExist:
        response['status'] = 'error'
        response['message'] = 'User does not exist.'
        return JsonResponse(response)
    except json.JSONDecodeError:
        response['status'] = 'error'
        response['message'] = 'Invalid JSON format.'
        return JsonResponse(response)
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        return JsonResponse(response)

@csrf_exempt
def reset_password(request):
    """
    处理密码重置请求
    :param request: POST 请求，包含 email 和新密码
    :return: JsonResponse
    """
    response = {}

    try:
        # 解析请求数据
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        new_password = data.get('password')

        if not email or not new_password:
            response['status'] = 'error'
            response['message'] = 'Email and password are required.'
            return JsonResponse(response)

        # 查找用户
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            response['status'] = 'error'
            response['message'] = 'User does not exist.'
            return JsonResponse(response, status=404)

        if len(new_password) < 6:
            response['status'] = 'error'
            response['message'] = '密码长度必须至少为6个字符'

        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$', new_password):
            response['status'] = 'error'
            response['message'] = '密码必须含有至少一个字母和数字'
            return JsonResponse(response)
        # 更新用户密码
        user.password = make_password(new_password)
        user.save()
        response['status'] = 'success'
        response['message'] = 'Password changed successfully.'
        return JsonResponse(response, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def reset_email(request):
    """
    通过密码重置邮箱
    :param request: user_id, email, password
    :return: JsonResponse
    """
    response = {}
    if request.method != "POST":
        response["error"] = "请求方法错误，仅支持 POST。"
        return JsonResponse(response, status=400)

    # 获取请求数据
    data = json.loads(request.body.decode('utf-8'))
    user_id = data.get("user_id")
    new_email =data.get("email")
    password = data.get("password")

    if not all([user_id, new_email, password]):
        response["status"] = 'error'
        response["message"] = "参数不完整。需要 user_id, email 和 password"
        return JsonResponse(response, status=400)

    try:
        # 查找用户
        user = Account.objects.get(id=user_id)
    except Account.DoesNotExist:
        response["status"] = 'error'
        response["message"] = "用户不存在"
        return JsonResponse(response, status=404)

    # 验证密码
    if not check_password(password, user.password):
        response["status"] = 'error'
        response["message"] = "密码错误"
        return JsonResponse(response, status=403)

    # 验证新邮箱是否已被使用
    if Account.objects.filter(email=new_email).exists():
        response["status"] = 'error'
        response["message"] = "该邮箱已被绑定到其他账户"
        return JsonResponse(response, status=409)

    # 更新邮箱
    user.email = new_email
    user.save()
    response["status"] = 'success'
    response["message"] = "邮箱更新成功"
    return JsonResponse(response, status=200)


def identify_platform(url):
    """
    判断链接是否属于淘宝或京东，并检查链接是否有效。
    """
    # 定义正则表达式模式
    taobao_pattern = re.compile(r'(detail\.tmall\.com|item\.taobao\.com)')
    jd_pattern = re.compile(r'item\.jd\.com')

    # 检查链接是否为淘宝链接
    if taobao_pattern.search(url):
        platform = '淘宝'
    # 检查链接是否为京东链接
    elif jd_pattern.search(url):
        platform = '京东'
    else:
        platform = '未知平台'

    # 尝试打开链接
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # 如果响应状态码不是 200，则引发 HTTPError
        print(f"链接有效，平台: {platform}")
    except requests.exceptions.RequestException as e:
        print(f"无法打开链接: {url}\n错误信息: {e}")
        platform = None

    return platform


@csrf_exempt
@require_http_methods(["GET"])
def update_and_show_price(request):
    """
    更新价格函数
    :param request:
    :return:
    """
    response = {}
    try:
        url = request.GET.get("search")
        print(url)

        if not url:
            response['status'] = 'error'
            response['message'] = 'url cannot be empty.'
            return JsonResponse(response)

        try:
            good = Products.objects.get(link=url)
        except ObjectDoesNotExist:
            response['status'] = 'error'
            response['message'] = 'Product matching the query does not exist.'
            return JsonResponse(response)

        platform = identify_platform(url)

        if platform == '淘宝':
            tb_update_price(good, url)
        elif platform == '京东':
            jd_update_price(good, url)
        else:
            response['status'] = 'error'
            response['message'] = '不支持该平台'
            return JsonResponse(response)

        # 查找当前商品的历史价格
        price_history = Prices.objects.filter(product=good).order_by('created_at')

        # 准备返回给前端的历史价格数据
        price_history_list = []

        if price_history:
            for entry in price_history:
                price_history_list.append({
                    'date': entry.created_at.strftime('%Y-%m-%d'),  # 转换日期格式
                    'price': entry.price
                })
        else:
            price_history_list.append({
                'date': now().strftime('%Y-%m-%d'),  # 当前日期
                'price': good.price,
            })

        # 返回给前端的数据
        response['status'] = 'success'
        response['message'] = '更新并显示商品价格成功。'
        response['priceHistory'] = price_history_list  # 将历史价格数据返回给前端

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)

@csrf_exempt
@require_http_methods(["GET"])
def show_price(request):
    response = {}
    try:
        product_id = request.GET.get("id")
        good = Products.objects.get(id=product_id)
        price_history = Prices.objects.filter(product=good).order_by('created_at')

        price_history_list = []
        if price_history:
            for entry in price_history:
                price_history_list.append({
                    'date': entry.created_at.strftime('%Y-%m-%d'),  # 转换日期格式
                    'price': entry.price
                })
        else:
            price_history_list.append({
                'date': now().strftime('%Y-%m-%d'),  # 当前日期
                'price': good.price,
            })

        # 返回给前端的数据
        response['status'] = 'success'
        response['message'] = '显示商品价格成功'
        response['priceHistory'] = price_history_list  # 将历史价格数据返回给前端

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
def search_products(request):
    """
    搜索库中的产品，支持分词处理和平台过滤
    :param request:
    :return:
    """
    response = {
        "status": "success",
        "message": "Search successful.",
        "products": []  # 确保初始化 products 为空列表
    }

    try:
        # 获取请求中的数据
        search = request.GET.get("search")

        # 如果search为空，直接返回空结果
        if not search:
            response["status"] = "error"
            response["message"] = "搜索关键词为空"
            return JsonResponse(response)

        # 调用数据库搜索逻辑
        products = search_database(jieba.lcut(search))

        # 构建返回结果
        for product in products:
            response["products"].append({
                "id": product.id,
                "title": product.title,
                "price": product.price,
                "info": product.info,
                "shop": product.shop,
                "img": product.img,
                "link": product.link,
                "platform": product.platform
            })

    except json.JSONDecodeError:
        response["status"] = "error"
        response["message"] = "Invalid JSON format"
    except Exception as e:
        response["status"] = "error"
        response["message"] = str(e)

    return JsonResponse(response)

def search_database(search_terms):
    query_list = []
    for term in search_terms:
        # 同时考虑包含该关键词以及关键词靠后的情况（示例逻辑）
        query_contains = Q(title__icontains=term)
        query_ends = Q(title__iendswith=term)
        # 通过组合多个以关键词结尾的查询条件来体现更高权重（这里简单用两次结尾匹配模拟更高权重，可按需调整）
        weighted_query = query_ends | query_ends | query_contains
        query_list.append(weighted_query)

    combined_query = query_list[0]
    for q in query_list[1:]:
        combined_query &= q

    return Products.objects.filter(combined_query).order_by('title')

@csrf_exempt
@require_http_methods(["GET"])
def search_platform_products(request):
    """
    在平台上搜索、爬虫，并将数据加入数据库后搜索数据库中的商品
    :return:
    """
    response = {
        "status": "success",
        "message": "",
        "products": []
    }
    try:
        # 获取请求数据
        search = request.GET.get("search")
        platform = request.GET.get("platform")

        # 检查必填字段
        if not search or not platform:
            response["status"] = "error"
            response["message"] = "搜索关键词为空或未选择平台"
            return JsonResponse(response)

        # 根据平台爬取数据
        if platform == 'Taobao':
            crawl_tb(search)  # 从淘宝搜索商品并加入数据库
        elif platform == 'JD':
            crawl_jd(search)
        else:
            response["status"] = "error"
            response["message"] = f"不支持的平台: {platform}"
            return JsonResponse(response)

        # 调用数据库搜索逻辑
        products = search_database(jieba.lcut(search))

        # 构建返回结果
        for product in products:
            response["products"].append({
                "id": product.id,
                "title": product.title,
                "price": product.price,
                "info": product.info,
                "shop": product.shop,
                "img": product.img,
                "link": product.link,
                "platform": product.platform
            })

        response["message"] = "爬取并搜索成功"

    except Exception as e:
        response["status"] = "error"
        response["message"] = str(e)

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["POST"])
def like(request):
    """
    关注某个商品
    :param request:
    :return:JsonResponse
    """
    response = {}
    try:
        data = json.loads(request.body.decode('utf-8'))
        product_id = data.get('id')
        product = Products.objects.get(id=product_id)
        user_id = data.get('user_id')
        user = Account.objects.get(id=user_id)

        if not product:
            response['status'] = 'error'
            response['message'] = 'Product does not exist.'
            return JsonResponse(response)

        user_like = Likes(user_id=user, product=product)
        user_like.save()

        response['status'] = 'success'
        response['message'] = 'Like product successful'

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)

@csrf_exempt
@require_http_methods(["POST"])
def unlike(request):
    """
    取消关注某个商品
    :param request:
    :return:
    """
    response = {}
    try:
        data = json.loads(request.body.decode('utf-8'))

        product_id = data.get('id')
        product = Products.objects.get(id=product_id)

        user_id = data.get('user_id')
        user = Account.objects.get(id=user_id)
        # 查询用户是否已经关注了该商品
        user_like = Likes.objects.filter(user_id=user, product=product).first()

        if user_like:
            user_like.delete()  # 如果存在记录，则删除，表示取消关注
            response['status'] = 'success'
            response['message'] = 'Unlike product successful.'
        else:
            response['status'] = 'error'
            response['message'] = 'No like record.'

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
def get_favorites(request):
    """
    获取用户关注的商品列表
    """
    response = {}
    try:
        user_id = request.GET.get('user_id')
        if not user_id:
            response['status'] = 'error'
            response['message'] = 'Missing user ID'
            return JsonResponse(response)

        favorites = Likes.objects.filter(user_id=user_id).select_related('product')

        product_list = [{
            'id': favorite.product.id,
            'title': favorite.product.title,
            'img': favorite.product.img,
            'price': favorite.product.price,
            'shop': favorite.product.shop,
            'platform': favorite.product.platform,
            'link': favorite.product.link,
        } for favorite in favorites]

        response['status'] = 'success'
        response['favorites'] = product_list

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)



@csrf_exempt
@require_http_methods(["POST"])
def change_email_service_state(request):
    """
    更改是否发送邮件状态
    :param request: 
    :return: 
    """
    response = {}
    try:
    # 获取请求数据
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id')
        state = data.get('state')
        # 获取用户信息
        user = Account.objects.get(id=user_id)
        user.change_email_state(state)
        response['status'] = 'success'
        response['message'] = 'Change Email Service State successfully.'
    
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        
    return JsonResponse(response)

@csrf_exempt
@require_http_methods(["GET"])
def get_user_info(request):
    response = {}
    try:
        user_id = request.GET.get('user_id')  # 从查询参数中获取 user_id
        if not user_id:
            raise ValueError("user_id is required")

        user = Account.objects.get(id=user_id)
        response['status'] = 'success'
        response['message'] = 'Get User Info successfully.'
        response['username'] = user.username
        response['email'] = user.email

    except Account.DoesNotExist:
        response['status'] = 'error'
        response['message'] = 'User not found.'
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(["GET"])
def search_through_categories(request):
    """
    根据分类，在数据中搜索商品，并返回商品列表
    :param request: categories (GET 参数)
    :return: JsonResponse
    """
    try:
        # 获取分类参数
        category_id = request.GET.get("category", None)
        if category_id is None:
            return JsonResponse({"error": "Missing 'category' parameter"}, status=400)

        # 查询分类下的商品
        products = Products.objects.filter(category_id=category_id).values(
            "id", "title", "price", "shop", "img", "link","platform", "info",
        )

        # 如果没有找到商品
        if not products.exists():
            return JsonResponse({"message": "No products found for the given category"}, status=404)

        # 构造响应数据
        response = {
            "category_id": category_id,
            "products": list(products),
        }
        return JsonResponse(response, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_category_tree(parent=None):
    """
    递归构建分类树
    :param parent: 当前父级分类（或 None 表示顶级分类）
    :return: 分类树列表
    """
    categories = Categories.objects.filter(parent=parent).order_by('name')  # 按名称排序
    category_tree = []

    for category in categories:
        category_tree.append({
            "id": category.id,
            "name": category.name,
            "subcategories": get_category_tree(category)  # 递归获取子分类
        })

    return category_tree

@csrf_exempt
@require_http_methods(["GET"])
def get_categories(request):
    """
    获取分类树的 API
    """
    try:
        category_tree = get_category_tree()  # 获取顶级分类开始的分类树
        return JsonResponse({"categories": category_tree}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)