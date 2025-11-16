from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BlogPost


@receiver(post_save, sender=BlogPost)
def send_congratulation_email(sender, instance, **kwargs):
    """
    Отправляет email поздравление когда статья достигает 100 просмотров
    """
    if instance.views_count >= 100:
        subject = f'🎉 Поздравляем! Статья "{instance.title}" достигла 100 просмотров!'
        message = f"""
        Поздравляем! Ваша статья "{instance.title}" достигла значимого рубежа - 100 просмотров!

        Статистика статьи:
        - Заголовок: {instance.title}
        - Просмотров: {instance.views_count}
        - Дата создания: {instance.created_at.strftime("%d.%m.%Y")}
        - Ссылка: http://127.0.0.1:8000/blog/post/{instance.pk}/

        Продолжайте в том же духе! 🚀
        """

        # Отправляем email (в разработке показывается в консоли)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["admin@example.com"],  # Замени на свой email
            fail_silently=False,
        )
