import os
import requests


def get_twitch_token():
    client_id = os.getenv("IGDB_CLIENT_ID")
    client_secret = os.getenv("IGDB_CLIENT_SECRET")
    url = f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials"
    response = requests.post(url)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def fetch_game_data(search_query):
    token = get_twitch_token()
    client_id = os.getenv("IGDB_CLIENT_ID")
    if not token or not client_id:
        return None
    url = "https://api.igdb.com/v4/games"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}"
    }
    query = f'search "{search_query}"; fields name, cover.image_id, artworks.image_id; limit 1;'
    response = requests.post(url, headers=headers, data=query)
    if response.status_code == 200 and len(response.json()) > 0:
        game_info = response.json()[0]
        cover_url = None
        banner_url = None
        if 'cover' in game_info:
            cover_id = game_info['cover']['image_id']
            cover_url = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{cover_id}.jpg"
        if 'artworks' in game_info:
            # Games can have multiple artworks, we just grab the first one for the banner
            artwork_id = game_info['artworks'][0]['image_id']
            banner_url = f"https://images.igdb.com/igdb/image/upload/t_1080p/{artwork_id}.jpg"
        return {
            'name': game_info.get('name', search_query),
            'cover_url': cover_url,
            'banner_url': banner_url
        }

    return None


def get_game_suggestions(search_query):
    """Fetches up to 5 game results with thumbnail URLs for an autocomplete dropdown"""
    token = get_twitch_token()
    client_id = os.getenv("IGDB_CLIENT_ID")
    if not token or not client_id:
        return []
    url = "https://api.igdb.com/v4/games"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}"
    }
    query = f'search "{search_query}"; fields name, cover.image_id; limit 5;'
    response = requests.post(url, headers=headers, data=query)
    if response.status_code == 200:
        games_data = response.json()
        results = []
        for game in games_data:
            icon_url = ""
            if 'cover' in game:
                cover_id = game['cover']['image_id']
                icon_url = f"https://images.igdb.com/igdb/image/upload/t_cover_small/{cover_id}.jpg"
            results.append({
                'name': game.get('name', 'Unknown Game'),
                'icon_url': icon_url
            })
        return results
    return []