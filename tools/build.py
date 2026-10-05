"""يبني صفحات الموقع (العربية في الجذر، والإنجليزية في en/) من القالب ومحتوى tools/pages/.

    python3 tools/build.py

الملفات الناتجة هي ما ينشره GitHub Pages مباشرة، فلا خطوة بناء عند النشر.
عدّل المحتوى في tools/pages/ (العربية) أو tools/pages/en/ (الإنجليزية)، أو البيانات
في SITE والنصوص في UI ثم أعد التشغيل.

داخل ملفات المحتوى:
    {{key}}            قيمة من SITE بلغة الصفحة (مثل {{phone_display}})
    {{barrel:sles}}    برميل التركيز للمادة (sles | labsa | hypo)
    {{icon:phone}}     أيقونة من _I
    {{include:name}}   ملف من tools/pages/_partials/ (أو en/_partials/)
    {{base}}           بادئة روابط الصفحات     {{root}}  بادئة مسار الجذر للملفات الثابتة
"""
import json, os, re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
PAGES_DIR = os.path.join(ROOT, 'tools', 'pages')

LANGS = {
    'ar': dict(dir='rtl', prefix='', locale='ar_LY', card='social-card.jpg'),
    'en': dict(dir='ltr', prefix='en/', locale='en_US', card='social-card-en.jpg'),
}

# --------------------------------------------------------------- بيانات الشركة
SITE = {
    'url': 'https://zephora.ly',
    'name_en': 'Zephora',
    'legal_name_ar': 'شركة زيفورا لاستيراد المواد الخام والمواد الكيميائية',
    'legal_name_en': 'Zephora for the Import of Raw Materials and Chemicals',
    'phone': '+218942228899',
    'phone_display': '094 222 8899',
    'whatsapp': '218942228899',
    'email': 'info@zephora.ly',
    'map': 'https://maps.app.goo.gl/4NXWzondp5onHd6x9',
    'lat': 32.1618621,
    'lng': 20.1157743,
    # البيانات القانونية — تظهر في الموقع فور تعبئتها
    'cr': '1825',          # رقم السجل التجاري
    'tax': '1685',         # الرقم الضريبي
    'chamber': '13/875',   # رقم القيد في الغرفة التجارية
    # رمز التحقق من Google Search Console (طريقة وسم HTML) — اتركه فارغًا إن وثّقت النطاق عبر DNS
    'gsc': '',
}

# ما يختلف باختلاف اللغة
SITE_L = {
    'ar': dict(
        name='زيفورا', legal_name='شركة زيفورا لاستيراد المواد الخام والمواد الكيميائية',
        tagline='لاستيراد المواد الخام والكيميائية', city='بودزيرة، بنغازي', district='بودزيرة',
        locality='بنغازي', chamber_name='غرفة تجارة طبرق'),
    'en': dict(
        name='Zephora', legal_name='Zephora for the Import of Raw Materials and Chemicals',
        tagline='Raw materials & chemicals import', city='Boudzira, Benghazi', district='Boudzira',
        locality='Benghazi', chamber_name='Tobruk Chamber of Commerce'),
}

def S(lang):
    return {**SITE, **SITE_L[lang]}

PRODUCTS = {
    'sles': {'page': 'sles.html', 'pct': 70,
             'short': {'ar': '<span class="latin">SLES 70%</span> (تكسابون)', 'en': '<span class="latin">SLES 70%</span> (Texapon)'}},
    'labsa': {'page': 'labsa.html', 'pct': 96,
              'short': {'ar': '<span class="latin">LABSA 96%</span> (سلفونيك)', 'en': '<span class="latin">LABSA 96%</span> (sulfonic acid)'}},
    'hypo': {'page': 'sodium-hypochlorite.html', 'pct': 12,
             'short': {'ar': 'هيبوكلوريت الصوديوم <span class="latin">12%</span>', 'en': 'Sodium hypochlorite <span class="latin">12%</span>'}},
}

