from django import forms
from .models import TrainingType, TrainingPart, TrainingLocation, UserCustomMenus, TrainingGoals




class TrainingTypeForm(forms.ModelForm):
    name = forms.CharField(label='トレーニングタイプ名称')

    class Meta:
        model = TrainingType
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    # ユーザー紐づけロジック
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance

class TrainingPartForm(forms.ModelForm):
    name = forms.CharField(label='トレーニング部位名称')

    class Meta:
        model = TrainingPart
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    # ユーザー紐づけロジック
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance

class TrainingLocationForm(forms.ModelForm):
    name = forms.CharField(label='トレーニング場所名称')

    class Meta:
        model = TrainingLocation
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    # ユーザー紐づけロジック
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance

class UserCustomMenusForm(forms.ModelForm):
    menu_name = forms.CharField(label='メニュー名')
    menu_details = forms.CharField(label='詳細', widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False)
    training_type = forms.ModelChoiceField(queryset=TrainingType.objects.none(), label='トレーニングタイプ', required=False)
    training_part = forms.ModelChoiceField(queryset=TrainingPart.objects.none(), label='対象部位', required=False)
    training_location = forms.ModelChoiceField(queryset=TrainingLocation.objects.none(), label='場所', required=False)
    reference_video_url = forms.URLField(label='動画URL', required=False, widget=forms.TextInput(attrs={'placeholder': 'URLを入力'}))
    reference_site_url = forms.URLField(label='サイトURL', required=False, widget=forms.TextInput(attrs={'placeholder': 'URLを入力'}))
    day_of_week = forms.ChoiceField(choices=UserCustomMenus.DAY_OF_WEEK_CHOICES, label='曜日', required=False)

    class Meta:
        model = UserCustomMenus
        fields = ['day_of_week', 'menu_name', 'menu_details', 'training_type', 'training_part', 'training_location', 'reference_video_url', 'reference_site_url']

    # 自身のユーザー分のみ表示ロジック
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['training_type'].queryset = TrainingType.objects.filter(user=self.user)
            self.fields['training_part'].queryset = TrainingPart.objects.filter(user=self.user)
            self.fields['training_location'].queryset = TrainingLocation.objects.filter(user=self.user)

    # ユーザー紐づけロジック
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance

class TrainingSearchForm(forms.Form):
    day_of_week = forms.ChoiceField(
        choices=[('', '---------')] + list(UserCustomMenus.DAY_OF_WEEK_CHOICES),
        required=False,
        label='曜日',
    )
    menu_name = forms.CharField(label='メニュー名', required=False)
    training_type_name = forms.CharField(label='トレーニングタイプ', required=False)
    training_part_name = forms.CharField(label='対象部位', required=False)
    training_location_name = forms.CharField(label='場所', required=False)
    current_only = forms.BooleanField(label='現在選択中のみ表示', required=False, initial=False)

class TrainingGoalsForm(forms.ModelForm):
    name = forms.CharField(label='トレーニング目標', required=False, widget=forms.TextInput(attrs={'class': 'wide'}))

    class Meta:
        model = TrainingGoals
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    # ユーザー紐づけロジック
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
