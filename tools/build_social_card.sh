#!/bin/sh
# يصوّر tools/social-card.html إلى بطاقتي المشاركة (العربية والإنجليزية) عبر Chrome.
# يحتاج خادمًا محليًا لتحميل الخطوط:  python3 -m http.server 8765
set -e
cd "$(dirname "$0")/.."
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP="$(mktemp -d)"
shoot() {  # الاستعلام  اسم-الملف
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --window-size=1200,630 --virtual-time-budget=3000 \
    --screenshot="$TMP/card.png" "http://127.0.0.1:8765/tools/social-card.html$1" >/dev/null 2>&1
  python3 -c "from PIL import Image; Image.open('$TMP/card.png').convert('RGB').save('assets/img/brand/$2', quality=88, optimize=True, progressive=True)"
  echo "✓ assets/img/brand/$2"
}
shoot "" social-card.jpg
shoot "?lang=en" social-card-en.jpg
rm -rf "$TMP"
