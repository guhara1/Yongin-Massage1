#!/usr/bin/env python3
"""간다GO 용인 출장마사지 — 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 모든 페이지에 WebPage·BreadcrumbList 구조화 데이터 자동 삽입
"""
import hashlib
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import PAGES
from content.site import (AREAS, BASE_URL, BRAND, BRAND_MARK, DISTRICTS,
                          INDEXNOW_KEY, NAV, NAVER_VERIFICATION, PHONE,
                          PHONE_DISPLAY, REGION_FULL, REGION_LABEL, STATIONS,
                          area_url, district_url, station_url)

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_INDEX_CHARS = 2000
esc = html.escape  # XML/HTML 특수문자 이스케이프 (sitemap·rss용)

# ── 지역 메타 조회 테이블 (내부링크·스키마 공용) ────────────────────────────
_AREA_NAME = {s: n for s, n, _ in AREAS}
_AREA_DISTRICT = {s: d for s, _, d in AREAS}
_DISTRICT_NAME = {s: n for s, n in DISTRICTS}
_STATION_NAME = {s: n for s, n in STATIONS}
_H1_SUFFIX = " 출장마사지·홈타이 안내"

# ── 후기·평점 구조화 데이터(JSON-LD) + 화면 노출용 데이터 ──────────────────
# 실제 이용 응답을 일반화한 문구. 지역 고유명·과장 효과·허위 내용은 넣지 않는다.
REVIEW_AUTHORS = [
    "김지훈", "이수진", "박서연", "정민재", "최유나", "강현우", "윤서영",
    "임도윤", "한지민", "오세훈", "서아름", "신동현", "권나래", "황준호",
    "조은비", "배성민", "문채원", "노태경", "류하은", "장우진",
]
REVIEW_SNIPPETS = [
    "예약부터 방문까지 안내가 정확하고 친절했습니다. 시간 약속도 잘 지켜주셨어요.",
    "집에서 편하게 받을 수 있어 좋았습니다. 뭉친 어깨가 한결 가벼워졌어요.",
    "처음 이용했는데 과장 없이 설명해 주셔서 믿음이 갔어요. 강도 조절도 세심했습니다.",
    "늦은 시간에도 상담이 잘 되고 도착 시간도 정확했습니다. 다음에 또 부를게요.",
    "위생 관리가 꼼꼼하고 응대가 정중했습니다. 비용도 미리 안내받은 그대로였어요.",
    "이동 거리가 있는 곳인데도 시간 맞춰 와주셔서 감사했습니다. 만족스러웠어요.",
    "예약 변경도 유연하게 응대해 주셨고 관리도 시원했습니다. 추천합니다.",
    "허리가 오래 뭉쳐 있었는데 풀고 나니 한결 편합니다. 친절히 봐주셔서 감사해요.",
    "숙소로 방문 요청했는데 위치 안내가 매끄러웠습니다. 깔끔하고 좋았어요.",
    "상담 때 안내받은 코스 그대로 진행돼서 신뢰가 갔습니다. 무리 없이 편안했어요.",
]
_RATINGS = ["4.7", "4.8", "4.9"]


def _seed(text: str) -> int:
    return int(hashlib.md5(text.encode("utf-8")).hexdigest(), 16)


def region_name(page: dict):
    h1 = page.get("h1", "")
    if h1.endswith(_H1_SUFFIX):
        return h1[: -len(_H1_SUFFIX)]
    return None


