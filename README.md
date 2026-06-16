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
node build.js   # 저장소 루트에 정적 사이트(HTML·sitemap·robots) 생성
```

- `site.config.js` — 상호·전화번호·도메인 설정 (커스텀 도메인 연결 시 `SITE_URL` 교체)
- `data.js` — 행정구/읍면동/역세권/기타 페이지 데이터 및 description
- `build.js` — 정적 HTML·sitemap·robots 생성기 (저장소 루트로 출력)
- `src/style.css` — 모바일 우선 스타일(소스)
- 생성 결과물: `index.html`(→메인 리다이렉트), `yongin-chuljangmassage/`, `yongin/...`, `reservation/` 등, `assets/`, `sitemap.xml`, `robots.txt`

## 배포 (Cloudflare Pages · GitHub 자동 배포)

이 저장소는 **빌드 결과물이 루트에 포함**되어 있어 추가 빌드 없이 그대로 배포됩니다.

Cloudflare Pages 프로젝트 설정 권장값:

| 항목 | 값 |
|------|-----|
| Production branch | `main` |
| Framework preset | None |
| Build command | (비움) |
| Build output directory | `/` (비움 = 루트) |

`main` 브랜치에 푸시하면 `https://yongin-massage1.pages.dev` 로 자동 배포됩니다.
커스텀 도메인을 연결하면 `site.config.js`의 `SITE_URL`을 바꾸고 `node build.js`를 다시 실행하세요.
