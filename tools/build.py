"""يبني صفحات الموقع من القالب ومن محتوى الصفحات في tools/pages/.

    python3 tools/build.py

الملفات الناتجة في جذر المستودع هي ما ينشره GitHub Pages مباشرة، فلا خطوة بناء
عند النشر. عدّل المحتوى في tools/pages/ أو البيانات في SITE ثم أعد التشغيل.

داخل ملفات المحتوى:
    {{key}}            قيمة من SITE (مثل {{phone_display}})
    {{barrel:sles}}    برميل التركيز للمادة (sles | labsa | hypo)
    {{icon:phone}}     أيقونة من ICONS
    {{include:name}}   ملف من tools/pages/_partials/
"""
import json, os, re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
PAGES_DIR = os.path.join(ROOT, 'tools', 'pages')

# --------------------------------------------------------------- بيانات الشركة
SITE = {
    'url': 'https://zephora.ly',
    'name': 'زيفورا',
    'name_en': 'Zephora',
    'legal_name': 'شركة زيفورا لاستيراد المواد الخام والمواد الكيميائية',
    'legal_name_en': 'Zephora for the Import of Raw Materials and Chemicals',
    'tagline': 'لاستيراد المواد الخام والكيميائية',
    'phone': '+218942228899',
    'phone_display': '094 222 8899',
    'whatsapp': '218942228899',
    'email': 'info@zephora.ly',
    'city': 'بودزيرة، بنغازي',
    'district': 'بودزيرة',
    'map': 'https://maps.app.goo.gl/4NXWzondp5onHd6x9',
    'lat': 32.1618621,
    'lng': 20.1157743,
    # البيانات القانونية — تظهر في الموقع فور تعبئتها
    'cr': '1825',        # رقم السجل التجاري
    'tax': '1685',       # الرقم الضريبي
    'chamber': '13/875',   # رقم القيد في الغرفة التجارية
    'chamber_name': 'غرفة تجارة طبرق',
}

PRODUCTS = {
    'sles':  {'page': 'sles.html', 'code': 'SLES 70%', 'name': 'سلفات لوريل إيثر الصوديوم', 'pct': 70, 'origin': 'الصين', 'short': '<span class="latin">SLES 70%</span> (تكسابون)'},
    'labsa': {'page': 'labsa.html', 'code': 'LABSA 96%', 'name': 'حمض السلفونيك', 'pct': 96, 'origin': 'السعودية', 'short': '<span class="latin">LABSA 96%</span> (سلفونيك)'},
    'hypo':  {'page': 'sodium-hypochlorite.html', 'code': 'NaOCl 12%', 'name': 'هيبوكلوريت الصوديوم', 'pct': 12, 'origin': 'مصر', 'short': 'هيبوكلوريت الصوديوم <span class="latin">12%</span>'},
}

