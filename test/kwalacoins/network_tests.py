#!/usr/bin/env python3
"""KwalaCoins peer-discovery / networking test-suite (mainnet parameters, real nodes, real sockets).

Needs: Linux, root (adds loopback aliases 11.1.0.1 / 12.2.0.1 / 13.3.0.1 because Bitcoin-derived nodes
refuse to store non-routable addresses, and appends test names to /etc/hosts for the DNS seed tests),
Python 3 and the built kwalacoind + kwalacoin-cli.

    python3 test/kwalacoins/network_tests.py --bin src [--keep]

Covered: genesis agreement, two-node sync, three-node sync, DNS-seed discovery (multiple seed operators,
unresolvable seed tolerated), fixed-seed fallback (-fixedseedfile), addr peer exchange, reconnection after a
node restarts, wrong-network-magic / Bitcoin-node / old-protocol rejection, and rejection of headers
that are not rooted in the KwalaCoins genesis block.
"""
import argparse, fcntl, hashlib, json, os, shutil, socket, struct, subprocess, sys, tempfile, time

GENESIS = "000005a7744de206a970ec5617008850bf853009c2f121f087c63c7902a72625"
MAGIC = bytes.fromhex("c74b57a1")
BITCOIN_MAGIC = bytes.fromhex("f9beb4d9")
MINE_ADDR = "kwala1qw508d6qejxtdg4y5r3zarvary0c5xw7k35qhye"
IPS = {"A": "11.1.0.1", "B": "12.2.0.1", "C": "13.3.0.1"}
HERE = os.path.dirname(os.path.abspath(__file__))
MINER = os.path.join(HERE, "..", "..", "contrib", "kwalacoins", "kwala_miner.py")
results = []

def dsha(b): return hashlib.sha256(hashlib.sha256(b).digest()).digest()

