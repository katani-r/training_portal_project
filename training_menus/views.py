from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.edit import (
    UpdateView, DeleteView, CreateView
)
from django.urls import reverse_lazy
import os
from .models import(
    UserCustomMenus, TrainingType, TrainingPart, TrainingLocation,
    TrainingGoals
)
from .forms import(
    UserCustomMenusForm, TrainingTypeForm, TrainingPartForm,
    TrainingLocationForm, TrainingSearchForm, TrainingGoalsForm
)
from . import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from accounts.models import Users
from accounts import forms
import os

# Create your views here.

# トレーニングメニュー一覧画面
class TrainingListView(LoginRequiredMixin, ListView):
    template_name = os.path.join('training_menus', 'training_list.html')
    model = UserCustomMenus

    # 検索時のクエリフィルター
    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        form = TrainingSearchForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data
            if data.get('day_of_week'):
                queryset = queryset.filter(day_of_week=data['day_of_week'])
            if data.get('menu_name'):
                queryset = queryset.filter(menu_name__icontains=data['menu_name'])
            if data.get('training_type_name'):
                queryset = queryset.filter(training_type__name__icontains=data['training_type_name'])
            if data.get('training_part_name'):
                queryset = queryset.filter(training_part__name__icontains=data['training_part_name'])
            if data.get('training_location_name'):
                queryset = queryset.filter(training_location__name__icontains=data['training_location_name'])
            if data.get('current_only'):
                queryset = queryset.filter(is_current=True)
        return queryset

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TrainingSearchForm(initial=self.request.GET)
        return context
    
    # ホーム画面に表示されるメニューの選択ロジックと最終実施日の更新ロジック
    def post(self, request, *args, **kwargs):
        all_menus = UserCustomMenus.objects.filter(user=request.user)
        initially_checked_ids = list(all_menus.filter(is_current=True).values_list('id', flat=True))
        current_ids = [key.split('_')[-1] for key, value in request.POST.items() if key.startswith('is_current_')]
        all_menus.update(is_current=False)
        all_menus.filter(id__in=current_ids).update(is_current=True, last_performed_date="現在選択中")
        unchecked_ids = set(initially_checked_ids) - set(map(int, current_ids))
        if unchecked_ids:
            all_menus.filter(id__in=unchecked_ids).update(last_performed_date=timezone.now().strftime('%Y-%m-%d'))
        messages.success(request, '現在選択を更新しました。')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('training_menus:training_list')

# ホーム画面
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    
    # ホーム画面の表示と現在選択中と曜日指定の表示ロジック
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = Users.objects.get(id=self.request.user.id)
        timezone_now = timezone.now()
        context['profile'] = user_profile
        context['picture_form'] = forms.PictureUploadForm(instance=user_profile)
        context['now'] = timezone_now
        context['goals'], created = TrainingGoals.objects.get_or_create(user=self.request.user)
        weekdays_ja = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]
        context['weekdays_ja'] = weekdays_ja[timezone_now.weekday()]
        is_current = UserCustomMenus.objects.filter(user=self.request.user, is_current=True)
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        day_name = weekdays[timezone_now.weekday()]
        context['day_of_weeks_free'] = is_current.filter(day_of_week="free")
        context['day_of_weeks'] = is_current.filter(day_of_week=day_name)
        return context
    
    # プロフィール画像のロジック
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        picture_form = forms.PictureUploadForm(request.POST, request.FILES, instance=context['profile'])

        if 'picture-clear' in request.POST:
            old_picture = Users.objects.get(id=self.request.user.id).picture
            if old_picture:
                old_picture_path = old_picture.path
                if os.path.isfile(old_picture_path):
                    os.remove(old_picture_path)
                old_picture.delete()
                messages.success(request, '画像をクリアしました。')
            return HttpResponseRedirect(self.get_success_url())

        if picture_form.is_valid():
            user_profile = picture_form.save(commit=False) 
            if 'picture' in request.FILES:
                if user_profile.picture:  
                    old_picture = Users.objects.get(id=self.request.user.id).picture
                    if old_picture:
                        old_picture_path = old_picture.path
                        if os.path.isfile(old_picture_path):
                            os.remove(old_picture_path)
                user_profile.save()
                messages.success(request, '画像を更新しました。')
            else:
                # ファイルが選択されていないがフォームが有効な場合（クリア以外）
                messages.info(request, '画像ファイルを選択してください。')
            
        else:
            # フォームが無効な場合のエラーメッセージをハンドリング
            for field in picture_form:
                for error in field.errors:
                    messages.error(request, error)
        
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('training_menus:home')
    
