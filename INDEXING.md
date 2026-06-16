# 색인(인덱싱) 설정 가이드

간다GO 용인 출장마사지 사이트의 검색엔진 빠른 색인 구성 정리입니다.
도메인: `https://yongin-massage1.pages.dev/`

## 자동 생성되는 파일 (`python3 build.py`)

| 파일 | 용도 |
|------|------|
| `sitemap.xml` | 색인 허용 62개 URL (lastmod·changefreq·priority 포함) |
| `rss.xml` | RSS 2.0 피드 — 네이버·구글이 사이트맵 대체로 수집(신규 발견 가속) |
| `robots.txt` | Googlebot·Yeti(네이버)·Bingbot·Daum 명시 허용 + 사이트맵 2종 |
| `f250d3453a65550cf161e7ba85bba88c.txt` | IndexNow 키 검증 파일 |
| `<head>` 메타 | 네이버 소유확인(`naver-site-verification`) — 전 페이지 |

## 1) IndexNow — Bing·네이버·얀덱스 즉시 통보 (의존성 없음)

```bash
python3 indexnow.py                       # sitemap 전체 제출
python3 indexnow.py /yongin/jukjeon-dong-chuljangmassage/   # 특정 글만
```

- 한 엔드포인트(`api.indexnow.org`)에 제출하면 참여 검색엔진으로 전파됩니다.
- **네이버가 IndexNow 참여사**라 네이버 색인에 가장 효과적입니다.
- 키 파일이 `https://<도메인>/<KEY>.txt` 로 접근 가능해야 검증됩니다(배포 후 자동 충족).

## 2) 자동화 — 푸시할 때마다 통보 (GitHub Actions)

`.github/workflows/indexnow.yml` 가 `main` 푸시(=새 글 배포) 시 자동 실행되어
IndexNow로 전체 URL을 제출합니다. (Cloudflare 배포 반영을 위해 90초 대기 후 제출)
수동 실행은 Actions 탭 → "색인 통보" → Run workflow.

## 3) Google — IndexNow 미참여

> 구글은 IndexNow에 참여하지 않고, 사이트맵 ping 엔드포인트도 2023년 폐지됐습니다.
> 일반 페이지의 정석은 **Search Console**입니다.

1. [Google Search Console](https://search.google.com/search-console) 속성 추가 →
   소유확인(HTML 태그/DNS 등)
2. **Sitemaps** 에 `sitemap.xml` 제출 (원하면 `rss.xml` 도 추가)
3. 급할 때는 **URL 검사 → 색인 생성 요청**

### (선택) Google Indexing API 자동화
⚠️ 공식적으로 **JobPosting·BroadcastEvent** 전용 API라 일반 페이지 색인은 보장되지 않습니다.
보조 수단으로 쓰려면:

1. GCP 서비스 계정 생성 → JSON 키 발급, **Indexing API** 사용 설정
2. Search Console 속성에 서비스 계정 이메일을 **소유자**로 추가
3. 로컬: `pip install google-auth requests` 후
   `GOOGLE_APPLICATION_CREDENTIALS=sa.json python3 google_index.py`
4. CI 자동화: GitHub 저장소 Secrets에 **`GCP_SA_JSON`** (키 JSON 전체)을 등록하면
   워크플로가 푸시마다 Google Indexing API도 함께 호출합니다.

## 새 글/수정 후 색인 흐름 요약

1. `python3 build.py` → 커밋 → `main` 푸시
2. Cloudflare Pages 자동 배포
3. GitHub Action이 IndexNow 자동 제출(네이버·빙) / (시크릿 등록 시 구글 API)
4. 구글은 Search Console 사이트맵으로 수집 + 필요 시 URL 검사 요청
