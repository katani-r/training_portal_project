from django.urls import path
from .views import (
    TrainingListView, TrainingAddView, TrainingUpdateView,
    TrainingDeleteView, TrainingSettingsView, TrainingTypeUpdateView,
    TrainingTypeDeleteView, TrainingPartUpdateView, TrainingPartDeleteView,
    TrainingLocationUpdateView, TrainingLocationDeleteView, HomeView,
    TrainingGoalsUpdateView
)

app_name = 'training_menus'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('training_list/', TrainingListView.as_view(), name='training_list'),
    path('training_add/', TrainingAddView.as_view(), name='training_add'),
    path('training_update/<int:pk>', TrainingUpdateView.as_view(), name='training_update'),
    path('training_delete/<int:pk>', TrainingDeleteView.as_view(), name='training_delete'),
    path('training_settings/', TrainingSettingsView.as_view(), name='training_settings'),
    path('type_update/<int:pk>', TrainingTypeUpdateView.as_view(), name='type_update'),
    path('type_delete/<int:pk>', TrainingTypeDeleteView.as_view(), name='type_delete'),
    path('part_update/<int:pk>', TrainingPartUpdateView.as_view(), name='part_update'),
    path('part_delete/<int:pk>', TrainingPartDeleteView.as_view(), name='part_delete'),
    path('location_update/<int:pk>', TrainingLocationUpdateView.as_view(), name='location_update'),
    path('location_delete/<int:pk>', TrainingLocationDeleteView.as_view(), name='location_delete'),
    path('goals_update/', TrainingGoalsUpdateView.as_view(), name='goals_update'),
]