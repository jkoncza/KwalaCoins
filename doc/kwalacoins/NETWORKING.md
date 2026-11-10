# KwalaCoins networking and automatic peer discovery

**Honest status:** the discovery *software* is complete and tested. Public automatic discovery is **not
operational yet**, because no KwalaCoins DNS seed or bootstrap node has been deployed. Until real seeds exist
(see `SEED_DEPLOYMENT.md`), a new node can only find peers you give it (`-addnode`, `-seednode`,
`-dnsseedhost`, `-fixedseedfile`) or peers that connect to it. This document never lists invented servers.

## 1. Audit of the original networking code

| Item | What was found |
|---|---|
| `src/kernel/chainparams.cpp` mainnet | `vSeeds.clear()` and `vFixedSeeds = chainparams_seed_main()`. The `.clear()` calls removed Bitcoin's DNS seeds; they are correct, not a bug, but leave **no** discovery source. |
| `src/chainparamsseeds.h` | Verified: contains **zero** entries (no Bitcoin addresses, nothing on port 8333). Testnet, testnet4 and signet fixed seeds are also empty. Bitcoin's built-in seed list was fully removed. |
| `contrib/seeds/*.txt`, `generate-seeds.py`, README | `nodes_*.txt` were Bitcoin-derived; now empty with KwalaCoins instructions. README previously pointed at Bitcoin seed crawlers; rewritten. |
| `src/net.cpp` DNS seeding | Bitcoin Core's `ThreadDNSAddressSeed` is intact (multiple seeds, shuffled, staggered, only 3 seeds queried at once once peers are known, failures tolerated). It only read the compiled-in list, so seeds could not be added without recompiling. |
| `src/net.cpp` fixed seeds | Intact fallback (immediately if `-dnsseed=0` and no addnode/seednode, otherwise after 60 s with an empty addrman). Only compiled-in list was supported. |
| `src/addrman.cpp`, `net_processing.cpp` | Untouched: address manager, `addr`/`addrv2` relay, `getaddr`, eviction, feeler connections, anchors, reconnection. |
| Peer validation | Network magic is checked on every message (wrong magic => disconnect, v1 and v2 transport). `MIN_PEER_PROTO_VERSION` rejects old protocol. The P2P version message carries no genesis hash; a peer on a *different* chain is rejected because its headers do not connect to the KwalaCoins genesis block and are dropped/penalised. Bitcoin nodes use a different magic (`f9beb4d9` vs KwalaCoins `c74b57a1`), so they are rejected at the first message. |

Network identity (unchanged): P2P 9777, RPC 9776 (localhost only by default), magic `c7 4b 57 a1`,
genesis `000005a7744de206a970ec5617008850bf853009c2f121f087c63c7902a72625`, block target spacing **120 s**.

## 2. What was changed (files)

| File | Change |
|---|---|
| `src/init.cpp` | New options `-dnsseedhost=<domain>` (repeatable) and `-fixedseedfile=<file>` (repeatable). |
| `src/net.cpp` | DNS seeding also queries every `-dnsseedhost`; a clear log line when no seeds exist; fixed-seed fallback also loads `-fixedseedfile` entries (skips malformed or non-routable lines, logs them); warning when the node has no discovery source at all. |
| `src/kernel/chainparams.cpp` | Target block spacing 120 s (mainnet and testnet), retarget window 720 blocks (1 day), activation window/thresholds scaled (648 / 540). Seed lists stay empty. Genesis block and magic untouched. |
| `src/chainparamsseeds.h`, `contrib/seeds/*` | Clean, empty, KwalaCoins-specific, with generation instructions. |
| `test/kwalacoins/network_tests.py` | New automated network test-suite (section 6). |
| `doc/kwalacoins/*`, `README.md`, `MINING.md`, `kwalacoin.conf.example` | Documentation. |

No consensus, transaction-validation, block-validation, proof-of-work or genesis code was modified by the
networking work. Bitcoin's address manager and relay code were preserved.

## 3. How a new node finds peers (order of precedence)
1. `-connect` (if set, nothing else is used).
2. `-seednode=<ip:port>`: connect once, ask for addresses, disconnect.
3. `peers.dat` / `anchors.dat` from earlier runs.
4. DNS seeds: built-in list (empty today) plus every `-dnsseedhost=<domain>`. The node asks for `x9.<domain>`.
   Several independent seed operators are supported; unresolvable seeds are logged and skipped.
5. Fixed seeds if still nothing: compiled list plus `-fixedseedfile` entries (after 60 s, or immediately with
   `-dnsseed=0`).
6. Peer exchange (`getaddr` / `addr` / `addrv2`) once connected: this is how the network grows after bootstrap.

Config example (`~/.kwalacoin/kwalacoin.conf`), placeholders only:
```
dnsseed=1
dnsseedhost=seed1.example-kwala-seed.invalid     # REPLACE with a real seed once one exists
dnsseedhost=seed2.example-kwala-other-operator.invalid
fixedseedfile=/path/to/nodes_main.txt            # one ip:port per line
```

## 4. Updating seeds
* Runtime (no rebuild): edit the `dnsseedhost=` lines or the `fixedseedfile` text file.
* Compiled in (releases): put verified, reachable, long-running nodes in `contrib/seeds/nodes_main.txt`
  (`ip:9777`), run `python3 contrib/seeds/generate-seeds.py contrib/seeds > src/chainparamsseeds.h`, and to
  ship DNS seeds add `vSeeds.emplace_back("seed1.<your-domain>.");` in `chainparams.cpp` (mainnet block).
  Never add addresses you have not verified are real KwalaCoins nodes.

## 5. Connect two computers to the same network (no seed servers needed)
Computer 1 (reachable on TCP 9777; open it in firewall/router; **do not** open 9776):
```
kwalacoind -maxtipage=315360000 -externalip=<computer-1-public-ip>
```
Computer 2:
```
kwalacoind -maxtipage=315360000 -addnode=<computer-1-public-ip>:9777
```
Check: `kwalacoin-cli getpeerinfo`, `kwalacoin-cli getblockhash 0` must equal the genesis hash above on both.
Mine on either with `contrib/kwalacoins/kwala_miner.py` (see `MINING.md`). `-maxtipage` is only needed while
the chain is brand new / has no recent blocks.

## 6. Tests
```
python3 test/kwalacoins/network_tests.py --bin src      # needs Linux + root; ~1-2 minutes
```
It starts three real mainnet-parameter nodes on loopback aliases (11.1.0.1, 12.2.0.1, 13.3.0.1, added
temporarily, because nodes refuse non-routable addresses) and verifies: genesis agreement; two-node sync;
DNS discovery with two seed operators and one unresolvable seed; graceful handling when all seeds are down;
fixed-seed fallback; three-node peer exchange (a node that only knows B learns and connects to A) and block
sync; reconnection after a node restarts; rejection of Bitcoin-magic, Bitcoin-testnet, random-magic and
old-protocol peers; rejection of headers from a chain not rooted in the KwalaCoins genesis (with a control
case proving a legitimate header is accepted).

Result when this was run: 9/9 passed (Linux x86-64 build).
Not tested: a *second chain with a different genesis and the same magic* as a running node (needs a second
build); real internet DNS; Windows/macOS runtime; the Qt GUI.
