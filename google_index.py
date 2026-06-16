#!/usr/bin/env python3
"""Google Indexing API 색인 통보 스크립트.

⚠️ 중요: 구글 Indexing API는 공식적으로 JobPosting·BroadcastEvent 페이지만
대상으로 합니다. 일반 페이지에 대한 색인 보장은 없으며(동작하는 경우도 있으나
ToS상 보장 X), 일반 콘텐츠의 정석은 Search Console 사이트맵 제출 + URL 검사입니다.
이 스크립트는 사용자가 요청 시 보조 수단으로 제공됩니다.

사전 준비:
  1) Google Cloud에서 서비스 계정 생성 → JSON 키 다운로드
  2) Indexing API 사용 설정(API 라이브러리에서 'Indexing API' 사용)
  3) Search Console 속성에 서비스 계정 이메일을 '소유자'로 추가
  4) pip install google-auth requests

사용법:
  GOOGLE_APPLICATION_CREDENTIALS=/path/sa.json python3 google_index.py
  python3 google_index.py /path/sa.json /yongin/jukjeon-dong-chuljangmassage/
"""
import os
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from content.site import BASE_URL

BASE = BASE_URL.rstrip("/")
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def urls_from_sitemap():
    with open("sitemap.xml", encoding="utf-8") as f:
        return re.findall(r"<loc>([^<]+)</loc>", f.read())


def normalize(arg):
    if arg.startswith("http"):
        return arg
    return BASE + (arg if arg.startswith("/") else "/" + arg)


def main(argv):
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        print("의존성이 필요합니다:  pip install google-auth requests")
        return 1

    sa_path = None
    args = []
    for a in argv:
        if a.endswith(".json") and os.path.exists(a) and sa_path is None:
            sa_path = a
        else:
            args.append(a)
    sa_path = sa_path or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not sa_path or not os.path.exists(sa_path):
        print("서비스 계정 JSON 경로가 필요합니다 "
              "(GOOGLE_APPLICATION_CREDENTIALS 또는 인자).")
        return 1

    urls = [normalize(a) for a in args] if args else urls_from_sitemap()
    creds = service_account.Credentials.from_service_account_file(sa_path, scopes=SCOPES)
    session = AuthorizedSession(creds)

    ok = 0
    for url in urls:
        r = session.post(ENDPOINT, json={"url": url, "type": "URL_UPDATED"})
        if r.status_code == 200:
            ok += 1
        else:
            print(f"  실패 {r.status_code}: {url}\n    {r.text[:200]}")
    print(f"Google Indexing API: {ok}/{len(urls)} 성공")
    return 0 if ok == len(urls) else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
