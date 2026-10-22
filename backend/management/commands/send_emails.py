from django.core import mail
from django.core.management.base import BaseCommand
from backend.models import Account, Likes, Prices


def get_alert_price(like):
    """
    获取该关注记录的降价提醒阈值
    :param like: 用户的关注记录
    :return: float 低于该价格才提醒
    """
    if like.alert_price is not None:
        return like.alert_price

    # 兼容新增 alert_price 字段前的关注记录：取关注前最近一次的价格
    pre_liked_price = Prices.objects.filter(
        product=like.product, created_at__lt=like.created_at
    ).order_by('created_at').last()
    return pre_liked_price.price if pre_liked_price else like.product.price


class Command(BaseCommand):
    help = "Send price alert emails to users who have liked products that dropped in price."

    def handle(self, *args, **kwargs):
        """
        通过命令行执行邮件发送任务。
        遍历所有用户，检查他们关注的商品当前价格是否低于提醒阈值，若降价则发送邮件。
        """
        users = Account.objects.filter(email_active=True)

        if not users.exists():
            self.stdout.write("没有用户启用邮件服务")
            return

        with mail.get_connection() as connection:
            for user in users:
                likes = Likes.objects.filter(user_id=user).select_related('product')

                lowered_likes = [like for like in likes if like.product.price < get_alert_price(like)]
                if not lowered_likes:
                    self.stdout.write(f"用户 {user.username} 没有降价的商品")
                    continue

                items_info = "\n".join(
                    f"{like.product.title}: {like.product.price}元 对应链接：{like.product.link}"
                    for like in lowered_likes
                )
                subject = "您关注的商品已降价！"
                message = f"亲爱的 {user.username},\n\n商品比价网站提醒您，您关注的以下商品已降价：\n\n{items_info}\n\n快去抢购吧！"

                try:
                    mail.EmailMessage(subject, message, None, [user.email], connection=connection).send()
                except Exception as e:
                    # 单个用户发送失败不影响其他用户
                    self.stderr.write(f"向用户 {user.username} 发送邮件失败: {e}")
                    continue

                # 把阈值更新为本次提醒的价格，同一次降价不重复提醒
                for like in lowered_likes:
                    like.alert_price = like.product.price
                    like.save(update_fields=['alert_price'])

                self.stdout.write(f"已向用户 {user.username} 发送降价通知")