# ---------------------------------------------------------------- الصفحات
# nav: الرابط المميّز في القائمة | crumbs: مسار التنقّل لبيانات Google
PAGES = [
    dict(src='home', out='index.html', nav='home', schema='org',
         title='زيفورا لاستيراد المواد الخام | SLES وLABSA وهيبوكلوريت الصوديوم في ليبيا',
         desc='شركة زيفورا في بنغازي تستورد المواد الخام لصناعة المنظّفات ومعالجة المياه: SLES 70% من الصين، وLABSA 96% من السعودية، وهيبوكلوريت الصوديوم 12% من مصر.'),
    dict(src='products', out='products.html', nav='products',
         title='المنتجات: SLES وLABSA وهيبوكلوريت الصوديوم | زيفورا',
         desc='تعرّف على المواد الثلاث التي تستوردها زيفورا: ما هي، وأين تُستخدم، ومنشأ كل منها وتركيزها، مع إجابات لأكثر الأسئلة شيوعًا.',
         crumbs=[('المنتجات', 'products.html')]),
    dict(src='sles', out='sles.html', nav='products',
         title='SLES 70% (تكسابون) — سلفات لوريل إيثر الصوديوم | زيفورا',
         desc='SLES 70% منشأ الصين: المادة الأساسية للرغوة في الشامبو والصابون السائل وسائل الجلي. المواصفات وطرق الاستخدام والتخزين، واطلب السعر من زيفورا في بنغازي.',
         crumbs=[('المنتجات', 'products.html'), ('SLES 70%', 'sles.html')]),
    dict(src='labsa', out='labsa.html', nav='products',
         title='LABSA 96% (حمض السلفونيك) — منشأ السعودية | زيفورا',
         desc='LABSA 96% منشأ السعودية: المادة المنظّفة الأساسية في مسحوق الغسيل وسائل الجلي ومنظّفات الأرضيات. المواصفات والاستخدامات والتخزين الآمن.',
         crumbs=[('المنتجات', 'products.html'), ('LABSA 96%', 'labsa.html')]),
    dict(src='hypo', out='sodium-hypochlorite.html', nav='products',
         title='هيبوكلوريت الصوديوم 12% (الكلور السائل) | زيفورا',
         desc='هيبوكلوريت الصوديوم 12% منشأ مصر لمعالجة المياه والتعقيم وصناعة الكلور المنزلي. المواصفات وطريقة التخفيف وتعليمات السلامة.',
         crumbs=[('المنتجات', 'products.html'), ('هيبوكلوريت الصوديوم 12%', 'sodium-hypochlorite.html')]),
    dict(src='about', out='about.html', nav='about', schema='org',
         title='عن الشركة | زيفورا لاستيراد المواد الخام والكيميائية',
         desc='زيفورا شركة ليبية في بنغازي تستورد المواد الخام لصناعة المنظّفات والتعقيم. تعرّف علينا وعلى منشأ موادنا وبيانات الشركة الرسمية.',
         crumbs=[('عن الشركة', 'about.html')]),
    dict(src='contact', out='contact.html', nav='contact', schema='org',
         title='تواصل معنا واطلب عرض سعر | زيفورا',
         desc='اطلب سعر SLES أو LABSA أو هيبوكلوريت الصوديوم من زيفورا في بنغازي. اتصل على 0942228899 أو راسلنا على info@zephora.ly.',
         crumbs=[('تواصل معنا', 'contact.html')]),
    dict(src='privacy', out='privacy.html', nav=None,
         title='سياسة الخصوصية | زيفورا',
         desc='كيف نتعامل مع بياناتك عند تصفّح موقع زيفورا أو التواصل معنا.',
         crumbs=[('الخصوصية', 'privacy.html')]),
    dict(src='terms', out='terms.html', nav=None,
         title='شروط الاستخدام | زيفورا',
         desc='شروط استخدام موقع زيفورا لاستيراد المواد الخام والمواد الكيميائية.',
         crumbs=[('شروط الاستخدام', 'terms.html')]),
    dict(src='thanks', out='thanks.html', nav=None, noindex=True,
         title='وصلتنا رسالتك | زيفورا', desc='شكرًا لتواصلك مع زيفورا.'),
    dict(src='404', out='404.html', nav=None, noindex=True, absolute=True,
         title='الصفحة غير موجودة | زيفورا', desc='الصفحة التي تبحث عنها غير موجودة.'),
]

# ---------------------------------------------------------------- الأيقونات
_I = {
    'phone': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    'chat': '<path d="M3 20l1.3-3.9A8.5 8.5 0 1 1 7.9 19.7z"/><path d="M9 10h.01M12 10h.01M15 10h.01" stroke-width="2.4"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    'pin': '<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'close': '<path d="M6 6l12 12M18 6 6 18"/>',
    'alert': '<path d="M12 3 2 20h20L12 3z"/><path d="M12 10v4M12 17h.01"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    'doc': '<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    'handshake': '<path d="M8 12h.01M3 11l4-4 3 1 3-2 4 1 4 4-7 7-3-3"/><path d="m7 7 5 5M14 12l3 3M11 15l2 2"/>',
    'stamp': '<path d="M9 3h6l-1 7h4v4H6v-4h4z"/><path d="M5 18h14v3H5z"/>',
    'arrow': '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
}