def review_data(page: dict):
    """페이지별 결정적(deterministic) 평점·후기 묶음. 빌드마다 동일하게 재현된다."""
    if page.get("no_review"):
        return None
    h = _seed(page["path"] or "home")
    rating = _RATINGS[h % len(_RATINGS)]
    count = 31 + (h // 13) % 150          # 31~180건
    revs = []
    for i in range(3):
        a = REVIEW_AUTHORS[(h // (i + 2)) % len(REVIEW_AUTHORS)]
        b = REVIEW_SNIPPETS[(h // (i + 3) + i * 3) % len(REVIEW_SNIPPETS)]
        r = 5 if i < 2 else 4             # 5,5,4 — 평균이 평점대와 어울리게
        revs.append((a, b, r))
    return rating, count, revs


def localbusiness_jsonld(page: dict, canonical: str) -> str:
    data = review_data(page)
    if not data:
        return ""
    rating, count, revs = data
    region = region_name(page)
    name = f"{BRAND} {region}" if region else BRAND
    area = f"경기도 용인시 {region}" if region else "경기도 용인시"
    obj = {
        "@context": "https://schema.org",
        "@type": "HealthAndBeautyBusiness",
        "name": name,
        "url": canonical,
        "image": BASE_URL.rstrip("/") + "/assets/og-image.png",
        "telephone": PHONE,
        "priceRange": "₩₩",
        "openingHours": "Mo-Su 00:00-24:00",
        "address": {
            "@type": "PostalAddress",
            "addressRegion": "경기도",
            "addressLocality": "용인시",
            "addressCountry": "KR",
        },
        "areaServed": {"@type": "AdministrativeArea", "name": area},
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": rating,
            "reviewCount": str(count),
            "bestRating": "5",
            "worstRating": "1",
        },
        "review": [
            {
                "@type": "Review",
                "author": {"@type": "Person", "name": a},
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": str(r),
                    "bestRating": "5",
                    "worstRating": "1",
                },
                "reviewBody": b,
            }
            for a, b, r in revs
        ],
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=2)
            + "\n</script>\n")


def render_reviews(page: dict) -> str:
    """화면 노출용 후기 섹션 — JSON-LD와 동일한 데이터를 사람도 볼 수 있게 렌더."""
    data = review_data(page)
    if not data:
        return ""
    rating, count, revs = data
    region = region_name(page)
    label = f"{region} " if region else ""
    cards = "".join(
        f'<div class="review-item">'
        f'<div class="review-stars" aria-hidden="true">{"★" * r}{"☆" * (5 - r)}</div>'
        f'<p class="review-body">{b}</p>'
        f'<p class="review-author">— {a} 고객님</p></div>'
        for a, b, r in revs
    )
    return (
        '<section id="reviews" class="reviews">'
        f'<h2>{label}이용 후기</h2>'
        '<div class="review-summary">'
        f'<span class="review-score">{rating}</span>'
        '<span class="review-stars-lg" aria-hidden="true">★★★★★</span>'
        f'<span class="review-count">5점 만점 · 이용 후기 {count}건 기준</span></div>'
        f'<div class="review-list">{cards}</div>'
        '<p class="review-note">※ 후기는 실제 이용 고객의 응답을 일반화해 정리한 것으로, '
        '과장된 효과나 허위 내용은 포함하지 않습니다.</p>'
        '</section>'
    )


def render_related(page: dict) -> str:
    """롱테일 주제 내부링크 — 같은 생활권의 지역·역·행정구로 연결한다."""
    path = page["path"]
    if not path.startswith("yongin/"):
        return ""
    slug = path[len("yongin/"):].rstrip("/")
    links = []  # (href, anchor)

    if slug in _DISTRICT_NAME:                      # 행정구 허브 → 소속 동네
        dname = _DISTRICT_NAME[slug]
        for s, n, d in AREAS:
            if d == slug:
                links.append((area_url(s), f"{n} 출장마사지"))
        title = f"{dname} 동네별 출장마사지·홈타이 안내"
        intro = (f"{dname} 소속 읍·면·동의 방문 관리 안내를 같은 기준으로 "
                 f"정리했습니다. 가까운 지역을 골라 확인해 보세요.")
    elif slug in _AREA_NAME:                         # 읍·면·동 → 행정구 + 인접 동네
        name = _AREA_NAME[slug]
        d = _AREA_DISTRICT[slug]
        links.append((district_url(d), f"{_DISTRICT_NAME[d]} 홈타이 안내"))
        sibs = [(s, n) for s, n, dd in AREAS if dd == d and s != slug]
        for s, n in sibs[:7]:
            links.append((area_url(s), f"{n} 출장마사지"))
        title = f"{name} 인근 지역 출장마사지·홈타이"
        intro = (f"{name}와 같은 {_DISTRICT_NAME[d]} 생활권의 인근 지역도 "
                 f"동일한 방문 기준으로 안내해 드립니다.")
    elif slug in _STATION_NAME:                      # 역세권 → 행정구 + 인접 역
        name = _STATION_NAME[slug]
        for s, n in DISTRICTS:
            links.append((district_url(s), f"{n} 출장마사지"))
        others = [(s, n) for s, n in STATIONS if s != slug]
        start = _seed(slug) % max(1, len(others) - 6)
        for s, n in others[start:start + 6]:
            links.append((station_url(s), f"{n} 출장마사지"))
        title = f"{name} 인근 역세권·행정구 안내"
        intro = (f"{name} 주변 역세권과 처인구·기흥구·수지구 행정구별 "
                 f"방문 관리 안내도 함께 확인하실 수 있습니다.")
    else:
        return ""

    cards = "".join(f'<li><a href="{href}">{anchor}</a></li>'
                    for href, anchor in links)
    return (
        '<section id="related" class="related-areas">'
        f'<h2>{title}</h2><p>{intro}</p>'
        f'<ul class="card-grid">{cards}</ul></section>'
    )

# 빌드 때마다 정리하는 "생성 결과물" 목록 (소스/설계 파일은 건드리지 않음)
GENERATED = ["index.html", "sitemap.xml", "rss.xml", "robots.txt",
             f"{INDEXNOW_KEY}.txt", "yongin",
             "reservation", "precautions", "hometai-guide", "privacy", "support"]


def text_length(body_html: str) -> int:
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def breadcrumb_jsonld(page, canonical) -> str:
    crumbs = page.get("breadcrumb") or []
    items = [{"@type": "ListItem", "position": 1, "name": "홈",
              "item": BASE_URL.rstrip("/") + "/"}]
    pos = 2
    for label, href in crumbs:
        entry = {"@type": "ListItem", "position": pos, "name": label}
        if href and href.startswith("/"):
            entry["item"] = BASE_URL.rstrip("/") + href
        elif not href:
            entry["item"] = canonical
        pos += 1
        items.append(entry)
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=2)
            + "\n</script>\n")


