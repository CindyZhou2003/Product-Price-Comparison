from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.core import mail
from backend.crawler import tb_update_price, jd_update_price
from backend.models import Account, Likes, Products, Prices
from backend.views import identify_platform


def check_price(item_url):
    """
    确认当前价格是否低于之前价格
    :param item_url: 商品的url
    :return: bool True or False
    """
    try:
        # 尝试获取对应的商品记录
        good = Products.objects.get(link=item_url)
    except ObjectDoesNotExist:
        raise ValueError("商品未被收录")  # 抛出异常，说明商品未被收录

    # 判断商品所属平台
    platform = identify_platform(item_url)

    # 更新商品价格
    if platform == '淘宝':
        tb_update_price(good, item_url)
    elif platform == '京东':
        jd_update_price(good, item_url)
    else:
        raise ValueError("不支持的平台")  # 抛出异常，说明该平台无法查询价格

    try:
        # 获取用户关注商品的时间
        liked_time = Likes.objects.get(product=good).created_at
    except ObjectDoesNotExist:
        raise ValueError("未找到用户对该商品的关注记录")  # 抛出异常，说明未找到关注记录

    # 查询商品的历史价格记录
    price_history = Prices.objects.filter(product=good).order_by('created_at')

    # 找到关注时间之前最近一次的价格
    pre_liked_price = price_history.filter(created_at__lt=liked_time).last()

    # 如果关注时间之前没有价格记录，使用 Products 表中的价格
    if not pre_liked_price:
        pre_liked_price_value = good.price
    else:
        pre_liked_price_value = pre_liked_price.price

    # 找到关注时间之后的所有价格
    post_liked_prices = price_history.filter(created_at__gte=liked_time)

    # 比较逻辑：检查关注时间后的价格是否低于关注时间前的最后价格
    for post_price in post_liked_prices:
        if post_price.price < pre_liked_price_value:
            return True  # 找到符合条件的价格，返回True

    # 如果没有找到更低的价格，返回False
    return False


class Command(BaseCommand):
    help = "Send price alert emails to users who have liked products that dropped in price."

    def handle(self, *args, **kwargs):
        """
        通过命令行执行邮件发送任务。
        遍历所有用户，检查他们关注的商品是否降价，若降价则发送邮件。
        """
        response = {}
        try:
            # 获取所有用户
            users = Account.objects.filter(email_active=True)

            if not users.exists():
                self.stdout.write("没有用户启用邮件服务")
                return

            for user in users:
                user_email = user.email
                username = user.username

                # 查询用户关注的商品
                likes = Likes.objects.filter(user_id=user.id)

                if not likes.exists():
                    self.stdout.write(f"用户 {username} 没有关注任何商品")
                    continue

                # 检查是否有降价商品
                lowered_price_items = []
                for like in likes:
                    product = like.product
                    if check_price(product.link):  # 假设 check_price 是检查降价的函数
                        lowered_price_items.append(product)

                if not lowered_price_items:
                    self.stdout.write(f"用户 {username} 没有降价的商品")
                    continue

                # 拼接降价商品信息
                items_info = "\n".join([
                    f"{item.title}: {item.price} - {item.link}" for item in lowered_price_items
                ])
                subject = "您关注的商品已降价！"
                message = f"亲爱的 {username},\n\n商品比价网站提醒您，您关注的以下商品已降价：\n\n{items_info}\n\n快去抢购吧！"

                # 使用邮件连接发送
                connection = mail.get_connection()
                connection.open()
                email = mail.EmailMessage(
                    subject,
                    message,
                    'CindyZhou6418@gmail.com',  # 替换为发件人地址
                    [user_email],
                )
                email.send()
                connection.close()

                self.stdout.write(f"已向用户 {username} 发送降价通知")

        except Exception as e:
            self.stderr.write(f"发生错误: {str(e)}")