# ----------------------------------------------------- نصوص الواجهة المشتركة
UI = {
    'ar': dict(
        skip='تخطَّ إلى المحتوى', home='الرئيسية', nav_aria='القائمة الرئيسية', menu='القائمة',
        menu_aria='قائمة الجوال', quote='اطلب عرض سعر', call='اتصل:',
        nav={'products': 'المنتجات', 'about': 'عن الشركة', 'contact': 'تواصل معنا'},
        footer_about='نستورد المواد الخام لصناعة المنظّفات ومعالجة المياه، ونوفّرها للمصانع والموزّعين من بنغازي.',
        f_products='المنتجات', f_company='الشركة', f_about='عن الشركة', f_faq='أسئلة شائعة', f_contact='تواصل',
        rights='جميع الحقوق محفوظة.', dev='تصميم وتطوير', dev_name='ديـوان التقنيـة الليبـي',
        privacy='الخصوصية', terms='الشروط', legal_nav='روابط ختامية', crumbs_aria='مسار التنقّل',
        cr='السجل التجاري', tax='الرقم الضريبي', reg_chamber='رقم القيد — {chamber_name}',
        reg_name='الاسم القانوني', reg_hq='المقر', pending='يُضاف قريبًا',
        barrel='برميل ممتلئ بنسبة {pct}% يمثّل تركيز المادة',
        switch_label='English', switch_aria='Switch to English',
        brand_aria='{name} — الصفحة الرئيسية'),
    'en': dict(
        skip='Skip to content', home='Home', nav_aria='Main menu', menu='Menu',
        menu_aria='Mobile menu', quote='Request a quote', call='Call:',
        nav={'products': 'Products', 'about': 'About', 'contact': 'Contact'},
        footer_about='We import raw materials for detergent manufacturing and water treatment, and supply factories and distributors from Benghazi.',
        f_products='Products', f_company='Company', f_about='About us', f_faq='FAQ', f_contact='Contact',
        rights='All rights reserved.', dev='Design and development by', dev_name='Libyan Tech Diwan',
        privacy='Privacy', terms='Terms', legal_nav='Legal links', crumbs_aria='Breadcrumb',
        cr='Commercial registry', tax='Tax number', reg_chamber='Chamber membership — {chamber_name}',
        reg_name='Legal name', reg_hq='Location', pending='Coming soon',
        barrel='Barrel filled to {pct}%, showing the concentration of the product',
        switch_label='العربية', switch_aria='التبديل إلى العربية',
        brand_aria='{name} — Home'),
}

# ---------------------------------------------------------------- الصفحات
# nav: الرابط المميّز في القائمة | parent: صفحة الأب لمسار التنقّل | crumb: اسم الصفحة فيه
def L(ar, en):
    return {'ar': ar, 'en': en}

