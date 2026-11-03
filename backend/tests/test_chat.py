"""Offline tests for the NVIDIA chat backend.

The NVIDIA API is replaced with a fake httpx AsyncClient; no network or real
API key is required.
"""
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

os.environ.setdefault("NVIDIA_API_KEY", "test-key")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

import app.main as main


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


class FakeAsyncClient:
    """Records the payload it is asked to POST."""

    last_payload = None

    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def post(self, url, headers=None, json=None):
        FakeAsyncClient.last_payload = json
        return FakeResponse(
            {
                "choices": [{"message": {"content": "ok"}, "finish_reason": "stop"}],
                "model": json["model"],
                "usage": {},
            }
        )


class TestTemperaturePassthrough(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app)

    def _post(self, **overrides):
        body = {"messages": [{"role": "user", "content": "hi"}]}
        body.update(overrides)
        with mock.patch.object(main.httpx, "AsyncClient", FakeAsyncClient):
            resp = self.client.post("/api/chat", json=body)
        self.assertEqual(resp.status_code, 200)
        return FakeAsyncClient.last_payload

    def test_explicit_zero_temperature_is_preserved(self):
        payload = self._post(temperature=0.0)
        self.assertEqual(payload["temperature"], 0.0)

    def test_omitted_temperature_uses_default(self):
        payload = self._post()
        self.assertEqual(payload["temperature"], main.TEMPERATURE)

    def test_explicit_temperature_is_preserved(self):
        payload = self._post(temperature=0.2)
        self.assertEqual(payload["temperature"], 0.2)


if __name__ == "__main__":
    unittest.main()