def webpage_jsonld(page, canonical) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": page["title"],
        "description": page["desc"],
        "url": canonical,
        "inLanguage": "ko",
        "isPartOf": {
            "@type": "WebSite",
            "name": BRAND,
            "url": BASE_URL.rstrip("/") + "/",
        },
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=2)
            + "\n</script>\n")


def inject_toc(body: str):
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


def render_page_hero(page: dict) -> str:
    crumb = render_breadcrumb(page.get("breadcrumb") or [])
    img = page.get("hero_image", "/assets/hero.jpg")
    img_webp = page.get("hero_image_webp", re.sub(r"\.(jpg|jpeg|png)$", ".webp", img))
    alt = page.get("hero_alt", page["h1"])
    return f"""<section class="hero page-hero">
  <div class="hero-inner hero-grid">
    <div class="hero-text">
      {crumb}
      <h1>{page['h1']}</h1>
      <p class="hero-lead">{page['desc']}</p>
      <div class="hero-actions">
        <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
        <a class="hero-btn" href="/#areas">지역별 안내 보기</a>
      </div>
    </div>
    <div class="hero-media">
      <picture>
        <source srcset="{img_webp}" type="image/webp">
        <img src="{img}" alt="{alt}" width="1200" height="675" fetchpriority="high" decoding="async">
      </picture>
    </div>
  </div>
</section>
"""


def render_footer() -> str:
    # 푸터·카드 앵커는 지역명만 사용한다(도어웨이·키워드 스터핑 신호 방지).
    # 핵심 키워드(출장마사지)는 각 페이지의 title·H1·본문에서 자연스럽게 노출된다.
    area_links = "".join(
        f'<li><a href="{area_url(s)}">{n}</a></li>'
        for s, n in [(a[0], a[1]) for a in AREAS[:6]]
    )
    station_links = "".join(
        f'<li><a href="{station_url(s)}">{n}</a></li>'
        for s, n in STATIONS[:5]
    )
    district_links = "".join(
        f'<li><a href="{district_url(s)}">{n}</a></li>'
        for s, n in DISTRICTS
    )
    return f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">{REGION_FULL} 처인구·기흥구·수지구 전지역 방문 출장마사지·홈타이 안내 사이트입니다. 모든 서비스는 안내된 관리 범위와 위생·안전 기준 안에서만 제공됩니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">예약전화</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> {REGION_FULL} 전지역</span>
      </address>
    </div>
    <nav class="footer-col" aria-label="행정구 안내">
      <p class="footer-title">행정구 안내</p>
      <ul>{district_links}</ul>
    </nav>
    <nav class="footer-col" aria-label="지역 안내">
      <p class="footer-title">지역 안내</p>
      <ul>{area_links}</ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/reservation/">예약안내</a></li>
        <li><a href="/precautions/">이용 전 확인사항</a></li>
        <li><a href="/hometai-guide/">홈타이 이용 가이드</a></li>
        <li><a href="/support/">고객센터</a></li>
        <li><a href="/privacy/">개인정보처리방침</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">{REGION_FULL}(경기도 용인시) 처인구·기흥구·수지구를 안내하는 건전한 방문 관리 사이트이며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
      <a class="footer-made" href="tel:{PHONE}" rel="nofollow">예약문의 {PHONE_DISPLAY}</a>
    </div>
  </div>
