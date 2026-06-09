"""
Telegram notification helper for the FA Agent.

Usage:
  python send_telegram.py <config_path> <message_file_or_text> [html_report_path]

If the second argument is a file path that exists, reads the message from that file.
Otherwise, treats it as the message text directly.

If a third argument is provided and points to an existing file, it will be sent
as a document attachment after the text message.

Supports Markdown formatting (Telegram MarkdownV2 parse mode).
"""
import sys
import json
import urllib.request
import urllib.parse
import os
import uuid
import mimetypes


def send_message(bot_token, chat_id, message):
    """Send a message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    # Telegram has a 4096 char limit per message — split if needed
    max_len = 4000
    chunks = [message[i:i + max_len] for i in range(0, len(message), max_len)]

    for i, chunk in enumerate(chunks):
        data = urllib.parse.urlencode({
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "Markdown"
        }).encode("utf-8")

        req = urllib.request.Request(url, data=data)
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read())
                if result["ok"]:
                    print(f"Message chunk {i + 1}/{len(chunks)} sent successfully")
                else:
                    print(f"Telegram API error: {result}")
                    return False
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            print(f"HTTP Error {e.code}: {error_body}")
            # If Markdown fails, retry without parse_mode
            if "parse_mode" in error_body.lower() or e.code == 400:
                print("Retrying without Markdown formatting...")
                data = urllib.parse.urlencode({
                    "chat_id": chat_id,
                    "text": chunk
                }).encode("utf-8")
                req2 = urllib.request.Request(url, data=data)
                try:
                    with urllib.request.urlopen(req2) as resp2:
                        result2 = json.loads(resp2.read())
                        if result2["ok"]:
                            print(f"Message chunk {i + 1}/{len(chunks)} sent (plain text fallback)")
                        else:
                            print(f"Fallback also failed: {result2}")
                            return False
                except Exception as e2:
                    print(f"Fallback error: {e2}")
                    return False
            else:
                return False
        except Exception as e:
            print(f"Error sending message: {e}")
            return False

    return True


def send_document(bot_token, chat_id, file_path, caption=None):
    """Send a file as a document attachment via Telegram Bot API (multipart/form-data)."""
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    # Build multipart/form-data manually (no external dependencies)
    boundary = uuid.uuid4().hex
    filename = os.path.basename(file_path)
    content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"

    with open(file_path, "rb") as f:
        file_data = f.read()

    # Construct the multipart body
    parts = []

    # chat_id field
    parts.append(
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="chat_id"\r\n\r\n'
        f"{chat_id}\r\n"
    )

    # caption field (optional)
    if caption:
        parts.append(
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="caption"\r\n\r\n'
            f"{caption}\r\n"
        )

    # Build the text portion as bytes
    text_body = "".join(parts).encode("utf-8")

    # File part header
    file_header = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="document"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8")

    # Closing boundary
    closing = f"\r\n--{boundary}--\r\n".encode("utf-8")

    # Combine everything
    body = text_body + file_header + file_data + closing

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            if result["ok"]:
                print(f"Document '{filename}' sent successfully")
                return True
            else:
                print(f"Telegram API error: {result}")
                return False
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code} sending document: {error_body}")
        return False
    except Exception as e:
        print(f"Error sending document: {e}")
        return False


def main():
    if len(sys.argv) < 3:
        print("Usage: python send_telegram.py <config_path> <message_or_file> [html_report_path]")
        sys.exit(1)

    config_path = sys.argv[1]
    message_arg = sys.argv[2]
    html_report_path = sys.argv[3] if len(sys.argv) >= 4 else None

    # Load config
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    bot_token = config["telegram"]["bot_token"]
    chat_id = config["telegram"]["chat_id"]

    # Check if message_arg is a file path
    if os.path.isfile(message_arg):
        with open(message_arg, "r", encoding="utf-8") as f:
            message = f.read()
    else:
        message = message_arg

    if not message.strip():
        print("Empty message, skipping send.")
        sys.exit(0)

    # Send the text report
    success = send_message(bot_token, chat_id, message)

    # Send the HTML report as a document attachment if provided
    if html_report_path and os.path.isfile(html_report_path):
        doc_success = send_document(
            bot_token,
            chat_id,
            html_report_path,
            caption="📊 Full Intelligence Report — open in browser for the interactive dashboard."
        )
        if not doc_success:
            print("Warning: Text report sent, but HTML attachment failed.")
    elif html_report_path:
        print(f"Warning: HTML report path '{html_report_path}' not found, skipping attachment.")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
