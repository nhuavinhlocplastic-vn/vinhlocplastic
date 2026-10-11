"""Sinh website tĩnh Vĩnh Lộc Plastic.

    python3 build.py            -> public/   (URL đẹp: gioi-thieu/, san-pham/<danh-muc>/ — đưa lên hosting)
    python3 build.py preview    -> preview/  (file phẳng .html — mở thẳng file index.html, không cần server)
    python3 build.py artifact   -> artifact/ (như preview nhưng nhúng sẵn CSS/JS/ảnh vào từng trang)

Mọi đường dẫn đều là đường dẫn tương đối, nên website chạy đúng dù đặt ở tên miền gốc
hay trong thư mục con. Header, footer, menu dùng chung; mỗi trang có title, meta description,
canonical, Open Graph, breadcrumb và dữ liệu cấu trúc (JSON-LD) riêng để làm SEO.
"""
import base64, html, json, re, shutil, sys
from pathlib import Path
from data import SITE, CATEGORIES, PRODUCTS, NEWS, INDUSTRIES, PALETTE, SOLUTIONS, STEPS
from urllib.parse import quote

ROOT = Path(__file__).parent
MODE = sys.argv[1] if len(sys.argv) > 1 else "public"
if MODE not in ("public", "preview", "artifact"):
    sys.exit("Chế độ không hợp lệ. Dùng: public | preview | artifact")
FLAT = MODE in ("preview", "artifact")          # file phẳng .html thay vì thư mục
OUT = ROOT / MODE
CAT = {c["slug"]: c for c in CATEGORIES}
CURRENT = "home"                                # trang đang được sinh (để tính đường dẫn tương đối)
e = html.escape


# ---------------------------------------------------------------- URL
def path(page):
    """Đường dẫn chuẩn tính từ gốc tên miền (dùng cho canonical, sitemap, JSON-LD)."""
    if page == "home": return "/"
    if page == "about": return "/gioi-thieu/"
    if page == "products": return "/san-pham/"
    if page == "solutions": return "/giai-phap/"
    if page == "news": return "/tin-tuc/"
    if page == "contact": return "/lien-he/"
    if page.startswith("post:"): return f"/tin-tuc/{page[5:]}/"
    return f"/san-pham/{page[4:]}/"  # "cat:<slug>"

def prefix():
    """'../' lặp lại theo độ sâu thư mục của trang đang sinh (chỉ bản public)."""
    return "" if FLAT else "../" * path(CURRENT).strip("/").count("/") + ("../" if CURRENT != "home" else "")

def url(page, anchor=""):
    """Link tương đối từ trang hiện tại tới `page`."""
    if FLAT:
        target = {"home": "index.html", "about": "gioi-thieu.html", "products": "san-pham.html",
                  "solutions": "giai-phap.html", "news": "tin-tuc.html", "contact": "lien-he.html"}.get(page) \
            or (f"tin-tuc-{page[5:]}.html" if page.startswith("post:") else f"san-pham-{page[4:]}.html")
    else:
        target = (prefix() + path(page).lstrip("/")) or "./"
    return target + (f"#{anchor}" if anchor else "")

def asset(p):
    return prefix() + p

def out_file(page):
    if FLAT:
        return OUT / url(page)
    return OUT / path(page).strip("/") / "index.html" if page != "home" else OUT / "index.html"


# ---------------------------------------------------------------- Minh họa SVG
def svg_pouch(c, label="VL"):
    d, m, l = c
    label = label or "VL"
    return f'''<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<path d="M38 22h124l6 176c0 14-10 24-24 24H56c-14 0-24-10-24-24z" fill="{d}"/>
<path d="M38 22h124l1 26H37z" fill="{m}" opacity=".55"/>
<path d="M42 54h116" stroke="{l}" stroke-width="3" stroke-dasharray="6 4" opacity=".8"/>
<circle cx="100" cy="34" r="5" fill="{l}" opacity=".9"/>
<rect x="56" y="96" width="88" height="70" rx="12" fill="{l}"/>
<text x="100" y="140" text-anchor="middle" font-family="Be Vietnam Pro,sans-serif" font-weight="800" font-size="26" fill="{d}">{label}</text>
<path d="M44 70c10 60 4 110 0 140" stroke="#fff" stroke-width="8" opacity=".12" stroke-linecap="round"/></svg>'''

def svg_vacuum(c, fill="block"):
    d, m, l = c
    if fill == "grain":
        inner = "".join(
            f'<ellipse cx="{62 + (i % 7) * 13 + (i // 7 % 2) * 6}" cy="{92 + (i // 7) * 22}" rx="6" ry="9" fill="{d}" opacity="{.55 + (i % 3) * .15:.2f}"/>'
            for i in range(34))
    else:
        inner = (f'<rect x="54" y="78" width="92" height="118" rx="22" fill="{d}"/>'
                 f'<path d="M66 100c20 10 46 10 68 0M66 130c20 10 46 10 68 0M66 160c20 10 46 10 68 0" stroke="{m}" stroke-width="5" fill="none" opacity=".7" stroke-linecap="round"/>')
    return f'''<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<rect x="40" y="26" width="120" height="194" rx="14" fill="{l}" stroke="{m}" stroke-width="3"/>
<rect x="40" y="26" width="120" height="22" rx="8" fill="{m}" opacity=".6"/>
<path d="M46 37h108" stroke="{l}" stroke-width="2" stroke-dasharray="3 3"/>{inner}
<rect x="40" y="26" width="120" height="194" rx="14" fill="#fff" opacity=".16"/>
<path d="M52 64c6 50 4 110 0 146" stroke="#fff" stroke-width="7" opacity=".55" stroke-linecap="round"/>
<path d="M150 70c-3 20-3 40 0 60" stroke="#fff" stroke-width="4" opacity=".4" stroke-linecap="round"/></svg>'''

def svg_flat(c, _=""):
    d, m, l = c
    return f'''<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<rect x="34" y="20" width="132" height="200" rx="10" fill="{l}" stroke="{m}" stroke-width="3"/>
<rect x="34" y="20" width="132" height="34" rx="10" fill="{d}"/>
<path d="M40 46h120" stroke="{l}" stroke-width="3"/>
<rect x="54" y="80" width="92" height="10" rx="5" fill="{m}"/>
<rect x="54" y="100" width="60" height="10" rx="5" fill="{m}" opacity=".6"/>
<rect x="54" y="150" width="92" height="48" rx="10" fill="{d}" opacity=".9"/>
<path d="M48 70c6 50 4 100 0 140" stroke="#fff" stroke-width="8" opacity=".35" stroke-linecap="round"/></svg>'''

def svg_roll(c, _=""):
    d, m, l = c
    return f'''<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<rect x="40" y="40" width="120" height="96" rx="16" fill="{d}"/>
<ellipse cx="40" cy="88" rx="16" ry="48" fill="{m}"/>
<ellipse cx="40" cy="88" rx="6" ry="18" fill="{l}"/>
<path d="M150 136v70c0 10-8 14-16 10l-8-4-8 4-8-4-8 4-8-4-8 4-8-4-8 4V136z" fill="{m}" opacity=".85"/>
<path d="M60 60h80M60 76h60" stroke="{l}" stroke-width="5" stroke-linecap="round" opacity=".5"/></svg>'''

ART = {"pouch": svg_pouch, "vacuum": svg_vacuum, "flat": svg_flat, "roll": svg_roll}

