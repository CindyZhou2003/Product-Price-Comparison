import json
import re
import secrets
from functools import wraps

import jieba  # 引入jieba进行中文分词
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db.models import Q
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from backend.crawler import crawl_tb, crawl_jd, tb_update_price, jd_update_price
from backend.models import *

CODE_TTL = 300  # 验证码有效期（秒）
CODE_RESEND_INTERVAL = 60
MAX_CODE_ATTEMPTS = 5  # 限制错误次数，防止暴力枚举6位验证码
PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$')


def login_required_json(view):
    """
    要求已登录，未登录时返回 401 JSON 而不是重定向到登录页
    """
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': '请先登录'}, status=401)
        return view(request, *args, **kwargs)
    return wrapper


@ensure_csrf_cookie
@require_http_methods(["GET"])
def csrf(request):
    """
    下发 CSRF Cookie，前端在第一次 POST 之前调用
    """
    return JsonResponse({'status': 'success'})


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

        account_exists = Account.objects.filter(email=user_email).exists()
        if forget and not account_exists:
            return JsonResponse({'status': 'error', 'message': '账号不存在'})
        if not forget and account_exists:
            return JsonResponse({'status': 'error', 'message': '邮箱已被注册过'})

        if not cache.add(f'verify_cooldown:{user_email}', 1, timeout=CODE_RESEND_INTERVAL):
            return JsonResponse({'status': 'error', 'message': '发送过于频繁，请稍后再试'})

        send_verification_email(user_email)
        response['status'] = 'success'
        response['message'] = '验证码已发送到您的邮箱'

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)


def send_verification_email(user_email):
    """
    辅助函数：生成验证码并发送邮件
    """
    verification_code = f'{secrets.randbelow(10 ** 6):06d}'

    cache.set(f'verify:{user_email}', verification_code, timeout=CODE_TTL)
    cache.set(f'verify_attempts:{user_email}', 0, timeout=CODE_TTL)

    subject = "您的验证码"
    message = f"亲爱的用户，\n\n您的验证码是：{verification_code}\n\n验证码有效时间为5分钟，请及时使用。"

    send_mail(subject, message, None, [user_email], fail_silently=False)


def check_verification_code(email, code, consume=False):
    """
    校验验证码，错误次数过多时作废；返回错误信息，校验通过返回 None
    :param consume: 校验通过后是否作废验证码（真正执行敏感操作时为 True）
    """
    stored_code = cache.get(f'verify:{email}')
    if not stored_code:
        return '验证码已过期或无效，请重新获取'

    if stored_code != code:
        if cache.incr(f'verify_attempts:{email}') >= MAX_CODE_ATTEMPTS:
            cache.delete(f'verify:{email}')
        return '验证码错误'

    if consume:
        cache.delete(f'verify:{email}')
    return None


@require_http_methods(["POST"])
def verify_code(request):
    """
    验证用户输入的验证码是否正确，并检查是否在有效时间内
    仅用于前端分步交互，不作废验证码；真正的敏感操作会再次校验
    :param request: POST请求，包含用户邮箱和验证码
    :return: JsonResponse
    """
    response = {}

    try:
        data = json.loads(request.body.decode('utf-8'))
        user_email = data.get('email')
        user_code = data.get('verification_code')

        if not user_email or not user_code:
            response['status'] = 'error'
            response['message'] = '请提供邮箱和验证码'
            return JsonResponse(response)

        error = check_verification_code(user_email, user_code)
        if error:
            response['status'] = 'error'
            response['message'] = error
        else:
            response['status'] = 'success'
            response['message'] = '验证码验证成功'

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)


@require_http_methods(["POST"])
def login(request):
    """
    用户登录函数，成功后建立 Session
    :param request:
    :return:
    """
    response = {}
    try:
        data = json.loads(request.body.decode('utf-8'))
        user = authenticate(request, username=data.get('username'), password=data.get('password'))

        if user is not None:
            auth_login(request, user)
            response['status'] = 'success'
            response['message'] = 'Login Successfully.'
        else:
            # 用户不存在和密码错误返回相同提示，防止枚举账号
            response['status'] = 'error'
            response['message'] = '用户名或密码错误'

    except json.JSONDecodeError:
        response['status'] = 'error'
        response['message'] = 'Invalid JSON format.'
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)


@require_http_methods(["POST"])
def logout(request):
    """
    用户登出，清除 Session
    """
    auth_logout(request)
    return JsonResponse({'status': 'success', 'message': 'Logout successfully.'})


