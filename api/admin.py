from django.contrib import admin
from .models import User, UserPreference, CachedAnime

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active']

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'favorite_genres', 'created_at', 'updated_at']

@admin.register(CachedAnime)
class CachedAnimeAdmin(admin.ModelAdmin):
    list_display = ['anime_id', 'title_romaji', 'title_english', 'popularity', 'cached_at']
