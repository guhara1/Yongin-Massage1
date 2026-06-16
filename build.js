#!/usr/bin/env node
/* 간다GO 용인 출장마사지·홈타이 정적 사이트 생성기 */
const fs = require('fs');
const path = require('path');
const cfg = require('./site.config.js');
const { districts, dongs, stations, pages } = require('./data.js');

// Cloudflare Pages 기본 설정(출력 디렉터리=루트)에서 바로 열리도록 저장소 루트에 생성합니다.
const OUT = __dirname;
// 빌드 때마다 정리하는 "생성 결과물" 목록 (소스 파일은 절대 건드리지 않음)
const GENERATED = [
  'index.html', 'sitemap.xml', 'robots.txt', 'assets',
  'yongin', 'yongin-chuljangmassage',
  'reservation', 'notice', 'homethai-guide', 'privacy', 'support',
];
const { BRAND, PHONE, PHONE_TEL, SITE_URL, SITE_NAME, MAIN_SLUG } = cfg;

// ---- helpers ----------------------------------------------------------
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const len = (s) => [...String(s)].length; // 문자 수(이모지/한글 안전)

function warnDesc(label, desc) {
  if (len(desc) > 80) console.warn(`  [경고] ${label} description ${len(desc)}자 (80자 초과): ${desc}`);
}

function writeFile(slug, html) {
  const dir = path.join(OUT, slug.replace(/^\//, ''));
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), html, 'utf8');
}

const districtBySlugKey = Object.fromEntries(districts.map((d) => [d.key, d]));

// 공통 레이아웃 ----------------------------------------------------------
function layout({ slug, title, desc, h1, bodyHtml, breadcrumbs, schemaExtra }) {
  const canonical = SITE_URL + slug;
  const crumbItems = breadcrumbs.map((b, i) => ({
    '@type': 'ListItem', position: i + 1, name: b.name,
    item: SITE_URL + b.slug,
  }));
  const schema = [
    {
      '@context': 'https://schema.org', '@type': 'WebPage',
      name: title, description: desc, url: canonical,
      inLanguage: 'ko-KR',
      isPartOf: { '@type': 'WebSite', name: SITE_NAME, url: SITE_URL + MAIN_SLUG },
    },
    {
      '@context': 'https://schema.org', '@type': 'BreadcrumbList',
      itemListElement: crumbItems,
    },
    {
      '@context': 'https://schema.org', '@type': 'Organization',
      name: BRAND, url: SITE_URL + MAIN_SLUG,
      telephone: PHONE,
      contactPoint: {
        '@type': 'ContactPoint', telephone: PHONE,
        contactType: 'reservations', areaServed: 'KR', availableLanguage: 'Korean',
      },
    },
  ];
  if (schemaExtra) schema.push(schemaExtra);

  const crumbHtml = breadcrumbs
    .map((b, i) => i === breadcrumbs.length - 1
      ? `<span aria-current="page">${esc(b.name)}</span>`
      : `<a href="${b.slug}">${esc(b.name)}</a>`)
    .join('<span class="sep">›</span>');

  return `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<link rel="canonical" href="${canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="${esc(SITE_NAME)}">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:url" content="${canonical}">
<meta property="og:image" content="${SITE_URL}/assets/og-image.png">
<meta name="format-detection" content="telephone=yes">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">${JSON.stringify(schema)}</script>
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="${MAIN_SLUG}">${esc(BRAND)} <span>용인 출장마사지·홈타이</span></a>
    <a class="call" href="tel:${PHONE_TEL}">전화예약 ${esc(PHONE)}</a>
  </div>
</header>
<nav class="breadcrumb"><div class="wrap">${crumbHtml}</div></nav>
<main class="wrap">
  <h1>${esc(h1)}</h1>
  ${bodyHtml}
</main>
<aside class="cta">
  <div class="wrap">
    <p>용인 전지역 출장마사지·홈타이 방문 예약</p>
    <a class="call-lg" href="tel:${PHONE_TEL}">${esc(BRAND)} 전화예약 ${esc(PHONE)}</a>
  </div>
</aside>
<footer class="site-footer">
  <div class="wrap">
    <p class="biz">${esc(BRAND)} · 용인 출장마사지·홈타이 방문 예약 안내</p>
    <p class="tel">전화예약 <a href="tel:${PHONE_TEL}">${esc(PHONE)}</a></p>
    <ul class="foot-links">
      <li><a href="${MAIN_SLUG}">홈</a></li>
      <li><a href="/reservation/">예약 안내</a></li>
      <li><a href="/notice/">이용 전 확인사항</a></li>
      <li><a href="/homethai-guide/">홈타이 이용 가이드</a></li>
      <li><a href="/privacy/">개인정보 처리방침</a></li>
      <li><a href="/support/">고객센터</a></li>
    </ul>
    <p class="notice">본 사이트는 합법적인 방문형 관리(출장마사지·홈타이) 예약 안내 사이트이며, 불법·선정적 서비스를 제공하지 않습니다.</p>
  </div>
</footer>
</body>
</html>`;
}

// 링크 리스트 블록
function linkList(title, items) {
  if (!items.length) return '';
  const lis = items.map((it) => `<li><a href="${it.slug}">${esc(it.name)} 출장마사지</a></li>`).join('');
  return `<section class="link-block"><h2>${esc(title)}</h2><ul class="grid-links">${lis}</ul></section>`;
}

// 신뢰/이용 안내 공통 블록
function trustBlock(area) {
  return `<section class="trust">
  <h2>${esc(area)} 예약 전 확인사항</h2>
  <ul class="check">
    <li>방문 가능 지역 및 인근 생활권 확인</li>
    <li>예약 가능 시간과 방문 소요 시간 안내</li>
    <li>지역에 따른 추가 이동비 여부 확인</li>
    <li>결제 방식 및 취소 기준 안내</li>
    <li>서비스 범위와 개인정보 처리 기준 확인</li>
  </ul>
  <p class="muted">용인은 면적이 넓어 처인구 외곽 읍면 지역은 차량 이동 시간이 길어질 수 있습니다. 예약 가능 시간과 추가 이동비를 먼저 확인하신 뒤 전화로 문의해 주세요.</p>
</section>`;
}

// ---- 메인페이지 -------------------------------------------------------
function buildMain() {
  const slug = MAIN_SLUG;
  const title = '용인 출장마사지｜용인시 홈타이 지역별 예약 안내';
  const desc = '용인 출장마사지·홈타이 예약 전 처인구, 기흥구, 수지구 정보를 정리했습니다.';
  warnDesc('메인', desc);
  const h1 = '용인 출장마사지 · 용인시 홈타이 지역별 예약 안내';

  const districtCards = districts.map((d) =>
    `<a class="card" href="${d.slug}"><strong>${esc(d.name)} 출장마사지</strong><span>${esc(d.areas)}</span></a>`
  ).join('');

  const dongsByDistrict = (key) => dongs.filter((x) => x.district === key);
  const cheoinDongs = linkList('처인구 대표 읍면동별 안내', dongsByDistrict('cheoin'));
  const giheungDongs = linkList('기흥구 대표 읍면동별 안내', dongsByDistrict('giheung'));
  const sujiDongs = linkList('수지구 대표 읍면동별 안내', dongsByDistrict('suji'));
  const stationLinks = linkList('지하철역·경전철역별 안내', stations);

  const body = `
<p class="lead">용인 출장마사지를 찾는 분들은 대부분 현재 위치에서 가까운 방문 가능 지역을 먼저 확인합니다. 용인시는 처인구, 기흥구, 수지구로 나뉘고 세 행정구의 생활권 차이가 큽니다. ${esc(BRAND)}는 용인 전지역 방문형 출장마사지·홈타이 예약을 전화로 안내합니다.</p>

<section class="link-block">
  <h2>용인시에서 출장마사지를 찾는 이유</h2>
  <p>용인은 안양·안산처럼 행정구가 있는 도시이지만 면적이 훨씬 넓고 도시 성격도 구마다 다릅니다. 처인구는 용인시청·에버랜드·양지·백암 같은 넓은 차량 이동 생활권, 기흥구는 기흥역·동백역 역세권과 주거·업무 수요, 수지구는 죽전역·수지구청역 중심의 강남 접근 생활권이 핵심입니다.</p>
</section>

<section class="link-block">
  <h2>처인구·기흥구·수지구 생활권 차이</h2>
  <div class="cards">${districtCards}</div>
</section>

${cheoinDongs}
${giheungDongs}
${sujiDongs}

<section class="link-block">
  <h2>죽전역·기흥역·수지구청역·동백역 역세권 안내</h2>
  <p>역세권 페이지는 실제 검색어와 가까운 제목을 사용합니다. 같은 역을 노선별로 나누지 않으며, 기흥역은 수인분당선·에버라인을 합쳐 1개 페이지로만 안내합니다.</p>
</section>
${stationLinks}

<section class="link-block">
  <h2>용인 홈타이 예약 전 확인사항</h2>
  <p>용인 홈타이는 자택, 숙소, 사무실 인근에서 예약 가능 여부를 먼저 확인한 뒤 이용하는 방문형 관리 서비스입니다. 방문 가능 지역, 예약 가능 시간, 추가 이동비, 결제 방식, 취소 기준을 미리 확인하시면 편리합니다.</p>
  <ul class="grid-links">
    <li><a href="/reservation/">예약 안내</a></li>
    <li><a href="/notice/">이용 전 확인사항</a></li>
    <li><a href="/homethai-guide/">홈타이 이용 가이드</a></li>
    <li><a href="/support/">고객센터</a></li>
  </ul>
</section>

<section class="link-block">
  <h2>용인 출장마사지 사이트 이용 가이드</h2>
  <p>메인페이지는 용인시 전체 안내, 행정구 페이지는 처인구·기흥구·수지구 생활권, 대표 읍면동 페이지는 세부 지역, 역세권 페이지는 실제 검색 수요가 있는 역명을 담당합니다. 원하는 지역을 선택해 방문 가능 여부를 확인하신 뒤 전화로 예약해 주세요.</p>
</section>
`;
  warnDesc('메인', desc);
  const html = layout({
    slug, title, desc, h1, bodyHtml: body,
    breadcrumbs: [{ name: '홈', slug: MAIN_SLUG }],
  });
  writeFile(slug, html);
}

