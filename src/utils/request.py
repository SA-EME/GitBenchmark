import sys
import requests

from env import URL, TOKEN, PLATFORM

def request(path: str, method: str = "GET", **kwargs) -> dict:
    data = kwargs.get('data')
    json: dict = kwargs.get('json')
    headers: dict = kwargs.get('headers', {})
    files = kwargs.get('files')

    default_headers = {}

    if PLATFORM == "GITEA":
        default_headers = {"Authorization": f"token {TOKEN}"}

    elif PLATFORM == "GITHUB":
        default_headers = {"Accept": "application/vnd.github+json","Authorization": f"Bearer {TOKEN}", "X-GitHub-Api-Version": "2022-11-28"}

    default_headers.update(headers)
    try:
        response = requests.request(
            method,
            f"{URL}/{path}",
            headers=default_headers,
            verify=False,
            timeout=10,
            data=data if data else None,
            json=json if json else None,
            files=files if files else None
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        if response.status_code == 404:
            return None
        else:
            print(f"Erreur lors de la requête : {e}")
            sys.exit(1)

    try:
        return response.json()
    except Exception as e:
        print(f"Erreur lors de la lecture de la réponse : {e}")
        sys.exit(1)