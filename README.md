# Spotify Playlist Cover Downloader

This Python script downloads the cover art for all of a Spotify user's playlists. It saves the images to a local directory and creates a CSV file to index the downloaded covers.

## Features

- Downloads cover art for all public and private playlists.
- Optionally, download covers only for playlists you own.
- Saves images in the highest available resolution.
- Creates a `covers_index.csv` log file with details about the downloaded images (Playlist ID, Name, Owner, and local file path).
- Sanitizes playlist names to create safe filenames.
- Adjustable sleep timer between downloads to avoid hitting API rate limits.

## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
    Install the required packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

To use this script, you need to have a Spotify account and create a Spotify App to get API credentials.

1.  **Create a Spotify App:**
    - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/).
    - Log in with your Spotify account.
    - Click on "Create an App".
    - Fill in the app name and description.
    - Once the app is created, you will see your `Client ID` and you can click "Show client secret" to see the `Client Secret`.

2.  **Set the Redirect URI:**
    - In your app's settings on the Spotify Developer Dashboard, click on "Edit Settings".
    - In the "Redirect URIs" field, add `https://http.cat/images/102.jpg`.
    - Click "Save".

3.  **Update `secrets_shhh.py`:**
    - Open the `secrets_shhh.py` file.
    - Replace the placeholder values for `CLIENT_ID` and `CLIENT_SECRET` with the credentials from your Spotify App.
    - The `REDIRECT_URI` should already be set correctly, but ensure it matches what you entered in the app settings.

    ```python
    # secrets_shhh.py
    CLIENT_ID = "your-spotify-client-id"
    CLIENT_SECRET = "your-spotify-client-secret"
    REDIRECT_URI = "https://http.cat/images/102.jpg"
    ```

## Usage

Once you have installed the dependencies and configured your credentials, you can run the script:

```bash
python main.py
```

The first time you run the script, it will open a browser window and ask you to log in to your Spotify account and grant permission to your app. After you approve, you will be redirected to the redirect URI you set. Copy the full URL of the page you were redirected to and paste it into the terminal when prompted.

The script will then start downloading the playlist covers.

## Output

The script will create a directory named `spotify_playlist_covers` in the same directory where the script is located. Inside this directory, you will find:
- The downloaded playlist cover images, named in the format `<sanitized_playlist_name>_<playlist_id>.jpg`.
- A `covers_index.csv` file containing a log of all downloaded covers. The CSV has the following columns: `playlist_id`, `playlist_name`, `owner_id`, `saved_path`.

## Customization

You can customize the script's behavior by editing the following variables at the top of `main.py`:

- `SAVE_DIR`: The directory where the covers and the log file will be saved. Defaults to `"spotify_playlist_covers"`.
- `MINE_ONLY`: Set to `True` to download covers only for playlists you own. Set to `False` to download covers for all playlists you follow, including collaborative ones. Defaults to `True`.
- `SLEEP_BETWEEN`: The time in seconds to wait between downloading each cover. This helps to avoid API rate limits. Defaults to `0.05`.