PAGES = [
    dict(src='home', out='index.html', nav='home', schema='org', website=True,
         title=L('زيفورا لاستيراد المواد الخام | SLES وLABSA وهيبوكلوريت الصوديوم في ليبيا',
                 'Zephora | SLES, LABSA & Sodium Hypochlorite Supplier in Libya'),
         desc=L('شركة زيفورا في بنغازي تستورد المواد الخام لصناعة المنظّفات ومعالجة المياه: SLES 70% من الصين، وLABSA 96% من السعودية، وهيبوكلوريت الصوديوم 12% من مصر.',
                'Zephora imports raw materials for detergents and water treatment in Benghazi, Libya: SLES 70% from China, LABSA 96% from Saudi Arabia, and sodium hypochlorite 12% from Egypt.')),
    dict(src='products', out='products.html', nav='products', crumb=L('المنتجات', 'Products'),
         title=L('المنتجات: SLES وLABSA وهيبوكلوريت الصوديوم | زيفورا',
                 'Products: SLES, LABSA & Sodium Hypochlorite | Zephora'),
         desc=L('تعرّف على المواد الثلاث التي تستوردها زيفورا: ما هي، وأين تُستخدم، ومنشأ كل منها وتركيزها، مع إجابات لأكثر الأسئلة شيوعًا.',
                'The three materials Zephora imports: what each one is, where it is used, its origin and concentration, with answers to common questions.')),
    dict(src='sles', out='sles.html', nav='products', parent='products', crumb=L('SLES 70%', 'SLES 70%'),
         title=L('SLES 70% (تكسابون) — سلفات لوريل إيثر الصوديوم | زيفورا',
                 'SLES 70% (Texapon) — Sodium Lauryl Ether Sulfate | Zephora'),
         desc=L('SLES 70% منشأ الصين: المادة الأساسية للرغوة في الشامبو والصابون السائل وسائل الجلي. المواصفات وطرق الاستخدام والتخزين، واطلب السعر من زيفورا في بنغازي.',
                'SLES 70% from China: the foaming base of shampoo, liquid soap and dishwashing liquid. Specifications, uses and storage. Request a price from Zephora in Benghazi.')),
    dict(src='labsa', out='labsa.html', nav='products', parent='products', crumb=L('LABSA 96%', 'LABSA 96%'),
         title=L('LABSA 96% (حمض السلفونيك) — منشأ السعودية | زيفورا',
                 'LABSA 96% (Sulfonic Acid) — Origin Saudi Arabia | Zephora'),
         desc=L('LABSA 96% منشأ السعودية: المادة المنظّفة الأساسية في مسحوق الغسيل وسائل الجلي ومنظّفات الأرضيات. المواصفات والاستخدامات والتخزين الآمن.',
                'LABSA 96% from Saudi Arabia: the main cleaning agent in washing powder, dishwashing liquid and floor cleaners. Specifications, uses and safe storage.')),
    dict(src='hypo', out='sodium-hypochlorite.html', nav='products', parent='products',
         crumb=L('هيبوكلوريت الصوديوم 12%', 'Sodium Hypochlorite 12%'),
         title=L('هيبوكلوريت الصوديوم 12% (الكلور السائل) | زيفورا',
                 'Sodium Hypochlorite 12% (Liquid Chlorine) | Zephora'),
         desc=L('هيبوكلوريت الصوديوم 12% منشأ مصر لمعالجة المياه والتعقيم وصناعة الكلور المنزلي. المواصفات وطريقة التخفيف وتعليمات السلامة.',
                'Sodium hypochlorite 12% from Egypt for water treatment, disinfection and household bleach production. Specifications, dilution and safety instructions.')),
    dict(src='about', out='about.html', nav='about', schema='org', crumb=L('عن الشركة', 'About'),
         title=L('عن الشركة | زيفورا لاستيراد المواد الخام والكيميائية',
                 'About Us | Zephora Raw Materials & Chemicals Import'),
         desc=L('زيفورا شركة ليبية في بنغازي تستورد المواد الخام لصناعة المنظّفات والتعقيم. تعرّف علينا وعلى منشأ موادنا وبيانات الشركة الرسمية.',
                'Zephora is a Libyan company in Benghazi importing raw materials for detergents and disinfection. Learn about us, where our materials come from, and our official company details.')),
    dict(src='contact', out='contact.html', nav='contact', schema='org', crumb=L('تواصل معنا', 'Contact'),
         title=L('تواصل معنا واطلب عرض سعر | زيفورا', 'Contact Us & Request a Quote | Zephora'),
         desc=L('اطلب سعر SLES أو LABSA أو هيبوكلوريت الصوديوم من زيفورا في بنغازي. اتصل على 0942228899 أو راسلنا على info@zephora.ly.',
                'Request a price for SLES, LABSA or sodium hypochlorite from Zephora in Benghazi. Call 0942228899 or email info@zephora.ly.')),
    dict(src='privacy', out='privacy.html', nav=None, crumb=L('الخصوصية', 'Privacy'),
         title=L('سياسة الخصوصية | زيفورا', 'Privacy Policy | Zephora'),
         desc=L('كيف نتعامل مع بياناتك عند تصفّح موقع زيفورا أو التواصل معنا.',
                'How we handle your data when you browse the Zephora website or contact us.')),
    dict(src='terms', out='terms.html', nav=None, crumb=L('شروط الاستخدام', 'Terms of use'),
         title=L('شروط الاستخدام | زيفورا', 'Terms of Use | Zephora'),
         desc=L('شروط استخدام موقع زيفورا لاستيراد المواد الخام والمواد الكيميائية.',
                'Terms of use for the Zephora raw materials and chemicals website.')),
    dict(src='thanks', out='thanks.html', nav=None, noindex=True,
         title=L('وصلتنا رسالتك | زيفورا', 'We received your message | Zephora'),
         desc=L('شكرًا لتواصلك مع زيفورا.', 'Thank you for contacting Zephora.')),
    dict(src='404', out='404.html', nav=None, noindex=True, absolute=True, langs=['ar'],
         title=L('الصفحة غير موجودة | زيفورا', 'Page not found | Zephora'),
         desc=L('الصفحة التي تبحث عنها غير موجودة.', 'The page you are looking for does not exist.')),
]
BY_SRC = {p['src']: p for p in PAGES}

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