# شعار واتساب مصمت (لا يُرسم بخط مثل بقية الأيقونات)
_WHATSAPP = 'M12.04 2.25c-5.4 0-9.79 4.39-9.79 9.79 0 1.72.45 3.4 1.31 4.88L2.3 21.75l4.96-1.3a9.75 9.75 0 0 0 4.78 1.25h.01c5.4 0 9.79-4.39 9.79-9.79s-4.4-9.66-9.8-9.66zm0 1.75a8.04 8.04 0 0 1 8.04 7.95 8.04 8.04 0 0 1-8.03 8.04h-.01a8.1 8.1 0 0 1-4.12-1.13l-.3-.17-3.06.8.82-2.98-.19-.31a8.03 8.03 0 0 1 6.85-12.2zm-3.6 4.03c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1s.9 2.44 1.03 2.6c.13.18 1.75 2.79 4.28 3.8 2.1.83 2.53.67 2.99.63.46-.04 1.48-.6 1.69-1.19.21-.58.21-1.08.15-1.19-.06-.1-.23-.17-.48-.29-.25-.13-1.48-.73-1.71-.81-.23-.09-.4-.13-.56.12-.17.25-.65.81-.79.98-.15.17-.29.19-.54.06-.25-.12-1.06-.39-2.01-1.24-.74-.66-1.24-1.48-1.39-1.73-.14-.25-.01-.38.11-.5.11-.11.25-.29.38-.44.12-.15.16-.25.25-.42.08-.17.04-.31-.02-.44-.06-.12-.55-1.35-.77-1.85-.2-.48-.4-.42-.55-.42h-.24z'

def icon(name, cls=''):
    c = f' class="{cls}"' if cls else ''
    if name == 'whatsapp':
        return f'<svg{c} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="{_WHATSAPP}"/></svg>'
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>')

# ------------------------------------------------------- برميل التركيز (SVG)
_barrel_n = [0]

def barrel(key, decorative=True):
    """برميل على شكل برميل الشعار؛ ارتفاع السائل فيه = تركيز المادة."""
    p = PRODUCTS[key]
    _barrel_n[0] += 1
    cid = f'clip-{key}-{_barrel_n[0]}'
    top, bottom = 24.0, 158.0
    y = round(bottom - (bottom - top) * p['pct'] / 100, 1)
    body = 'M12 24V146C12 154 34 160 60 160S108 154 108 146V24'
    aria = ('aria-hidden="true"' if decorative else
            f'role="img" aria-label="برميل ممتلئ بنسبة {p["pct"]}% يمثّل تركيز المادة"')
    return (
        f'<svg class="barrel barrel--{key}" viewBox="0 0 120 170" {aria}>'
        f'<defs><clipPath id="{cid}"><path d="{body}Z"/></clipPath></defs>'
        f'<path class="barrel__shell" d="{body}Z"/>'
        f'<g clip-path="url(#{cid})"><g class="barrel__fill">'
        f'<rect class="barrel__liquid" x="0" y="{y}" width="120" height="{170 - y}"/>'
        f'<ellipse class="barrel__surface" cx="60" cy="{y}" rx="48" ry="7"/>'
        f'</g></g>'
        f'<path class="barrel__rib" d="M12 68C30 76 90 76 108 68M12 112C30 120 90 120 108 112"/>'
        f'<path class="barrel__line" d="{body}"/>'
        f'<ellipse class="barrel__top" cx="60" cy="24" rx="48" ry="10"/>'
        f'<ellipse class="barrel__bung" cx="80" cy="22" rx="7" ry="2.6"/>'
        f'</svg>')