def add_alias(i, ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    name = f"lo:{i}".encode()
    fcntl.ioctl(s, 0x8916, struct.pack('16sH2s4s8s', name, socket.AF_INET, b'\0\0', socket.inet_aton(ip), b'\0' * 8))
    fcntl.ioctl(s, 0x891C, struct.pack('16sH2s4s8s', name, socket.AF_INET, b'\0\0', socket.inet_aton("255.255.255.255"), b'\0' * 8))

class Node:
    def __init__(self, name, ip, idx, binpath, root, extra=()):
        self.name, self.ip, self.bin = name, ip, binpath
        self.dir = os.path.join(root, name); os.makedirs(self.dir, exist_ok=True)
        self.rpcport = 29000 + idx
        self.onion = 29100 + idx
        self.extra = list(extra); self.proc = None
    def args(self):
        return [os.path.join(self.bin, "kwalacoind"), f"-datadir={self.dir}", "-listen=1", f"-bind={self.ip}:9777",
                f"-bind=127.0.0.1:{self.onion}=onion", f"-rpcport={self.rpcport}", f"-externalip={self.ip}",
                "-maxtipage=315360000", "-dnsseed=0", "-fixedseeds=0", "-discover=0", "-server=1", "-printtoconsole=0"] + self.extra
    def start(self, extra=None):
        a = self.args() + (extra or [])
        self.proc = subprocess.Popen(a, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            try: self.cli("getblockcount"); return
            except Exception: time.sleep(0.5)
        raise RuntimeError(f"{self.name} did not start")
    def cli(self, *args):
        o = subprocess.run([os.path.join(self.bin, "kwalacoin-cli"), f"-datadir={self.dir}", f"-rpcport={self.rpcport}", "-rpcwait=0"] + [str(x) for x in args],
                           capture_output=True, text=True, timeout=60)
        if o.returncode: raise RuntimeError(o.stderr.strip())
        out = o.stdout.strip()
        try: return json.loads(out)
        except Exception: return out
    def stop(self):
        if self.proc:
            try: self.cli("stop")
            except Exception: pass
            try: self.proc.wait(30)
            except Exception: self.proc.kill()
            self.proc = None
    def peers(self): return self.cli("getpeerinfo")
    def log(self): return open(os.path.join(self.dir, "debug.log"), errors="replace").read()

def wait_for(cond, timeout, what):
    end = time.time() + timeout
    while time.time() < end:
        try:
            if cond(): return
        except Exception: pass
        time.sleep(1)
    raise AssertionError("timeout waiting for " + what)

def mine(node, n):
    subprocess.run([sys.executable, MINER, "--cli", f"{os.path.join(node.bin,'kwalacoin-cli')} -datadir={node.dir} -rpcport={node.rpcport}",
                    "--address", MINE_ADDR, "--blocks", str(n)], check=True, capture_output=True, text=True, timeout=600)

def clear_peers(node):
    for f in ("peers.dat", "anchors.dat", "banlist.json"):
        try: os.remove(os.path.join(node.dir, f))
        except OSError: pass

def has_peer(node, ip): return any(p["addr"].startswith(ip + ":") for p in node.peers())

def test(fn):
    def run(*a, **k):
        t = time.time()
        try:
            fn(*a, **k); results.append((fn.__name__, "PASS", time.time() - t)); print(f"PASS  {fn.__name__}", flush=True)
        except Exception as e:
            results.append((fn.__name__, f"FAIL: {e}", time.time() - t)); print(f"FAIL  {fn.__name__}: {e}", flush=True)
    return run

# ---------- raw-socket helpers ----------
def msg(magic, cmd, payload=b""):
    return magic + cmd.ljust(12, b"\0") + struct.pack("<I", len(payload)) + dsha(payload)[:4] + payload
def version_payload(ver=70016):
    na = struct.pack("<Q", 0) + b"\0" * 10 + b"\xff\xff" + b"\x7f\0\0\1" + struct.pack(">H", 9777)
    ua = b"/kwala-test:1/"
    return struct.pack("<iQq", ver, 9, int(time.time())) + na + na + struct.pack("<Q", int.from_bytes(os.urandom(8), "little")) + bytes([len(ua)]) + ua + struct.pack("<i", 0) + b"\1"
def read_msgs(sock, wait):
    sock.settimeout(wait); buf = b""; closed = False
    try:
        while True:
            d = sock.recv(65536)
            if not d: closed = True; break
            buf += d
    except socket.timeout: pass
    except OSError: closed = True
    cmds = []; i = 0
    while len(buf) - i >= 24 and buf[i:i+4] == MAGIC:
        ln = struct.unpack("<I", buf[i+16:i+20])[0]; cmds.append(buf[i+4:i+16].rstrip(b"\0").decode()); i += 24 + ln
    return cmds, closed, buf

def mine_header(prev_hash_le, bits=0x1e0fffff):
    target = (bits & 0xffffff) << (8 * ((bits >> 24) - 3)); merkle = os.urandom(32); t = int(time.time()); n = 0
    while True:
        h = struct.pack("<i", 0x20000000) + prev_hash_le + merkle + struct.pack("<III", t, bits, n)
        if int.from_bytes(dsha(h), "little") <= target: return h
        n += 1

# ---------- tests ----------
@test
def t_genesis_and_two_node_sync(A, B):
    for n in (A, B): assert n.cli("getblockhash", 0) == GENESIS, f"{n.name} genesis mismatch"
    A.cli("addnode", f"{B.ip}:9777", "add")
    wait_for(lambda: has_peer(A, B.ip) or has_peer(B, A.ip), 60, "A<->B connection")
    mine(A, 3)
    wait_for(lambda: B.cli("getblockcount") == 3 and B.cli("getbestblockhash") == A.cli("getbestblockhash"), 60, "B sync to height 3")

@test
def t_dns_discovery_multi_seed(A, B, C):
    # B and C find A only through DNS seeds (two independent seed operators; one is unresolvable)
    for n in (B, C): n.stop(); clear_peers(n)
    B.start(["-dnsseed=1", "-dnsseedhost=seed.kwalatest.local", "-dnsseedhost=seed2.kwalatest.local", "-dnsseedhost=does-not-exist.kwalatest.invalid"])
    wait_for(lambda: has_peer(B, A.ip), 90, "B discovers A via DNS seed")
    assert "Loading addresses from DNS seed seed.kwalatest.local" in B.log() or "Loading addresses from DNS seed seed2.kwalatest.local" in B.log()
    wait_for(lambda: B.cli("getblockcount") == A.cli("getblockcount"), 60, "B syncs from DNS-discovered peer")

@test
def t_dns_all_seeds_down_is_graceful(A, C):
    C.stop(); clear_peers(C)
    C.start(["-dnsseed=1", "-dnsseedhost=down1.kwalatest.invalid", "-dnsseedhost=down2.kwalatest.invalid"])
    time.sleep(8)
    assert C.cli("getblockcount") is not None  # still alive, no crash, no endless loop
    assert C.log().count("Loading addresses from DNS seed") <= 4, "DNS seeds queried too often"
    C.stop()

@test
def t_fixed_seed_fallback(A, C, tmp):
    C.stop()
    for f in ("peers.dat", "anchors.dat"):
        try: os.remove(os.path.join(C.dir, f))
        except OSError: pass
    seedfile = os.path.join(tmp, "nodes_main.txt")
    open(seedfile, "w").write(f"# test fixed seeds\n{A.ip}:9777\nnot-an-address\n")
    C.start([f"-fixedseedfile={seedfile}", "-fixedseeds=1"])
    wait_for(lambda: has_peer(C, A.ip), 90, "C connects via fixed seed fallback")
    assert "Adding fixed seeds" in C.log()
    assert "Ignoring unusable entry in -fixedseedfile: not-an-address" in C.log()
    wait_for(lambda: C.cli("getblockcount") == A.cli("getblockcount"), 60, "C syncs after fixed-seed connect")

@test
def t_three_node_peer_exchange_and_sync(A, B, C):
    # B is only linked to A, C only knows B (fixed seed). C must learn A through addr exchange.
    for n in (B, C): n.stop(); clear_peers(n)
    B.start([f"-addnode={A.ip}:9777"])
    wait_for(lambda: has_peer(B, A.ip), 60, "B connects to A")
    seedfile = os.path.join(C.dir, "seed.txt"); open(seedfile, "w").write(f"{B.ip}:9777\n")
    C.start([f"-fixedseedfile={seedfile}", "-fixedseeds=1"])
    wait_for(lambda: has_peer(C, B.ip), 90, "C connects to B")
    wait_for(lambda: any(x["address"] == A.ip for x in C.cli("getnodeaddresses", 0)), 180, "C learns A's address through peer exchange")
    wait_for(lambda: has_peer(C, A.ip), 180, "C connects to A on its own")
    mine(A, 2)
    for n in (B, C): wait_for(lambda n=n: n.cli("getbestblockhash") == A.cli("getbestblockhash"), 90, f"{n.name} sync after new blocks")

@test
def t_reconnect_after_restart(B, C):
    C.stop(); C.start()   # same datadir: peers.dat/anchors.dat remembered
    wait_for(lambda: has_peer(C, B.ip) or has_peer(C, IPS["A"]), 120, "C reconnects after restart")
    B.stop(); time.sleep(3); B.start()
    wait_for(lambda: has_peer(C, B.ip), 240, "C auto-reconnects to B after B was down")

def raw_connect(ip):
    s = socket.create_connection((ip, 9777), 10); return s

@test
def t_rejects_wrong_networks(A):
    base = A.cli("getconnectioncount")
    for label, magic in (("bitcoin-mainnet", BITCOIN_MAGIC), ("bitcoin-testnet3", bytes.fromhex("0b110907")), ("random", os.urandom(4))):
        s = raw_connect(A.ip); s.sendall(msg(magic, b"version", version_payload()))
        cmds, closed, _ = read_msgs(s, 8); s.close()
        assert "version" not in cmds and "verack" not in cmds, f"node answered a {label} peer: {cmds}"
    time.sleep(1)
    assert not any(p.get("subver", "").startswith("/kwala-test") for p in A.peers()), "foreign peer stayed connected"
    # sanity: the correct magic IS accepted
    s = raw_connect(A.ip); s.sendall(msg(MAGIC, b"version", version_payload()))
    cmds, closed, _ = read_msgs(s, 5); s.close()
    assert "version" in cmds and "verack" in cmds, f"valid-network peer not accepted: {cmds}"

@test
def t_rejects_old_protocol(A):
    s = raw_connect(A.ip); s.sendall(msg(MAGIC, b"version", version_payload(ver=100)))
    cmds, closed, _ = read_msgs(s, 6); s.close()
    assert "verack" not in cmds, f"old protocol peer got verack: {cmds}"

@test
def t_rejects_foreign_genesis_chain(A):
    h0 = A.cli("getblockchaininfo"); headers_before, blocks_before = h0["headers"], h0["blocks"]
    s = raw_connect(A.ip); s.sendall(msg(MAGIC, b"version", version_payload()))
    cmds, _, _ = read_msgs(s, 4); s.sendall(msg(MAGIC, b"verack"))
    # a valid-PoW header whose parent is NOT our genesis lineage (i.e. a chain with a different genesis)
    foreign = mine_header(bytes.fromhex("11" * 32))
    for _ in range(3): s.sendall(msg(MAGIC, b"headers", b"\x01" + foreign + b"\x00")); time.sleep(0.5)
    time.sleep(3); s.close()
    h1 = A.cli("getblockchaininfo")
    assert h1["headers"] == headers_before and h1["blocks"] == blocks_before, "foreign-genesis header was accepted!"
    assert all(t["status"] == "active" for t in A.cli("getchaintips")), "foreign fork tip appeared"
    # control: the same kind of message with a header that DOES build on our chain is accepted,
    # proving the foreign header was rejected because of its lineage and not because the test is broken.
    s = raw_connect(A.ip); s.sendall(msg(MAGIC, b"version", version_payload()))
    read_msgs(s, 3); s.sendall(msg(MAGIC, b"verack"))
    tip = bytes.fromhex(A.cli("getbestblockhash"))[::-1]
    good = mine_header(tip)
    s.sendall(msg(MAGIC, b"headers", b"\x01" + good + b"\x00")); time.sleep(3); s.close()
    assert A.cli("getblockchaininfo")["headers"] == headers_before + 1, "control header on our chain was not accepted"

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--bin", default="src"); ap.add_argument("--keep", action="store_true")
    a = ap.parse_args(); binp = os.path.abspath(a.bin)
    for i, ip in enumerate(IPS.values(), 1):
        try: add_alias(i, ip)
        except OSError as e: print("cannot add loopback alias (need root/CAP_NET_ADMIN):", e); sys.exit(2)
    root = tempfile.mkdtemp(prefix="kwala-nettest-")
    hosts_bak = open("/etc/hosts").read()
    open("/etc/hosts", "a").write(f"\n{IPS['A']} x9.seed.kwalatest.local seed.kwalatest.local\n{IPS['A']} x9.seed2.kwalatest.local seed2.kwalatest.local\n")
    nodes = {k: Node(k, ip, i, binp, root) for i, (k, ip) in enumerate(IPS.items(), 1)}
    A, B, C = nodes["A"], nodes["B"], nodes["C"]
    try:
        A.start(); B.start(); C.start()
        t_genesis_and_two_node_sync(A, B)
        t_dns_discovery_multi_seed(A, B, C)
        t_dns_all_seeds_down_is_graceful(A, C)
        t_fixed_seed_fallback(A, C, root)
        t_three_node_peer_exchange_and_sync(A, B, C)
        t_reconnect_after_restart(B, C)
        t_rejects_wrong_networks(A)
        t_rejects_old_protocol(A)
        t_rejects_foreign_genesis_chain(A)
    finally:
        for n in nodes.values(): n.stop()
        open("/etc/hosts", "w").write(hosts_bak)
        if not a.keep: shutil.rmtree(root, ignore_errors=True)
        else: print("data kept in", root)
    print("\n==== summary ====")
    for n, r, t in results: print(f"{r[:4]:5s} {n}  ({t:.0f}s)" + ("" if r == "PASS" else "  " + r))
    sys.exit(0 if all(r == "PASS" for _, r, _ in results) else 1)

if __name__ == "__main__":
    main()