def barrel(key, lang, decorative=True):
    """برميل على شكل برميل الشعار؛ ارتفاع السائل فيه = تركيز المادة."""
    p = PRODUCTS[key]
    _barrel_n[0] += 1
    cid = f'clip-{key}-{_barrel_n[0]}'
    top, bottom = 24.0, 158.0
    y = round(bottom - (bottom - top) * p['pct'] / 100, 1)
    body = 'M12 24V146C12 154 34 160 60 160S108 154 108 146V24'
    label = UI[lang]['barrel'].format(pct=p['pct'])
    aria = 'aria-hidden="true"' if decorative else f'role="img" aria-label="{label}"'
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

# ----------------------------------------------------------- مسارات وروابط
def page_url(page, lang):
    tail = '' if page['out'] == 'index.html' else page['out']
    return f"{SITE['url']}/{LANGS[lang]['prefix']}{tail}"

def switch_href(page, lang):
    """رابط النسخة المقابلة من الصفحة نفسها، نسبيًا من موقع الصفحة الحالية."""
    other = 'en' if lang == 'ar' else 'ar'
    tail = '' if page['out'] == 'index.html' else page['out']
    if page.get('absolute'):
        return '/en/'
    return (('en/' if other == 'en' else '../') + tail)

def crumb_chain(page):
    chain = [page]
    while chain[0].get('parent'):
        chain.insert(0, BY_SRC[chain[0]['parent']])
    return chain

