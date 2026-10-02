#!/usr/bin/env python3
"""Trigger sniper cycle on Vercel + report result.

Usage:
  python3 scripts/trigger_sniper.py
  python3 scripts/trigger_sniper.py --chain base
  python3 scripts/trigger_sniper.py --mint <contract_address>

No env vars needed — Vercel endpoint reads its own env vars (PIMLICO_API_KEY,
SIGNER_PRIVATE_KEY, PIMLICO_SPONSOR_POLICY_ID, etc.) from Vercel project settings.
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error

VERCEL_URL = os.environ.get("SNIPER_URL", "https://base-airdrop-radar.vercel.app")
CRON_SECRET = os.environ.get("CRON_SECRET", "")  # optional


def call_endpoint(path: str, method: str = "POST", timeout: int = 90) -> dict:
    url = f"{VERCEL_URL}{path}"
    if CRON_SECRET:
        url += f"?secret={CRON_SECRET}"

    print(f"[Trigger] {method} {url}")
    req = urllib.request.Request(url, method=method, headers={
        "Accept": "application/json",
        "User-Agent": "makar52nn2016-jpg-sniper-trigger",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode()
            try:
                return {"status": resp.status, "json": json.loads(body)}
            except json.JSONDecodeError:
                return {"status": resp.status, "text": body[:2000]}
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:2000]
        return {"status": e.code, "error": body}
    except Exception as e:
        return {"status": 0, "error": str(e)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chain", help="Optional: filter to chain")
    parser.add_argument("--mint", help="Optional: try mint on contract address")
    parser.add_argument("--scan-only", action="store_true", help="Run only scan, no mint")
    args = parser.parse_args()

    print("=" * 60)
    print(f"[Trigger] Target: {VERCEL_URL}")
    print(f"[Trigger] Time: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    print("=" * 60)

    if args.scan_only:
        result = call_endpoint("/api/sniper/scan")
    elif args.mint:
        # mint endpoint requires contract in body
        url = f"{VERCEL_URL}/api/sniper/mint"
        if CRON_SECRET:
            url += f"?secret={CRON_SECRET}"
        body = json.dumps({"contractAddress": args.mint, "chain": args.chain or "base"}).encode()
        req = urllib.request.Request(url, data=body, method="POST", headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "makar52nn2016-jpg-sniper-trigger",
        })
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                result = {"status": resp.status, "json": json.loads(resp.read().decode())}
        except urllib.error.HTTPError as e:
            result = {"status": e.code, "error": e.read().decode()[:2000]}
        except Exception as e:
            result = {"status": 0, "error": str(e)}
        print(f"\n[Mint] Result: {json.dumps(result, indent=2)[:3000]}")
        return
    else:
        # Default: run full cycle (scan + mint top candidates)
        result = call_endpoint("/api/sniper/run")

    print(f"\n[Result] HTTP {result.get('status', '?')}")
    if "json" in result:
        print(json.dumps(result["json"], indent=2, ensure_ascii=False)[:4000])
    elif "text" in result:
        print(result["text"][:2000])
    elif "error" in result:
        print(f"ERROR: {result['error'][:2000]}")

    # Try to extract key info
    if "json" in result:
        data = result["json"]
        if isinstance(data, dict):
            success = data.get("success", False)
            scanned = data.get("scanned", 0)
            results = data.get("results", []) or []
            attempted = len(results)
            minted = sum(1 for r in results if r.get("success"))
            failed = attempted - minted
            print("\n" + "=" * 60)
            print(f"  SUCCESS: {success}")
            print(f"  SCANNED: {scanned}    ATTEMPTED: {attempted}    MINTED: {minted}    FAILED: {failed}")
            print(f"  RESULTS (first 5):")
            for r in results[:5]:
                cand = r.get("candidate", {}) or {}
                ok = "✓" if r.get("success") else "✗"
                err = (r.get("error") or "")[:140]
                print(f"    {ok} {cand.get('chain','?')} | {cand.get('contract','?')[:14]}... | {err}")
            print("=" * 60)


if __name__ == "__main__":
    main()
