
from quart import Quart, request, Response, stream_with_context
from telethon import TelegramClient, events
import re
import os
import argparse
import asyncio

def parse_args():
    parser = argparse.ArgumentParser(description='Telegram Video Downloader')
    parser.add_argument('--api_id', help='Your Telegram API ID', default=os.getenv('API_ID'))
    parser.add_argument('--api_hash', help='Your Telegram API Hash', default=os.getenv('API_HASH'))
    parser.add_argument('--session_file', help='Session file name', default=os.getenv('SESSION_FILE', 'session_name'))
    parser.add_argument('--mode', help='Your Telegram API ID', default='http')
    parser.add_argument('--url', help='Your Telegram message URL with media', default=None)
    parser.add_argument('--output', help='Your output folder', default=None)


    args = parser.parse_args()
    return args

# Initialization of the Telegram client
args = parse_args()
client = TelegramClient(args.session_file, args.api_id, args.api_hash)
app = Quart(__name__)
CHUNK_SIZE = 64 * 1024  # 64 KB

async def download_generator(client, document, start, end):
    pos = start
    remaining = end - start + 1
    async for chunk in client.iter_download(document, offset=pos, limit=remaining):
        yield chunk
        remaining -= len(chunk)
        if remaining <= 0:
            break

async def download_url(url, output):
    split_url = url.split('/')
    channel = split_url[-3]  # Ajusta según el formato real de tu URL.
    message_id = int(split_url[-1])

    await client.start()
    message = await client.get_messages(channel, ids=int(message_id))
    if not message or not hasattr(message, 'media'):
        return "Message not found or it doesn't contain any media", 404
    
    # Obteniendo el nombre del archivo del documento
    if hasattr(message.media, 'document') and hasattr(message.media.document, 'attributes'):
        for attribute in message.media.document.attributes:
            if hasattr(attribute, 'file_name'):
                file_name = attribute.file_name
                break
    else:
        file_name = "downloaded_file.mp4"  # Nombre por defecto si no se encuentra el nombre del archivo

    def progress_callback(current_bytes, total_bytes):
        print(f"\rDownloaded {current_bytes} out of {total_bytes} bytes: {(current_bytes/total_bytes)*100:.1f}%", end='')

    # Asegúrate de imprimir una nueva línea después de la descarga
    file_path = await client.download_media(message.media, file=os.path.join(output, file_name), progress_callback=progress_callback)
    print("\nFile downloaded to", file_path)

    return file_path
    
@app.route("/telegram/direct/<telegram_id>")
async def telegram_direct(telegram_id):
    channel = telegram_id.split('-')[0]
    video_id = int(telegram_id.split('-')[1])
    if not video_id:
        return "Video ID is required", 400

    await client.start()
    message = await client.get_messages(channel, ids=[video_id])
    if not message or not hasattr(message[0], 'media'):
        return "Message not found or it doesn't contain any media", 404

    document = message[0].media.document
    file_size = document.size

    range_header = request.headers.get("Range")
    start, end = 0, file_size - 1 # Suposiciones iniciales
    headers = {
        "Accept-Ranges": "bytes", 
    }

    if range_header:
        match = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if match:
            start, end = match.groups()
            start = int(start)
            end = int(end) if end else file_size - 1

            headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
            headers["Content-Length"] = str(end - start + 1)
            status_code = 206  # Partial Content
        else:
            return "Invalid Range header", 416  # Range Not Satisfiable
    else:
        status_code = 200  # OK
        headers["Content-Length"] = str(file_size)

    return Response(download_generator(client, document, start, end), status=status_code, headers=headers, content_type="video/mp4")

def main():
    if args.mode == 'http':
        app.run(port=5151)
    elif args.mode == 'download':
        if args.url and args.output:
            if 'https://t.me/':
                asyncio.run(download_url(args.url, args.output))
            else:
                print('Starts Telegram message URL with https://t.me/...')
        else:
            print('With download mode a message url and output are required')

    
if __name__ == '__main__':
    main()