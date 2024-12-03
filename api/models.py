from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model for extending Django's default User model.
    You can add additional fields here if needed.
    """
    # Add custom fields if needed
    pass


class UserPreference(models.Model):
    """
    Model to store user preferences, such as favorite genres.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    favorite_genres = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Preferences"


class CachedAnime(models.Model):
    """
    Model to store cached anime data fetched from AniList for performance.
    """
    anime_id = models.IntegerField(unique=True)  # AniList anime ID
    title_romaji = models.CharField(max_length=255)
    title_english = models.CharField(max_length=255, blank=True, null=True)
    genres = models.JSONField(default=list)  # Store a list of genres
    popularity = models.IntegerField()
    cached_at = models.DateTimeField(auto_now_add=True)  # When it was cached

    def __str__(self):
        return f"Cached: {self.title_romaji} (ID: {self.anime_id})"