# ---------------------------------------------------------------- القالب
def head(page, lang, root):
    lg, s, ui = LANGS[lang], S(lang), UI[lang]
    url = page_url(page, lang)
    title, desc = page['title'][lang], page['desc'][lang]
    if page.get('noindex'):
        robots = '<meta name="robots" content="noindex">'
        alt = ''
    else:
        robots = f'<link rel="canonical" href="{url}">'
        alt = ''.join(f'\n<link rel="alternate" hreflang="{l}" href="{page_url(page, l)}">' for l in LANGS)
        alt += f'\n<link rel="alternate" hreflang="x-default" href="{page_url(page, "ar")}">'
    ld = []
    if page.get('website'):
        ld.append({
            '@context': 'https://schema.org', '@type': 'WebSite',
            '@id': SITE['url'] + '/#website', 'url': SITE['url'] + '/',
            'name': SITE_L['ar']['name'],
            'alternateName': [SITE['name_en'], SITE_L['ar']['legal_name'], SITE['legal_name_en']],
            'inLanguage': list(LANGS)})
    if page.get('schema') == 'org':
        org = {
            '@context': 'https://schema.org',
            '@type': 'LocalBusiness',
            '@id': SITE['url'] + '/#company',
            'name': s['legal_name'],
            'alternateName': [SITE_L['ar']['name'], SITE['name_en'], SITE['legal_name_en'], SITE_L['ar']['legal_name']],
            'description': PAGES[0]['desc'][lang],
            'url': SITE['url'] + '/' + lg['prefix'],
            'logo': SITE['url'] + '/assets/img/brand/icon-512.png',
            'image': SITE['url'] + '/assets/img/brand/' + lg['card'],
            'telephone': SITE['phone'],
            'email': SITE['email'],
            'address': {'@type': 'PostalAddress', 'streetAddress': s['district'],
                        'addressLocality': s['locality'], 'addressCountry': 'LY'},
            'geo': {'@type': 'GeoCoordinates', 'latitude': SITE['lat'], 'longitude': SITE['lng']},
            'hasMap': SITE['map'],
            'areaServed': {'@type': 'Country', 'name': 'Libya'},
            'knowsAbout': ['SLES 70%', 'LABSA 96%', 'Sodium Hypochlorite 12%'],
        }
        if SITE['tax']:
            org['taxID'] = SITE['tax']
        ld.append(org)
    if page.get('crumb'):
        chain = [(ui['home'], '')] + [(p['crumb'][lang], p['out']) for p in crumb_chain(page)]
        ld.append({
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n,
                                 'item': f"{SITE['url']}/{lg['prefix']}{h}"} for i, (n, h) in enumerate(chain)]})
    ld_html = ''.join('\n<script type="application/ld+json">\n' +
                      json.dumps(x, ensure_ascii=False, indent=2) + '\n</script>' for x in ld)
    og_url = url if not page.get('noindex') else f"{SITE['url']}/{lg['prefix']}"
    gsc = f'\n<meta name="google-site-verification" content="{SITE["gsc"]}">' if SITE['gsc'] else ''
    fonts = ''
    if lang == 'ar':
        fonts = (f'\n<link rel="preload" href="{root}assets/fonts/gess-two-medium.woff2" as="font" type="font/woff2" crossorigin>'
                 f'\n<link rel="preload" href="{root}assets/fonts/gess-two-bold.woff2" as="font" type="font/woff2" crossorigin>')
    card = f"{SITE['url']}/assets/img/brand/{lg['card']}"
    site_name = f"{SITE_L['ar']['name']} — {SITE['name_en']}" if lang == 'ar' else SITE['name_en']
    return f'''<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}{alt}{gsc}
<meta name="theme-color" content="#f5f4ef">
<link rel="icon" href="{root}favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="{root}assets/img/brand/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="{root}assets/img/brand/icon-192.png">
<link rel="apple-touch-icon" href="{root}apple-touch-icon.png">
<link rel="manifest" href="{root}site.webmanifest">{fonts}
<link rel="stylesheet" href="{root}assets/css/main.css">
<meta property="og:type" content="website">
<meta property="og:locale" content="{lg['locale']}">
<meta property="og:site_name" content="{site_name}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{og_url}">
<meta property="og:image" content="{card}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script>document.documentElement.classList.add("js")</script>{ld_html}
</head>'''

def header(page, lang, root, base):
    s, ui = S(lang), UI[lang]
    def links():
        out = []
        for key in ('products', 'about', 'contact'):
            href = {'products': 'products.html', 'about': 'about.html', 'contact': 'contact.html'}[key]
            cur = ' aria-current="page"' if page['nav'] == key else ''
            out.append(f'<a href="{base}{href}"{cur}>{ui["nav"][key]}</a>')
        return '\n        '.join(out)
    home_cur = ' aria-current="page"' if page['nav'] == 'home' else ''
    other = 'en' if lang == 'ar' else 'ar'
    sw = f'<a class="lang-switch" href="{switch_href(page, lang)}" hreflang="{other}" lang="{other}" aria-label="{ui["switch_aria"]}">{ui["switch_label"]}</a>'
    return f'''<a class="skip" href="#main">{ui['skip']}</a>
<header class="header" data-header>
  <div class="wrap header__bar">
    <a class="brand" href="{base or './'}" aria-label="{ui['brand_aria'].format(name=s['name'])}">
      <picture><source srcset="{root}assets/img/brand/mark-160.webp" type="image/webp"><img src="{root}assets/img/brand/mark-160.png" width="160" height="148" alt=""></picture>
      <span class="brand__text"><span class="brand__name">{s['name']}</span><span class="brand__tag">{s['tagline']}</span></span>
    </a>
    <nav class="nav" aria-label="{ui['nav_aria']}">
        {links()}
    </nav>
    {sw}
    <a class="btn btn--sm header__cta" href="{base}contact.html">{ui['quote']}</a>
    <details class="menu">
      <summary aria-label="{ui['menu']}">{icon('menu', 'i-open')}{icon('close', 'i-close')}</summary>
      <nav class="menu__panel" aria-label="{ui['menu_aria']}">
        <a href="{base or './'}"{home_cur}>{ui['home']}</a>
        {links()}
        <a class="btn" href="tel:{SITE['phone']}">{icon('phone')}<span>{ui['call']} <span class="latin">{SITE['phone_display']}</span></span></a>
      </nav>
    </details>
  </div>
</header>'''

