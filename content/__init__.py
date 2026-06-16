# 전체 페이지 목록 집계
from . import (areas_cheoin, areas_giheung, areas_suji, districts, info, main,
               stations_a, stations_b)

PAGES = (
    [main.PAGE]
    + districts.PAGES
    + areas_cheoin.PAGES
    + areas_giheung.PAGES
    + areas_suji.PAGES
    + stations_a.PAGES
    + stations_b.PAGES
    + info.PAGES
)