SVG_FACTORY = '''<svg viewBox="0 0 500 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Minh họa nhà xưởng Vĩnh Lộc Plastic">
<rect width="500" height="400" fill="#F7EBD3"/><circle cx="410" cy="80" r="40" fill="#E2B867"/>
<path d="M0 300h500v100H0z" fill="#EBD9B8"/>
<path d="M60 300V170l80 50v-50l80 50v-50l80 50V120h50v180z" fill="#9E1815"/>
<rect x="340" y="60" width="26" height="80" fill="#6E110E"/>
<circle cx="360" cy="45" r="14" fill="#fff" opacity=".8"/><circle cx="385" cy="28" r="10" fill="#fff" opacity=".6"/>
<g fill="#E2B867"><rect x="90" y="240" width="30" height="24" rx="3"/><rect x="170" y="240" width="30" height="24" rx="3"/><rect x="250" y="240" width="30" height="24" rx="3"/></g>
<rect x="390" y="230" width="70" height="70" rx="6" fill="#2B2422"/><rect x="398" y="240" width="54" height="8" fill="#BF8217"/>
<text x="425" y="285" text-anchor="middle" font-family="Be Vietnam Pro,sans-serif" font-weight="800" font-size="22" fill="#fff">VL</text></svg>'''

def cat_art(c):
    shape = {"tui-hut-chan-khong-pa-pe": ("vacuum", "block"), "bao-bi-thuc-pham": ("pouch", ""),
             "bao-bi-nong-san": ("vacuum", "grain"), "bao-bi-cong-nghiep": ("roll", "")}[c["slug"]]
    return ART[shape[0]](PALETTE[c["color"]], shape[1]) if shape[0] != "pouch" else svg_pouch(PALETTE[c["color"]])


# ---------------------------------------------------------------- Thành phần dùng chung
def dot(c):
    d, m, _ = PALETTE[c["color"]]
    return f'<span class="dot" style="background:linear-gradient(135deg,{d},{m})"></span>'

def head(title, desc, page, jsonld):
    canonical = SITE["url"] + path(page)
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="vi_VN">
<meta property="og:site_name" content="{e(SITE["name"])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE["url"]}/img/logo-vinhloc.png">
<link rel="icon" href="{asset("img/logo-vl-mark.png")}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{asset("css/tokens.css")}">
<link rel="stylesheet" href="{asset("css/main.css")}">
{ld}'''

def header(active):
    def act(k): return ' class="is-active" aria-current="page"' if active == k else ""
    mega = "".join(
        f'<a href="{url("cat:" + c["slug"])}"{" class=\"is-active\" aria-current=\"page\"" if active == "cat:" + c["slug"] else ""}>{dot(c)}{e(c["name"])}</a>'
        for c in CATEGORIES)
    prod_active = " is-active" if active == "products" or active.startswith("cat:") else ""
    news_act = act("news") if active == "news" else (' class="is-active"' if active.startswith("post:") else "")
    return f'''<a class="skip" href="#main">Bỏ qua tới nội dung</a>
<div class="topbar">
  <div class="container topbar__inner">
    <span>{e(SITE["slogan"])}</span>
    <div class="topbar__links">
      <a href="tel:{SITE["phone"]}">☎ {SITE["phone_display"]}</a>
      <a href="mailto:{SITE["email"]}" class="topbar__mail">✉ {SITE["email"]}</a>
      <button class="theme-toggle" id="themeToggle" type="button" aria-label="Đổi giao diện sáng/tối">◐</button>
    </div>
  </div>
</div>
<header class="header" id="header">
  <div class="container header__inner">
    <a href="{url("home")}" class="logo" aria-label="{e(SITE["name"])} — Trang chủ">
      <img class="logo__img logo__img--color" src="{asset("img/logo-vinhloc.png")}" alt="{e(SITE["name"])}" width="900" height="352">
      <img class="logo__img logo__img--white" src="{asset("img/logo-vinhloc-white.png")}" alt="" width="900" height="352">
    </a>
    <nav class="nav" id="nav" aria-label="Điều hướng chính">
      <a href="{url("home")}"{act("home")}>Trang chủ</a>
      <a href="{url("about")}"{act("about")}>Giới thiệu</a>
      <div class="nav__item">
        <a href="{url("products")}" class="nav__parent{prod_active}"{' aria-current="page"' if active == "products" else ""}>Sản phẩm <span class="caret">▾</span></a>
        <div class="dropdown dropdown--mega">{mega}
          <a href="{url("products")}" class="dropdown__all">Xem tất cả sản phẩm →</a>
        </div>
      </div>
      <a href="{url("solutions")}"{act("solutions")}>Giải pháp</a>
      <a href="{url("news")}"{news_act}>Tin tức</a>
      <a href="{url("contact")}"{act("contact")}>Liên hệ</a>
    </nav>
    <div class="header__actions">
      <form class="search" id="searchForm" role="search" data-target="{url("products", "tat-ca")}">
        <label class="sr-only" for="searchInput">Tìm kiếm sản phẩm</label>
        <input type="search" placeholder="Tìm sản phẩm…" id="searchInput" autocomplete="off">
      </form>
      <button class="btn btn--cta btn--sm" type="button" data-open-modal>Nhận báo giá</button>
      <button class="burger" id="burger" type="button" aria-label="Mở menu" aria-expanded="false"><span></span></button>
    </div>
  </div>
</header>'''

def footer():
    cats = "".join(f'<li><a href="{url("cat:" + c["slug"])}">{e(c["name"])}</a></li>' for c in CATEGORIES)
    return f'''<footer class="footer" id="lien-he">
  <div class="container footer__grid">
    <div>
      <a href="{url("home")}" class="logo logo--light" aria-label="{e(SITE["name"])} — Trang chủ"><img class="logo__img" src="{asset("img/logo-vinhloc-white.png")}" alt="{e(SITE["name"])}" width="900" height="352"></a>
      <p class="footer__desc">{e(SITE["slogan"])}. Chuyên cung cấp bao bì PA/PE, túi hút chân không.</p>
      <ul class="footer__links"><li><a href="{url("about")}">Giới thiệu công ty</a></li><li><a href="{url("products")}">Sản phẩm</a></li><li><a href="{url("solutions")}">Giải pháp</a></li><li><a href="{url("news")}">Tin tức</a></li><li><a href="{url("contact")}">Liên hệ</a></li></ul>
    </div>
    <div>
      <h2 class="footer__h">Thông tin doanh nghiệp</h2>
      <dl class="info">
        <dt>Tên công ty</dt><dd>{e(SITE["legal_name"])}</dd>
        <dt>Lĩnh vực</dt><dd>{e(SITE["field"])}</dd>
        <dt>Địa chỉ</dt><dd>{e(SITE["address"])}</dd>
        <dt>Mã số thuế</dt><dd>{SITE["tax_id"]}</dd>
      </dl>
    </div>
    <div>
      <h2 class="footer__h"><a href="{url("contact")}">Liên hệ</a></h2>
      <dl class="info">
        <dt>Điện thoại / Zalo</dt><dd><a href="tel:{SITE["phone"]}">{SITE["phone_display"]}</a></dd>
        <dt>Email</dt><dd><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></dd>
        <dt>Website</dt><dd>{SITE["website"]}</dd>
      </dl>
    </div>
    <div>
      <h2 class="footer__h">Danh mục sản phẩm</h2>
      <ul>{cats}</ul>
    </div>
  </div>
  <div class="footer__bottom container">© 2026 {e(SITE["name"])} · {e(SITE["slogan"])}</div>