def footer(page, lang, root, base):
    s, ui = S(lang), UI[lang]
    legal = [s['legal_name']]
    for key, label in (('cr', ui['cr']), ('tax', ui['tax']), ('chamber', s['chamber_name'])):
        if SITE[key]:
            legal.append(f'{label}: <span class="latin">{SITE[key]}</span>')
    legal_html = ''.join(f'<span>{x}</span>' for x in legal)
    prods = '\n          '.join(f'<li><a href="{base}{p["page"]}">{p["short"][lang]}</a></li>' for p in PRODUCTS.values())
    other = 'en' if lang == 'ar' else 'ar'
    return f'''<footer class="footer">
  <div class="wrap footer__top">
    <div>
      <div class="footer__brand">
        <picture><source srcset="{root}assets/img/brand/mark-white-160.webp" type="image/webp"><img src="{root}assets/img/brand/mark-white-160.png" width="160" height="148" alt="" loading="lazy"></picture>
        <div><b>{s['name']}</b><span>{s['tagline']}</span></div>
      </div>
      <p class="footer__about">{ui['footer_about']}</p>
    </div>
    <div>
      <h2>{ui['f_products']}</h2>
      <ul role="list">
          {prods}
      </ul>
    </div>
    <div>
      <h2>{ui['f_company']}</h2>
      <ul role="list">
        <li><a href="{base}about.html">{ui['f_about']}</a></li>
        <li><a href="{base}products.html#faq">{ui['f_faq']}</a></li>
        <li><a href="{base}contact.html">{ui['quote']}</a></li>
      </ul>
    </div>
    <div>
      <h2>{ui['f_contact']}</h2>
      <ul role="list" class="footer__contact">
        <li>{icon('phone')}<a href="tel:{SITE['phone']}" class="latin">{SITE['phone_display']}</a></li>
        <li>{icon('mail')}<a href="mailto:{SITE['email']}" class="latin">{SITE['email']}</a></li>
        <li>{icon('pin')}<a href="{SITE['map']}" target="_blank" rel="noopener">{s['city']}</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer__legal">{legal_html}</div>
  <div class="wrap footer__bottom">
    <p>© <span data-year>2026</span> {s['name']} — {ui['rights']}</p>
    <p class="footer__dev">{ui['dev']} <a href="https://yosef.ly" target="_blank" rel="noopener">{ui['dev_name']}</a></p>
    <nav aria-label="{ui['legal_nav']}"><a href="{switch_href(page, lang)}" hreflang="{other}" lang="{other}">{UI[lang]['switch_label']}</a><a href="{base}privacy.html">{ui['privacy']}</a><a href="{base}terms.html">{ui['terms']}</a></nav>
  </div>
</footer>'''

def crumbs_html(page, lang, base):
    if not page.get('crumb'):
        return ''
    ui = UI[lang]
    items = [(ui['home'], base or './')] + [(p['crumb'][lang], base + p['out']) for p in crumb_chain(page)]
    lis = []
    for i, (n, h) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li aria-current="page">{n}</li>')
        else:
            lis.append(f'<li><a href="{h}">{n}</a></li>')
    return f'<nav aria-label="{ui["crumbs_aria"]}"><ol class="crumbs" role="list">' + ''.join(lis) + '</ol></nav>'

# ------------------------------------------------------------ معالجة المحتوى
def content_dir(lang):
    return PAGES_DIR if lang == 'ar' else os.path.join(PAGES_DIR, 'en')

