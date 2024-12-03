# Anime Recommendation System

This project is a REST API-based Anime Recommendation System that allows users to:
- Search for anime by name or genre.
- View recommended anime based on user preferences.
- Authenticate and manage user-specific anime preferences.

The backend leverages Django REST Framework, PostgreSQL, and the AniList GraphQL API to fetch and manage anime data.

---

## **Table of Contents**
- [Features](#features)
- [Technologies](#technologies)
- [Setup and Installation](#setup-and-installation)
- [Available Endpoints](#available-endpoints)
- [Sample Requests and Responses](#sample-requests-and-responses)

---

## **Features**
1. **Authentication**: 
   - JWT-based authentication.
   - Endpoints for user registration and login.
2. **Anime Search**:
   - Search anime by name or genre.
   - Cached results for faster access.
3. **Anime Recommendations**:
   - Personalized recommendations based on user preferences.
4. **User Preferences**:
   - Manage favorite genres via a dedicated endpoint.

---

## **Technologies**
- **Framework**: Django, Django REST Framework.
- **Database**: PostgreSQL.
- **Authentication**: JWT (JSON Web Tokens).
- **Anime Data**: AniList GraphQL API.

---

## **Setup and Installation**
### **Requirements**
- Python 3.10+
- PostgreSQL
- Docker (optional for containerized setup)

### **Local Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/Ayushsinha2629/anime_recommendation.git
   cd anime_recommendation
   ```
2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3. Docker Setup
    ```bash
    docker-compose up --build
    ```

## Available Endpoints

### Authentication

| Endpoint         | Method | Description                  |
|------------------|--------|------------------------------|
| `/auth/register` | POST   | Register a new user          |
| `/auth/login`    | POST   | Login and get JWT token      |

### Anime

| Endpoint                 | Method | Description                           |
|--------------------------|--------|---------------------------------------|
| `/anime/search`           | GET    | Search anime by name/genre           |
| `/anime/recommendations`  | GET    | Get personalized recommendations     |

### User Preferences

| Endpoint                | Method | Description                       |
|-------------------------|--------|-----------------------------------|
| `/user/preferences`     | POST   | Add or update preferences         |

---