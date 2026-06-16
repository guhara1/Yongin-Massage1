# 간다GO 용인 출장마사지 · 홈타이 지역 SEO 사이트

경기도 용인시(처인구·기흥구·수지구) 방문형 **출장마사지 · 홈타이** 예약 안내 지역 SEO 정적 사이트입니다.

- **상호:** 간다GO
- **전화예약:** 0508-202-4719
- **메인 URL:** `/yongin-chuljangmassage/`

## 구조 (총 63개 페이지)

| 구분 | 개수 |
|------|------|
| 메인페이지 | 1 |
| 행정구 (처인·기흥·수지) | 3 |
| 대표 읍면동 (번호 동 통합) | 30 |
| 지하철역·경전철역 | 24 |
| 기타(예약·이용안내·홈타이가이드·개인정보·고객센터) | 5 |

## 구글/네이버 가이드라인 준수

- 모든 `meta description`은 **80자 이내** (현재 최장 42자)
- 번호 행정동(유림1·2동, 동백1~3동 등)은 **대표 페이지로 통합** → 중복 콘텐츠 방지
- 환승역(기흥역=수인분당선·에버라인 등)은 **역명 기준 1개 URL**만 생성
- 예정역·예정 노선은 단독 색인 페이지를 만들지 않고 본문 보조 설명으로만 처리
- 페이지별 고유 본문(생활권 설명) + `WebPage`/`BreadcrumbList`/`Organization` JSON-LD
- 실제 오프라인 주소가 없으므로 `LocalBusiness` 스키마는 사용하지 않음
- `canonical`, `og:*`, `sitemap.xml`, `robots.txt` 포함

## 빌드

```bash
node build.js   # public/ 에 정적 사이트 생성
```

- `site.config.js` — 상호·전화번호·도메인 설정 (배포 도메인이 정해지면 `SITE_URL` 교체)
- `data.js` — 행정구/읍면동/역세권/기타 페이지 데이터 및 description
- `build.js` — 정적 HTML·sitemap·robots 생성기
- `assets/style.css` — 모바일 우선 스타일
- `public/` — 생성 결과물(배포 대상)

## 배포

`public/` 디렉터리를 정적 호스팅(예: GitHub Pages, Netlify, Cloudflare Pages)에 올리면 됩니다.
배포 전 `site.config.js`의 `SITE_URL`을 실제 도메인으로 변경한 뒤 `node build.js`를 다시 실행하세요.