# メニュー追加画面
class TrainingAddView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = os.path.join('training_menus', 'training_add.html')
    form_class = UserCustomMenusForm
    model = UserCustomMenus
    success_message = 'メニューを追加しました'
    success_url = reverse_lazy('training_menus:training_list')

    # ユーザー紐づけロジック
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

# メニュー更新画面
class TrainingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = os.path.join('training_menus', 'training_update.html')
    form_class = UserCustomMenusForm
    model = UserCustomMenus
    success_message = 'メニューを更新しました'
    success_url = reverse_lazy('training_menus:training_list')

    # ユーザー紐づけロジック
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

# メニュー削除画面
class TrainingDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = os.path.join('training_menus', 'training_delete.html')
    model = UserCustomMenus
    success_message = 'メニューを削除しました'
    success_url = reverse_lazy('training_menus:training_list')


# トレーニング設定画面
class TrainingSettingsView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('training_menus', 'training_settings.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_form = TrainingTypeForm(user=self.request.user)
        part_form = TrainingPartForm(user=self.request.user)
        location_form = TrainingLocationForm(user=self.request.user)
        context['type_form'] = type_form
        context['part_form'] = part_form
        context['location_form'] = location_form
        context['type'] = TrainingType.objects.filter(user=self.request.user)
        context['part'] = TrainingPart.objects.filter(user=self.request.user)
        context['location'] = TrainingLocation.objects.filter(user=self.request.user)
        return context

    # タイプ、部位、場所追加ロジック
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'submit_type' in request.POST:
            type_form = TrainingTypeForm(request.POST, user=request.user)
            if type_form.is_valid():
                type_form.save()
                messages.success(request, 'トレーニングタイプを追加しました。')
        elif 'submit_part' in request.POST:
            part_form = TrainingPartForm(request.POST, user=request.user)
            if part_form.is_valid():
                part_form.save()
                messages.success(request, 'トレーニング部位を追加しました。')
        elif 'submit_location' in request.POST:
            location_form = TrainingLocationForm(request.POST, user=request.user)
            if location_form.is_valid():
                location_form.save()
                messages.success(request, 'トレーニング場所を追加しました。')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('training_menus:training_settings')
    

# トレーニングタイプ更新画面
class TrainingTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = os.path.join('training_menus', 'type_update.html')
    form_class = TrainingTypeForm
    model = TrainingType
    success_message = 'トレーニングタイプを更新しました'
    success_url = reverse_lazy('training_menus:training_settings')

    # ユーザー紐づけロジック
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

# トレーニングタイプ削除画面
class TrainingTypeDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = os.path.join('training_menus', 'type_delete.html')
    model = TrainingType
    success_message = 'トレーニングタイプを削除しました'
    success_url = reverse_lazy('training_menus:training_settings')

# トレーニング部位更新画面
class TrainingPartUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = os.path.join('training_menus', 'part_update.html')
    form_class = TrainingPartForm
    model = TrainingPart
    success_message = 'トレーニング部位を更新しました'
    success_url = reverse_lazy('training_menus:training_settings')

    # ユーザー紐づけロジック
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

# トレーニング部位削除画面
class TrainingPartDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = os.path.join('training_menus', 'part_delete.html')
    model = TrainingPart
    success_message = 'トレーニング部位を削除しました'
    success_url = reverse_lazy('training_menus:training_settings')

# トレーニング部位場所画面
class TrainingLocationUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = os.path.join('training_menus', 'location_update.html')
    form_class = TrainingLocationForm
    model = TrainingLocation
    success_message = 'トレーニング場所を更新しました'
    success_url = reverse_lazy('training_menus:training_settings')

    # ユーザー紐づけロジック
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

# トレーニング部位削除画面
class TrainingLocationDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = os.path.join('training_menus', 'location_delete.html')
    model = TrainingLocation
    success_message = 'トレーニング場所を削除しました'
    success_url = reverse_lazy('training_menus:training_settings')

# トレーニング目標更新画面
class TrainingGoalsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = os.path.join('training_menus', 'goals_update.html')
    form_class = TrainingGoalsForm
    model = TrainingGoals
    success_message = 'トレーニング目標を更新しました'
    success_url = reverse_lazy('training_menus:home')

    # 既存目標の表示ロジック
    def get_object(self, queryset=None):
        try:
            obj = TrainingGoals.objects.get(user=self.request.user)
        except TrainingGoals.DoesNotExist:
            obj = TrainingGoals(user=self.request.user)
        return obj

    # ユーザー紐づけロジック
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs









