# 사이트 공통 설정 (간다GO · 용인 출장마사지·홈타이)
# 배포 도메인 확정 후 BASE_URL 을 실제 도메인으로 변경하세요.
BASE_URL = "https://yongin-massage1.pages.dev"

BRAND = "간다GO"
BRAND_MARK = "GO"
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# 검색엔진 사이트 소유확인 코드
NAVER_VERIFICATION = "815b57c52edbf38f8941977a1f39ec1e98e5ba72"

REGION_LABEL = "용인시"
REGION_FULL = "경기도 용인시"

# 행정구 3곳 (slug, 한글명) — 허브 페이지
DISTRICTS = [
    ("cheoin-gu-chuljangmassage", "처인구"),
    ("giheung-gu-chuljangmassage", "기흥구"),
    ("suji-gu-chuljangmassage", "수지구"),
]

# 대표 읍·면·동 30곳 (slug, 한글명, 소속 행정구 slug)
# 번호 행정동(유림1·2동, 영덕1·2동, 동백1~3동, 풍덕천1·2동, 죽전1~3동, 상현1~3동)은
# 대표 동으로 통합해 중복 페이지 위험을 줄인다.
AREAS = [
    # 처인구 (12)
    ("pogok-eup-chuljangmassage", "포곡읍", "cheoin-gu-chuljangmassage"),
    ("mohyeon-eup-chuljangmassage", "모현읍", "cheoin-gu-chuljangmassage"),
    ("idong-eup-chuljangmassage", "이동읍", "cheoin-gu-chuljangmassage"),
    ("namsa-eup-chuljangmassage", "남사읍", "cheoin-gu-chuljangmassage"),
    ("yangji-eup-chuljangmassage", "양지읍", "cheoin-gu-chuljangmassage"),
    ("wonsam-myeon-chuljangmassage", "원삼면", "cheoin-gu-chuljangmassage"),
    ("baegam-myeon-chuljangmassage", "백암면", "cheoin-gu-chuljangmassage"),
    ("jungang-dong-chuljangmassage", "중앙동", "cheoin-gu-chuljangmassage"),
    ("yeokbuk-dong-chuljangmassage", "역북동", "cheoin-gu-chuljangmassage"),
    ("samga-dong-chuljangmassage", "삼가동", "cheoin-gu-chuljangmassage"),
    ("yurim-dong-chuljangmassage", "유림동", "cheoin-gu-chuljangmassage"),
    ("dongbu-dong-chuljangmassage", "동부동", "cheoin-gu-chuljangmassage"),
    # 기흥구 (12)
    ("singal-dong-chuljangmassage", "신갈동", "giheung-gu-chuljangmassage"),
    ("yeongdeok-dong-chuljangmassage", "영덕동", "giheung-gu-chuljangmassage"),
    ("gugal-dong-chuljangmassage", "구갈동", "giheung-gu-chuljangmassage"),
    ("sanggal-dong-chuljangmassage", "상갈동", "giheung-gu-chuljangmassage"),
    ("bora-dong-chuljangmassage", "보라동", "giheung-gu-chuljangmassage"),
    ("giheung-dong-chuljangmassage", "기흥동", "giheung-gu-chuljangmassage"),
    ("seonong-dong-chuljangmassage", "서농동", "giheung-gu-chuljangmassage"),
    ("guseong-dong-chuljangmassage", "구성동", "giheung-gu-chuljangmassage"),
    ("mabuk-dong-chuljangmassage", "마북동", "giheung-gu-chuljangmassage"),
    ("dongbaek-dong-chuljangmassage", "동백동", "giheung-gu-chuljangmassage"),
    ("sangha-dong-chuljangmassage", "상하동", "giheung-gu-chuljangmassage"),
    ("bojeong-dong-chuljangmassage", "보정동", "giheung-gu-chuljangmassage"),
    # 수지구 (6)
    ("pungdeokcheon-dong-chuljangmassage", "풍덕천동", "suji-gu-chuljangmassage"),
    ("sinbong-dong-chuljangmassage", "신봉동", "suji-gu-chuljangmassage"),
    ("jukjeon-dong-chuljangmassage", "죽전동", "suji-gu-chuljangmassage"),
    ("dongcheon-dong-chuljangmassage", "동천동", "suji-gu-chuljangmassage"),
    ("sanghyeon-dong-chuljangmassage", "상현동", "suji-gu-chuljangmassage"),
    ("seongbok-dong-chuljangmassage", "성복동", "suji-gu-chuljangmassage"),
]

