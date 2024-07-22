from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class RegistForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and len(username) < 3:
            raise forms.ValidationError(_("ユーザー名は3文字以上である必要があります。"))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError(_("このメールアドレスは既に登録されています。"))
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as e:
                # パスワードバリデーションエラーをフォームのエラーに追加
                raise forms.ValidationError(_("パスワードが基準を満たしていません: ") + str(e))
        return password
    
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    _("ログイン情報が間違っています。ユーザー名とパスワードを確認してください。"),
                    code='invalid_login'
                )

        return self.cleaned_data


class PictureUploadForm(forms.ModelForm):
    picture = forms.FileField(required=False)

    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        if not picture:
            raise forms.ValidationError(_("画像ファイルを選択してください。"))
        return picture

    class Meta:
        model = Users
        fields = ['picture',]
    

    