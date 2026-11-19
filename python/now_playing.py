# Print the currently-playing Spotify track (the logic the ESP32 will replicate).
import requests
from refresh import get_access_token

access_token = get_access_token()

r = requests.get("https://api.spotify.com/v1/me/player/currently-playing",
                 headers={"Authorization": f"Bearer {access_token}"})

print("Status: ", r.status_code)

if r.status_code == 200:
    d = r.json()
    if d.get("item"):  # item is null for ads / some podcast states
        print(d['item']['name'], "—", d['item']['artists'][0]['name'])
    else:
        print("playing, but no track info (ad or podcast)")
elif r.status_code == 204:
    print("nothing playing...")
else:
    print(r.text)
