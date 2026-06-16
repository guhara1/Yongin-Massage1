# 메인 페이지 — 허브 역할. 모든 키워드를 밀어 넣지 않고 상세 페이지로 연결한다.
from .site import (AREAS, BASE_URL, BRAND, DISTRICTS, PHONE, PHONE_DISPLAY,
                   STATIONS, area_url, areas_in, district_url, station_url)
from .pricing import PRICING

# 카드 앵커 텍스트는 지역명만 사용(도어웨이·키워드 스터핑 신호 방지).
_DISTRICT_CARDS = "".join(
    f'<li><a href="{district_url(slug)}">{name}</a></li>'
    for slug, name in DISTRICTS
)
_AREA_CARDS = "".join(
    f'<li><a href="{area_url(slug)}">{name}</a></li>'
    for slug, name, _ in AREAS
)
_STATION_CARDS = "".join(
    f'<li><a href="{station_url(slug)}">{name}</a></li>'
    for slug, name in STATIONS
)

_JSONLD = f"""<link rel="preload" as="image" href="/assets/hero.webp" type="image/webp" fetchpriority="high">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{BRAND}",
  "url": "{BASE_URL}/",
  "telephone": "{PHONE}",
  "image": "{BASE_URL}/assets/og-image.png",
  "logo": "{BASE_URL}/assets/icon-512.png",
  "description": "경기도 용인시 처인구·기흥구·수지구 전지역 방문 출장마사지·홈타이 예약 안내",
  "areaServed": {{
    "@type": "AdministrativeArea",
    "name": "경기도 용인시"
  }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "용인시 전지역 방문이 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "처인구, 기흥구, 수지구 세 행정구의 대표 읍·면·동과 역세권을 기준으로 용인시 전지역을 안내합니다. 처인구 백암·원삼·이동 같은 외곽 지역은 차량 이동 기준으로 가능 여부를 확인합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "용인은 행정구가 어떻게 나뉘나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "용인시는 처인구, 기흥구, 수지구 3개 행정구로 나뉩니다. 처인구는 용인시청·에버랜드 생활권, 기흥구는 기흥역·동백역 역세권, 수지구는 죽전역·수지구청역 중심의 강남 접근 생활권입니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "동백1·2·3동처럼 번호 동은 왜 따로 없나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "동백1·2·3동은 동백동, 죽전1·2·3동은 죽전동, 상현1·2·3동은 상현동 등 번호 행정동은 대표 동 페이지로 통합해 중복 페이지 위험을 줄였습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "기흥역처럼 환승역도 안내되나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "기흥역(수인분당선·에버라인 환승)은 노선별로 나누지 않고 1개 역세권 페이지로 안내합니다. 죽전역·수지구청역 등 신분당선 역도 역별 1개 페이지로 정리했습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "외곽 지역은 추가 이동비가 있나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "처인구 백암면·원삼면·이동읍·남사읍처럼 이동 거리가 먼 외곽 지역은 추가 이동비가 발생할 수 있으며, 예약 시 총비용으로 먼저 안내합니다."
      }}
    }}
  ]
}}
</script>
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner hero-grid">
    <div class="hero-text">
      <p class="hero-badge">Premium Visiting Spa · 경기도 용인시 전지역</p>
      <h1>용인 출장마사지·용인시 홈타이<br>지역별 예약 안내</h1>
      <p class="hero-lead">샵까지 갈 필요 없이, 계신 곳에서 받는 방문 관리.<br>처인구·기흥구·수지구 어디든 전화 한 통이면 예약이 끝납니다.</p>
      <div class="hero-actions">
        <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
        <a class="hero-btn" href="#areas">지역별 안내 보기</a>
      </div>
      <ul class="hero-stats">
        <li><strong>3개</strong><span>행정구</span></li>
        <li><strong>30곳</strong><span>대표 읍·면·동</span></li>
        <li><strong>24개</strong><span>역세권</span></li>
        <li><strong>24시간</strong><span>예약 상담</span></li>
      </ul>
    </div>
    <div class="hero-media">
      <picture>
        <source srcset="/assets/hero.webp" type="image/webp">
        <img src="/assets/hero.jpg" alt="용인 출장마사지·용인시 홈타이 방문 관리 안내" width="1200" height="675" fetchpriority="high" decoding="async">
      </picture>
    </div>
  </div>
</section>
"""

