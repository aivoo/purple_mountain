from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('api/', views.api_data),
    path('article/list/', views.article_list),
    path('article/<int:pk>/', views.article_one, name='article_one'),
    path('tutorial/list/', views.tutorial_list, name='tutorial_list'),
    path('tutorial/<int:pk>/', views.tutorial_one, name='tutorial_one'),
    path('tutorial/new/', views.tutorial_new, name='tutorial_new'),
]