// ---- 행정구 페이지 ----------------------------------------------------
function buildDistrict(d) {
  warnDesc(d.name, d.desc);
  const childDongs = dongs.filter((x) => x.district === d.key);
  const childStations = stations.filter((x) => x.district === d.key);
  const body = `
<p class="lead">${esc(d.blurb)}</p>
<section class="link-block">
  <h2>${esc(d.name)} 출장마사지·홈타이 방문 가능 지역</h2>
  <p>${esc(d.name)}의 주요 생활권은 ${esc(d.areas)}입니다. 아래 대표 읍면동과 역세권 페이지에서 본인 위치에 가까운 지역을 선택해 방문 가능 여부를 확인하실 수 있습니다.</p>
</section>
${linkList(d.name + ' 대표 읍면동별 안내', childDongs)}
${linkList(d.name + ' 인근 역세권 안내', childStations)}
${trustBlock(d.name)}
<section class="link-block">
  <h2>다른 행정구 안내</h2>
  <ul class="grid-links">
    ${districts.filter((x) => x.key !== d.key).map((x) => `<li><a href="${x.slug}">${esc(x.name)} 출장마사지</a></li>`).join('')}
  </ul>
</section>`;
  const html = layout({
    slug: d.slug, title: d.title, desc: d.desc, h1: d.h1, bodyHtml: body,
    breadcrumbs: [
      { name: '홈', slug: MAIN_SLUG },
      { name: '행정구별 안내', slug: MAIN_SLUG },
      { name: d.name, slug: d.slug },
    ],
  });
  writeFile(d.slug, html);
}

