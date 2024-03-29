from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Article


@receiver(pre_save, sender=Article)
def track_article_changes(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Article.objects.get(pk=instance.pk)
        changes = []

        if instance.title != old_instance.title:
            changes.append(f"Заголовок изменен с '{old_instance.title}' на '{instance.title}'")
        if instance.content != old_instance.content:
            changes.append(f"Содержание изменено с '{old_instance.content}' на '{instance.content}'")

        if changes:
            print("Изменения в статье:")
            for change in changes:
                print(change)
