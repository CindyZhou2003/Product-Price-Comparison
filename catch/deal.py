import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')  # 替换'myproject'为你的项目名称
django.setup()

from backend.models import Products
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage

from backend.views import tb_update_price, jd_update_price


def update_prices():
    """
    对数据库所有商品更新价格，包含事务处理、异常捕获及批量处理。
    """
    try:
        # 批量处理商品，设置每页处理数量
        batch_size = 5

        # 更新淘宝商品价格
        tb_products = Products.objects.filter(platform="淘宝")
        tb_paginator = Paginator(tb_products, batch_size)

        for page_number in tb_paginator.page_range:
            try:
                with transaction.atomic():
                    page = tb_paginator.page(page_number)
                    for product in page.object_list:
                        try:
                            tb_update_price(product, product.link)
                        except Exception as e:
                            # 捕获单个商品更新异常并记录日志
                            print(f"Failed to update price for 淘宝商品 {product.id}: {e}")
            except Exception as e:
                # 捕获分页事务异常并记录日志
                print(f"Transaction failed for 淘宝商品 batch {page_number}: {e}")

        # 更新京东商品价格
        jd_products = Products.objects.filter(platform="京东")
        jd_paginator = Paginator(jd_products, batch_size)

        for page_number in jd_paginator.page_range:
            try:
                with transaction.atomic():
                    page = jd_paginator.page(page_number)
                    for product in page.object_list:
                        try:
                            jd_update_price(product, product.link)
                        except Exception as e:
                            # 捕获单个商品更新异常并记录日志
                            print(f"Failed to update price for 京东商品 {product.id}: {e}")
            except Exception as e:
                # 捕获分页事务异常并记录日志
                print(f"Transaction failed for 京东商品 batch {page_number}: {e}")

    except Exception as e:
        # 捕获整个更新过程中的异常
        print(f"Overall update_prices process failed: {e}")