// ---- 읍면동 페이지 ----------------------------------------------------
function buildDong(x) {
  warnDesc(x.name, x.desc);
  const parent = districtBySlugKey[x.district];
  const h1 = `${x.name} 출장마사지 · 홈타이 방문 예약 안내`;
  const siblings = dongs.filter((s) => s.district === x.district && s.slug !== x.slug).slice(0, 8);
  const nearStations = stations.filter((s) => s.district === x.district).slice(0, 6);
  const body = `
<p class="lead">${esc(x.blurb)}</p>
<section class="link-block">
  <h2>${esc(x.name)} 홈타이 방문 안내</h2>
  <p>${esc(x.name)} 출장마사지·홈타이는 자택, 숙소, 사무실 인근에서 예약 가능 여부를 먼저 확인한 뒤 이용하는 방문형 관리 서비스입니다. ${esc(parent.name)} 생활권에 속하며, 방문 가능 시간과 이동 기준을 전화로 안내해 드립니다.</p>
</section>
${trustBlock(x.name)}
${linkList(parent.name + ' 인근 지역 안내', siblings)}
${linkList(parent.name + ' 인근 역세권 안내', nearStations)}
<section class="link-block">
  <h2>${esc(parent.name)} 전체 안내</h2>
  <p><a href="${parent.slug}">${esc(parent.name)} 출장마사지 안내 페이지</a>에서 ${esc(parent.name)} 전체 생활권과 방문 가능 지역을 확인하실 수 있습니다.</p>
</section>`;
  const html = layout({
    slug: x.slug, title: x.title, desc: x.desc, h1, bodyHtml: body,
    breadcrumbs: [
      { name: '홈', slug: MAIN_SLUG },
      { name: parent.name, slug: parent.slug },
      { name: x.name, slug: x.slug },
    ],
  });
  writeFile(x.slug, html);
}

// ---- 역세권 페이지 ----------------------------------------------------
function buildStation(x) {
  warnDesc(x.name, x.desc);
  const parent = districtBySlugKey[x.district];
  const h1 = `${x.name} 출장마사지 · 홈타이 방문 예약 안내`;
  const siblings = stations.filter((s) => s.district === x.district && s.slug !== x.slug).slice(0, 8);
  const nearDongs = dongs.filter((s) => s.district === x.district).slice(0, 6);
  const body = `
<p class="lead">${esc(x.blurb)}</p>
<section class="link-block">
  <h2>${esc(x.name)} 출장마사지·홈타이 방문 안내</h2>
  <p>${esc(x.name)} 인근에서 출장마사지·홈타이를 찾으신다면 방문 가능 지역과 예약 가능 시간을 먼저 확인하시는 것이 좋습니다. ${esc(parent.name)} 생활권에 속하며, ${esc(BRAND)} 전화 예약으로 방문 기준을 안내해 드립니다.</p>
</section>
${trustBlock(x.name)}
${linkList(parent.name + ' 인근 역세권 안내', siblings)}
${linkList(parent.name + ' 인근 지역 안내', nearDongs)}
<section class="link-block">
  <h2>${esc(parent.name)} 전체 안내</h2>
  <p><a href="${parent.slug}">${esc(parent.name)} 출장마사지 안내 페이지</a>에서 ${esc(parent.name)} 전체 생활권을 확인하실 수 있습니다.</p>
</section>`;
  const html = layout({
    slug: x.slug, title: x.title, desc: x.desc, h1, bodyHtml: body,
    breadcrumbs: [
      { name: '홈', slug: MAIN_SLUG },
      { name: '역세권 안내', slug: MAIN_SLUG },
      { name: x.name, slug: x.slug },
    ],
  });
  writeFile(x.slug, html);
}

