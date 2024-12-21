from django.core.management.base import BaseCommand
from django.core.paginator import Paginator
from django.db import transaction
from backend.models import Products, Likes
from backend.crawler import tb_update_price, jd_update_price  # 假设这些工具函数已经定义

class Command(BaseCommand):
    help = "Update prices for products that users have marked as favorites."

    def handle(self, *args, **kwargs):
        """
        管理命令：更新用户关注商品的价格，支持分平台批量处理。
        """
        try:
            # 批量处理商品，设置每页处理数量
            batch_size = 5

            # 获取用户关注的所有商品，并根据平台分类
            favorite_products = Products.objects.filter(
                id__in=Likes.objects.values_list('product_id', flat=True).distinct()
            )
            self.stdout.write(f"喜欢的商品数: {Likes.objects.count()}")
            self.stdout.write(f"关注商品的ID列表: {Likes.objects.values_list('product_id', flat=True).distinct()}")
            self.stdout.write(f"过滤后的商品数: {favorite_products.count()}")

            # 淘宝商品价格更新
            tb_products = favorite_products.filter(platform="淘宝").order_by('id')
            tb_paginator = Paginator(tb_products, batch_size)
            self.stdout.write(f"淘宝商品数: {tb_products.count()}")

            for page_number in tb_paginator.page_range:
                try:
                    with transaction.atomic():
                        page = tb_paginator.page(page_number)
                        for product in page.object_list:
                            try:
                                tb_update_price(product, product.link)
                            except Exception as e:
                                # 捕获单个商品更新异常并记录日志
                                self.stdout.write(f"Failed to update price for 淘宝商品 {product.id}: {e}")
                except Exception as e:
                    # 捕获分页事务异常并记录日志
                    self.stdout.write(f"Transaction failed for 淘宝商品 batch {page_number}: {e}")

            # 京东商品价格更新
            jd_products = favorite_products.filter(platform="京东").order_by('id')
            jd_paginator = Paginator(jd_products, batch_size)
            self.stdout.write(f"京东商品数: {jd_products.count()}")

            for page_number in jd_paginator.page_range:
                try:
                    with transaction.atomic():
                        page = jd_paginator.page(page_number)
                        for product in page.object_list:
                            try:
                                jd_update_price(product, product.link)
                            except Exception as e:
                                # 捕获单个商品更新异常并记录日志
                                self.stdout.write(f"Failed to update price for 京东商品 {product.id}: {e}")
                except Exception as e:
                    # 捕获分页事务异常并记录日志
                    self.stdout.write(f"Transaction failed for 京东商品 batch {page_number}: {e}")

        except Exception as e:
            # 捕获整个更新过程中的异常
            self.stderr.write(f"Overall update_prices process failed: {e}")
