# One-time step: swap an authorization code for a refresh token.
# Usage: python get_token.py <code from the ?code= part of the redirect URL>
import sys, requests, base64
from spotify_secrets import CLIENT_ID, CLIENT_SECRET

if len(sys.argv) != 2:
    sys.exit("Usage: python get_token.py <authorization_code>")
CODE = sys.argv[1]

auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

r = requests.post("https://accounts.spotify.com/api/token",
                  headers={"Authorization": f"Basic {auth}"},
                  data={
                      "grant_type": "authorization_code",
                      "code": CODE,
                      "redirect_uri": "http://127.0.0.1:8888/callback"
                  })

print(r.status_code)
print(r.json())  # copy "refresh_token" into spotify_secrets.py
