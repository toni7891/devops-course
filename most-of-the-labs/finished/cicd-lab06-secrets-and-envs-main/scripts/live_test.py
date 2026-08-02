#!/usr/bin/env python
"""Live smoke test against an ALREADY-RUNNING server + real MongoDB.

REFERENCE SOLUTION (instructor copy)
====================================
This script does NOT start the server. The CI workflow (or you, locally)
starts it in a separate step / terminal first. This script only makes
HTTP calls against it and FAILS LOUDLY if anything is wrong.

Exercises the full user lifecycle: health -> status -> create -> read ->
update -> delete -> confirm-gone. Used to validate the pipeline works
before lab instructions are written.

Run locally — terminal 1:

    python -m uvicorn app.main:app --port 3000

Terminal 2:

    python scripts/live_test.py

Required env (same vars app/config.py reads): APP_ENV, PORT.
Exit code 0 = all checks passed. Non-zero = something failed.
"""
from __future__ import annotations

import os
import sys
import time

import httpx

PORT = int(os.environ.get("PORT", "3000"))
BASE_URL = f"http://localhost:{PORT}"
REQUEST_TIMEOUT_S = 10
READY_TIMEOUT_S = 30


class CheckError(AssertionError):
    """Raised when a live check fails."""


def check(label: str, condition: bool, detail: str = "") -> None:
    """Assert `condition`; print a PASS/FAIL line either way."""
    if condition:
        print(f"PASS  {label}")
        return
    print(f"FAIL  {label}  {detail}")
    raise CheckError(f"{label} {detail}".strip())


def wait_until_ready() -> None:
    """Poll /livez until the (already-started) server answers.

    Provided. Guards against the test step racing the server step.
    """
    deadline = time.time() + READY_TIMEOUT_S
    while time.time() < deadline:
        try:
            if httpx.get(f"{BASE_URL}/livez", timeout=2).status_code == 200:
                print(f"Server reachable at {BASE_URL}")
                return
        except httpx.HTTPError:
            pass
        time.sleep(1)
    raise RuntimeError(f"Server not reachable within {READY_TIMEOUT_S}s")


def run_checks() -> None:
    """Exercise the live API end to end.

    Use a single httpx.Client. A unique email keeps re-runs from colliding
    on the unique-email constraint.
    """
    run_id = os.environ.get("GITHUB_RUN_ID", str(int(time.time())))
    email = f"live-{run_id}@example.com"

    with httpx.Client(base_url=BASE_URL, timeout=REQUEST_TIMEOUT_S) as client:
        # 1) Health
        r = client.get("/livez")
        check("GET /livez -> 200 ok", r.status_code == 200 and r.json().get("status") == "ok", str(r.text))

        r = client.get("/readyz")
        check(
            "GET /readyz -> 200 ready",
            r.status_code == 200 and r.json().get("status") == "ready",
            str(r.text),
        )

        # 2) Status reflects env
        r = client.get("/status")
        expected_env = os.environ.get("APP_ENV", "DEV").upper()
        check(
            "GET /status -> APP_ENV",
            r.status_code == 200 and r.json().get("status") == expected_env,
            f"want {expected_env}, got {r.text}",
        )

        # 3) Create a user
        r = client.post("/api/users", json={"name": "Live Tester", "email": email})
        check("POST /api/users -> 201 + id", r.status_code == 201 and "id" in r.json(), str(r.text))
        user_id: str = r.json()["id"]

        # 4) Read it back
        r = client.get(f"/api/users/{user_id}")
        check(
            "GET /api/users/{id} -> created user",
            r.status_code == 200 and r.json().get("email") == email,
            str(r.text),
        )

        # 5) Update it
        r = client.patch(f"/api/users/{user_id}", json={"name": "Live Tester Updated"})
        check(
            "PATCH /api/users/{id} -> updated",
            r.status_code == 200 and r.json().get("name") == "Live Tester Updated",
            str(r.text),
        )

        # 6) Delete it (cleanup — leave the DB clean)
        r = client.delete(f"/api/users/{user_id}")
        check("DELETE /api/users/{id} -> 204", r.status_code == 204, str(r.status_code))

        # 7) Confirm gone
        r = client.get(f"/api/users/{user_id}")
        check("GET deleted user -> 404", r.status_code == 404, str(r.status_code))


def main() -> int:
    try:
        wait_until_ready()
        run_checks()
        print("\nAll live checks passed")
        return 0
    except (CheckError, RuntimeError, httpx.HTTPError) as exc:
        print(f"\nLive test failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
