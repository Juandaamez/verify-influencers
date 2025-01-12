import requests
from app.core.config import settings


def fetch_tweets(keywords):
    """
    Busca tweets basados en las palabras clave utilizando el Bearer Token.
    """

    headers = {
        "Authorization": f"Bearer {settings.x_bearer_token}",
        "Content-Type": "application/json"
    }

    tweets = []
    try:
        for keyword in keywords:
            url = f"https://api.twitter.com/2/tweets/search/recent?query={keyword}&max_results=10"
            response = requests.get(url, headers=headers)


            if response.status_code != 200:
                print(f"Error al buscar tweets: {response.status_code}, {response.text}")
                continue


            data = response.json()
            for tweet in data.get("data", []):
                tweets.append({
                    "id": tweet["id"],
                    "text": tweet["text"],
                    "author_id": tweet["author_id"]
                })

    except Exception as e:
        print(f"Error inesperado: {e}")

    return tweets