_BODY = f"""
<section id="service">
<h2>용인시에서 출장마사지를 찾는 이유</h2>
<p>용인 출장마사지를 찾는 분들은 대부분 지금 계신 곳에서 가까운 방문 가능 지역을 먼저 확인합니다. 경기도 용인시는 면적이 넓고 처인구·기흥구·수지구 세 행정구의 생활권 차이가 큽니다. 처인구는 용인시청·용인터미널·명지대·에버랜드와 양지·백암·남사·이동 같은 넓은 차량 이동 생활권이 중요하고, 기흥구는 기흥역·동백역·보정동·신갈동·구성동·마북동처럼 역세권과 주거·업무 수요가 함께 있습니다. 수지구는 죽전역·수지구청역·성복역·상현역·동천역을 중심으로 주거지와 강남 접근성이 강한 생활권입니다. {BRAND}는 예약 확인부터 방문 관리까지 정해진 절차에 따라 진행하며, 이 페이지는 용인 전체 구조를 설명하는 허브 역할을 합니다. 더 자세한 내용은 행정구 페이지와 읍·면·대표 행정동 페이지, 역세권 페이지에서 확인하실 수 있습니다.</p>
<p>용인은 안양·안산처럼 행정구가 있는 도시이지만 면적은 훨씬 넓고 도시 성격도 구마다 다릅니다. 그래서 메인페이지 아래에 처인구·기흥구·수지구 행정구 페이지를 먼저 두고, 그 아래 대표 읍·면·동 페이지와 역세권 페이지를 연결하는 방식으로 구성했습니다.</p>
</section>

<section id="districts">
<h2>처인구·기흥구·수지구 행정구별 안내</h2>
<p>용인 지역 안내는 세 행정구를 허브로 삼아 구성합니다. 각 행정구 페이지에서는 생활권 특징과 대표 읍·면·동, 인근 역세권을 함께 정리해 드리니, 익숙한 행정구부터 선택해 주세요.</p>
<ul class="card-grid">
{_DISTRICT_CARDS}
</ul>
<p>처인구는 용인시청·김량장·에버랜드 생활권, 기흥구는 기흥역·동백역·보정동 생활권, 수지구는 죽전역·수지구청역·성복역 생활권을 중심으로 안내합니다.</p>
</section>

<section id="coverage">
<h2>용인 홈타이 이용 전 확인할 사항</h2>
<p>용인 홈타이는 자택, 숙소, 사무실 인근에서 예약 가능 여부를 먼저 확인한 뒤 이용하는 방문형 관리 서비스입니다. 용인시는 처인구·기흥구·수지구 3개 행정구로 나뉘고, 번호가 붙은 행정동은 개별 페이지로 만들지 않습니다. 유림1·2동은 유림동, 영덕1·2동은 영덕동, 동백1·2·3동은 동백동, 풍덕천1·2동은 풍덕천동, 죽전1·2·3동은 죽전동, 상현1·2·3동은 상현동 대표 페이지로 통합해 중복 콘텐츠 위험을 줄였습니다. 각 페이지마다 생활권과 이동 기준을 다르게 설명합니다.</p>
</section>

<section id="areas">
<h2>대표 읍·면·동별 방문 가능 지역 안내</h2>
<p>지역별 안내는 처인구 12곳, 기흥구 12곳, 수지구 6곳, 모두 30개 대표 읍·면·동을 기준으로 구성됩니다. 각 페이지에서는 해당 생활권의 특징, 가까운 역, 방문 전 확인사항, 예약 가능 시간, 추가 이동비 여부를 지역마다 고유한 내용으로 설명합니다. 거주하시거나 머무시는 지역을 선택해 주세요.</p>
<ul class="card-grid">
{_AREA_CARDS}
</ul>
<p>처인구는 중앙동·역북동·삼가동 도심권과 포곡·양지·남사 외곽권을, 기흥구는 기흥역·동백역·보정동 역세권을, 수지구는 죽전·풍덕천·성복·상현·동천 신분당선 생활권을 중심으로 안내합니다.</p>
</section>

<section id="stations">
<h2>죽전역·기흥역·수지구청역·동백역 역세권 안내</h2>
<p>역세권 안내는 용인시를 지나는 수인분당선·신분당선·용인경전철(에버라인) 역을 기준으로 구성합니다. 각 역 페이지에서는 주변 읍·면·동, 이동 동선, 이용 시간대, 예약 전 확인사항을 역마다 다르게 설명하며, 같은 역을 노선별로 나눈 중복 페이지는 만들지 않습니다. 기흥역은 수인분당선·에버라인 환승역이지만 1개 페이지로만 안내합니다.</p>
<ul class="card-grid">
{_STATION_CARDS}
</ul>
<p>죽전역은 죽전동·단국대 생활권과, 기흥역은 신갈·구갈 생활권과, 수지구청역은 풍덕천동 중심 상권과, 동백역은 동백지구와 연결됩니다.</p>
</section>

<section id="check">
<h2>예약 전 꼭 확인해야 할 기준</h2>
<p>예약 전에는 방문 가능 지역, 관리 가능 시간, 추가 이동비, 결제 방식, 취소 기준, 서비스 범위를 먼저 확인해야 합니다. 용인은 같은 시 안에서도 수지구 죽전·성복 생활권과 처인구 백암·원삼·양지 생활권의 이동 시간이 크게 다를 수 있습니다. 특히 처인구 외곽 읍·면 지역은 차량 이동 기준 안내가 중요하므로, 자세한 준비 방법은 <a href="/precautions/">이용 전 확인사항</a>에서, 예약 절차와 결제·이동비 안내는 <a href="/reservation/">예약안내</a>에서 확인해 주세요. 홈타이가 처음이라면 <a href="/hometai-guide/">홈타이 이용 가이드</a>를 함께 보시면 도움이 됩니다.</p>
</section>

<section id="guide">
<h2>용인 출장마사지 사이트 이용 가이드</h2>
<p>메인페이지는 용인시 전체 안내를 담당하고, 행정구 페이지는 처인구·기흥구·수지구 생활권을, 대표 읍·면·동 페이지는 세부 지역 검색을, 역세권 페이지는 죽전역·기흥역·수지구청역·동백역 같은 실제 검색 의도를 담당합니다. 거주 지역이 익숙하면 행정동 페이지를, 역 기준 위치가 익숙하면 역세권 페이지를 보시면 됩니다. 어느 페이지를 보셔도 예약 절차와 비용 기준은 동일하며, 최종 안내는 언제나 정확한 주소를 기준으로 이루어집니다. 과장된 표현이나 허위 후기, 불법·선정적인 안내는 사용하지 않으며, 이용 가능 지역과 예약 절차, 취소 기준, 개인정보 처리 기준을 분명하게 보여드리는 것을 원칙으로 합니다.</p>
</section>

<section id="faq">
<h2>자주 묻는 질문</h2>
<div class="faq-item">
<h3>용인시 전지역 방문이 가능한가요?</h3>
<p>처인구·기흥구·수지구 대표 읍·면·동 30곳과 역세권 24곳을 기준으로 용인시 전지역을 안내합니다. 처인구 백암·원삼·이동 같은 외곽 지역은 차량 이동 기준으로 가능 여부를 확인합니다.</p>
</div>
<div class="faq-item">
<h3>동백1·2·3동처럼 번호 동은 왜 페이지가 없나요?</h3>
<p>동백1·2·3동은 동백동, 죽전1·2·3동은 죽전동, 상현1·2·3동은 상현동 대표 페이지에서 통합 안내합니다. 같은 생활권을 나눠 반복 설명하지 않기 위해서입니다.</p>
</div>
<div class="faq-item">
<h3>기흥역처럼 환승역도 안내되나요?</h3>
<p>기흥역은 수인분당선·에버라인 환승역이지만 노선별로 나누지 않고 1개 역세권 페이지로 안내합니다. 본문에서 환승 특징을 함께 설명합니다.</p>
</div>
<div class="faq-item">
<h3>외곽 지역은 추가 이동비가 붙나요?</h3>
<p>처인구 백암면·원삼면·이동읍·남사읍처럼 이동 거리가 먼 지역은 추가 이동비가 발생할 수 있습니다. 예약 시 총비용으로 먼저 안내해 드립니다.</p>
</div>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>용인 방문 관리 예약과 상담은 전화로 가장 빠르게 진행됩니다. 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "용인 출장마사지｜용인시 홈타이 지역별 예약 안내",
    "desc": "용인 출장마사지·홈타이 예약 전 처인구, 기흥구, 수지구 정보를 정리했습니다.",
    "h1": "용인 출장마사지 · 용인시 홈타이 지역별 예약 안내",
    "body": _BODY,
    "extra_head": _JSONLD,
    "breadcrumb": [],
    "hero": _HERO,
}