# ---------------------------------------------------------------- القالب
NAV = [('products', 'products.html', 'المنتجات'),
       ('about', 'about.html', 'عن الشركة'),
       ('contact', 'contact.html', 'تواصل معنا')]

def head(page, base):
    url = SITE['url'] + '/' + ('' if page['out'] == 'index.html' else page['out'])
    robots = '<meta name="robots" content="noindex">' if page.get('noindex') else \
             f'<link rel="canonical" href="{url}">'
    ld = []
    if page.get('schema') == 'org':
        org = {
            '@context': 'https://schema.org',
            '@type': 'LocalBusiness',
            '@id': SITE['url'] + '/#company',
            'name': SITE['legal_name'],
            'alternateName': [SITE['name'], SITE['name_en'], SITE['legal_name_en']],
            'description': PAGES[0]['desc'],
            'url': SITE['url'] + '/',
            'logo': SITE['url'] + '/assets/img/brand/icon-512.png',
            'image': SITE['url'] + '/assets/img/brand/social-card.jpg',
            'telephone': SITE['phone'],
            'email': SITE['email'],
            'address': {'@type': 'PostalAddress', 'streetAddress': SITE['district'], 'addressLocality': 'بنغازي', 'addressCountry': 'LY'},
            'geo': {'@type': 'GeoCoordinates', 'latitude': SITE['lat'], 'longitude': SITE['lng']},
            'hasMap': SITE['map'],
            'areaServed': {'@type': 'Country', 'name': 'Libya'},
            'knowsAbout': ['SLES 70%', 'LABSA 96%', 'Sodium Hypochlorite 12%'],
        }
        if SITE['tax']:
            org['taxID'] = SITE['tax']
        ld.append(org)
    if page.get('crumbs'):
        items = [('الرئيسية', '')] + page['crumbs']
        ld.append({
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n,
                                 'item': SITE['url'] + '/' + h} for i, (n, h) in enumerate(items)]})
    ld_html = ''.join('\n<script type="application/ld+json">\n' +
                      json.dumps(x, ensure_ascii=False, indent=2) + '\n</script>' for x in ld)
    og_url = url if not page.get('noindex') else SITE['url'] + '/'
    return f'''<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page['title']}</title>
<meta name="description" content="{page['desc']}">
{robots}
<meta name="theme-color" content="#f5f4ef">
<link rel="icon" href="{base}favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="{base}assets/img/brand/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="{base}assets/img/brand/icon-192.png">
<link rel="apple-touch-icon" href="{base}apple-touch-icon.png">
<link rel="manifest" href="{base}site.webmanifest">
<link rel="preload" href="{base}assets/fonts/gess-two-medium.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{base}assets/fonts/gess-two-bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}assets/css/main.css">
<meta property="og:type" content="website">
<meta property="og:locale" content="ar_LY">
<meta property="og:site_name" content="{SITE['name']} — {SITE['name_en']}">
<meta property="og:title" content="{page['title']}">
<meta property="og:description" content="{page['desc']}">
<meta property="og:url" content="{og_url}">
<meta property="og:image" content="{SITE['url']}/assets/img/brand/social-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script>document.documentElement.classList.add("js")</script>{ld_html}
</head>'''

