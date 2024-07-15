from django.db import models
from accounts.models import Users
# Create your models here.


class TrainingType(models.Model):
    name = models.CharField(max_length=1000)
    user = models.ForeignKey(
        Users,
        on_delete = models.CASCADE,
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'training_type'

    def __str__(self):
        return self.name

class TrainingPart(models.Model):
    name = models.CharField(max_length=1000)
    user = models.ForeignKey(
        Users,
        on_delete = models.CASCADE,
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'training_part'

    def __str__(self):
        return self.name

class TrainingLocation(models.Model):
    name = models.CharField(max_length=1000)
    user = models.ForeignKey(
        Users,
        on_delete = models.CASCADE,
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'training_location'

    def __str__(self):
        return self.name
    
class UserCustomMenus(models.Model):
    DAY_OF_WEEK_CHOICES = (
        ('free', 'フリー'),
        ('monday', '月曜日'),
        ('tuesday', '火曜日'),
        ('wednesday', '水曜日'),
        ('thursday', '木曜日'),
        ('friday', '金曜日'),
        ('saturday', '土曜日'),
        ('sunday', '日曜日'),
    )

    menu_name = models.CharField(max_length=1000, verbose_name='メニュー名')
    menu_details = models.CharField(max_length=2000, blank=True, null=True, verbose_name='詳細')
    training_type = models.ForeignKey(
        TrainingType,
        on_delete = models.CASCADE,
        blank=True,
        null=True,
        verbose_name='トレーニングタイプ'
    )
    training_part = models.ForeignKey(
        TrainingPart,
        on_delete = models.CASCADE,
        blank=True,
        null=True,
        verbose_name='対象部位'
    )
    training_location = models.ForeignKey(
        TrainingLocation,
        on_delete = models.CASCADE,
        blank=True,
        null=True,
        verbose_name='場所'
    )
    reference_video_url = models.URLField(max_length=1000, blank=True, null=True, verbose_name='動画URL')
    reference_site_url = models.URLField(max_length=1000, blank=True, null=True, verbose_name='サイトURL')
    last_performed_date = models.CharField(max_length=1000, default='未実施', verbose_name='最終実施日')
    is_current = models.BooleanField(default=False, verbose_name='現在選択')
    day_of_week = models.CharField(max_length=10, choices=DAY_OF_WEEK_CHOICES, blank=True, null=True, verbose_name='曜日')
    user = models.ForeignKey(
        Users,
        on_delete = models.CASCADE,
        related_name='custom_menus',
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'training_custom_menus'
        verbose_name = 'ユーザーカスタムメニュー'
        verbose_name_plural = 'ユーザーカスタムメニュー'

    def __str__(self):
        return self.menu_name
    

class TrainingGoals(models.Model):
    name = models.CharField(max_length=1000, blank=True, null=True, verbose_name='トレーニング目標')
    user = models.OneToOneField(
        Users,
        on_delete = models.CASCADE,
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'training_goals'

    def __str__(self):
        return self.name













