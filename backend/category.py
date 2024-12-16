## 记录 236 错
import pandas as pd
from django.db import transaction

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()

from backend.models import Products, Categories  # 替换为你的 Django 应用名称

def print_category_hierarchy(parent=None, prefix=""):
    """递归打印分类层级路径"""
    children = Categories.objects.filter(parent=parent).order_by("id")
    for child in children:
        path = f"{prefix}{child.name}"
        print(path)
        print_category_hierarchy(parent=child, prefix=f"{path} -> ")


# 读取 CSV 文件
file_path = '../data/backend_products.csv'
data = pd.read_csv(file_path)

# 检查数据格式
print("数据预览：")
print(data.head())

# 假设你的数据包含 "title" 列
if "title" not in data.columns:
    raise ValueError("文件中缺少 'title' 列！请确认数据格式。")

# 预设的分类选项
categories = Categories.objects.all()
category_dict = {i: category for i, category in enumerate(categories)}


def display_category_hierarchy(category):
    """显示品类层级路径"""
    hierarchy = []
    current = category
    while current:
        hierarchy.insert(0, current.name)
        current = current.parent
    return " -> ".join(hierarchy)


def manual_classify():
    """人工为商品分配分类，并直接写入数据库"""
    with transaction.atomic():
        for index, row in data.iterrows():
            try:
                # 获取商品对象
                product = Products.objects.get(id=row['id'])

                # 仅处理分类为空的商品
                if product.category is not None:
                    continue
                print("----------------------------------------")
                print(f"ID：{row['id']}, 商品名称: {row['title']}")
                print("请选择分类:")

                # for i, category in category_dict.items():
                #     hierarchy = display_category_hierarchy(category)
                #     print(f"[{i}] {hierarchy}")

                choice = input("请输入分类编号 (或按 q 退出): ")
                if choice.lower() == "q":
                    print("退出分类任务。")
                    break

                choice = int(choice)
                selected_category = category_dict[choice]

                # 更新数据库中的商品分类
                product.category = selected_category
                product.save()

                print(f"商品 '{product.title}' 已分类到 '{display_category_hierarchy(selected_category)}'")

            except (ValueError, IndexError, Products.DoesNotExist):
                print("输入无效或商品不存在，请重新选择。")


def auto_classify_by_keyword(keyword, category_index, id_range):
    """
    自动为商品分配分类，根据标题中的关键词和 ID 范围。

    参数:
    - keyword: str，商品标题中包含的关键词
    - category_index: int，要分配的分类编号
    - id_range: tuple，指定商品 ID 的范围 (start_id, end_id)
    """
    start_id, end_id = id_range
    selected_category = category_dict.get(category_index)

    if not selected_category:
        print(f"分类编号 {category_index} 不存在，请检查输入。")
        return

    with transaction.atomic():
        # 筛选符合条件的商品
        products = Products.objects.filter(
            id__gte=start_id,
            id__lte=end_id,
            category__isnull=True,
            title__icontains=keyword,
        )

        if not products.exists():
            print(f"未找到标题包含 '{keyword}' 且 ID 在范围 {id_range} 内的商品。")
            return

        # 更新分类
        for product in products:
            product.category = selected_category
            product.save()
            print(
                f"商品 '{product.title}' (ID: {product.id}) 已分类到 '{display_category_hierarchy(selected_category)}'")

    print(f"完成对关键词 '{keyword}' 的商品分类。")


if __name__ == "__main__":
    # manual_classify()
    keyword = "挂件"
    index = 38
    range = (1911,2197)
    auto_classify_by_keyword(keyword, index, range)

