#!/usr/bin/env python3
"""Upload the youth football video to Cloudinary (signed multipart). Prints the URL."""
import json, time, hashlib, os, sys, uuid, urllib.request

def load_env(path):
    env = {}
    if os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env

cloud = key = secret = None
ENV = load_env(os.path.join(os.path.dirname(__file__), "..", ".env"))
url = ENV.get("CLOUDINARY_URL", "")
if url.startswith("cloudinary://"):
    creds, cloud = url[len("cloudinary://"):].split("@", 1)
    key, secret = creds.split(":", 1); cloud = cloud.split("/")[0].strip()
cloud  = cloud  or ENV.get("CLOUDINARY_CLOUD_NAME") or ENV.get("CLOUD_NAME")
key    = key    or ENV.get("CLOUDINARY_API_KEY")    or ENV.get("API_KEY")
secret = secret or ENV.get("CLOUDINARY_API_SECRET") or ENV.get("API_SECRET")
if not (cloud and key and secret):
    CFG = json.load(open(os.path.expanduser("~/.cloudinary/config.json")))
    cloud = cloud or CFG.get("cloud_name"); key = key or CFG.get("api_key"); secret = secret or CFG.get("api_secret")
assert cloud and key and secret, "missing cloudinary creds"

SRC = sys.argv[1] if len(sys.argv) > 1 else "assets/youthfootball_V1.mp4"
PUBLIC_ID = sys.argv[2] if len(sys.argv) > 2 else "youth-football"
FOLDER = "bhsfootball26"
ts = str(int(time.time()))
to_sign = f"folder={FOLDER}&overwrite=true&public_id={PUBLIC_ID}&timestamp={ts}"
sig = hashlib.sha1((to_sign + secret).encode()).hexdigest()

fields = {"api_key": key, "timestamp": ts, "public_id": PUBLIC_ID,
          "folder": FOLDER, "overwrite": "true", "signature": sig}
boundary = "----bhs" + uuid.uuid4().hex
CRLF = b"\r\n"
body = b""
for k, v in fields.items():
    body += b"--" + boundary.encode() + CRLF
    body += f'Content-Disposition: form-data; name="{k}"'.encode() + CRLF + CRLF
    body += str(v).encode() + CRLF
with open(SRC, "rb") as f:
    data = f.read()
body += b"--" + boundary.encode() + CRLF
body += f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(SRC)}"'.encode() + CRLF
body += b"Content-Type: video/mp4" + CRLF + CRLF + data + CRLF
body += b"--" + boundary.encode() + b"--" + CRLF

req = urllib.request.Request(
    f"https://api.cloudinary.com/v1_1/{cloud}/video/upload",
    data=body,
    headers={"Content-Type": "multipart/form-data; boundary=" + boundary},
)
with urllib.request.urlopen(req, timeout=600) as r:
    out = json.load(r)
print(out["secure_url"])
print("duration:", out.get("duration"), "w/h:", out.get("width"), out.get("height"))