</footer>
<div class="floating">
  <a href="https://zalo.me/{SITE["phone"]}" class="floating__btn floating__btn--zalo" aria-label="Chat Zalo">Zalo</a>
  <a href="tel:{SITE["phone"]}" class="floating__btn floating__btn--call" aria-label="Gọi {SITE["phone_display"]}">☎</a>
  <button class="floating__btn floating__btn--top" id="toTop" type="button" aria-label="Lên đầu trang">↑</button>
</div>
<div class="modal" id="modal" aria-hidden="true">
  <div class="modal__backdrop" data-close-modal></div>
  <div class="modal__box" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
    <button class="modal__close" type="button" data-close-modal aria-label="Đóng">×</button>
    <h2 id="modalTitle">Nhận tư vấn và báo giá</h2>
    <p>Điền thông tin, {e(SITE["name"])} sẽ liên hệ lại trong giờ làm việc.</p>
    <form class="form" id="contactForm">
      <label>Họ tên*<input required name="name" id="fName"></label>
      <label>Số điện thoại / Zalo*<input required name="phone" type="tel" id="fPhone"></label>
      <label>Sản phẩm quan tâm
        <select name="service" id="fService">{"".join(f"<option>{e(c['name'])}</option>" for c in CATEGORIES)}<option>Khác</option></select>
      </label>
      <label>Kích thước, số lượng, yêu cầu thêm<textarea name="note" rows="3" id="fNote"></textarea></label>
      <button class="btn btn--cta btn--block">Gửi yêu cầu</button>
    </form>
  </div>
</div>
<div class="toast" id="toast" role="status"></div>
<script src="{asset("js/main.js")}"></script>'''

def cta_band():
    return f'''<section class="cta-band">
  <div class="container cta-band__inner">
    <div>
      <h2>Cần bao bì cho dây chuyền của bạn?</h2>
      <p>Để lại số điện thoại, {e(SITE["name"])} sẽ gọi lại tư vấn và báo giá.</p>
    </div>
    <form class="subscribe" id="subscribe">
      <label class="sr-only" for="subPhone">Số điện thoại</label>
      <input id="subPhone" type="tel" placeholder="Số điện thoại của bạn" required>
      <button class="btn btn--cta">Gọi lại cho tôi</button>
    </form>
  </div>
</section>'''

def card(p, show_cat=True):
    name, slug, shape, color, tag, fill = p
    c = CAT[slug]
    tag_html = f'<span class="card__tag{" card__tag--eco" if tag == "Nông sản" else ""}">{e(tag)}</span>' if tag else ""
    cat_html = f'<a class="card__cat" href="{url("cat:" + slug)}">{e(c["short"])}</a>' if show_cat else ""
    return f'''<article class="card" data-cat="{slug}" data-name="{e(name.lower())}">
  <div class="card__media" style="background:{PALETTE[color][2]}">{tag_html}{ART[shape](PALETTE[color], fill)}</div>
  <div class="card__body">{cat_html}
    <h3>{e(name)}</h3>
    <div class="card__meta"><span>Sản xuất theo yêu cầu</span><button type="button" data-open-modal data-product="{e(name)}">Báo giá</button></div>
  </div>
</article>'''

def tabs_and_grid(limit=0, show_foot=True):
    tabs = '<button class="tab is-active" type="button" role="tab" aria-selected="true" data-filter="all" data-href="' + url("products") + '" data-label="Xem tất cả sản phẩm">Tất cả</button>' + "".join(
        f'<button class="tab" type="button" role="tab" aria-selected="false" data-filter="{c["slug"]}" data-href="{url("cat:" + c["slug"])}" data-label="Xem danh mục {e(c["name"])}">{e(c["name"])}</button>'
        for c in CATEGORIES)
    cards = "\n".join(card(p) for p in PRODUCTS)
    foot = f'<p class="grid-foot"><a class="btn btn--brand" id="catLink" href="{url("products")}">Xem tất cả sản phẩm</a></p>' if show_foot else ""
    return f'''<div class="tabs" role="tablist" id="tabs">{tabs}</div>
<div class="grid-products" id="productGrid" data-limit="{limit}">
{cards}
<p class="empty" id="emptyMsg" hidden>Không tìm thấy sản phẩm phù hợp.</p>
</div>
{foot}'''

def breadcrumb(items):
    """items: [(tên, page|None)] — phần tử cuối là trang hiện tại."""
    lis = "".join(
        f'<li><a href="{url(pg)}">{e(n)}</a></li>' if pg and i < len(items) - 1 else f'<li aria-current="page">{e(n)}</li>'
        for i, (n, pg) in enumerate(items))
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE["url"] + path(pg)}
        for i, (n, pg) in enumerate(items) if pg]}
    return f'<nav class="breadcrumb" aria-label="Breadcrumb"><ol>{lis}</ol></nav>', ld

def page_hero(crumb_html, eyebrow, h1, lead, art, actions=""):
    return f'''<section class="page-hero">
  <div class="container page-hero__inner">
    <div class="page-hero__body">
      {crumb_html}
      <span class="eyebrow">{e(eyebrow)}</span>
      <h1>{e(h1)}</h1>
      <p>{e(lead)}</p>
      {actions}
    </div>
    <div class="page-hero__art">{art}</div>
  </div>
</section>'''

def page(page_key, title, desc, body, jsonld):
    return f'''<!doctype html>
