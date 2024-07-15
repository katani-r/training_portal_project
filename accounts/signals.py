from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from training_menus.models import TrainingType, TrainingPart, TrainingLocation

User = get_user_model()

# ユーザー作成後のタイプ、部位、場所の既存分追加ロジック
@receiver(post_save, sender=User)
def create_user_training_defaults(sender, instance, created, **kwargs):
    if created:
        TrainingType.objects.create(name='筋トレ', user=instance)
        TrainingType.objects.create(name='ストレッチ', user=instance)
        TrainingType.objects.create(name='有酸素運動', user=instance)
        TrainingPart.objects.create(name='全身', user=instance)
        TrainingPart.objects.create(name='上半身', user=instance)
        TrainingPart.objects.create(name='下半身', user=instance)
        TrainingLocation.objects.create(name='ジム', user=instance)
        TrainingLocation.objects.create(name='自宅', user=instance)