@require_http_methods(["POST"])
def register(request):
    """
    用户注册函数
    :param request:
    :return:
    """
    response = {}
    try:
        # 解析前端传来的 JSON 数据
        data = json.loads(request.body.decode('utf-8'))
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        code = data.get("verification_code")

        # 1. 校验必填字段是否为空
        if not username or not email or not password or not code:
            response['status'] = 'error'
            response['message'] = '用户名、邮箱、密码和验证码不能为空'
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

        # 5. 密码复杂度检查
        if not PASSWORD_PATTERN.match(password):
            response['status'] = 'error'
            response['message'] = 'Password must contain at least one letter and one number.'
            return JsonResponse(response)

        # 6. 最后再校验验证码，避免表单错误白白消耗验证码
        error = check_verification_code(email, code, consume=True)
        if error:
            response['status'] = 'error'
            response['message'] = error
            return JsonResponse(response)

        # 7. 创建并保存用户（create_user 内部会加密密码）
        Account.objects.create_user(username=username, email=email, password=password)

        response['status'] = 'success'
        response['message'] = 'Registration successful.'

    except json.JSONDecodeError:
        response['status'] = 'error'
        response['message'] = 'Invalid JSON format.'
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)


@login_required_json
@require_http_methods(["POST"])
def change_password(request):
    """
    用户修改密码函数
    :param request:
    :return:
    """
    response = {}
    try:
        data = json.loads(request.body.decode('utf-8'))
        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if not old_password or not new_password:
            response['status'] = 'error'
            response['message'] = 'Old password and new password are required.'
            return JsonResponse(response)

        user = request.user
        if not user.check_password(old_password):
            response['status'] = 'error'
            response['message'] = 'Old password is incorrect.'
            return JsonResponse(response)

        if not PASSWORD_PATTERN.match(new_password):
            response['status'] = 'error'
            response['message'] = 'Password must contain at least one letter and one number.'
            return JsonResponse(response)

        user.set_password(new_password)
        user.save()
        # 保持当前 Session 登录状态，否则改密后会被登出
        update_session_auth_hash(request, user)

        response['status'] = 'success'
        response['message'] = 'Password changed successfully.'

    except json.JSONDecodeError:
        response['status'] = 'error'
        response['message'] = 'Invalid JSON format.'
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)


@require_http_methods(["POST"])
def reset_password(request):
    """
    通过邮箱验证码重置密码
    :param request: POST 请求，包含 email、验证码和新密码
    :return: JsonResponse
    """
    response = {}

    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        code = data.get('verification_code')
        new_password = data.get('password')

        if not email or not code or not new_password:
            response['status'] = 'error'
            response['message'] = 'Email, verification code and password are required.'
            return JsonResponse(response)

        if not PASSWORD_PATTERN.match(new_password):
            response['status'] = 'error'
            response['message'] = '密码必须至少6个字符，且含有至少一个字母和数字'
            return JsonResponse(response)

        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            response['status'] = 'error'
            response['message'] = 'User does not exist.'
            return JsonResponse(response, status=404)

        error = check_verification_code(email, code, consume=True)
        if error:
            response['status'] = 'error'
            response['message'] = error
            return JsonResponse(response, status=403)

        user.set_password(new_password)
        user.save()
        response['status'] = 'success'
        response['message'] = 'Password changed successfully.'
        return JsonResponse(response, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required_json
@require_http_methods(["POST"])
def reset_email(request):
    """
    通过密码和新邮箱的验证码重置邮箱
    :param request: email, verification_code, password
    :return: JsonResponse
    """
    response = {}

    data = json.loads(request.body.decode('utf-8'))
    new_email = data.get("email")
    code = data.get("verification_code")
    password = data.get("password")

    if not all([new_email, code, password]):
        response["status"] = 'error'
        response["message"] = "参数不完整。需要 email、验证码和 password"
        return JsonResponse(response, status=400)

    user = request.user

    # 验证密码
    if not user.check_password(password):
        response["status"] = 'error'
        response["message"] = "密码错误"
        return JsonResponse(response, status=403)

    # 验证新邮箱是否已被使用
    if Account.objects.filter(email=new_email).exists():
        response["status"] = 'error'
        response["message"] = "该邮箱已被绑定到其他账户"
        return JsonResponse(response, status=409)

    # 验证新邮箱确实属于当前用户
    error = check_verification_code(new_email, code, consume=True)
    if error:
        response["status"] = 'error'
        response["message"] = error
        return JsonResponse(response, status=403)

    user.email = new_email
    user.save()
    response["status"] = 'success'
    response["message"] = "邮箱更新成功"
    return JsonResponse(response, status=200)


def build_price_history(good):
    """
    整理商品历史价格，没有记录时用当前价格补一个点
    """
    price_history = Prices.objects.filter(product=good).order_by('created_at')
    if not price_history:
        return [{'date': now().strftime('%Y-%m-%d'), 'price': good.price}]
    return [{'date': entry.created_at.strftime('%Y-%m-%d'), 'price': entry.price} for entry in price_history]


@login_required_json
@require_http_methods(["GET"])
def update_and_show_price(request):
    """
    爬取单个商品的最新价格并返回历史价格
    :param request:
    :return:
    """
    response = {}
    try:
        url = request.GET.get("search")

        if not url:
            response['status'] = 'error'
            response['message'] = 'url cannot be empty.'
            return JsonResponse(response)

        try:
            good = Products.objects.get(link=url)
        except Products.DoesNotExist:
            response['status'] = 'error'
            response['message'] = 'Product matching the query does not exist.'
            return JsonResponse(response)

        if good.platform == '淘宝':
            tb_update_price(good, url)
        elif good.platform == '京东':
            jd_update_price(good, url)
        else:
            response['status'] = 'error'
            response['message'] = '不支持该平台'
            return JsonResponse(response)

        response['status'] = 'success'
        response['message'] = '更新并显示商品价格成功。'
        response['priceHistory'] = build_price_history(good)

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)