<html lang="vi">
<head>
{head(title, desc, page_key, jsonld)}
</head>
<body>
{header(page_key)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''

ORG = {
    "@context": "https://schema.org", "@type": "Organization",
    "name": SITE["name"], "legalName": SITE["legal_name"], "url": SITE["url"],
    "logo": SITE["url"] + "/img/logo-vinhloc.png", "email": SITE["email"],
    "telephone": "+84" + SITE["phone"].lstrip("0"), "taxID": SITE["tax_id"],
    "foundingDate": SITE["founded"], "slogan": SITE["slogan"],
    "address": {"@type": "PostalAddress", "streetAddress": "252 ấp Nhơn Hòa 1, xã Mỹ Hạnh",
                "addressRegion": SITE["region"], "addressCountry": "VN"},
}

TIMELINE = '''<ol class="timeline">
  <li class="timeline__item reveal"><span class="timeline__year">2013</span><h3>Thành lập</h3>
    <p>Ngày 12/6/2013, công ty ra đời với tiền thân là doanh nghiệp xuất nhập khẩu, xác định kiến thức chuyên môn, uy tín và chất lượng dịch vụ là nền tảng phát triển lâu dài.</p></li>
  <li class="timeline__item reveal"><span class="timeline__year">2018</span><h3>Bước ngoặt phát triển</h3>
    <p>Mở rộng hoạt động, đầu tư máy móc, thiết bị và công nghệ để trực tiếp sản xuất bao bì nhựa, chuyển từ thương mại sang vừa sản xuất vừa cung cấp giải pháp.</p></li>
  <li class="timeline__item reveal"><span class="timeline__year">Nay</span><h3>Đồng hành cùng nhà máy</h3>
    <p>Trực tiếp đồng hành cùng nhà máy, doanh nghiệp sản xuất và chế biến, đáp ứng yêu cầu đóng gói, bảo quản và vận chuyển hàng hóa.</p></li>
</ol>'''

PILLARS = '''<div class="pillars">
  <article class="pillar reveal"><span class="pillar__icon">⚙</span><h3>Công nghệ</h3>
    <p>Không ngừng nâng cao năng lực sản xuất và trình độ kỹ thuật, đầu tư thiết bị phù hợp yêu cầu đóng gói.</p></article>
  <article class="pillar reveal"><span class="pillar__icon">◆</span><h3>Chất lượng</h3>
    <p>Đa dạng hóa sản phẩm, đáp ứng yêu cầu đóng gói, bảo quản và vận chuyển của công nghiệp và nông nghiệp.</p></article>
  <article class="pillar reveal"><span class="pillar__icon">♥</span><h3>Khách hàng</h3>
    <p>Mở rộng hợp tác với các nhà máy sản xuất, chế biến, đóng gói trong lĩnh vực công nghiệp và nông nghiệp.</p></article>
</div>'''

PLEDGE = '''<blockquote class="pledge reveal">
  <span class="eyebrow eyebrow--dark">Cam kết của Vĩnh Lộc Plastic</span>
  <p>Trở thành đối tác kỹ thuật, đồng hành cùng khách hàng trong việc lựa chọn và hoàn thiện giải pháp đóng gói phù hợp; tạo ra những sản phẩm thiết thực, đóng góp vào sự phát triển của ngành công nghiệp và nông nghiệp Việt Nam.</p>
</blockquote>'''

ABOUT_INTRO_P = '''<p>Được thành lập ngày 12/6/2013, Vĩnh Lộc Plastic có tiền thân là một doanh nghiệp hoạt động trong lĩnh vực xuất nhập khẩu. Ngay từ những ngày đầu, công ty xác định kiến thức chuyên môn, uy tín và chất lượng dịch vụ là nền tảng cho sự phát triển lâu dài.</p>
<p>Với đội ngũ lãnh đạo giàu chuyên môn, am hiểu ngành nhựa, nguyên liệu, công nghệ và thiết bị sản xuất, Vĩnh Lộc Plastic từng bước tích lũy kinh nghiệm, xây dựng quan hệ hợp tác và phát triển nền tảng vững chắc.</p>'''

STATS = '''<ul class="stats">
  <li><b class="plus" data-count="13">13</b><span>Năm hoạt động</span></li>
  <li><b>2018</b><span>Bắt đầu tự sản xuất</span></li>
  <li><b>PA/PE</b><span>Vật liệu chủ lực</span></li>
</ul>'''

def about_media():
    return f'''<div class="about__media reveal">
  <div class="about__card">{SVG_FACTORY}</div>
  <div class="about__badge"><b>2018</b><span>Trực tiếp sản xuất<br>bao bì nhựa</span></div>
</div>'''



def steps_html():
    return '<ol class="steps">' + "".join(
        f'<li><span>{i + 1}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for i, (t, d) in enumerate(STEPS)) + "</ol>"

def vn_date(iso):
    y, m, d = iso.split("-")
    return f"{d}.{m}.{y}"

def post_thumb(n):
    dk, md, lt = PALETTE[n["color"]]
    return (f'<div class="post__thumb" style="background:linear-gradient(135deg,{dk},{md})">'
            f'<svg viewBox="0 0 320 180" width="100%" height="100%" aria-hidden="true"><circle cx="260" cy="40" r="60" fill="{lt}" opacity=".18"/>'
            f'<circle cx="40" cy="170" r="70" fill="{lt}" opacity=".12"/><rect x="120" y="50" width="80" height="90" rx="10" fill="{lt}" opacity=".9"/>'
            f'<rect x="134" y="70" width="52" height="8" rx="4" fill="{dk}"/><rect x="134" y="86" width="36" height="8" rx="4" fill="{md}"/></svg>'
            f'<time datetime="{n["date"]}">{vn_date(n["date"])}</time></div>')

def post_card(n, tag="h3"):
    href = url("post:" + n["slug"])
    return (f'<article class="post reveal"><a href="{href}" class="post__link" tabindex="-1" aria-hidden="true">{post_thumb(n)}</a>'
            f'<div class="post__body"><{tag}><a href="{href}">{e(n["title"])}</a></{tag}><p>{e(n["excerpt"])}</p>'
            f'<a class="link-more" href="{href}">Đọc tiếp →</a></div></article>')

def render_blocks(blocks):
    out = []
    for b in blocks:
        k = b[0]
        if k == "p": out.append(f"<p>{e(b[1])}</p>")
        elif k == "h2": out.append(f"<h2>{e(b[1])}</h2>")
        elif k in ("ul", "ol"): out.append(f"<{k}>" + "".join(f"<li>{e(x)}</li>" for x in b[1]) + f"</{k}>")
        elif k == "note": out.append(f'<p class="callout">{e(b[1])}</p>')
        elif k == "table":
            head = "".join(f'<th scope="col">{e(h)}</th>' for h in b[1])
            rows = "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in b[2])
            out.append(f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>')
    return "\n".join(out)

# ---------------------------------------------------------------- Trang chủ
def build_home():
    slides = [
        ("Vinhloc Plastic", "Giải pháp bao bì cho ", "công nghiệp và nông nghiệp", "",
         "Chuyên bao bì PA/PE và túi hút chân không, sản xuất trực tiếp tại Tây Ninh từ năm 2018.",
         f'<button class="btn btn--light" type="button" data-open-modal>Nhận báo giá</button><a class="btn btn--ghost-light" href="{url("about")}">Về chúng tôi</a>',
         svg_vacuum(("#9E1815", "#E2B867", "#FFF6EE"), "block")),
        ("Túi hút chân không PA/PE", "Giữ trọn độ tươi, ", "kéo dài thời gian bảo quản", "",
         "Màng PA/PE chịu nhiệt, chống thấm khí, phù hợp thịt, thủy sản đông lạnh và nông sản khô.",
         f'<a class="btn btn--light" href="{url("cat:tui-hut-chan-khong-pa-pe")}">Xem túi hút chân không</a>',
         svg_pouch(("#FFFFFF", "#F7EBD3", "#9E1815"))),
        ("Đối tác kỹ thuật", "Đồng hành cùng ", "nhà máy và dây chuyền", " của bạn",
         "Tư vấn vật liệu, kích thước và độ dày phù hợp với từng ngành hàng và phương pháp đóng gói.",
         '<button class="btn btn--light" type="button" data-open-modal>Liên hệ tư vấn</button>',
         svg_roll(("#BF8217", "#E2B867", "#2B2422"))),
    ]
    slide_html = ""
    for i, (eb, a, em, b, p, cta, art) in enumerate(slides):
        tag = "h1" if i == 0 else "h2"
        slide_html += f'''<article class="slide slide--{i + 1}">
  <div class="slide__body"><span class="eyebrow">{e(eb)}</span>
    <{tag} class="slide__title">{e(a)}<em>{e(em)}</em>{e(b)}</{tag}>
    <p>{e(p)}</p><div class="slide__cta">{cta}</div></div>
  <div class="slide__art">{art}</div>
</article>'''

    sol_html = "".join(
        f'<a class="service reveal" href="{url("solutions", x["slug"])}"><div class="service__tag">{e(x["tag"])}</div>'
        f'<h3>{e(x["for"])}</h3><p>{e(x["short"])}</p><span class="service__more">Xem giải pháp →</span></a>'
        for x in SOLUTIONS)
    news_html = "".join(post_card(n) for n in NEWS)
    marquee = "".join(f"<span>{e(x)}</span>" for x in INDUSTRIES * 2)

    body = f'''<section class="hero">
  <div class="container">
    <div class="slider" id="slider">
      <div class="slider__track">{slide_html}</div>
      <button class="slider__btn slider__btn--prev" type="button" aria-label="Slide trước">‹</button>
      <button class="slider__btn slider__btn--next" type="button" aria-label="Slide sau">›</button>
      <div class="slider__dots" role="tablist"></div>
    </div>
  </div>
</section>
<section class="usp">
  <div class="container usp__grid">
    <div class="usp__item"><span class="usp__icon">13+</span><div><h3>Năm kinh nghiệm</h3><p>Hoạt động từ năm 2013, am hiểu ngành nhựa và nguyên liệu.</p></div></div>
    <div class="usp__item"><span class="usp__icon">⚙</span><div><h3>Sản xuất trực tiếp</h3><p>Đầu tư máy móc, thiết bị và công nghệ từ năm 2018.</p></div></div>
    <div class="usp__item"><span class="usp__icon">◎</span><div><h3>Giải pháp theo ngành</h3><p>Phù hợp từng dây chuyền và phương pháp đóng gói.</p></div></div>
    <div class="usp__item"><span class="usp__icon">✓</span><div><h3>Đối tác kỹ thuật</h3><p>Đồng hành từ chọn vật liệu đến hoàn thiện bao bì.</p></div></div>
  </div>
</section>
<section class="section about">
  <div class="container about__grid">
    <div class="about__text reveal">
      <span class="eyebrow eyebrow--dark">Giới thiệu công ty</span>
      <h2 class="title">Từ nền tảng thương mại đến <span class="hl">sản xuất bao bì chuyên nghiệp</span></h2>
      {ABOUT_INTRO_P}
      {STATS}
      <a class="btn btn--brand" href="{url("about")}">Xem giới thiệu đầy đủ</a>
    </div>
    {about_media()}
  </div>
</section>
<section class="section section--alt" id="san-pham-noi-bat">
  <div class="container">
    <div class="section__head">
      <div><span class="eyebrow eyebrow--dark">Sản phẩm</span><h2 class="title">Bao bì PA/PE và túi hút chân không</h2></div>
      <a class="link-more" href="{url("products")}">Tất cả sản phẩm →</a>
    </div>
    {tabs_and_grid(limit=8)}
  </div>
</section>
<section class="section" id="giai-phap">
  <div class="container">
    <div class="section__head"><div><span class="eyebrow eyebrow--dark">Giải pháp theo ngành hàng</span><h2 class="title">Bao bì phù hợp từng dây chuyền đóng gói</h2></div><a class="link-more" href="{url("solutions")}">Tất cả giải pháp →</a></div>
    <div class="services">{sol_html}</div>
  </div>
</section>
<section class="workshop">
  <div class="container workshop__grid">
    <div class="workshop__intro">
      <span class="eyebrow">Quy trình làm việc</span>
      <h2>Từ nhu cầu thực tế đến bao bì hoàn thiện</h2>
      <p>Mỗi đơn hàng bắt đầu từ việc hiểu sản phẩm, dây chuyền và cách bảo quản của khách hàng.</p>
      <a class="btn btn--light" href="{url("solutions", "quy-trinh")}">Xem quy trình</a>
    </div>
    {steps_html()}
  </div>
</section>
<section class="partners" aria-label="Ngành hàng phục vụ"><div class="marquee"><div class="marquee__track">{marquee}</div></div></section>
<section class="section" id="tin-tuc">
  <div class="container">
    <div class="section__head"><div><span class="eyebrow eyebrow--dark">Kiến thức bao bì</span><h2 class="title">Tin tức mới nhất</h2></div><a class="link-more" href="{url("news")}">Tất cả tin tức →</a></div>
    <div class="news">{news_html}</div>
  </div>
</section>
{cta_band()}'''
    site_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"], "url": SITE["url"]}
    return page("home", f"{SITE['name']} – Bao bì PA/PE, túi hút chân không tại Tây Ninh",
                "Vĩnh Lộc Plastic chuyên sản xuất bao bì PA/PE, túi hút chân không cho công nghiệp và nông nghiệp. Xưởng tại Tây Ninh, nhận làm theo yêu cầu, giao toàn quốc.",
                body, [ORG, site_ld])


# ---------------------------------------------------------------- Giới thiệu (gộp 3 phần)
def build_about():
    crumb, crumb_ld = breadcrumb([("Trang chủ", "home"), ("Giới thiệu", "about")])
    subnav = [("ve-chung-toi", "Về chúng tôi"), ("hanh-trinh", "Hành trình phát triển"), ("khach-hang", "Khách hàng là trọng tâm"),
              ("tam-nhin", "Tầm nhìn &amp; cam kết"), ("thong-tin", "Thông tin doanh nghiệp")]
    sub = "".join(f'<a href="#{i}">{t}</a>' for i, t in subnav)
    body = page_hero(crumb, "Giới thiệu công ty", "Giới thiệu Vĩnh Lộc Plastic",
                     "Hành trình phát triển từ nền tảng thương mại đến sản xuất bao bì chuyên nghiệp.",
                     svg_pouch(("#FFFFFF", "#F7EBD3", "#9E1815"))) + f'''
<nav class="subnav" aria-label="Mục trong trang"><div class="container subnav__inner">{sub}</div></nav>
<section class="section about" id="ve-chung-toi">
  <div class="container about__grid">
    <div class="about__text reveal">
      <span class="eyebrow eyebrow--dark">Về chúng tôi</span>
      <h2 class="title">Từ nền tảng thương mại đến <span class="hl">sản xuất bao bì chuyên nghiệp</span></h2>
      {ABOUT_INTRO_P}
      {STATS}
    </div>
    {about_media()}
  </div>
</section>
<section class="section section--alt" id="hanh-trinh">
  <div class="container">
    <div class="section__head section__head--center"><span class="eyebrow eyebrow--dark">Hành trình phát triển</span><h2 class="title">Bước ngoặt năm 2018: từ thương mại đến sản xuất</h2></div>
    {TIMELINE}
  </div>
</section>
<section class="section" id="khach-hang">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow eyebrow--dark">Lấy nhu cầu khách hàng làm trọng tâm</span>
      <h2 class="title">Giá trị không chỉ nằm ở sản phẩm</h2>
      <p>Vĩnh Lộc Plastic luôn xác định giá trị của doanh nghiệp không chỉ nằm ở sản phẩm, mà còn ở khả năng đáp ứng hiệu quả nhu cầu thực tế của khách hàng.</p>
      <p>Công ty phát triển các giải pháp bao bì phù hợp với từng ngành hàng, dây chuyền sản xuất và phương pháp đóng gói, đặc biệt trong lĩnh vực nông sản và thực phẩm.</p>
    </div>
    <ul class="checklist reveal">
      <li><b>Theo ngành hàng</b><span>Nông sản, thực phẩm chế biến, đông lạnh, công nghiệp.</span></li>
      <li><b>Theo dây chuyền</b><span>Kích thước, độ dày tương thích máy đóng gói của khách.</span></li>
      <li><b>Theo phương pháp đóng gói</b><span>Hút chân không, hàn miệng, lót thùng, quấn cuộn.</span></li>
    </ul>
  </div>
</section>
<section class="section section--alt" id="tam-nhin">
  <div class="container">
    <div class="section__head section__head--center"><span class="eyebrow eyebrow--dark">Tầm nhìn và định hướng</span><h2 class="title">Công nghệ – Chất lượng – Khách hàng</h2></div>
    {PILLARS}
    {PLEDGE}
  </div>
</section>
<section class="section" id="thong-tin">
  <div class="container">
    <div class="section__head section__head--center"><span class="eyebrow eyebrow--dark">Vinhloc Plastic</span><h2 class="title">Thông tin doanh nghiệp</h2></div>
    <div class="company-card reveal">
      <table>
        <tr><th scope="row">Tên công ty</th><td>{e(SITE["legal_name"])}</td></tr>
        <tr><th scope="row">Lĩnh vực</th><td>Chuyên cung cấp bao bì PA/PE, túi hút chân không</td></tr>
        <tr><th scope="row">Địa chỉ</th><td>{e(SITE["address"])}</td></tr>
        <tr><th scope="row">Website</th><td>{SITE["website"]}</td></tr>
        <tr><th scope="row">Email</th><td><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></td></tr>
        <tr><th scope="row">Điện thoại / Zalo</th><td><a href="tel:{SITE["phone"]}">{SITE["phone_display"]}</a></td></tr>
        <tr><th scope="row">Mã số thuế</th><td>{SITE["tax_id"]}</td></tr>
      </table>
    </div>
  </div>
</section>
{cta_band()}'''
    about_ld = {"@context": "https://schema.org", "@type": "AboutPage", "name": "Giới thiệu Vĩnh Lộc Plastic",
                "url": SITE["url"] + path("about"), "mainEntity": ORG}
    return page("about", "Giới thiệu Vĩnh Lộc Plastic – Hành trình từ 2013 đến nay",
                "Vĩnh Lộc Plastic thành lập năm 2013, trực tiếp sản xuất bao bì nhựa từ 2018. Phát triển trên ba nền tảng Công nghệ – Chất lượng – Khách hàng.",
                body, [crumb_ld, about_ld])


# ---------------------------------------------------------------- Tất cả sản phẩm
def build_products():
    crumb, crumb_ld = breadcrumb([("Trang chủ", "home"), ("Sản phẩm", "products")])
    cat_cards = "".join(f'''<a class="cat-card reveal" href="{url("cat:" + c["slug"])}">
  <div class="cat-card__media" style="background:{PALETTE[c["color"]][2]}">{cat_art(c)}</div>
  <div class="cat-card__body"><h2>{e(c["name"])}</h2><p>{e(c["desc"])}</p><span class="link-more">Xem danh mục →</span></div>
</a>''' for c in CATEGORIES)
    body = page_hero(crumb, "Sản phẩm", "Sản phẩm bao bì Vĩnh Lộc Plastic",
                     "Bao bì PA/PE, túi hút chân không, bao bì thực phẩm, nông sản và công nghiệp. Sản xuất theo kích thước, độ dày và in ấn theo yêu cầu.",
                     svg_vacuum(PALETTE["red"], "block")) + f'''
<section class="section">
  <div class="container">
    <div class="section__head"><div><span class="eyebrow eyebrow--dark">Danh mục</span><h2 class="title">Chọn danh mục sản phẩm</h2></div></div>
    <div class="cat-grid">{cat_cards}</div>
  </div>
</section>
<section class="section section--alt" id="tat-ca">
  <div class="container">
    <div class="section__head"><div><span class="eyebrow eyebrow--dark">Tất cả sản phẩm</span><h2 class="title">{len(PRODUCTS)} sản phẩm đang cung cấp</h2></div></div>
    {tabs_and_grid(limit=0, show_foot=False)}
  </div>
</section>
{cta_band()}'''
    return page("products", "Sản phẩm bao bì PA/PE, túi hút chân không | Vĩnh Lộc Plastic",
                "Danh mục sản phẩm Vĩnh Lộc Plastic: túi hút chân không PA/PE, bao bì thực phẩm, bao bì nông sản, bao bì công nghiệp. Sản xuất theo yêu cầu tại Tây Ninh.",
                body, [crumb_ld])


# ---------------------------------------------------------------- Trang danh mục
def build_category(c):
    key = "cat:" + c["slug"]
    crumb, crumb_ld = breadcrumb([("Trang chủ", "home"), ("Sản phẩm", "products"), (c["name"], key)])
    items = [p for p in PRODUCTS if p[1] == c["slug"]]
    cards = "\n".join(card(p, show_cat=False) for p in items)
    uses = "".join(f"<li>{e(u)}</li>" for u in c["uses"])
    specs = "".join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k, v in c["specs"])
    others = "".join(f'<a class="chip" href="{url("cat:" + o["slug"])}">{dot(o)}{e(o["name"])}</a>' for o in CATEGORIES if o is not c)
    actions = '<div class="slide__cta"><button class="btn btn--light" type="button" data-open-modal>Nhận báo giá</button><a class="btn btn--ghost-light" href="#san-pham">Xem sản phẩm</a></div>'
    body = page_hero(crumb, "Danh mục sản phẩm", c["name"], c["lead"], cat_art(c), actions) + f'''
<section class="section" id="san-pham">
  <div class="container">
    <div class="section__head"><div><span class="eyebrow eyebrow--dark">{len(items)} sản phẩm</span><h2 class="title">Sản phẩm thuộc danh mục {e(c["name"])}</h2></div></div>
    <div class="grid-products">{cards}</div>
  </div>
</section>
<section class="section section--alt">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow eyebrow--dark">Ứng dụng</span>
      <h2 class="title">{e(c["name"])} dùng cho</h2>
      <ul class="bullets">{uses}</ul>
    </div>
    <div class="company-card reveal">
      <h2 class="company-card__h">Thông số tham khảo</h2>
      <table>{specs}</table>
      <p class="note">Kích thước, độ dày và in ấn được tư vấn theo từng đơn hàng.</p>
    </div>
  </div>
</section>
<section class="section section--tight">
  <div class="container">
    <h2 class="title title--sm">Danh mục khác</h2>
    <div class="chips">{others}</div>
  </div>
</section>
{cta_band()}'''
    coll_ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": c["name"],
               "description": c["desc"], "url": SITE["url"] + path(key),
               "mainEntity": {"@type": "ItemList", "itemListElement": [
                   {"@type": "ListItem", "position": i + 1, "name": p[0]} for i, p in enumerate(items)]}}
    return page(key, f'{c["title"]} | {SITE["name"]}', c["desc"], body, [crumb_ld, coll_ld])


# ---------------------------------------------------------------- Xuất file

# ---------------------------------------------------------------- Giải pháp
def build_solutions():
    crumb, crumb_ld = breadcrumb([("Trang chủ", "home"), ("Giải pháp", "solutions")])
    jump = "".join(f'<a href="#{x["slug"]}">{e(x["tag"])}</a>' for x in SOLUTIONS) + '<a href="#quy-trinh">Quy trình</a>'
    blocks = ""
    arts = {"nong-san": svg_vacuum(PALETTE["rice"], "grain"), "thuc-pham": svg_pouch(PALETTE["gold"]),
            "dong-lanh": svg_vacuum(PALETTE["red"], "block"), "cong-nghiep": svg_roll(PALETTE["coal"])}
    for i, x in enumerate(SOLUTIONS):
        c = CAT[x["category"]]
        items = [pr for pr in PRODUCTS if pr[1] == x["category"]]
        chips = "".join(f'<li>{e(pr[0])}</li>' for pr in items)
        approach = "".join(f"<li>{e(a)}</li>" for a in x["approach"])
        blocks += f'''<section class="solution{" solution--flip" if i % 2 else ""}" id="{x["slug"]}">
  <div class="container solution__inner">
    <div class="solution__art reveal" style="background:{PALETTE[c["color"]][2]}">{arts[x["slug"]]}</div>
    <div class="solution__body reveal">
      <span class="service__tag">{e(x["tag"])}</span>
      <h2 class="title">{e(x["title"])}</h2>
      <p class="solution__for">Dành cho: {e(x["for"])}</p>
      <div class="solution__grid">
        <div><h3>Thách thức</h3><p>{e(x["challenge"])}</p></div>
        <div><h3>Giải pháp đề xuất</h3><ul class="bullets">{approach}</ul></div>
      </div>
      <h3>Sản phẩm phù hợp</h3>
      <ul class="tags">{chips}</ul>
      <div class="solution__cta">
        <a class="btn btn--brand" href="{url("cat:" + c["slug"])}">Xem danh mục {e(c["name"])}</a>
        <button class="btn btn--outline" type="button" data-open-modal data-product="Giải pháp: {e(x["title"])}">Nhận tư vấn</button>
      </div>
    </div>
  </div>
</section>'''
    body = page_hero(crumb, "Giải pháp theo ngành hàng", "Giải pháp bao bì cho từng ngành hàng",
                     "Mỗi ngành hàng có cách bảo quản và dây chuyền đóng gói riêng. Vĩnh Lộc Plastic tư vấn vật liệu, kích thước và độ dày phù hợp cho nông sản, thực phẩm, hàng đông lạnh và nhà máy.",
                     svg_roll(("#BF8217", "#E2B867", "#2B2422"))) + f'''
<nav class="subnav" aria-label="Mục trong trang"><div class="container subnav__inner">{jump}</div></nav>
{blocks}
<section class="workshop" id="quy-trinh">
  <div class="container workshop__grid">
    <div class="workshop__intro">
      <span class="eyebrow">Quy trình làm việc</span>
      <h2>Từ nhu cầu thực tế đến bao bì hoàn thiện</h2>
      <p>Mỗi đơn hàng bắt đầu từ việc hiểu sản phẩm, dây chuyền và cách bảo quản của khách hàng.</p>
      <button class="btn btn--light" type="button" data-open-modal>Liên hệ tư vấn</button>
    </div>
    {steps_html()}
  </div>
</section>
{cta_band()}'''
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Giải pháp bao bì theo ngành hàng",
          "url": SITE["url"] + path("solutions"), "about": [x["title"] for x in SOLUTIONS]}
    return page("solutions", "Giải pháp bao bì cho nông sản, thực phẩm, đông lạnh | Vĩnh Lộc Plastic",
                "Giải pháp bao bì PA/PE, túi hút chân không theo ngành hàng: nông sản khô, thực phẩm chế biến, thịt và thủy sản đông lạnh, nhà máy và kho vận.",
                body, [crumb_ld, ld])


