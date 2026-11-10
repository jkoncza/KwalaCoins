# Deploying KwalaCoins seed infrastructure

**None of this exists yet.** KwalaCoins has no public DNS seeds or bootstrap nodes. This is the checklist to
create them. Everything below uses placeholders (`<...>` / `.invalid`); do not publish them as real.

## 1. Bootstrap nodes (needed first)
Run at least 3-5 long-lived full nodes, in different networks/hosts/countries, with static IPs:
```
# kwalacoin.conf on each bootstrap node
server=1
listen=1
externalip=<public-ipv4-of-this-node>
rpcbind=127.0.0.1          # RPC must stay private
rpcallowip=127.0.0.1
txindex=0
maxconnections=125
```
Firewall (example `ufw`): allow `9777/tcp` from anywhere; allow SSH from your own IP only; **never** open `9776`.
```
ufw default deny incoming && ufw allow from <your-admin-ip> to any port 22 && ufw allow 9777/tcp && ufw enable
```
Verify each node is reachable from outside: `nc -vz <ip> 9777`, and `kwalacoin-cli getpeerinfo` shows inbound peers.
Connect the bootstrap nodes to each other with `addnode=` until the network has other members.

## 2. DNS seeds (at least two independent operators)
A DNS seed is a DNS server that answers A/AAAA queries with IPs of healthy KwalaCoins nodes. Use a crawler
(an open-source Bitcoin-style DNS seeder, e.g. sipa's `bitcoin-seeder`, adapted) which must be changed to
KwalaCoins values: network magic `c7 4b 57 a1`, port 9777, genesis hash, user-agent filter and protocol
version. *I have not built or tested such a seeder; adapting it is your task.* Each operator runs their own.

DNS records per operator (placeholders):
```
; zone example-kwala-seed.invalid  (you own the real domain)
seed1   IN NS   ns1.seed1.<operator-domain>.
ns1.seed1 IN A  <seeder-server-ipv4>
; and for IPv6 if available
```
Seeders must answer `x9.<seed-domain>` too (the node queries `x9.seed1.<domain>`; `9` = NODE_NETWORK|NODE_WITNESS).
Open `53/udp` and `53/tcp` on the seeder host. Test: `dig x9.seed1.<operator-domain> A` returns reachable node IPs.

## 3. Wiring seeds into clients
* Per user, no rebuild: `dnsseedhost=seed1.<operator-domain>` and `dnsseedhost=seed2.<other-operator-domain>`.
* In releases: add both domains to the mainnet block of `src/kernel/chainparams.cpp` with
  `vSeeds.emplace_back("seed1.<operator-domain>.");` and bake verified IPs via `contrib/seeds/` (see `NETWORKING.md` section 4).

## 4. Monitoring and maintenance
* Alert if `getconnectioncount` is 0, `getblockcount` falls behind peers, or `9777` stops answering.
* Check each seed domain from outside weekly: `dig x9.<seed> A`; remove seeds that return dead IPs.
* Keep at least two seed operators so one failure does not strand new nodes; rotate fixed seeds each release.
* Back up nothing secret on seed hosts (they need no wallet). Keep the OS and kwalacoind updated.
* Do not use Bitcoin nodes, Bitcoin DNS seeds or random third-party IPs as bootstrap sources.
