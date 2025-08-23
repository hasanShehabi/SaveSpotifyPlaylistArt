# Author: Hasan Shehabi
# Date 23/8/2025

import os, re, csv, time, requests, spotipy
from spotipy.oauth2 import SpotifyOAuth

#fetch creds from secrets_shhh
try:
    from secrets_shhh import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
except ImportError:
    print("could not fetch creds")
    exit(1)

SAVE_DIR = "spotify_playlist_covers" 
MINE_ONLY = True  
SLEEP_BETWEEN = 0.05  

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-read-private playlist-read-collaborative"
))

me = sp.current_user()
my_id = me["id"]

os.makedirs(SAVE_DIR, exist_ok=True)
log_path = os.path.join(SAVE_DIR, "covers_index.csv")

def safe_name(name: str) -> str:
    return re.sub(r'[^-\w\s.,()+&@]', '_', name).strip()[:100]

def iter_user_playlists():
    offset = 0
    while True:
        #limiited to 50 pages otherwise no work
        page = sp.current_user_playlists(limit=50, offset=offset)
        items = page.get("items", [])
        if not items:
            break
        for pl in items:
            if (not MINE_ONLY) or (pl.get("owner", {}).get("id") == my_id):
                yield pl
        offset += len(items)
        if len(items) < 50:
            break

def download_playlist_cover(playlist_id, playlist_name):
    images = sp.playlist_cover_image(playlist_id)  
    if not images:
        return None
    best = max(images, key=lambda i: ((i.get("width") or 0), (i.get("height") or 0)))
    url = best["url"]
    fname = f"{safe_name(playlist_name)}_{playlist_id}.jpg"
    out = os.path.join(SAVE_DIR, fname)

    r = requests.get(url, timeout=30)
    r.raise_for_status()
    with open(out, "wb") as f:
        f.write(r.content)
    return out

with open(log_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["playlist_id", "playlist_name", "owner_id", "saved_path"])
    count = 0
    for pl in iter_user_playlists():
        pid = pl["id"]
        pname = pl["name"]
        owner = pl.get("owner", {}).get("id")

        try:
            path = download_playlist_cover(pid, pname)
            if path:
                writer.writerow([pid, pname, owner, path])
                print(f"Saved: {pname} -> {path}")
                count += 1
            else:
                print(f"No cover available: {pname}")
        except requests.HTTPError as e:
            print(f"HTTP error for {pname}: {e}")
        except Exception as e:
            print(f"Error for {pname}: {e}")

        time.sleep(SLEEP_BETWEEN)

print(f"Coolio. All art saved ({count}) to: {SAVE_DIR}")