# ---------------------------------------------------------------- Tin tức
def build_news():
    crumb, crumb_ld = breadcrumb([("Trang chủ", "home"), ("Tin tức", "news")])
    first, rest = NEWS[0], NEWS[1:]
    href = url("post:" + first["slug"])
    feature = f'''<article class="feature reveal">
  <a href="{href}" class="feature__media" tabindex="-1" aria-hidden="true">{post_thumb(first)}</a>
  <div class="feature__body">
    <span class="eyebrow eyebrow--dark">Bài mới nhất</span>
    <h2><a href="{href}">{e(first["title"])}</a></h2>
    <p>{e(first["excerpt"])}</p>
    <a class="btn btn--brand" href="{href}">Đọc bài viết</a>
  </div>
</article>'''
    cards = "".join(post_card(n, "h2") for n in rest)
    body = page_hero(crumb, "Kiến thức bao bì", "Tin tức và kiến thức bao bì",
                     "Hướng dẫn chọn vật liệu, độ dày và cách bảo quản bằng túi hút chân không, từ kinh nghiệm sản xuất của Vĩnh Lộc Plastic.",
                     svg_flat(PALETTE["gold"])) + f'''
<section class="section">
  <div class="container">
    {feature}
    <div class="news news--list">{cards}</div>
  </div>
</section>
{cta_band()}'''
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Tin tức và kiến thức bao bì",
          "url": SITE["url"] + path("news"),
          "mainEntity": {"@type": "ItemList", "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "url": SITE["url"] + path("post:" + n["slug"]), "name": n["title"]}
              for i, n in enumerate(NEWS)]}}
    return page("news", "Tin tức, kiến thức bao bì PA/PE và túi hút chân không | Vĩnh Lộc Plastic",
                "Kiến thức bao bì từ Vĩnh Lộc Plastic: túi PA/PE là gì, cách chọn độ dày túi hút chân không, bảo quản nông sản khô đúng cách.",
                body, [crumb_ld, ld])


