<p align="center"><img src="doc/kwala-logo.png" width="120" alt="KwalaCoins"></p>

# KwalaCoins (KWALA)

**KwalaCoins is its own coin and network**, built from the open-source Bitcoin Core codebase (MIT license)
but with its own chain, supply, speed, addresses, ports, genesis block, message-signing domain and branding.
 Programs: `kwalacoind`, `kwalacoin-cli`, `kwalacoin-tx`, `kwalacoin-util`, `kwalacoin-wallet`.

## Specs

| | KwalaCoins |
|---|---|
| Max supply | **500,000,000 KWALA** |
| Block time | **120 seconds** target |
| Block reward | 100 KWALA, halving every 2,500,000 blocks (~9.5 years at 120 s) |
| Difficulty retarget | every 720 blocks (~1 day), so it reacts to hash power quickly |
| Algorithm | SHA-256d proof-of-work, Schnorr/Taproot, SegWit, v2 encrypted P2P |
| Ports | P2P 9777, RPC 9776 (testnet 19777/19776, regtest 19444/19443) |
| Addresses | legacy `W...`, script `K...`, bech32 `kwala1...` (testnet `tkwala1...`) |
| Network magic | `c7 4b 57 a1` |
| Genesis | `000005a7744de206a970ec5617008850bf853009c2f121f087c63c7902a72625` (5 Nov 2026) |
| Data dir / config | `~/.kwalacoin/kwalacoin.conf` (see `kwalacoin.conf.example`) |
| User agent | `/KwalaCoins:1.0.0/` |

## Improvements over the Bitcoin baseline
- **Timewarp attack fix** (BIP94 rules) enforced from block 1 on every KwalaCoins network.
- **No legacy baggage:** BIP34/65/66, CSV, SegWit and Taproot are active from genesis; no historic
  script-validation exceptions, checkpoints, assumeutxo snapshots or inherited Bitcoin seed nodes.
- **Faster and more responsive:** daily difficulty retargeting.
- **Own genesis** for mainnet and testnet, with an easy starting difficulty so a new network can bootstrap.
- Supply math is checked: `python3 contrib/kwalacoins/check_supply.py` -> 499,999,999.725 KWALA (<= cap).


## 🌐 Connecting to the KwalaCoins Network

KwalaCoins currently does not have public DNS seed servers. To connect to the KwalaCoins network, users must manually add an initial peer.

### Method 1: Using the `kwalacoin.conf` File

1. Open File Explorer Then go into your search bar.
2. Enter `C:\Users\<YOUR_USER_NAME>\AppData\Local\KwalaCoin` and press Enter. This opens your KwalaCoins data directory inside your Windows user profile.
3. Look for a file named `kwalacoin.conf`.
4. If the file does not exist, create a new text file named `kwalacoin.conf`.
5. Open the file and add the following line:

```ini
addnode=158.247.73.205:9777
```

6. Save the file and restart your KwalaCoins wallet.

### Method 2: Using the GUI Console

1. Open your KwalaCoins wallet.
2. Navigate to **Window → Console**.
3. Enter the following command:

```bash
addnode "158.247.73.205:9777" "add"
```

4. Press Enter to connect to the KwalaCoins network.

### Network Information

The following node is provided as an initial connection point for users joining the KwalaCoins network:

**Node:** `158.247.73.205:9777`

As the KwalaCoins network grows, additional public nodes and DNS seed servers may become available.


## Build (verified on Linux, g++ 13)
    ./autogen.sh
    ./configure --without-gui --enable-wallet
    make -j$(nproc)          # binaries land in src/
See `doc/build-unix.md` for dependencies (Boost headers, libevent, sqlite3).

## Quick start
    ./src/kwalacoind -daemon
    ./src/kwalacoin-cli createwallet mywallet
    ./src/kwalacoin-cli getnewaddress          # a kwala1... address
Automatic peer discovery is implemented (DNS seeds, fixed seeds, peer exchange) but **no public seed servers exist yet**:
until you deploy some, connect nodes with `addnode=<ip>:9777`. See `doc/kwalacoins/NETWORKING.md` and `SEED_DEPLOYMENT.md`.
For local testing use `-regtest` (`kwalacoin-cli -regtest generatetoaddress 101 <addr>`).

## Networking and tests
- `-dnsseedhost=<domain>` and `-fixedseedfile=<file>` let you supply seeds without rebuilding.
- `python3 test/kwalacoins/network_tests.py --bin src` runs the 3-node network test-suite (9 tests, passing on Linux).


## License
MIT (see `COPYING`). Built on Bitcoin Core, (c) The Bitcoin Core developers; KwalaCoins changes (c) 2026 The KwalaCoins developers.
