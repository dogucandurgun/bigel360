#!/usr/bin/env python3
"""Tell IndexNow (Bing, Yandex, Seznam, Naver...) about the site's URLs. Run by hand after a deploy only.

    python3 scripts/indexnow.py          # dry run: prints what would be sent, sends nothing
    python3 scripts/indexnow.py --send   # POSTs every URL in sitemap.xml to https://api.indexnow.org/indexnow

The key is the name of the <key>.txt file at the site root (its content is the same key); it must already
be live at https://bigel360.com/<key>.txt before --send, so deploy first.
"""
import glob, json, os, re, sys, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "bigel360.com"
ENDPOINT = "https://api.indexnow.org/indexnow"

def find_key():
    for path in glob.glob(os.path.join(ROOT, "*.txt")):
        name = os.path.splitext(os.path.basename(path))[0]
        if re.fullmatch(r"[0-9a-f]{32}", name):
            with open(path, encoding="utf-8") as fh:
                if fh.read().strip() == name:
                    return name
    sys.exit("IndexNow key file (<32 hex>.txt containing the same key) not found at the repo root.")

def sitemap_urls():
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(os.path.join(ROOT, "sitemap.xml"))
    urls = [loc.text.strip() for loc in tree.getroot().findall("s:url/s:loc", ns)]
    return [u for u in urls if u.startswith(f"https://{HOST}/")]

def main():
    send = "--send" in sys.argv[1:]
    key = find_key()
    payload = {"host": HOST, "key": key, "keyLocation": f"https://{HOST}/{key}.txt", "urlList": sitemap_urls()}
    print(f"{len(payload['urlList'])} URLs, keyLocation {payload['keyLocation']}")
    if not send:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        print("\nDry run: nothing sent. Add --send to submit (after the deploy is live).")
        return
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"IndexNow answered HTTP {resp.status} (200/202 = accepted)")
    except urllib.error.HTTPError as e:
        print(f"IndexNow answered HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:500]}")
        sys.exit(1)

if __name__ == "__main__":
    main()
