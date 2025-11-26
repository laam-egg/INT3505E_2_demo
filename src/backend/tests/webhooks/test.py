#!/usr/bin/env python3
"""
Simple script to test webhook creation and delivery using only Python standard library.
"""

import json
import http.server
import threading
import urllib.request
import urllib.error
import urllib.parse
import time
import uuid
import os
import re

def is_status_success(status_code: int | str) -> bool:
    c = str(status_code)
    return re.match(r"2\d{2}", c) is not None

# -------------------------------
# Configuration
# -------------------------------
BACKEND_URL = os.getenv("BACKEND_URL", "")
if not BACKEND_URL:
    raise ValueError("Please set the BACKEND_URL environment variable to the backend server URL (including the version, e.g., http://localhost:5000/api/v4)")
BACKEND_URL = BACKEND_URL.rstrip("/") + '/'

def join_url(base: str, path: str) -> str:
    return urllib.parse.urljoin(base, path.lstrip("/"))

WEBHOOK_TARGET_DOMAIN = os.getenv("WEBHOOK_TARGET_DOMAIN", "127.0.0.1")
WEBHOOK_TARGET_PORT = 4999  # Port where this script will listen for webhook callbacks
WEBHOOK_TARGET_PATH = "/webhook-destination"  # Path for webhook
# ATTENTION: Webhook target URL must not be localhost
WEBHOOK_TARGET_URL = f"http://{WEBHOOK_TARGET_DOMAIN}:{WEBHOOK_TARGET_PORT}{WEBHOOK_TARGET_PATH}"

print(f"[Config] BACKEND_URL = {BACKEND_URL}")
print(f"[Config] WEBHOOK_TARGET_URL = {WEBHOOK_TARGET_URL}")

# Global flag to indicate webhook was called
webhook_called = threading.Event()
received_payload = None

# -------------------------------
# HTTP Server to receive webhook
# -------------------------------
class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        global received_payload
        if self.path != WEBHOOK_TARGET_PATH:
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            received_payload = json.loads(body)
        except json.JSONDecodeError:
            received_payload = body

        print(f"[WebhookServer] Received webhook payload: {received_payload}")

        self.send_response(200)
        self.end_headers()
        webhook_called.set()

    # Suppress logging
    def log_message(self, format, *args):
        return

def start_webhook_server():
    server = http.server.HTTPServer(("0.0.0.0", WEBHOOK_TARGET_PORT), WebhookHandler)
    print(f"[WebhookServer] Listening on port {WEBHOOK_TARGET_PORT}")
    server.serve_forever()

