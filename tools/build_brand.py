"""يولّد ملفات العلامة من صورة الشعار الأصلية (رسم كحلي على خلفية بيضاء).

    python3 tools/build_brand.py [مسار الشعار]

يفصل الرسم عن الخلفية البيضاء، ويعيد تلوينه بكحلي موحّد لإزالة تشوّهات JPEG،
ثم يولّد: الشعار الشفاف بنسختيه (كحلي/أبيض)، والفافيكون، وأيقونات التطبيق.
بطاقة المشاركة تُولَّد بسكربت منفصل: tools/build_social_card.sh
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'assets/img/brand/source/logo-original.jpg')
OUT = os.path.join(ROOT, 'assets/img/brand')
os.makedirs(OUT, exist_ok=True)

NAVY = (9, 31, 78)          # لون الشعار الفعلي (#091F4E)
WHITE = (255, 255, 255)

# ---------- 1. فصل الرسم عن الخلفية ----------
src = Image.open(SRC).convert('RGB')
up = src.resize((src.width * 3, src.height * 3), Image.LANCZOS)   # تكبير قبل القصّ لحواف أنعم
lum = np.asarray(up.convert('L')).astype(np.float32)
ramp = lambda x, lo, hi: np.clip((x - lo) / (hi - lo), 0, 1)
alpha = 1 - ramp(lum, 70, 235)          # أبيض = شفاف، كحلي = معتم
alpha[alpha < 0.03] = 0

ys, xs = np.nonzero(alpha > 0.2)
pad = 6
box = (xs.min() - pad, ys.min() - pad, xs.max() + pad + 1, ys.max() + pad + 1)
alpha = alpha[box[1]:box[3], box[0]:box[2]]

def tinted(color, a=alpha):
    h, w = a.shape
    rgb = np.empty((h, w, 3), np.uint8); rgb[:] = color
    return Image.fromarray(np.dstack([rgb, (a * 255).round().astype(np.uint8)]))

mark = tinted(NAVY)
mark_white = tinted(WHITE)
print('mark', mark.size)

def resize_w(img, w):
    return img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)

# ---------- 2. الشعار الشفاف (الترويسة، التذييل، الصفحات) ----------
for name, img in (('mark', mark), ('mark-white', mark_white)):
    big = resize_w(img, 640)
    big.save(f'{OUT}/{name}.png', optimize=True)
    big.save(f'{OUT}/{name}.webp', quality=92, method=6)
    small = resize_w(img, 160)                 # الترويسة والتذييل (حتى ٨٠ بكسل × ٢)
    small.save(f'{OUT}/{name}-160.png', optimize=True)
    small.save(f'{OUT}/{name}-160.webp', quality=92, method=6)

# ---------- 3. الأيقونات: لوح كحلي والرسم أبيض ----------
def plate(size, radius_ratio=0.0):
    p = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    r = round(size * radius_ratio)
    ImageDraw.Draw(p).rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=NAVY + (255,))
    return p

def icon(size, scale, radius_ratio=0.0, art=mark_white):
    # نرسم بدقة ٤ أضعاف ثم نصغّر، لحواف نظيفة في المقاسات الصغيرة
    S = size * 4
    canvas = plate(S, radius_ratio)
    r = min(S * scale / art.width, S * scale / art.height)
    fg = art.resize((round(art.width * r), round(art.height * r)), Image.LANCZOS)
    canvas.alpha_composite(fg, ((S - fg.width) // 2, (S - fg.height) // 2))
    return canvas.resize((size, size), Image.LANCZOS)

icon(512, 0.80).convert('RGB').save(f'{OUT}/icon-512.png', optimize=True)
icon(192, 0.80).convert('RGB').save(f'{OUT}/icon-192.png', optimize=True)
icon(512, 0.62).convert('RGB').save(f'{OUT}/icon-maskable-512.png', optimize=True)
icon(180, 0.80).convert('RGB').save(os.path.join(ROOT, 'apple-touch-icon.png'), optimize=True)

# فافيكون: البرميل وحرف Z وحدهما (الدائرة والسهم يزدحمان في ١٦ بكسل)،
# على لوح مستدير الزوايا ليبقى واضحًا في الوضعين الفاتح والداكن للمتصفح
def crop_src(x0, y0, x1, y1):
    k = 3   # معامل التكبير أعلاه
    a = alpha[y0 * k - box[1]:y1 * k - box[1], x0 * k - box[0]:x1 * k - box[0]]
    return tinted(WHITE, a)

barrel = crop_src(272, 196, 556, 636)
fav = {s: icon(s, 0.84, 0.22, barrel) for s in (16, 32, 48)}
fav[32].save(f'{OUT}/favicon-32.png', optimize=True)
fav[16].save(f'{OUT}/favicon-16.png', optimize=True)
fav[48].save(os.path.join(ROOT, 'favicon.ico'), format='ICO',
             sizes=[(48, 48), (32, 32), (16, 16)], append_images=[fav[32], fav[16]])

for f in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, f)
    if os.path.isfile(p):
        im = Image.open(p)
        print(f'{f:26s} {str(im.size):12s} {im.mode:5s} {os.path.getsize(p)//1024:5d} KB')
