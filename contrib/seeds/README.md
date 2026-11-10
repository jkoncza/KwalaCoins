# KwalaCoins seeds

`nodes_main.txt`, `nodes_test.txt`, `nodes_testnet4.txt` hold the fixed-seed lists that are compiled into the
client (see `src/chainparamsseeds.h`). They are intentionally **empty**: no public KwalaCoins nodes exist yet.
Only add addresses of real, verified, long-running KwalaCoins nodes (mainnet port 9777), one per line:
`<ip>:9777`, `[<ipv6>]:9777`, `<name>.onion:9777`.

Regenerate the header (from the repo root):

    python3 contrib/seeds/generate-seeds.py contrib/seeds > src/chainparamsseeds.h

Users can also supply seeds at run time with `-fixedseedfile=<file>` and `-dnsseedhost=<domain>` (no rebuild).
`makeseeds.py` is the Bitcoin-era crawler post-processor and still contains Bitcoin-specific filters; do not
use it unchanged. See `doc/kwalacoins/NETWORKING.md` and `SEED_DEPLOYMENT.md`.
