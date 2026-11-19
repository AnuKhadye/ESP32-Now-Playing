# ESP32 Spotify "Now Playing" Display

A small, always-on desk display that shows the track currently playing on my Spotify account, running on an ESP32 with a 2.8" 240×320 TFT ("Cheap Yellow Display", ESP32-2432S028R). No subscription and no phone app: the board talks to the Spotify Web API directly over Wi-Fi.

> **Status: work in progress (~60%).** The Spotify OAuth flow is proven in Python, and the ESP32 can join Wi-Fi and fetch and parse live HTTPS JSON. Spotify-on-the-chip and the screen are the next steps. See [Progress](#progress).

## How it works

```
ONE-TIME, on a laptop (get_token.py)
  browser login -> authorization code -> refresh token (long-lived, stored on device)

EVERY ~5 s, on the ESP32
  refresh token -> access token (valid 1 h, re-minted on expiry / 401)
  GET /v1/me/player/currently-playing
  parse item.name + item.artists[0].name
  draw on the TFT (redraw only when the song changes)
```

- **Why prototype in Python first:** OAuth is the riskiest part, so I proved the full flow (auth code → refresh token → access token → currently-playing, including the `204 No Content` "nothing playing" case) on a laptop, where it is easier to debug, before porting it to C++.
- **Why the refresh token matters:** access tokens expire after an hour. The device stores only the long-lived refresh token and mints new access tokens itself, so it can run unattended.
- **Why ESP32:** built-in Wi-Fi and TLS, dual-core 240 MHz, and cheap boards with an integrated screen exist.
- **Memory constraint:** the ESP32 has roughly 200 KB of usable RAM, so Spotify's large JSON responses will be filtered to only the needed fields (ArduinoJson filter) rather than parsed whole.

## Repository layout

| Path | What it is |
|---|---|
| `python/get_token.py` | One-time: swaps an authorization code for a refresh token |
| `python/refresh.py` | Mints an access token from the refresh token (`get_access_token()`) |
| `python/now_playing.py` | Prints the current track; handles 200 and 204 |
| `python/spotify_secrets.example.py` | Template for credentials (the real file is gitignored) |
| `esp32/fetch_test/` | Arduino sketch: Wi-Fi connect + HTTPS GET + ArduinoJson parse, output to Serial |
| `esp32/fetch_test/secrets.example.h` | Template for Wi-Fi credentials (the real `secrets.h` is gitignored) |

## Progress

**Done**
- [x] Spotify developer app; OAuth 2.0 Authorization Code flow working in Python, refresh token obtained
- [x] Python: refresh token → access token → currently-playing, handling `200` and `204`
- [x] ESP32 toolchain (Arduino IDE 2, Espressif core 3.3.x, CH340/CP2102 drivers); board flashing over USB
- [x] ESP32: Wi-Fi connect, HTTPS GET of a public JSON API, parse with ArduinoJson, print to Serial

**Next: Spotify on the chip**
- [ ] Token refresh on ESP32 (HTTPS POST with a Basic auth header via `WiFiClientSecure`)
- [ ] Fetch currently-playing with a Bearer token and parse `item.name` / `item.artists[0].name`
- [ ] Handle `204` (nothing playing) and `401` (token expired → refresh and retry)
- [ ] Non-blocking `millis()` poll loop (~5 s)

**Then: screen and album art**
- [ ] TFT_eSPI configured for the CYD; layout for title, artist and art
- [ ] Album art: smallest image (~64 px) from `item.album.images[]`, decoded on-chip with TJpg_Decoder, redrawn only when the song changes

**Hardening (planned)**
- [ ] Replace `setInsecure()` with Spotify's root CA certificate
- [ ] Watch `ESP.getFreeHeap()`; filter JSON; replace `String` with fixed buffers if the heap fragments

## Running it

**Python prototype**
```powershell
cd python
pip install -r requirements.txt
copy spotify_secrets.example.py spotify_secrets.py   # then fill in your values
python now_playing.py
```

**ESP32 sketch:** open `esp32/fetch_test/fetch_test.ino` in Arduino IDE 2, copy `secrets.example.h` to `secrets.h` and fill it in, install **ArduinoJson** (by Benoît Blanchon), select **ESP32 Dev Module**, upload, and open the Serial Monitor at 115200 baud.

## Hardware

- ESP32-2432S028R "Cheap Yellow Display": ESP32-D0WD-V3 + 2.8" 240×320 TFT, resistive touch, CH340 USB-serial
- Spare ESP32 dev boards (CP2102) for breadboard experiments