def build_post(n):
    key = "post:" + n["slug"]
    crumb, crumb_ld = breadcrumb([("Trang chủ", "home"), ("Tin tức", "news"), (n["title"], key)])
    others = "".join(post_card(o) for o in NEWS if o is not n)
    related = [c for c in CATEGORIES if c["slug"] in ("tui-hut-chan-khong-pa-pe", "bao-bi-nong-san")]
    rel = "".join(f'<li><a href="{url("cat:" + c["slug"])}">{dot(c)}{e(c["name"])}</a></li>' for c in related)
    body = f'''<article class="article">
  <header class="article__head">
    <div class="container container--narrow">
      {crumb}
      <h1>{e(n["title"])}</h1>
      <p class="article__meta"><time datetime="{n["date"]}">{vn_date(n["date"])}</time> · {e(SITE["name"])}</p>
      <p class="article__lead">{e(n["excerpt"])}</p>
    </div>
  </header>
  <div class="container article__layout">
    <div class="prose">{render_blocks(n["body"])}</div>
    <aside class="article__aside">
      <div class="aside-card">
        <h2>Cần tư vấn bao bì?</h2>
        <p>Gửi sản phẩm và cách đóng gói của bạn, chúng tôi đề xuất loại túi và độ dày phù hợp.</p>
        <button class="btn btn--cta btn--block" type="button" data-open-modal data-product="Tư vấn sau bài: {e(n["title"])}">Nhận tư vấn</button>
        <p class="aside-card__phone">Hoặc gọi <a href="tel:{SITE["phone"]}">{SITE["phone_display"]}</a></p>
      </div>
      <div class="aside-card">
        <h2>Sản phẩm liên quan</h2>
        <ul class="aside-links">{rel}</ul>
      </div>
    </aside>
  </div>
</article>
<section class="section section--alt">
  <div class="container">
    <div class="section__head"><div><span class="eyebrow eyebrow--dark">Đọc thêm</span><h2 class="title">Bài viết khác</h2></div><a class="link-more" href="{url("news")}">Tất cả tin tức →</a></div>
    <div class="news news--two">{others}</div>
  </div>
</section>
{cta_band()}'''
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": n["title"], "description": n["excerpt"],
          "datePublished": n["date"], "dateModified": n["date"], "inLanguage": "vi",
          "mainEntityOfPage": SITE["url"] + path(key),
          "author": {"@type": "Organization", "name": SITE["name"], "url": SITE["url"]},
          "publisher": {"@type": "Organization", "name": SITE["name"],
                        "logo": {"@type": "ImageObject", "url": SITE["url"] + "/img/logo-vinhloc.png"}}}
    return page(key, f'{n["title"]} | {SITE["name"]}', n["excerpt"], body, [crumb_ld, ld])


