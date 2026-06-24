#!/usr/bin/env python3
"""Upload the enhanced scoreboard photo to Cloudinary. Prints only the URL."""
import json, time, hashlib, base64, urllib.parse, urllib.request, os, glob

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

import sys
src = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", "generated_imgs", "edited-*nd4a8z.png")))[-1]
PUBLIC_ID = sys.argv[2] if len(sys.argv) > 2 else "scoreboard-gameday"
with open(src, "rb") as f:
    data_uri = "data:image/png;base64," + base64.b64encode(f.read()).decode()

FOLDER = "bhsfootball26"
ts = str(int(time.time()))
to_sign = f"folder={FOLDER}&overwrite=true&public_id={PUBLIC_ID}&timestamp={ts}"
sig = hashlib.sha1((to_sign + secret).encode()).hexdigest()
body = urllib.parse.urlencode({
    "file": data_uri, "api_key": key, "timestamp": ts,
    "public_id": PUBLIC_ID, "folder": FOLDER, "overwrite": "true", "signature": sig,
}).encode()
req = urllib.request.Request(f"https://api.cloudinary.com/v1_1/{cloud}/image/upload", data=body)
with urllib.request.urlopen(req) as r:
    print(json.load(r)["secure_url"])
