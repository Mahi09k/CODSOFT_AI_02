from django.urls import path
from . import views

urlpatterns = [
    path('', views.choose_mode, name='choose_mode'),  # URL for choosing game mode
    path('ai-game/', views.index, name='ai_game_view_name'),  # URL for AI game view
    path('player-game/', views.player_game_view, name='player_game_view_name'),
]
