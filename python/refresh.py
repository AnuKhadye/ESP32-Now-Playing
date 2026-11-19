# Mint a short-lived (1 hour) access token from the long-lived refresh token.
import requests, base64
from spotify_secrets import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN


def get_access_token():
    auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    r = requests.post("https://accounts.spotify.com/api/token",
                      headers={"Authorization": f"Basic {auth}"},
                      data={
                          "grant_type": "refresh_token",
                          "refresh_token": REFRESH_TOKEN
                      })
    r.raise_for_status()  # fail loudly on a bad secret/token instead of a KeyError
    return r.json()["access_token"]


if __name__ == "__main__":
    token = get_access_token()
    print("Got access token:", token[:12] + "...")  # don't print the whole token
