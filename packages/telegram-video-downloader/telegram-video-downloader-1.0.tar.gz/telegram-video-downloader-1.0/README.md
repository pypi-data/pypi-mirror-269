# telegram-video-downloader
Command to download a video published on Telegram
Here is an example of a README.md for your Telegram Video Downloader project using Quart and Telethon, translated into English. Modify the details as necessary for your specific project.

---

# Telegram Video Downloader

This project enables you to download videos from Telegram directly to your computer, either via an HTTP API or by running the script in direct download mode. It utilizes Quart, an asynchronous Python framework, and Telethon, a Telegram client library.

## Prerequisites

Before you start, make sure you have the following:

- Python 3.7 or higher
- A Telegram account and API credentials (API ID and API Hash), which you can obtain through [my.telegram.org](https://my.telegram.org/)
- (Optional) A Python virtual environment for installing dependencies

## Installation

1. pip install.
   ```
   pip install telegram-video-downloader
   ```

2. Set up your environment variables or pass the necessary arguments (`api_id`, `api_hash`, `session_file`) to the script.

## Usage

The script can be run in two modes: `http` (by default) and `download`.

### HTTP Mode

This mode starts a local HTTP server that allows you to download videos directly via a specified URL.

```
telegram-video-downloader --api_id YOUR_API_ID --api_hash YOUR_API_HASH --session_file PATH_TO_YOUR_SESSION_FILE --mode http
```

Once the server is running, you can play videos using the path `/telegram/direct/{telegram_id}`, where `{telegram_id}` is a combination of the channel ID and the video ID, separated by a dash. For example:
```
http://127.0.0.1:5151/telegram/direct/pokemontvcastellano-2016
```
This telegram-video-downloader url's can be stored in strm files or played directly in vlc for example.

### Download Mode

This mode directly downloads a specific video to your computer using the video's Telegram URL.

```
telegram-video-downloader --api_id YOUR_API_ID --api_hash YOUR_API_HASH --session_file PATH_TO_YOUR_SESSION_FILE --mode download --url TELEGRAM_VIDEO_URL --output OUTPUT_FOLDER
```

## Examples of Use

- Starting the HTTP server:
  ```
  telegram-video-downloader --api_id 123456 --api_hash abcdef1234567890abcdef1234567890 --session_file session_name.session --mode http
  ```

- Directly downloading a video:
  ```
  telegram-video-downloader --api_id 123456 --api_hash abcdef1234567890abcdef1234567890 --session_file session_name.session --mode download --url https://t.me/pokemontvcastellano/1/2016 --output /media/telegram
  ```

## Contributions

Contributions are welcome. Please feel free to fork the repository and submit your pull requests.

## License

This project is licensed under MIT License. See the LICENSE file for more details.
