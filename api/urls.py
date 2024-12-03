from django.urls import path
from .views import RegisterView, LoginView, AnimeSearchView, AnimeRecommendationsView, UserPreferencesView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('anime/search', AnimeSearchView.as_view(), name='search'),
    path('anime/recommendations', AnimeRecommendationsView.as_view(), name='recommendations'),
    path('user/preferences', UserPreferencesView.as_view(), name='preferences'),
]