def render(text, page, lang, root, base):
    data = S(lang)
    def sub(m):
        kind, _, arg = m.group(1).partition(':')
        if kind == 'barrel':
            name, _, flag = arg.partition(':')
            return barrel(name, lang, decorative=(flag != 'label'))
        if kind == 'icon':
            return icon(arg)
        if kind == 'include':
            with open(os.path.join(content_dir(lang), '_partials', arg + '.html'), encoding='utf-8') as f:
                return render(f.read(), page, lang, root, base)
        if kind == 'crumbs':
            return crumbs_html(page, lang, base)
        if kind == 'base':
            return base
        if kind == 'root':
            return root
        if kind == 'registry':
            return registry_rows(lang)
        if kind == 'prefix':
            return LANGS[lang]['prefix']
        if kind in data:
            return str(data[kind])
        raise KeyError(f'وسم غير معروف: {m.group(0)}')
    return re.sub(r'\{\{([\w:-]+)\}\}', sub, text)

def isolate_numbers(html):
    """يعزل النسب المئوية داخل النص العربي حتى لا تنقلب إلى %12 بفعل اتجاه السطر."""
    parts = re.split(r'(<[^>]+>)', html)
    pat = re.compile(r'(?<![\w.])(\d+(?:\.\d+)?%)')
    for i in range(0, len(parts), 2):          # الأجزاء الزوجية نص، الفردية وسوم
        parts[i] = pat.sub(r'<bdi dir="ltr">\1</bdi>', parts[i])
    return ''.join(parts)

def registry_rows(lang):
    s, ui = S(lang), UI[lang]
    rows = [(ui['reg_name'], s['legal_name'], False)]
    for key, label in (('cr', ui['cr']), ('tax', ui['tax']), ('chamber', ui['reg_chamber'].format(chamber_name=s['chamber_name']))):
        rows.append((label, SITE[key], True))
    rows.append((ui['reg_hq'], s['city'], False))
    out = []
    for label, val, mono in rows:
        if val:
            cls = ' class="mono"' if mono else ''
            out.append(f'<div><dt>{label}</dt><dd{cls}>{val}</dd></div>')
        else:
            out.append(f'<div><dt>{label}</dt><dd class="pending">{ui["pending"]}</dd></div>')
    return '\n          '.join(out)

def build():
    os.makedirs(os.path.join(ROOT, 'en'), exist_ok=True)
    for page in PAGES:
        for lang in page.get('langs', list(LANGS)):
            lg = LANGS[lang]
            if page.get('absolute'):
                root = base = '/'
            else:
                root, base = ('../' if lang == 'en' else ''), ''
            _barrel_n[0] = 0
            with open(os.path.join(content_dir(lang), page['src'] + '.html'), encoding='utf-8') as f:
                body = render(f.read(), page, lang, root, base)
            if lang == 'ar':
                body = isolate_numbers(body)
            html = f'''<!doctype html>
<html lang="{lang}" dir="{lg['dir']}">
{head(page, lang, root)}
<body>
{header(page, lang, root, base)}

<main id="main">
{body.strip()}
</main>

{footer(page, lang, root, base)}
<script src="{root}assets/js/main.js" defer></script>
</body>
</html>
'''
            out = lg['prefix'] + page['out']
            with open(os.path.join(ROOT, out), 'w', encoding='utf-8') as f:
                f.write(html)
            print('✓', out)

    # خريطة الموقع، مع ربط كل صفحة بنسختها الأخرى
    pri = {'index.html': '1.0', 'products.html': '0.9', 'sles.html': '0.9', 'labsa.html': '0.9',
           'sodium-hypochlorite.html': '0.9', 'contact.html': '0.8', 'about.html': '0.7'}
    entries = []
    for page in PAGES:
        if page.get('noindex'):
            continue
        alts = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{page_url(page, l)}"/>' for l in LANGS)
        alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{page_url(page, "ar")}"/>'
        for lang in LANGS:
            entries.append(f'  <url>\n    <loc>{page_url(page, lang)}</loc>{alts}\n'
                           f'    <priority>{pri.get(page["out"], "0.3")}</priority>\n  </url>')
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
                + '\n'.join(entries) + '\n</urlset>\n')
    print('✓ sitemap.xml')

if __name__ == '__main__':
    build()