# -------------------------------
# Create webhook in backend
# -------------------------------
def create_webhook(webhook_url: str, event_name: str) -> bool:
    print(f"[Client] Creating webhook for event '{event_name}' to URL '{webhook_url}'...")
    url = join_url(BACKEND_URL, "webhooks")
    payload = {
        "eventName": event_name,
        "targetUrl": webhook_url
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp_body = resp.read().decode("utf-8")
            if not is_status_success(resp.status):
                print(f"[Client] Failed to create webhook: {resp.status}. Body: {resp_body}")
                return False
            print(f"[Client] Webhook created: {resp.status} {resp_body}")
            return True
    except urllib.error.HTTPError as e:
        print(f"[Client] HTTPError: {e.code} {e.reason} {e.read().decode('utf-8')}")
    except urllib.error.URLError as e:
        print(f"[Client] URLError: {e.reason}")
    return False

# -------------------------------
# Remove webhook in backend
# -------------------------------
def remove_webhook(webhook_url: str, event_name: str) -> bool:
    print(f"[Client] Removing webhook for event '{event_name}' to URL '{webhook_url}'...")
    # First, list webhooks to find the ID
    list_url = join_url(BACKEND_URL, "webhooks")
    query_params = urllib.parse.urlencode({"targetUrl": webhook_url})
    full_list_url = f"{list_url}?{query_params}"
    try:
        with urllib.request.urlopen(full_list_url, timeout=10) as resp:
            resp_body = resp.read().decode("utf-8")
            if not is_status_success(resp.status):
                print(f"[Client] Failed to list webhooks: {resp.status}. Body: {resp_body}")
                return False
            webhooks = json.loads(resp_body)['content']
            webhook_id = None
            for wh in webhooks:
                if wh.get("eventName") == event_name and wh.get("targetUrl") == webhook_url:
                    webhook_id = wh.get("id")
                    break
            if not webhook_id:
                print(f"[Client] Webhook not found for removal.")
                return False
            # Now, delete the webhook
            delete_url = join_url(BACKEND_URL, f"webhooks/{webhook_id}")
            req = urllib.request.Request(delete_url, method="DELETE")
            with urllib.request.urlopen(req, timeout=10) as del_resp:
                del_resp_body = del_resp.read().decode("utf-8")
                if not is_status_success(del_resp.status):
                    print(f"[Client] Failed to delete webhook: {del_resp.status}. Body: {del_resp_body}")
                    return False
                print(f"[Client] Webhook deleted: {del_resp.status} {del_resp_body}")
                return True
    except urllib.error.HTTPError as e:
        print(f"[Client] HTTPError: {e.code} {e.reason} {e.read().decode('utf-8')}")
    except urllib.error.URLError as e:
        print(f"[Client] URLError: {e.reason}")
    return False

# -------------------------------
# Trigger test event
# -------------------------------
def trigger_auth_login_failed_event():
    print(f"[Client] Triggering auth.login.failed event...")
    url = join_url(BACKEND_URL, "/auth/login")
    payload = {
        "email": "VERY_WRONG_EMAIL@whatever.com",
        "password": "VERY_WRONG_PASSWORD" + str(uuid.uuid4()),
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp_body = resp.read().decode("utf-8")
            print(f"[Client] Test event triggered: {resp.status} {resp_body}")
            return True
    except urllib.error.HTTPError as e:
        # Expecting failure due to wrong credentials
        if e.code in [401, 404]:
            print(f"[Client] Test event triggered (expected failure): {e.code} {e.reason} {e.read().decode('utf-8')}")
            return True
        else:
            print(f"[Client] HTTPError: {e.code} {e.reason} {e.read().decode('utf-8')}")
            return False
    except Exception as e:
        print(f"[Client] Failed to trigger test event: {e}")
        return False

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    # Start webhook HTTP server in separate thread
    server_thread = threading.Thread(target=start_webhook_server, daemon=True)
    server_thread.start()

    time.sleep(1)  # Small delay to ensure server is up

    # 1. Create webhooks
    print("[Main] --- 1. Create webhooks")
    if not create_webhook(WEBHOOK_TARGET_URL, "auth.login.failed"):
        print("[Main] Failed to create webhook `auth.login.failed`. Exiting.")
        exit(1)
    
    if not create_webhook(WEBHOOK_TARGET_URL, "auth.login.success"):
        print("[Main] Failed to create webhook `auth.login.success`. Exiting.")
        exit(1)

    # 2. Trigger test event
    print("[Main] --- 2. Trigger test event")
    if not trigger_auth_login_failed_event():
        print("[Main] Failed to trigger test event. Exiting.")
        exit(1)

    # 3. Wait for webhook to be called (max 15 seconds)
    print("[Main] --- 3. Wait for webhook to be called")
    print("[Main] Waiting for webhook to be called...")
    if webhook_called.wait(timeout=15):
        print("[Main] Webhook successfully called!")
        print(f"[Main] Payload: {received_payload}")
    else:
        print("[Main] Webhook was not called within 15 seconds.")
        exit(1)
    
    # 4. Remove webhook auth.login.success
    print("[Main] --- 4. Remove webhook `auth.login.success`")
    print("[Main] Removing webhook for event 'auth.login.success'...")
    if not remove_webhook(WEBHOOK_TARGET_URL, "auth.login.success"):
        print("[Main] Failed to remove webhook `auth.login.success`. Exiting.")
        exit(1)

    ## 5. Re-trigger test event and make sure webhook is still called
    print("[Main] --- 5. Re-trigger test event and check webhook")
    webhook_called.clear()
    received_payload = None
    print("[Main] Re-triggering test event after removing one webhook...")
    if not trigger_auth_login_failed_event():
        print("[Main] Failed to trigger test event. Exiting.")
        exit(1)
    print("[Main] Waiting to see if webhook is called again...")
    if webhook_called.wait(timeout=15):
        print("[Main] Webhook successfully called again!")
        print(f"[Main] Payload: {received_payload}")
    else:
        print("[Main] Webhook was not called within 15 seconds after re-triggering.")
        exit(1)
    
    # 6. Remove webhook auth.login.failed
    print("[Main] --- 6. Remove webhook `auth.login.failed`")
    print("[Main] Removing webhook for event 'auth.login.failed'...")
    if not remove_webhook(WEBHOOK_TARGET_URL, "auth.login.failed"):
        print("[Main] Failed to remove webhook `auth.login.failed`. Exiting.")
        exit(1)
    
    # print(f"[Main] Waiting a few seconds to ensure backend processes webhook removals...")
    # time.sleep(3)

    # 7. Re-trigger test event and make sure webhook is NOT called
    print("[Main] --- 7. Re-trigger test event and check webhook is NOT called")
    webhook_called.clear()
    received_payload = None
    print("[Main] Re-triggering test event after removing webhook...")
    if not trigger_auth_login_failed_event():
        print("[Main] Failed to trigger test event. Exiting.")
        exit(1)

    print("[Main] Waiting to see if webhook is called again (should NOT be called)...")
    if webhook_called.wait(timeout=15):
        print("[Main] ERROR: Webhook was called again after removal!")
        print(f"[Main] Payload: {received_payload}")
        exit(1)
    else:
        print("[Main] Success: Webhook was NOT called after removal.")
    
    print("[Main] All tests completed successfully.")