# ---------------------------------------------------------------- Liên hệ
def build_contact():
    crumb, crumb_ld = breadcrumb([("Trang chủ", "home"), ("Liên hệ", "contact")])
    maps = "https://www.google.com/maps/search/?api=1&query=" + quote(SITE["address"])
    if MODE == "artifact":
        # Trang xem online không nhúng được bản đồ: thay bằng thẻ mở Google Maps
        map_html = f'''<a class="map-card" href="{maps}" target="_blank" rel="noopener">
  <span class="map-card__pin">📍</span><span><b>Xem đường đi trên Google Maps</b><br>{e(SITE["address"])}</span></a>'''
    else:
        embed = "https://www.google.com/maps?q=" + quote(SITE["address"]) + "&output=embed"
        map_html = f'''<div class="map-frame"><iframe src="{embed}" title="Bản đồ: {e(SITE["address"])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
<p class="map-link"><a href="{maps}" target="_blank" rel="noopener">Mở trong Google Maps →</a></p>'''
    options = "".join(f"<option>{e(c['name'])}</option>" for c in CATEGORIES)
    body = page_hero(crumb, "Liên hệ", "Liên hệ Vĩnh Lộc Plastic",
                     "Gọi điện, nhắn Zalo hoặc gửi yêu cầu bên dưới. Hãy cho chúng tôi biết sản phẩm, kích thước và số lượng để được báo giá nhanh.",
                     svg_pouch(("#FFFFFF", "#F7EBD3", "#9E1815"))) + f'''
<section class="section">
  <div class="container contact">
    <div class="contact__info">
      <h2 class="title">Thông tin liên hệ</h2>
      <ul class="contact-list">
        <li><span class="contact-list__icon">☎</span><div><b>Điện thoại / Zalo</b><a href="tel:{SITE["phone"]}" class="contact-list__big">{SITE["phone_display"]}</a>
          <div class="contact-list__actions"><a class="btn btn--cta btn--sm" href="tel:{SITE["phone"]}">Gọi ngay</a><a class="btn btn--outline btn--sm" href="https://zalo.me/{SITE["phone"]}" target="_blank" rel="noopener">Nhắn Zalo</a><button class="btn btn--ghost btn--sm" type="button" data-copy="{SITE["phone_display"]}">Sao chép số</button></div></div></li>
        <li><span class="contact-list__icon">✉</span><div><b>Email</b><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></div></li>
        <li><span class="contact-list__icon">⌂</span><div><b>Địa chỉ</b><span>{e(SITE["address"])}</span></div></li>
        <li><span class="contact-list__icon">#</span><div><b>Mã số thuế</b><span>{SITE["tax_id"]}</span></div></li>
      </ul>
      {map_html}
    </div>
    <div class="contact__form">
      <h2 class="title">Gửi yêu cầu báo giá</h2>
      <p class="muted">Các mục có dấu * là bắt buộc.</p>
      <form class="form form--page" id="pageForm" data-demo-form>
        <div class="form__row">
          <label>Họ tên*<input required name="name" id="cName" autocomplete="name"></label>
          <label>Công ty / cơ sở<input name="company" id="cCompany" autocomplete="organization"></label>
        </div>
        <div class="form__row">
          <label>Số điện thoại / Zalo*<input required name="phone" type="tel" id="cPhone" autocomplete="tel"></label>
          <label>Email<input name="email" type="email" id="cEmail" autocomplete="email"></label>
        </div>
        <div class="form__row">
          <label>Sản phẩm quan tâm<select name="product" id="cProduct">{options}<option>Khác</option></select></label>
          <label>Số lượng dự kiến<input name="qty" id="cQty" placeholder="Ví dụ: 10.000 túi/tháng"></label>
        </div>
        <label>Kích thước, độ dày, yêu cầu in ấn<textarea name="note" rows="5" id="cNote" placeholder="Ví dụ: túi 20×30 cm, 90 µm, in logo 1 màu"></textarea></label>
        <button class="btn btn--cta">Gửi yêu cầu</button>
      </form>
      <ol class="next-steps">
        <li><b>Liên hệ lại</b><span>Nhân viên gọi hoặc nhắn Zalo để làm rõ nhu cầu.</span></li>
        <li><b>Tư vấn và lấy mẫu</b><span>Đề xuất vật liệu, kích thước, độ dày phù hợp.</span></li>
        <li><b>Báo giá</b><span>Gửi báo giá theo số lượng và yêu cầu in ấn.</span></li>
      </ol>
    </div>
  </div>
</section>'''
    contact_org = dict(ORG)
    contact_org["contactPoint"] = {"@type": "ContactPoint", "telephone": ORG["telephone"], "email": SITE["email"],
                                   "contactType": "sales", "areaServed": "VN", "availableLanguage": "vi"}
    ld = {"@context": "https://schema.org", "@type": "ContactPage", "name": "Liên hệ Vĩnh Lộc Plastic",
          "url": SITE["url"] + path("contact"), "mainEntity": contact_org}
    return page("contact", "Liên hệ Vĩnh Lộc Plastic – Báo giá bao bì PA/PE, túi hút chân không",
                f"Liên hệ Vĩnh Lộc Plastic qua điện thoại/Zalo {SITE['phone_display']} hoặc email. Xưởng tại Mỹ Hạnh, Tây Ninh. Gửi yêu cầu để nhận báo giá bao bì.",
                body, [crumb_ld, ld])