# 지하철·경전철역 24곳 (slug, 한글명)
# 수인분당선·신분당선·용인경전철(에버라인). 환승역은 1개 URL만 생성.
STATIONS = [
    ("jukjeon-station-chuljangmassage", "죽전역"),
    ("bojeong-station-chuljangmassage", "보정역"),
    ("guseong-station-chuljangmassage", "구성역"),
    ("singal-station-chuljangmassage", "신갈역"),
    ("giheung-station-chuljangmassage", "기흥역"),
    ("sanggal-station-chuljangmassage", "상갈역"),
    ("dongcheon-station-chuljangmassage", "동천역"),
    ("suji-gu-office-station-chuljangmassage", "수지구청역"),
    ("seongbok-station-chuljangmassage", "성복역"),
    ("sanghyeon-station-chuljangmassage", "상현역"),
    ("gangnamdae-station-chuljangmassage", "강남대역"),
    ("jiseok-station-chuljangmassage", "지석역"),
    ("eojeong-station-chuljangmassage", "어정역"),
    ("dongbaek-station-chuljangmassage", "동백역"),
    ("chodang-station-chuljangmassage", "초당역"),
    ("samga-station-chuljangmassage", "삼가역"),
    ("yongin-cityhall-yongin-univ-station-chuljangmassage", "시청·용인대역"),
    ("myeongji-univ-station-chuljangmassage", "명지대역"),
    ("gimnyangjang-station-chuljangmassage", "김량장역"),
    ("stadium-songdam-univ-station-chuljangmassage", "운동장·송담대역"),
    ("gojin-station-chuljangmassage", "고진역"),
    ("bopyeong-station-chuljangmassage", "보평역"),
    ("dunjeon-station-chuljangmassage", "둔전역"),
    ("jeondae-everland-station-chuljangmassage", "전대·에버랜드역"),
]


def district_url(slug):
    return f"/yongin/{slug}/"


def area_url(slug):
    return f"/yongin/{slug}/"


def station_url(slug):
    return f"/yongin/{slug}/"


def areas_in(district_slug):
    return [(s, n) for s, n, d in AREAS if d == district_slug]


# 상단 메뉴 — 하위 메뉴에는 지역명·역명만 표시한다.
NAV = [
    ("홈", "/", []),
    ("출장마사지 안내", "/#service", [
        ("서비스 안내", "/#service"),
        ("전지역 방문 가능", "/#coverage"),
        ("예약 전 확인 기준", "/#check"),
        ("홈타이 이용 가이드", "/hometai-guide/"),
    ]),
    ("행정구별 안내", "/#districts", [
        (name, district_url(slug)) for slug, name in DISTRICTS
    ]),
    ("지역별 안내", "/#areas", [
        (name, area_url(slug)) for slug, name, _ in AREAS
    ]),
    ("지하철역별 안내", "/#stations", [
        (name, station_url(slug)) for slug, name in STATIONS
    ]),
    ("예약안내", "/reservation/", [
        ("예약 방법", "/reservation/#how"),
        ("예약 가능 시간", "/reservation/#hours"),
        ("방문 가능 지역", "/reservation/#place"),
        ("결제·이동비 안내", "/reservation/#payment"),
        ("변경·취소 안내", "/reservation/#change"),
    ]),
    ("이용 전 확인사항", "/precautions/", [
        ("방문 전 준비", "/precautions/#prepare"),
        ("외곽 지역 이동 기준", "/precautions/#outer"),
        ("위생·안전 기준", "/precautions/#hygiene"),
        ("자주 묻는 질문", "/precautions/#faq"),
    ]),
    ("고객센터", "/support/", [
        ("공지사항", "/support/#notice"),
        ("자주 묻는 질문", "/support/#faq"),
        ("1:1 문의", "/support/#contact"),
        ("개인정보처리방침", "/privacy/"),
    ]),
]
