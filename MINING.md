# Mining KwalaCoins (tested)

KwalaCoins mining is SHA-256d proof-of-work. `contrib/kwalacoins/kwala_miner.py` is a simple CPU miner
(Python 3 only). Real hash power can use any SHA-256 miner software that speaks `getblocktemplate`.

## 1. Start two nodes (the node refuses to give out work with zero peers)
Same machine example (the extra `-bind=...=onion` lines stop the two nodes clashing):

    ./kwalacoind -datadir=$HOME/kA -daemon -bind=127.0.0.1:9777 -bind=127.0.0.1:9779=onion -rpcport=9776 \
        -maxtipage=315360000 -dnsseed=0 -addnode=127.0.0.1:9877
    ./kwalacoind -datadir=$HOME/kB -daemon -bind=127.0.0.1:9877 -bind=127.0.0.1:9879=onion -rpcport=9876 \
        -maxtipage=315360000 -dnsseed=0 -addnode=127.0.0.1:9777

On two different machines you only need `-addnode=<other-ip>:9777` (no extra bind flags).
`-maxtipage` is needed while the chain is brand new: after 24h with no new blocks a node thinks it is still
syncing and won't hand out mining work. Remove it once blocks flow regularly.

## 2. Get a receiving address
    ./kwalacoin-cli -datadir=$HOME/kA -rpcport=9776 createwallet miner
    ./kwalacoin-cli -datadir=$HOME/kA -rpcport=9776 getnewaddress      # kwala1...

## 3. Mine
    python3 contrib/kwalacoins/kwala_miner.py --cli "./kwalacoin-cli -datadir=$HOME/kA -rpcport=9776" \
        --address <your kwala1... address>

Each block pays 100 KWALA (spendable after 100 more blocks). Difficulty starts very low and retargets daily.