// ---- 기타 페이지 ------------------------------------------------------
const pageBodies = {
  '/reservation/': `
<p class="lead">${BRAND} 용인 출장마사지·홈타이 예약은 전화로 진행됩니다. 방문 가능 지역과 예약 가능 시간을 확인한 뒤 예약해 주세요.</p>
<section class="link-block">
  <h2>예약 절차</h2>
  <ol class="steps">
    <li>방문 희망 지역(행정구·읍면동·역세권) 확인</li>
    <li>희망 방문 시간 및 소요 시간 안내</li>
    <li>추가 이동비·결제 방식·취소 기준 안내</li>
    <li>전화로 최종 예약 확정</li>
  </ol>
</section>
<section class="link-block">
  <h2>전화 예약</h2>
  <p>아래 번호로 전화 주시면 방문 가능 여부와 예약 시간을 안내해 드립니다.</p>
  <p><a class="call-lg" href="tel:${PHONE_TEL}">${BRAND} 전화예약 ${PHONE}</a></p>
</section>`,
  '/notice/': `
<p class="lead">용인 출장마사지·홈타이 이용 전 아래 사항을 확인해 주세요. 용인은 면적이 넓어 지역별 이동 기준이 다릅니다.</p>
<section class="trust">
  <h2>이용 전 확인사항</h2>
  <ul class="check">
    <li>방문 가능 지역 및 인근 생활권 확인</li>
    <li>예약 가능 시간과 방문 소요 시간</li>
    <li>지역별 추가 이동비 여부</li>
    <li>결제 방식 및 취소·변경 기준</li>
    <li>서비스 범위와 개인정보 처리 기준</li>
  </ul>
  <p class="muted">수지구 죽전·성복 생활권과 처인구 백암·원삼·양지 생활권은 이동 기준이 완전히 다릅니다. 외곽 읍면 지역은 차량 이동 시간이 길어질 수 있으므로 예약 가능 시간을 미리 확인해 주세요.</p>
</section>`,
  '/homethai-guide/': `
<p class="lead">용인 홈타이는 자택, 숙소, 사무실 인근에서 예약 가능 여부를 먼저 확인한 뒤 이용하는 방문형 관리 서비스입니다.</p>
<section class="link-block">
  <h2>홈타이 이용 가이드</h2>
  <p>홈타이와 출장마사지는 방문형 관리라는 점에서 같지만, 이용 전 방문 가능 지역과 시간을 확인하는 절차가 중요합니다. ${BRAND}는 용인 처인구·기흥구·수지구 전지역 방문 기준을 전화로 안내합니다.</p>
  <ul class="check">
    <li>방문 가능 지역과 인근 생활권 확인</li>
    <li>예약 가능 시간 및 소요 시간 안내</li>
    <li>추가 이동비·결제·취소 기준 확인</li>
  </ul>
</section>`,
  '/privacy/': `
<p class="lead">${BRAND} 용인 출장마사지 사이트는 이용자의 개인정보를 중요하게 생각하며 관련 법령을 준수합니다.</p>
<section class="link-block">
  <h2>수집 항목 및 이용 목적</h2>
  <p>전화 예약 과정에서 예약 확인에 필요한 최소한의 정보(연락처, 방문 희망 지역·시간)만 이용하며, 예약 안내 목적 외에는 사용하지 않습니다.</p>
  <h2>보유 및 파기</h2>
  <p>예약 안내 목적이 달성되면 관련 정보를 지체 없이 파기합니다.</p>
  <h2>문의</h2>
  <p>개인정보 관련 문의는 <a href="tel:${PHONE_TEL}">${PHONE}</a>로 연락해 주세요.</p>
</section>`,
  '/support/': `
<p class="lead">${BRAND} 용인 출장마사지·홈타이 고객센터입니다. 예약 및 문의는 전화로 안내해 드립니다.</p>
<section class="link-block">
  <h2>전화 문의</h2>
  <p><a class="call-lg" href="tel:${PHONE_TEL}">${BRAND} 전화예약 ${PHONE}</a></p>
  <h2>자주 찾는 안내</h2>
  <ul class="grid-links">
    <li><a href="/reservation/">예약 안내</a></li>
    <li><a href="/notice/">이용 전 확인사항</a></li>
    <li><a href="/homethai-guide/">홈타이 이용 가이드</a></li>
    <li><a href="/privacy/">개인정보 처리방침</a></li>
  </ul>
</section>`,
};