def header(page, base):
    def links(cls=''):
        out = []
        for key, href, label in NAV:
            cur = ' aria-current="page"' if page['nav'] == key else ''
            out.append(f'<a href="{base}{href}"{cur}>{label}</a>')
        return '\n        '.join(out)
    home_cur = ' aria-current="page"' if page['nav'] == 'home' else ''
    return f'''<a class="skip" href="#main">تخطَّ إلى المحتوى</a>
<header class="header" data-header>
  <div class="wrap header__bar">
    <a class="brand" href="{base or './'}" aria-label="{SITE['name']} — الصفحة الرئيسية">
      <picture><source srcset="{base}assets/img/brand/mark-160.webp" type="image/webp"><img src="{base}assets/img/brand/mark-160.png" width="160" height="148" alt=""></picture>
      <span class="brand__text"><span class="brand__name">{SITE['name']}</span><span class="brand__tag">{SITE['tagline']}</span></span>
    </a>
    <nav class="nav" aria-label="القائمة الرئيسية">
        {links()}
    </nav>
    <a class="btn btn--sm header__cta" href="{base}contact.html">اطلب عرض سعر</a>
    <details class="menu">
      <summary aria-label="القائمة">{icon('menu', 'i-open')}{icon('close', 'i-close')}</summary>
      <nav class="menu__panel" aria-label="قائمة الجوال">
        <a href="{base or './'}"{home_cur}>الرئيسية</a>
        {links()}
        <a class="btn" href="tel:{SITE['phone']}">{icon('phone')}<span>اتصل: <span class="latin">{SITE['phone_display']}</span></span></a>
      </nav>
    </details>
  </div>
</header>'''

def footer(base):
    legal = [SITE['legal_name']]
    for key, label in (('cr', 'السجل التجاري'), ('tax', 'الرقم الضريبي'), ('chamber', SITE['chamber_name'])):
        if SITE[key]:
            legal.append(f'{label}: <span class="latin">{SITE[key]}</span>')
    legal_html = ''.join(f'<span>{x}</span>' for x in legal)
    prods = '\n          '.join(f'<li><a href="{base}{p["page"]}">{p["short"]}</a></li>' for p in PRODUCTS.values())
    return f'''<footer class="footer">
  <div class="wrap footer__top">
    <div>
      <div class="footer__brand">
        <picture><source srcset="{base}assets/img/brand/mark-white-160.webp" type="image/webp"><img src="{base}assets/img/brand/mark-white-160.png" width="160" height="148" alt="" loading="lazy"></picture>
        <div><b>{SITE['name']}</b><span>{SITE['tagline']}</span></div>
      </div>
      <p class="footer__about">نستورد المواد الخام لصناعة المنظّفات ومعالجة المياه، ونوفّرها للمصانع والموزّعين من بنغازي.</p>
    </div>
    <div>
      <h2>المنتجات</h2>
      <ul role="list">
          {prods}
      </ul>
    </div>
    <div>
      <h2>الشركة</h2>
      <ul role="list">
        <li><a href="{base}about.html">عن الشركة</a></li>
        <li><a href="{base}products.html#faq">أسئلة شائعة</a></li>
        <li><a href="{base}contact.html">اطلب عرض سعر</a></li>
      </ul>
    </div>
    <div>
      <h2>تواصل</h2>
      <ul role="list" class="footer__contact">
        <li>{icon('phone')}<a href="tel:{SITE['phone']}" class="latin">{SITE['phone_display']}</a></li>
        <li>{icon('mail')}<a href="mailto:{SITE['email']}" class="latin">{SITE['email']}</a></li>
        <li>{icon('pin')}<a href="{SITE['map']}" target="_blank" rel="noopener">{SITE['city']}</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer__legal">{legal_html}</div>
  <div class="wrap footer__bottom">
    <p>© <span data-year>2026</span> {SITE['name']} — جميع الحقوق محفوظة.</p>
    <p class="footer__dev">تصميم وتطوير <a href="https://yosef.ly" target="_blank" rel="noopener">ديـوان التقنيـة الليبـي</a></p>
    <nav aria-label="روابط ختامية"><a href="{base}privacy.html">الخصوصية</a><a href="{base}terms.html">الشروط</a></nav>
  </div>
</footer>'''

