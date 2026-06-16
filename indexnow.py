#!/usr/bin/env python3
"""IndexNow 즉시 색인 통보 (Bing · Naver · Yandex 등 공유 엔드포인트).

사용법:
  python3 indexnow.py                # sitemap.xml 의 모든 URL 제출
  python3 indexnow.py /yongin/jukjeon-dong-chuljangmassage/   # 특정 경로만
  python3 indexnow.py https://yongin-massage1.pages.dev/...   # 전체 URL 직접

한 엔드포인트(api.indexnow.org)에 제출하면 참여 검색엔진으로 전파됩니다.
구글은 IndexNow 미참여 → google_index.py 또는 Search Console 사용.

외부 의존성 없음(표준 라이브러리). 사이트가 배포되어 키 파일
https://<host>/<KEY>.txt 가 접근 가능해야 검증됩니다.
"""
import json
import re
import sys
import urllib.request

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from content.site import BASE_URL, INDEXNOW_KEY

ENDPOINT = "https://api.indexnow.org/indexnow"
HOST = re.sub(r"^https?://", "", BASE_URL).strip("/")
BASE = BASE_URL.rstrip("/")


def urls_from_sitemap():
    with open("sitemap.xml", encoding="utf-8") as f:
        return re.findall(r"<loc>([^<]+)</loc>", f.read())


def normalize(arg):
    if arg.startswith("http"):
        return arg
    if arg.startswith("/"):
        return BASE + arg
    return BASE + "/" + arg


def main(argv):
    urls = [normalize(a) for a in argv] if argv else urls_from_sitemap()
    if not urls:
        print("제출할 URL이 없습니다.")
        return 1
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE}/{INDEXNOW_KEY}.txt",
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"IndexNow 응답: HTTP {resp.status}  ({len(urls)}개 URL 제출)")
            # 200/202 = 정상 접수
            return 0 if resp.status in (200, 202) else 2
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        print(f"IndexNow 오류: HTTP {e.code} {e.reason}\n{body}")
        return 2
    except Exception as e:  # noqa: BLE001
        print(f"IndexNow 요청 실패: {e}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
