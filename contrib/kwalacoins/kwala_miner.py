#!/usr/bin/env python3
"""KwalaCoins solo CPU miner using the local KwalaCoins node's RPC.

Example (Windows):
  python kwala_miner.py --cli "C:\\Users\\Owner\\Documents\\KwalaCoins-GUI\\bin\\kwalacoin-cli.exe" --datadir "C:\\Users\\Owner\\AppData\\Local\\KwalaCoin" --address "YOUR_KWALA_RECEIVING_ADDRESS"

The miner prints progress every 500,000 hashes. Press Ctrl+C to stop.
"""
import argparse
import hashlib
import json
import struct
import subprocess
import time


def dsha(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def varint(n):
    if n < 0xfd:
        return bytes([n])
    if n <= 0xffff:
        return b"\xfd" + struct.pack("<H", n)
    if n <= 0xffffffff:
        return b"\xfe" + struct.pack("<I", n)
    return b"\xff" + struct.pack("<Q", n)


def push_num(n):
    if n == 0:
        return b"\x00"
    if 1 <= n <= 16:
        return bytes([0x50 + n])
    b = bytearray()
    while n:
        b.append(n & 0xff)
        n >>= 8
    if b[-1] & 0x80:
        b.append(0)
    return bytes([len(b)]) + bytes(b)


def merkle(hashes):
    if not hashes:
        return b"\x00" * 32
    hashes = list(hashes)
    while len(hashes) > 1:
        if len(hashes) % 2:
            hashes.append(hashes[-1])
        hashes = [
            dsha(hashes[i] + hashes[i + 1])
            for i in range(0, len(hashes), 2)
        ]
    return hashes[0]


def main():
    ap = argparse.ArgumentParser(description="KwalaCoins solo CPU miner")
    ap.add_argument("--cli", required=True, help="Full path to kwalacoin-cli.exe")
    ap.add_argument("--datadir", help="KwalaCoins data directory")
    ap.add_argument("--address", required=True, help="Your KwalaCoins receiving address")
    ap.add_argument("--blocks", type=int, default=0,
                    help="Stop after N accepted blocks (0 = keep mining)")
    ap.add_argument("--status-interval", type=int, default=500000,
                    help="Print progress every N hashes (default: 500000)")
    a = ap.parse_args()

    if a.blocks < 0 or a.status_interval < 1:
        ap.error("--blocks must be >= 0 and --status-interval must be >= 1")

    # Pass the executable and data directory as separate Windows arguments.
    # This avoids shlex parsing problems with Windows paths and spaces.
    cli = [a.cli]
    if a.datadir:
        cli.append("-datadir=" + a.datadir)

    def rpc(*args, raw=False):
        out = subprocess.run(
            cli + [str(x) for x in args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if out.returncode:
            message = out.stderr.strip() or out.stdout.strip()
            raise RuntimeError(message or f"kwalacoin-cli exited with code {out.returncode}")
        result = out.stdout.strip()
        return result if raw else json.loads(result)

    info = rpc("validateaddress", a.address)
    if not info.get("isvalid"):
        raise SystemExit("ERROR: KwalaCoins node says this receiving address is invalid.")

    script_pub_key = bytes.fromhex(info["scriptPubKey"])
    print("Address accepted by KwalaCoins node.", flush=True)
    print("Requesting a block template...", flush=True)

    mined = 0
    while a.blocks == 0 or mined < a.blocks:
        template = rpc("getblocktemplate", '{"rules":["segwit"]}')
        height = template["height"]
        transactions = template.get("transactions", [])

        # BIP34 block height followed by a short miner tag.
        script_sig = push_num(height) + b"\x04kwal"
        if len(script_sig) < 2 or len(script_sig) > 100:
            raise RuntimeError("Coinbase scriptSig length is outside consensus limits.")

        outputs = [(template["coinbasevalue"], script_pub_key)]
        commitment_hex = template.get("default_witness_commitment")
        has_witness = bool(commitment_hex)
        if has_witness:
            outputs.append((0, bytes.fromhex(commitment_hex)))

        def serialize_coinbase(include_witness):
            tx = struct.pack("<i", 1)  # transaction version
            if include_witness:
                tx += b"\x00\x01"  # SegWit marker and flag

            # One coinbase input.
            tx += b"\x01"
            tx += b"\x00" * 32
            tx += struct.pack("<I", 0xffffffff)
            tx += varint(len(script_sig)) + script_sig
            tx += struct.pack("<I", 0xffffffff)

            # Coinbase outputs.
            tx += varint(len(outputs))
            for value, script in outputs:
                tx += struct.pack("<q", value)
                tx += varint(len(script)) + script

            # Witness reserved value required by the witness commitment.
            if include_witness:
                tx += b"\x01\x20" + b"\x00" * 32

            return tx + struct.pack("<I", 0)

        coinbase_txid = dsha(serialize_coinbase(False))
        txids = [coinbase_txid]
        txids.extend(bytes.fromhex(tx["txid"])[::-1] for tx in transactions)
        merkle_root = merkle(txids)

        target = int(template["target"], 16)
        previous_hash = bytes.fromhex(template["previousblockhash"])[::-1]
        header_prefix = (
            struct.pack("<i", template["version"])
            + previous_hash
            + merkle_root
            + struct.pack("<I", template["curtime"])
            + struct.pack("<I", int(template["bits"], 16))
        )

        print(
            f"Mining block height {height} "
            f"(difficulty {template.get('difficulty', 'see node')}); "
            f"{len(transactions)} transactions in template.",
            flush=True,
        )

        nonce = 0
        checked = 0
        started = time.time()
        last_report = started
        found_nonce = None

        # Keep advancing nonce until a valid hash is found or all 2^32
        # nonce values are exhausted. Never restart at nonce zero every 20s.
        while nonce < 2**32:
            header = header_prefix + struct.pack("<I", nonce)
            block_hash = dsha(header)
            checked += 1

            if int.from_bytes(block_hash, "little") <= target:
                found_nonce = nonce
                break

            nonce += 1
            if checked % a.status_interval == 0:
                now = time.time()
                elapsed = max(now - started, 0.001)
                rate = checked / elapsed
                print(
                    f"Progress: {checked:,} hashes checked; "
                    f"{rate:,.0f} hashes/sec; "
                    f"{elapsed:.1f}s elapsed; "
                    f"nonce {nonce:,}.",
                    flush=True,
                )
                last_report = now

        if found_nonce is None:
            print("Nonce range exhausted; requesting a fresh block template.", flush=True)
            continue

        block = (
            header_prefix
            + struct.pack("<I", found_nonce)
            + varint(len(txids))
            + serialize_coinbase(has_witness)
            + b"".join(bytes.fromhex(tx["data"]) for tx in transactions)
        )

        print("Valid proof of work found; submitting block to your node...", flush=True)
        result = rpc("submitblock", block.hex(), raw=True)

        if result in ("", "null"):
            mined += 1
            displayed_hash = dsha(header_prefix + struct.pack("<I", found_nonce))[::-1].hex()
            print(
                f"SUCCESS: node accepted block {height}; "
                f"hash {displayed_hash}; accepted blocks this run: {mined}.",
                flush=True,
            )
        else:
            print(f"BLOCK REJECTED by node: {result}", flush=True)

    print(f"Finished. Accepted blocks: {mined}.", flush=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.", flush=True)
    except Exception as exc:
        print(f"\nERROR: {exc}", flush=True)
        raise
