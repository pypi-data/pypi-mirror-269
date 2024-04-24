from typing import Optional
from json import dumps, loads

import urllib.request


class TrackingMore:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def request(self, endpoint: str, payload: Optional[dict | str] = None, method: Optional[str] = None):
        url = f"https://api.trackingmore.com/v3/trackings/{endpoint}"

        headers = {"Tracking-Api-Key": self.api_key}

        if isinstance(payload, dict):
            payload = dumps(payload)

        if payload:
            headers["Content-Type"] = "application/json"

        if payload and not method:
            method = "POST"
        elif method:
            method = method.upper()
        else:
            method = "GET"

        req = urllib.request.Request(
            url, payload.encode() if payload else None, headers=headers, method=method)

        res = urllib.request.urlopen(req)
        return loads(res.read())

    def get_carriers(self):
        return self.request("carriers").get("data", [])

    def detect_carrier(self, tracking_number: str):
        return self.request("detect", {"tracking_number": tracking_number}).get("data", {})

    def track_shipment(self, tracking_number: str, carrier_code: Optional[str] = None):
        payload = {
            "tracking_number": tracking_number,
            "courier_code": carrier_code or self.detect_carrier(tracking_number)[0]["courier_code"]
        }

        return self.request("realtime", payload).get("data", {})
