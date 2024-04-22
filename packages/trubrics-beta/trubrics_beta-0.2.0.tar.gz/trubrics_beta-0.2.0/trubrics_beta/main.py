import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import requests


class Trubrics:
    def __init__(
        self,
        api_key: str,
        host: str = "https://api.trubrics.com",
        max_workers: int | None = None,
    ):
        self.host = host
        self.api_key = api_key
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def track(self, user_id: str, event: str, properties: dict | None = None):
        self.executor.submit(self.post, self._post_body(user_id, event, properties))

    def post(self, data: dict):
        with requests.Session() as session:
            try:
                post_request = session.post(
                    f"{self.host}/publish_event",
                    params={"project_api_key": self.api_key},
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(data),
                )
                post_request.raise_for_status()
            except Exception as e:
                raise ValueError(f"Error posting event: {e}")

    def _post_body(self, user_id: str, event: str, properties: dict | None = None):
        return {
            "user_id": user_id,
            "event": event,
            "properties": properties,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