def inline_assets(htm):
    """Bản artifact: nhúng CSS, JS, ảnh thẳng vào trang (trang xem online chặn file CSS rời)."""
    css = lambda f: (ROOT / "assets" / f).read_text(encoding="utf-8")
    png = lambda f: "data:image/png;base64," + base64.b64encode((ROOT / "assets" / f).read_bytes()).decode()
    htm = re.sub(r'<link rel="stylesheet" href="(css/[^"]+)">', lambda m: f"<style>\n{css(m.group(1))}\n</style>", htm)
    htm = htm.replace('<script src="js/main.js"></script>', f"<script>\n{css('js/main.js')}\n</script>")
    htm = re.sub(r'(src|href)="(img/[^"]+\.png)"', lambda m: f'{m.group(1)}="{png(m.group(2))}"', htm)
    assert 'href="css/' not in htm and 'src="js/' not in htm and '"img/' not in htm
    return htm

def main():
    global CURRENT
    if OUT.exists(): shutil.rmtree(OUT)
    builders = [("home", build_home), ("about", build_about), ("products", build_products)] + \
               [("cat:" + c["slug"], lambda c=c: build_category(c)) for c in CATEGORIES] + \
               [("solutions", build_solutions), ("news", build_news)] + \
               [("post:" + n["slug"], lambda n=n: build_post(n)) for n in NEWS] + \
               [("contact", build_contact)]
    pages = {}
    for key, fn in builders:
        CURRENT = key
        pages[key] = fn()
    for k, htm in pages.items():
        if MODE == "artifact": htm = inline_assets(htm)
        f = out_file(k); f.parent.mkdir(parents=True, exist_ok=True); f.write_text(htm, encoding="utf-8")
    if MODE != "artifact":
        for d in ("css", "js", "img"):
            shutil.copytree(ROOT / "assets" / d, OUT / d)
    else:
        # Trang chính của artifact không có <html>/<head>/<body> riêng
        h = (OUT / "index.html").read_text(encoding="utf-8")
        head = re.search(r"<head>(.*)</head>", h, re.S).group(1)
        head = re.sub(r'<meta charset[^>]*>\s*|<meta name="viewport"[^>]*>\s*', "", head)
        body = re.search(r"<body>(.*)</body>", h, re.S).group(1)
        (OUT / "_home.html").write_text(head.strip() + "\n" + body, encoding="utf-8")
    if MODE == "public":
        urls = "".join(f"<url><loc>{SITE['url']}{path(k)}</loc></url>" for k in pages)
        (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
        (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n", encoding="utf-8")
    print(f"Đã tạo {len(pages)} trang trong {OUT.name}/")
    for k in pages: print(" ", path(k), "->", out_file(k).relative_to(OUT))

if __name__ == "__main__":
    main()
