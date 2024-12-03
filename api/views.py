from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserPreference, CachedAnime
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .authentication import JWTAuthentication
import logging
import jwt
import datetime
import requests


SECRET_KEY = '123456'

User = get_user_model()
logger = logging.getLogger(__name__)

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            payload = {
                'id': user.id,
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24),
                'iat': datetime.datetime.now(datetime.timezone.utc),
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



ANILIST_URL = 'https://graphql.anilist.co'


class AnimeRecommendationsView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user

        # Fetch user preferences
        try:
            user_preferences = user.preferences
        except UserPreference.DoesNotExist:
            return Response(
                {"error": "User preferences not found. Please set your preferences first."},
                status=404
            )

        favorite_genres = user_preferences.favorite_genres
        if not favorite_genres:
            return Response(
                {"error": "No favorite genres found in user preferences."},
                status=400
            )

        recommendations = []

        for genre in favorite_genres:
            # Check cache
            cached_anime = CachedAnime.objects.filter(genres__contains=[genre])
            if cached_anime.exists():
                recommendations.extend([
                    {
                        'anime_id': anime.anime_id,
                        'title_romaji': anime.title_romaji,
                        'title_english': anime.title_english,
                        'genres': anime.genres,
                        'popularity': anime.popularity,
                    }
                    for anime in cached_anime
                ])
            else:
                # Fetch from AniList if not in cache
                graphql_query = '''
                query ($genre: String) {
                    Page {
                        media(genre: $genre, sort: POPULARITY_DESC, type: ANIME) {
                            id
                            title {
                                romaji
                                english
                            }
                            genres
                            popularity
                        }
                    }
                }
                '''
                variables = {'genre': genre}
                response = requests.post(
                    ANILIST_URL,
                    json={'query': graphql_query, 'variables': variables}
                )

                if response.status_code == 200:
                    results = response.json().get('data', {}).get('Page', {}).get('media', [])
                    recommendations.extend(results)

                    # Cache the results
                    for anime in results:
                        CachedAnime.objects.update_or_create(
                            anime_id=anime['id'],
                            defaults={
                                'title_romaji': anime['title']['romaji'],
                                'title_english': anime['title'].get('english'),
                                'genres': anime['genres'],
                                'popularity': anime['popularity'],
                            }
                        )
                else:
                    return Response(
                        {"error": f"Failed to fetch recommendations for genre '{genre}'."},
                        status=response.status_code
                    )

        # Remove duplicates
        seen_ids = set()
        unique_recommendations = []
        for anime in recommendations:
            if anime['anime_id'] not in seen_ids:
                unique_recommendations.append(anime)
                seen_ids.add(anime['anime_id'])

        return Response(
            {"recommendations": unique_recommendations},
            status=200
        )
    
class UserPreferencesView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        favorite_genres = request.data.get('favorite_genres', [])
        
        # Create or update UserPreference
        user_preferences, created = UserPreference.objects.get_or_create(user=user)
        user_preferences.favorite_genres = favorite_genres
        user_preferences.save()
        
        return Response({'message': 'Preferences updated'}, status=status.HTTP_200_OK)
    
class AnimeSearchView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        query = request.GET.get('query')
        genre = request.GET.get('genre')

        # Check cache
        cached_anime = CachedAnime.objects.filter(genres__contains=[genre]) if genre else CachedAnime.objects.all()
        if query:
            cached_anime = cached_anime.filter(title_romaji__icontains=query)

        if cached_anime.exists():
            data = [
                {
                    'anime_id': anime.anime_id,
                    'title_romaji': anime.title_romaji,
                    'title_english': anime.title_english,
                    'genres': anime.genres,
                    'popularity': anime.popularity,
                }
                for anime in cached_anime
            ]
            return Response(data, status=status.HTTP_200_OK)

        # Fetch from AniList if not in cache
        graphql_query = '''
        query ($search: String, $genre: String) {
            Page {
                media(search: $search, genre: $genre, type: ANIME) {
                    id
                    title {
                        romaji
                        english
                    }
                    genres
                    popularity
                }
            }
        }
        '''
        variables = {'search': query, 'genre': genre}
        response = requests.post(ANILIST_URL, json={'query': graphql_query, 'variables': variables})

        if response.status_code == 200:
            results = response.json().get('data', {}).get('Page', {}).get('media', [])
            
            # Cache results
            for anime in results:
                CachedAnime.objects.update_or_create(
                    anime_id=anime['id'],
                    defaults={
                        'title_romaji': anime['title']['romaji'],
                        'title_english': anime['title'].get('english'),
                        'genres': anime['genres'],
                        'popularity': anime['popularity'],
                    }
                )
            return Response(results, status=status.HTTP_200_OK)
        return Response({'error': 'Failed to fetch anime'}, status=response.status_code)