@require_http_methods(["GET"])
def show_price(request):
    response = {}
    try:
        good = Products.objects.get(id=request.GET.get("id"))
        response['status'] = 'success'
        response['message'] = '显示商品价格成功'
        response['priceHistory'] = build_price_history(good)

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)


def serialize_product(product):
    return {
        "id": product.id,
        "title": product.title,
        "price": product.price,
        "info": product.info,
        "shop": product.shop,
        "img": product.img,
        "link": product.link,
        "platform": product.platform,
    }


@require_http_methods(["GET"])
def search_products(request):
    """
    搜索库中的产品，支持分词处理
    :param request:
    :return:
    """
    search = request.GET.get("search", "").strip()
    if not search:
        return JsonResponse({"status": "error", "message": "搜索关键词为空", "products": []})

    try:
        products = search_database(search)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e), "products": []})

    return JsonResponse({
        "status": "success",
        "message": "Search successful.",
        "products": [serialize_product(p) for p in products],
    })


def search_database(search):
    """
    分词后要求标题包含每一个词
    """
    # 去掉 jieba 切出的空白词，否则只能匹配含空格的标题
    terms = [term for term in jieba.lcut(search) if term.strip()]
    query = Q()
    for term in terms:
        query &= Q(title__icontains=term)
    return Products.objects.filter(query).order_by('title')


@login_required_json
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
        search = request.GET.get("search", "").strip()
        platform = request.GET.get("platform")

        if not search or not platform:
            response["status"] = "error"
            response["message"] = "搜索关键词为空或未选择平台"
            return JsonResponse(response)

        # 根据平台爬取数据
        if platform == 'Taobao':
            crawl_tb(search)
        elif platform == 'JD':
            crawl_jd(search)
        else:
            response["status"] = "error"
            response["message"] = f"不支持的平台: {platform}"
            return JsonResponse(response)

        response["products"] = [serialize_product(p) for p in search_database(search)]
        response["message"] = "爬取并搜索成功"

    except Exception as e:
        response["status"] = "error"
        response["message"] = str(e)

    return JsonResponse(response)


@login_required_json
@require_http_methods(["POST"])
def like(request):
    """
    关注某个商品，记录关注时的价格作为降价提醒的基准
    :param request:
    :return:JsonResponse
    """
    response = {}
    try:
        data = json.loads(request.body.decode('utf-8'))
        product = Products.objects.get(id=data.get('id'))

        Likes.objects.get_or_create(
            user_id=request.user, product=product, defaults={'alert_price': product.price}
        )

        response['status'] = 'success'
        response['message'] = 'Like product successful'

    except Products.DoesNotExist:
        response['status'] = 'error'
        response['message'] = 'Product does not exist.'
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)


@login_required_json
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
        deleted, _ = Likes.objects.filter(user_id=request.user, product_id=data.get('id')).delete()

        if deleted:
            response['status'] = 'success'
            response['message'] = 'Unlike product successful.'
        else:
            response['status'] = 'error'
            response['message'] = 'No like record.'

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)


@login_required_json
@require_http_methods(["GET"])
def get_favorites(request):
    """
    获取当前用户关注的商品列表
    """
    response = {}
    try:
        favorites = Likes.objects.filter(user_id=request.user).select_related('product')

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


@login_required_json
@require_http_methods(["POST"])
def change_email_service_state(request):
    """
    更改是否发送邮件状态
    :param request:
    :return:
    """
    response = {}
    try:
        data = json.loads(request.body.decode('utf-8'))
        request.user.change_email_state(bool(data.get('state')))
        response['status'] = 'success'
        response['message'] = 'Change Email Service State successfully.'

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response)


@login_required_json
@require_http_methods(["GET"])
def get_user_info(request):
    return JsonResponse({
        'status': 'success',
        'message': 'Get User Info successfully.',
        'username': request.user.username,
        'email': request.user.email,
        'email_active': request.user.email_active,
    })


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
