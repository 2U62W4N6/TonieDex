import time
from typing import Dict, Any, Generator, List
from model.tonie import Tonie, Tracks
import requests
from urllib.parse import urljoin
from utils.logger_setup import setup_logger
from requests.exceptions import RequestException


class TonieCrawler:
    def __init__(self, key: str):
        self.base_url = f"https://tonies.com/_next/data/{key}/de-de/tonies.json"
        self.logging = setup_logger(__name__, "logs/crawler.log")

    def get_payload(self, url: str) -> Dict[str, Any] | None:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except RequestException as e:
            self.logging.error(f"{e}")
        else:
            self.logging.info(f"{url}")
            return response.json()

    def extract_tonie_urls(self, payload: Dict[str, Any]) -> Generator[str, None, None]:
        for tonie in payload["pageProps"]["page"]["productList"]["normalizedProducts"]:
            yield urljoin(self.base_url, tonie["path"][1:-1] + ".json")

    def create_track_objects(self, payload_tracks: Dict[str, str]) -> List[Tracks]:
        return [
            Tracks(track_number=number, track_name=name)
            for number, name in enumerate(payload_tracks)
        ]

    def extract_tonie_information(
        self, payload: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        data = payload.pop("pageProps").pop("product")
        return {
            "name": data["name"],
            "series": data["series"]["label"],
            "image_url": data["images"][1]["src"],
            "description": data["description"],
            "run_time": data.get("runTime"),
            "age_min": data.get("ageMin"),
            "genre": data["genre"]["label"],
            "label": ",".join(t["label"] for t in data.get("theme", [])),
            "price_cent_amount": data["price"]["centAmount"],
            "tracks": self.create_track_objects(data.get("tracks", [])),
        }

    def create_tonie_object(self, payload: Dict[str, Dict[str, Any]]) -> Tonie:
        data = self.extract_tonie_information(payload)
        return Tonie(**data)

    def crawl_tonies(self) -> Generator[Tonie, None, None]:
        main_payload = self.get_payload(self.base_url)
        if not main_payload:
            return
        for url in self.extract_tonie_urls(main_payload):
            tonie_payload = self.get_payload(url)
            if not tonie_payload:
                continue
            yield self.create_tonie_object(tonie_payload)
            time.sleep(1)
