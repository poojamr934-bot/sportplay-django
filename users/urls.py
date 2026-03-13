from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('games/', views.game_list, name='game_list'),
    path('games/<int:id>/', views.game_detail, name='game_detail'),
    path('games/<int:id>/register/', views.register_game, name='register_game'),
    path('my-games/', views.my_games, name='my_games'),
    path('cancel/<int:reg_id>/', views.cancel_registration, name='cancel_registration'),
]