def crumbs_html(page, base):
    if not page.get('crumbs'):
        return ''
    items = [('الرئيسية', base or './')] + [(n, base + h) for n, h in page['crumbs']]
    lis = []
    for i, (n, h) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li aria-current="page">{n}</li>')
        else:
            lis.append(f'<li><a href="{h}">{n}</a></li>')
    return '<nav aria-label="مسار التنقّل"><ol class="crumbs" role="list">' + ''.join(lis) + '</ol></nav>'

# ------------------------------------------------------------ معالجة المحتوى
def render(text, page, base):
    def sub(m):
        kind, _, arg = m.group(1).partition(':')
        if kind == 'barrel':
            name, _, flag = arg.partition(':')
            return barrel(name, decorative=(flag != 'label'))
        if kind == 'icon':
            return icon(arg)
        if kind == 'include':
            with open(os.path.join(PAGES_DIR, '_partials', arg + '.html'), encoding='utf-8') as f:
                return render(f.read(), page, base)
        if kind == 'crumbs':
            return crumbs_html(page, base)
        if kind == 'base':
            return base
        if kind == 'registry':
            return registry_rows()
        if kind in SITE:
            return str(SITE[kind])
        raise KeyError(f'وسم غير معروف: {m.group(0)}')
    return re.sub(r'\{\{([\w:-]+)\}\}', sub, text)

def isolate_numbers(html):
    """يعزل النسب المئوية داخل النص العربي حتى لا تنقلب إلى %12 بفعل اتجاه السطر."""
    parts = re.split(r'(<[^>]+>)', html)
    pat = re.compile(r'(?<![\w.])(\d+(?:\.\d+)?%)')
    for i in range(0, len(parts), 2):          # الأجزاء الزوجية نص، الفردية وسوم
        parts[i] = pat.sub(r'<bdi dir="ltr">\1</bdi>', parts[i])
    return ''.join(parts)

def registry_rows():
    rows = [('الاسم القانوني', SITE['legal_name'], False)]
    for key, label in (('cr', 'السجل التجاري'), ('tax', 'الرقم الضريبي'), ('chamber', f'رقم القيد — {SITE["chamber_name"]}')):
        rows.append((label, SITE[key], True))
    rows.append(('المقر', SITE['city'], False))
    out = []
    for label, val, mono in rows:
        if val:
            cls = ' class="mono"' if mono else ''
            out.append(f'<div><dt>{label}</dt><dd{cls}>{val}</dd></div>')
        else:
            out.append(f'<div><dt>{label}</dt><dd class="pending">يُضاف قريبًا</dd></div>')
    return '\n          '.join(out)

def build():
    for page in PAGES:
        base = '/' if page.get('absolute') else ''
        _barrel_n[0] = 0
        with open(os.path.join(PAGES_DIR, page['src'] + '.html'), encoding='utf-8') as f:
            body = isolate_numbers(render(f.read(), page, base))
        html = f'''<!doctype html>
<html lang="ar" dir="rtl">
{head(page, base)}
<body>
{header(page, base)}

<main id="main">
{body.strip()}
</main>

{footer(base)}
<script src="{base}assets/js/main.js" defer></script>
</body>
</html>
'''
        with open(os.path.join(ROOT, page['out']), 'w', encoding='utf-8') as f:
            f.write(html)
        print('✓', page['out'])

    # خريطة الموقع
    urls = [p for p in PAGES if not p.get('noindex')]
    pri = {'index.html': '1.0', 'products.html': '0.9', 'sles.html': '0.9', 'labsa.html': '0.9',
           'sodium-hypochlorite.html': '0.9', 'contact.html': '0.8', 'about.html': '0.7'}
    entries = '\n'.join(
        f'  <url>\n    <loc>{SITE["url"]}/{"" if p["out"] == "index.html" else p["out"]}</loc>\n'
        f'    <priority>{pri.get(p["out"], "0.3")}</priority>\n  </url>' for p in urls)
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + entries + '\n</urlset>\n')
    print('✓ sitemap.xml')

if __name__ == '__main__':
    build()