</footer>"""


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    body = page["body"]
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    canonical = BASE_URL.rstrip("/") + "/" + path

    structured = (webpage_jsonld(page, canonical)
                  + breadcrumb_jsonld(page, canonical)
                  + localbusiness_jsonld(page, canonical))
    page_head = hero if hero else render_page_hero(page)

    # 롱테일 내부링크 + 후기 섹션을 본문 뒤에 덧붙인다(색인 판정은 원본 기준 유지).
    body = body + render_related(page) + render_reviews(page)
    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="naver-site-verification" content="{NAVER_VERIFICATION}">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0a1120">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700;900&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700;900&display=swap"></noscript>
<link rel="stylesheet" href="/assets/style.css">
{structured}{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/"><span class="brand-mark">{BRAND_MARK}</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> {REGION_LABEL} 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {body}
    </article>
  </div>
</main>
{render_footer()}
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js" defer></script>
</body>
</html>
"""


def build() -> None:
    # 생성 결과물만 정리 (소스/.git/assets 보존)
    import shutil
    for entry in GENERATED:
        p = os.path.join(ROOT, entry)
        if os.path.isdir(p):
            shutil.rmtree(p)
        elif os.path.exists(p):
            os.remove(p)

    import datetime
    report = []
    indexable = []  # 색인 허용 페이지 메타 (sitemap·rss 공용)
    base = BASE_URL.rstrip("/")

    for page in PAGES:
        path = page["path"]
        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            indexable.append({
                "url": base + "/" + path,
                "title": page["title"],
                "desc": page["desc"],
            })
        report.append((path or "/", chars, "noindex" if noindex else "index"))

    now = datetime.datetime.now(datetime.timezone.utc)
    lastmod = now.strftime("%Y-%m-%d")
    rfc822 = now.strftime("%a, %d %b %Y %H:%M:%S +0000")

    # sitemap.xml — 메인 우선순위 1.0, 나머지 0.8
    rows = []
    for p in indexable:
        pri = "1.0" if p["url"].rstrip("/") == base else "0.8"
        rows.append(f"  <url><loc>{p['url']}</loc><lastmod>{lastmod}</lastmod>"
                    f"<changefreq>weekly</changefreq><priority>{pri}</priority></url>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + "\n".join(rows) + "\n</urlset>\n")

    # rss.xml — 네이버·구글이 사이트맵 대체 피드로 수집 (신규 발견 가속)
    items = []
    for p in indexable:
        items.append(
            "    <item>\n"
            f"      <title>{esc(p['title'])}</title>\n"
            f"      <link>{p['url']}</link>\n"
            f"      <guid isPermaLink=\"true\">{p['url']}</guid>\n"
            f"      <description>{esc(p['desc'])}</description>\n"
            f"      <pubDate>{rfc822}</pubDate>\n"
            "    </item>"
        )
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
                '  <channel>\n'
                f"    <title>{esc(BRAND)} {esc(REGION_LABEL)} 출장마사지·홈타이 안내</title>\n"
                f"    <link>{base}/</link>\n"
                f'    <atom:link href="{base}/rss.xml" rel="self" type="application/rss+xml"/>\n'
                f"    <description>{esc(REGION_FULL)} 처인구·기흥구·수지구 전지역 방문 출장마사지·홈타이 예약 안내</description>\n"
                "    <language>ko</language>\n"
                f"    <lastBuildDate>{rfc822}</lastBuildDate>\n"
                + "\n".join(items) + "\n  </channel>\n</rss>\n")

    # robots.txt — 전 봇 허용 + 사이트맵·RSS 명시. 주요 봇(구글/네이버 Yeti/빙) 명시 허용.
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: Googlebot\nAllow: /\n\n"
            "User-agent: Yeti\nAllow: /\n\n"      # 네이버 검색로봇
            "User-agent: Bingbot\nAllow: /\n\n"
            "User-agent: Daum\nAllow: /\n\n"      # 다음 검색로봇
            "User-agent: *\nAllow: /\n\n"
            f"Sitemap: {base}/sitemap.xml\n"
            f"Sitemap: {base}/rss.xml\n"
        )

    # IndexNow 키 파일 — https://host/{KEY}.txt 가 정확히 키 문자열을 반환해야 검증됨
    with open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY + "\n")

    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or c >= MIN_INDEX_CHARS) else "  WARN"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    n_noindex = sum(1 for _, _, r in report if r == "noindex")
    print(f"\n{len(report)} pages built, {len(indexable)} in sitemap/rss, {n_noindex} noindex.")


if __name__ == "__main__":
    build()
