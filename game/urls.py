from django.urls import path

from . import views

app_name = 'game'
urlpatterns = [
    path('', views.index),
    path('index', views.index, name="index"),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout', views.logout_view, name="logout"),
    path('register', views.register_view, name="register"),
    path('new-game', views.new_game, name="new_game"),
    path('game/<uuid:id>', views.game, name="game"),
    path('search/', views.search_view, name="search_view"),
    path('start-game/', views.start_game, name="start_game"),
    path('join-game/', views.join_game, name="join_game"),
    path('update-score/', views.update_score, name="update_score"),
    path('update-round/', views.update_round, name="update_round"),
    path('finish-game/', views.finish_game, name="finish_game"),
    path('go-back/', views.go_back, name="go_back"),
]