function buildPage(p) {
  warnDesc(p.name, p.desc);
  const html = layout({
    slug: p.slug, title: p.title, desc: p.desc, h1: `${p.name}`,
    bodyHtml: pageBodies[p.slug] || '',
    breadcrumbs: [
      { name: '홈', slug: MAIN_SLUG },
      { name: p.name, slug: p.slug },
    ],
  });
  writeFile(p.slug, html);
}

// ---- 루트 리다이렉트 / 정적 자원 -------------------------------------
function buildRootRedirect() {
  const html = `<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<title>${esc(SITE_NAME)}</title>
<link rel="canonical" href="${SITE_URL + MAIN_SLUG}">
<meta http-equiv="refresh" content="0; url=${MAIN_SLUG}">
<meta name="robots" content="noindex">
</head><body><p><a href="${MAIN_SLUG}">용인 출장마사지·홈타이 안내로 이동</a></p></body></html>`;
  fs.writeFileSync(path.join(OUT, 'index.html'), html, 'utf8');
}

function buildSitemap() {
  const all = [
    { slug: MAIN_SLUG, pri: '1.0' },
    ...districts.map((d) => ({ slug: d.slug, pri: '0.9' })),
    ...dongs.map((d) => ({ slug: d.slug, pri: '0.8' })),
    ...stations.map((d) => ({ slug: d.slug, pri: '0.8' })),
    ...pages.map((d) => ({ slug: d.slug, pri: '0.5' })),
  ];
  const today = new Date().toISOString().slice(0, 10);
  const urls = all.map((u) =>
    `  <url><loc>${SITE_URL + u.slug}</loc><lastmod>${today}</lastmod><priority>${u.pri}</priority></url>`
  ).join('\n');
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>\n`;
  fs.writeFileSync(path.join(OUT, 'sitemap.xml'), xml, 'utf8');
}

function buildRobots() {
  const txt = `User-agent: *
Allow: /

Sitemap: ${SITE_URL}/sitemap.xml
`;
  fs.writeFileSync(path.join(OUT, 'robots.txt'), txt, 'utf8');
}

function copyAssets() {
  const dir = path.join(OUT, 'assets');
  fs.mkdirSync(dir, { recursive: true });
  fs.copyFileSync(path.join(__dirname, 'src', 'style.css'), path.join(dir, 'style.css'));
}

// ---- 실행 -------------------------------------------------------------
function run() {
  // 생성 결과물만 정리 (소스/.git 보존)
  for (const entry of GENERATED) {
    fs.rmSync(path.join(OUT, entry), { recursive: true, force: true });
  }
  copyAssets();
  buildMain();
  districts.forEach(buildDistrict);
  dongs.forEach(buildDong);
  stations.forEach(buildStation);
  pages.forEach(buildPage);
  buildRootRedirect();
  buildSitemap();
  buildRobots();

  const total = 1 + districts.length + dongs.length + stations.length + pages.length;
  console.log(`생성 완료: 메인 1 + 행정구 ${districts.length} + 읍면동 ${dongs.length} + 역세권 ${stations.length} + 기타 ${pages.length} = ${total}개 페이지`);
  console.log(`출력 경로: ${OUT}`);
}

run();
