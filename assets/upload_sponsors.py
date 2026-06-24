#!/usr/bin/env python3
"""One-off: upload Batavia football sponsor logos to Cloudinary. Prints only resulting URLs."""
import json, time, hashlib, urllib.parse, urllib.request, os

def load_env(path):
    env = {}
    if os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env

cloud = key = secret = None
ENV = load_env(os.path.join(os.path.dirname(__file__), "..", ".env"))
# Form 1: CLOUDINARY_URL=cloudinary://<key>:<secret>@<cloud>
url = ENV.get("CLOUDINARY_URL", "")
if url.startswith("cloudinary://"):
    rest = url[len("cloudinary://"):]
    creds, cloud = rest.split("@", 1)
    key, secret = creds.split(":", 1)
    cloud = cloud.split("/")[0].strip()
# Form 2: separate vars
cloud  = cloud  or ENV.get("CLOUDINARY_CLOUD_NAME") or ENV.get("CLOUD_NAME")
key    = key    or ENV.get("CLOUDINARY_API_KEY")    or ENV.get("API_KEY")
secret = secret or ENV.get("CLOUDINARY_API_SECRET") or ENV.get("API_SECRET")
# Fallback: global cloudinary config
if not (cloud and key and secret):
    CFG = json.load(open(os.path.expanduser("~/.cloudinary/config.json")))
    cloud  = cloud  or CFG.get("cloud_name") or CFG.get("cloudName")
    key    = key    or CFG.get("api_key")    or CFG.get("apiKey")
    secret = secret or CFG.get("api_secret") or CFG.get("apiSecret")
assert cloud and key and secret, "missing cloudinary creds (project .env or ~/.cloudinary/config.json)"

FOLDER = "bhsfootball26/sponsors"
SPONSORS = {
 "accurate-door":   "https://images.squarespace-cdn.com/content/v1/6819d6e19e62f2527432ff93/dc31a03a-28e3-4b62-896e-616768ac79d3/football-sponsors-accurate-door.png",
 "bulldog-plumbing":"https://images.squarespace-cdn.com/content/v1/6819d6e19e62f2527432ff93/4099b776-bfc5-479b-bf9d-53361b55b40d/football-sponsors-bulldog-plumbing.png",
 "pal-joeys":       "https://images.squarespace-cdn.com/content/v1/6819d6e19e62f2527432ff93/e8c8cdf0-8720-492c-b01d-d09652a1b609/football-sponsors-paljoeys.png",
 "k-hollis-jewelers":"https://images.squarespace-cdn.com/content/v1/6819d6e19e62f2527432ff93/8f9a160a-1c10-47d7-9967-9859a8ebbb32/football-sponsors-khollis-jewlers.png",
 "artlow-systems":  "https://images.squarespace-cdn.com/content/v1/6819d6e19e62f2527432ff93/54feb20c-cb4b-4cc2-a8c0-ff6c6788af48/football-sponsors-artlow.png",
 "docs-hvac":       "https://images.squarespace-cdn.com/content/v1/6819d6e19e62f2527432ff93/6607fc19-42b4-4c70-83b3-3a82110a15ef/football-sponsors-docs-hvac.png",
 "north-star-jcb":  "https://images.squarespace-cdn.com/content/v1/6819d6e19e62f2527432ff93/6b956468-16f6-4d55-89aa-f0d561c8184c/football-sponsors-jcb-north-star.png",
}

def upload(public_id, remote_url):
    ts = str(int(time.time()))
    to_sign = f"folder={FOLDER}&overwrite=true&public_id={public_id}&timestamp={ts}"
    sig = hashlib.sha1((to_sign + secret).encode()).hexdigest()
    data = urllib.parse.urlencode({
        "file": remote_url, "api_key": key, "timestamp": ts,
        "public_id": public_id, "folder": FOLDER, "overwrite": "true",
        "signature": sig,
    }).encode()
    url = f"https://api.cloudinary.com/v1_1/{cloud}/image/upload"
    with urllib.request.urlopen(urllib.request.Request(url, data=data)) as r:
        return json.load(r)["secure_url"]

for slug, src in SPONSORS.items():
    try:
        print(f"{slug} {upload(slug, src)}")
    except Exception as e:
        print(f"{slug} ERROR {e}")
