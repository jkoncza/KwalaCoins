# Copyright (c) 2013-2016 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

# Pattern rule to print variables, e.g. make print-top_srcdir
print-%: FORCE
	@echo '$*'='$($*)'

DIST_SUBDIRS = secp256k1

AM_LDFLAGS = $(LIBTOOL_LDFLAGS) $(HARDENED_LDFLAGS) $(SANITIZER_LDFLAGS) $(CORE_LDFLAGS)
AM_CXXFLAGS = $(CORE_CXXFLAGS) $(DEBUG_CXXFLAGS) $(HARDENED_CXXFLAGS) $(WARN_CXXFLAGS) $(NOWARN_CXXFLAGS) $(ERROR_CXXFLAGS) $(SANITIZER_CXXFLAGS)
AM_OBJCXXFLAGS = $(AM_CXXFLAGS)
AM_CPPFLAGS = $(DEBUG_CPPFLAGS) $(HARDENED_CPPFLAGS) $(CORE_CPPFLAGS)
AM_LIBTOOLFLAGS = --preserve-dup-deps
PTHREAD_FLAGS = $(PTHREAD_CFLAGS) $(PTHREAD_LIBS)
EXTRA_LIBRARIES =

lib_LTLIBRARIES =
noinst_LTLIBRARIES =

bin_PROGRAMS =
noinst_PROGRAMS =
check_PROGRAMS =
TESTS =
BENCHMARKS =

KWALACOIN_INCLUDES=-I$(builddir) -I$(srcdir)/$(MINISKETCH_INCLUDE_DIR_INT) -I$(srcdir)/secp256k1/include -I$(srcdir)/$(UNIVALUE_INCLUDE_DIR_INT)

LIBKWALACOIN_NODE=libkwalacoin_node.a
LIBKWALACOIN_COMMON=libkwalacoin_common.a
LIBKWALACOIN_CONSENSUS=libkwalacoin_consensus.a
LIBKWALACOIN_CLI=libkwalacoin_cli.a
LIBKWALACOIN_UTIL=libkwalacoin_util.a
LIBKWALACOIN_CRYPTO_BASE=crypto/libkwalacoin_crypto_base.la
LIBKWALACOINQT=qt/libkwalacoinqt.a
LIBSECP256K1=secp256k1/libsecp256k1.la

if ENABLE_ZMQ
LIBKWALACOIN_ZMQ=libkwalacoin_zmq.a
endif
if BUILD_KWALACOIN_KERNEL_LIB
LIBKWALACOINKERNEL=libkwalacoinkernel.la
endif
if ENABLE_WALLET
LIBKWALACOIN_WALLET=libkwalacoin_wallet.a
LIBKWALACOIN_WALLET_TOOL=libkwalacoin_wallet_tool.a
endif

LIBKWALACOIN_CRYPTO = $(LIBKWALACOIN_CRYPTO_BASE)
if ENABLE_SSE41
LIBKWALACOIN_CRYPTO_SSE41 = crypto/libkwalacoin_crypto_sse41.la
LIBKWALACOIN_CRYPTO += $(LIBKWALACOIN_CRYPTO_SSE41)
if ENABLE_X86_SHANI
LIBKWALACOIN_CRYPTO_X86_SHANI = crypto/libkwalacoin_crypto_x86_shani.la
LIBKWALACOIN_CRYPTO += $(LIBKWALACOIN_CRYPTO_X86_SHANI)
endif
endif
if ENABLE_AVX2
LIBKWALACOIN_CRYPTO_AVX2 = crypto/libkwalacoin_crypto_avx2.la
LIBKWALACOIN_CRYPTO += $(LIBKWALACOIN_CRYPTO_AVX2)
endif
if ENABLE_ARM_SHANI
LIBKWALACOIN_CRYPTO_ARM_SHANI = crypto/libkwalacoin_crypto_arm_shani.la
LIBKWALACOIN_CRYPTO += $(LIBKWALACOIN_CRYPTO_ARM_SHANI)
endif
noinst_LTLIBRARIES += $(LIBKWALACOIN_CRYPTO)

$(LIBSECP256K1): $(wildcard secp256k1/src/*.h) $(wildcard secp256k1/src/*.c) $(wildcard secp256k1/include/*)
	$(AM_V_at)$(MAKE) $(AM_MAKEFLAGS) -C $(@D) $(@F)

# Make is not made aware of per-object dependencies to avoid limiting building parallelization
# But to build the less dependent modules first, we manually select their order here:
EXTRA_LIBRARIES += \
  $(LIBKWALACOIN_UTIL) \
  $(LIBKWALACOIN_COMMON) \
  $(LIBKWALACOIN_CONSENSUS) \
  $(LIBKWALACOIN_NODE) \
  $(LIBKWALACOIN_CLI) \
  $(LIBKWALACOIN_IPC) \
  $(LIBKWALACOIN_WALLET) \
  $(LIBKWALACOIN_WALLET_TOOL) \
  $(LIBKWALACOIN_ZMQ)

if BUILD_KWALACOIND
  bin_PROGRAMS += kwalacoind
endif

if BUILD_KWALACOIN_NODE
  bin_PROGRAMS += kwalacoin-node
endif

if BUILD_KWALACOIN_CLI
  bin_PROGRAMS += kwalacoin-cli
endif

if BUILD_KWALACOIN_TX
  bin_PROGRAMS += kwalacoin-tx
endif

if ENABLE_WALLET
if BUILD_KWALACOIN_WALLET
  bin_PROGRAMS += kwalacoin-wallet
endif
endif

if BUILD_KWALACOIN_UTIL
  bin_PROGRAMS += kwalacoin-util
endif

if BUILD_KWALACOIN_CHAINSTATE
  bin_PROGRAMS += kwalacoin-chainstate
endif

.PHONY: FORCE check-symbols check-security
# kwalacoin core #
KWALACOIN_CORE_H = \
  addresstype.h \
  addrdb.h \
  addrman.h \
  addrman_impl.h \
  attributes.h \
  banman.h \
  base58.h \
  bech32.h \
  bip324.h \
  blockencodings.h \
  blockfilter.h \
  chain.h \
  chainparams.h \
  chainparamsbase.h \
  chainparamsseeds.h \
  checkqueue.h \
  clientversion.h \
  cluster_linearize.h \
  coins.h \
  common/args.h \
  common/bloom.h \
  common/init.h \
  common/run_command.h \
  common/types.h \
  common/url.h \
  compat/assumptions.h \
  compat/byteswap.h \
  compat/compat.h \
  compat/cpuid.h \
  compat/endian.h \
  common/messages.h \
  common/settings.h \
  common/signmessage.h \
  common/system.h \
  compressor.h \
  consensus/consensus.h \
  consensus/tx_check.h \
  consensus/tx_verify.h \
  core_io.h \
  core_memusage.h \
  cuckoocache.h \
  dbwrapper.h \
  deploymentinfo.h \
  deploymentstatus.h \
  external_signer.h \
  flatfile.h \
  headerssync.h \
  httprpc.h \
  httpserver.h \
  i2p.h \
  index/base.h \
  index/blockfilterindex.h \
  index/coinstatsindex.h \
  index/disktxpos.h \
  index/txindex.h \
  indirectmap.h \
  init.h \
  init/common.h \
  interfaces/chain.h \
  interfaces/echo.h \
  interfaces/handler.h \
  interfaces/init.h \
  interfaces/ipc.h \
  interfaces/mining.h \
  interfaces/node.h \
  interfaces/wallet.h \
  kernel/blockmanager_opts.h \
  kernel/chain.h \
  kernel/chainparams.h \
  kernel/chainstatemanager_opts.h \
  kernel/checks.h \
  kernel/coinstats.h \
  kernel/context.h \
  kernel/cs_main.h \
  kernel/disconnected_transactions.h \
  kernel/mempool_entry.h \
  kernel/mempool_limits.h \
  kernel/mempool_options.h \
  kernel/mempool_removal_reason.h \
  kernel/messagestartchars.h \
  kernel/notifications_interface.h \
  kernel/warning.h \
  key.h \
  key_io.h \
  logging.h \
  logging/timer.h \
  mapport.h \
  memusage.h \
  merkleblock.h \
  net.h \
  net_permissions.h \
  net_processing.h \
  net_types.h \
  netaddress.h \
  netbase.h \
  netgroup.h \
  netmessagemaker.h \
  node/abort.h \
  node/blockmanager_args.h \
  node/blockstorage.h \
  node/caches.h \
  node/chainstate.h \
  node/chainstatemanager_args.h \
  node/coin.h \
  node/coins_view_args.h \
  node/connection_types.h \
  node/context.h \
  node/database_args.h \
  node/eviction.h \
  node/interface_ui.h \
  node/kernel_notifications.h \
  node/mempool_args.h \
  node/mempool_persist.h \
  node/mempool_persist_args.h \
  node/miner.h \
  node/mini_miner.h \
  node/minisketchwrapper.h \
  node/peerman_args.h \
  node/protocol_version.h \
  node/psbt.h \
  node/timeoffsets.h \
  node/transaction.h \
  node/txreconciliation.h \
  node/types.h \
  node/utxo_snapshot.h \
  node/warnings.h \
  noui.h \
  outputtype.h \
  policy/feerate.h \
  policy/fees.h \
  policy/fees_args.h \
  policy/packages.h \
  policy/policy.h \
  policy/rbf.h \
  policy/settings.h \
  policy/truc_policy.h \
  pow.h \
  protocol.h \
  psbt.h \
  random.h \
  randomenv.h \
  rest.h \
  rpc/blockchain.h \
  rpc/client.h \
  rpc/mempool.h \
  rpc/mining.h \
  rpc/protocol.h \
  rpc/rawtransaction_util.h \
  rpc/register.h \
  rpc/request.h \
  rpc/server.h \
  rpc/server_util.h \
  rpc/util.h \
  scheduler.h \
  script/descriptor.h \
  script/keyorigin.h \
  script/miniscript.h \
  script/parsing.h \
  script/sigcache.h \
  script/sign.h \
  script/signingprovider.h \
  script/solver.h \
  signet.h \
  streams.h \
  support/allocators/pool.h \
  support/allocators/secure.h \
  support/allocators/zeroafterfree.h \
  support/cleanse.h \
  support/events.h \
  support/lockedpool.h \
  sync.h \
  threadsafety.h \
  torcontrol.h \
  txdb.h \
  txmempool.h \
  txorphanage.h \
  txrequest.h \
  undo.h \
  util/any.h \
  util/asmap.h \
  util/batchpriority.h \
  util/bip32.h \
  util/bitdeque.h \
  util/bitset.h \
  util/bytevectorhash.h \
  util/chaintype.h \
  util/check.h \
  util/epochguard.h \
  util/exception.h \
  util/fastrange.h \
  util/feefrac.h \
  util/fs.h \
  util/fs_helpers.h \
  util/golombrice.h \
  util/hash_type.h \
  util/hasher.h \
  util/insert.h \
  util/macros.h \
  util/moneystr.h \
  util/overflow.h \
  util/overloaded.h \
  util/rbf.h \
  util/readwritefile.h \
  util/result.h \
  util/serfloat.h \
  util/signalinterrupt.h \
  util/sock.h \
  util/strencodings.h \
  util/string.h \
  util/subprocess.h \
  util/syserror.h \
  util/task_runner.h \
  util/thread.h \
  util/threadinterrupt.h \
  util/threadnames.h \
  util/time.h \
  util/tokenpipe.h \
  util/trace.h \
  util/transaction_identifier.h \
  util/translation.h \
  util/types.h \
  util/ui_change_type.h \
  util/vecdeque.h \
  util/vector.h \
  validation.h \
  validationinterface.h \
  versionbits.h \
  wallet/bdb.h \
  wallet/coincontrol.h \
  wallet/coinselection.h \
  wallet/context.h \
  wallet/crypter.h \
  wallet/db.h \
  wallet/dump.h \
  wallet/external_signer_scriptpubkeyman.h \
  wallet/feebumper.h \
  wallet/fees.h \
  wallet/load.h \
  wallet/migrate.h \
  wallet/receive.h \
  wallet/rpc/util.h \
  wallet/rpc/wallet.h \
  wallet/salvage.h \
  wallet/scriptpubkeyman.h \
  wallet/spend.h \
  wallet/sqlite.h \
  wallet/transaction.h \
  wallet/types.h \
  wallet/wallet.h \
  wallet/walletdb.h \
  wallet/wallettool.h \
  wallet/walletutil.h \
  walletinitinterface.h \
  zmq/zmqabstractnotifier.h \
  zmq/zmqnotificationinterface.h \
  zmq/zmqpublishnotifier.h \
  zmq/zmqrpc.h \
  zmq/zmqutil.h


obj/build.h: FORCE
	@$(MKDIR_P) $(builddir)/obj
	$(AM_V_GEN) $(top_srcdir)/share/genbuild.sh "$(abs_top_builddir)/src/obj/build.h" \
	  "$(abs_top_srcdir)"
libkwalacoin_util_a-clientversion.$(OBJEXT): obj/build.h

# node #
libkwalacoin_node_a_CPPFLAGS = $(AM_CPPFLAGS) $(KWALACOIN_INCLUDES) $(LEVELDB_CPPFLAGS) $(BOOST_CPPFLAGS) $(MINIUPNPC_CPPFLAGS) $(NATPMP_CPPFLAGS) $(EVENT_CFLAGS) $(EVENT_PTHREADS_CFLAGS)
libkwalacoin_node_a_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS)
libkwalacoin_node_a_SOURCES = \
  addrdb.cpp \
  addrman.cpp \
  banman.cpp \
  bip324.cpp \
  blockencodings.cpp \
  blockfilter.cpp \
  chain.cpp \
  consensus/tx_verify.cpp \
  dbwrapper.cpp \
  deploymentstatus.cpp \
  flatfile.cpp \
  headerssync.cpp \
  httprpc.cpp \
  httpserver.cpp \
  i2p.cpp \
  index/base.cpp \
  index/blockfilterindex.cpp \
  index/coinstatsindex.cpp \
  index/txindex.cpp \
  init.cpp \
  kernel/chain.cpp \
  kernel/checks.cpp \
  kernel/coinstats.cpp \
  kernel/context.cpp \
  kernel/cs_main.cpp \
  kernel/disconnected_transactions.cpp \
  kernel/mempool_removal_reason.cpp \
  mapport.cpp \
  net.cpp \
  net_processing.cpp \
  netgroup.cpp \
  node/abort.cpp \
  node/blockmanager_args.cpp \
  node/blockstorage.cpp \
  node/caches.cpp \
  node/chainstate.cpp \
  node/chainstatemanager_args.cpp \
  node/coin.cpp \
  node/coins_view_args.cpp \
  node/connection_types.cpp \
  node/context.cpp \
  node/database_args.cpp \
  node/eviction.cpp \
  node/interface_ui.cpp \
  node/interfaces.cpp \
  node/kernel_notifications.cpp \
  node/mempool_args.cpp \
  node/mempool_persist.cpp \
  node/mempool_persist_args.cpp \
  node/miner.cpp \
  node/mini_miner.cpp \
  node/minisketchwrapper.cpp \
  node/peerman_args.cpp \
  node/psbt.cpp \
  node/timeoffsets.cpp \
  node/transaction.cpp \
  node/txreconciliation.cpp \
  node/utxo_snapshot.cpp \
  node/warnings.cpp \
  noui.cpp \
  policy/fees.cpp \
  policy/fees_args.cpp \
  policy/packages.cpp \
  policy/rbf.cpp \
  policy/settings.cpp \
  policy/truc_policy.cpp \
  pow.cpp \
  rest.cpp \
  rpc/blockchain.cpp \
  rpc/fees.cpp \
  rpc/mempool.cpp \
  rpc/mining.cpp \
  rpc/net.cpp \
  rpc/node.cpp \
  rpc/output_script.cpp \
  rpc/rawtransaction.cpp \
  rpc/server.cpp \
  rpc/server_util.cpp \
  rpc/signmessage.cpp \
  rpc/txoutproof.cpp \
  script/sigcache.cpp \
  signet.cpp \
  torcontrol.cpp \
  txdb.cpp \
  txmempool.cpp \
  txorphanage.cpp \
  txrequest.cpp \
  validation.cpp \
  validationinterface.cpp \
  versionbits.cpp \
  $(KWALACOIN_CORE_H)

if ENABLE_WALLET
libkwalacoin_node_a_SOURCES += wallet/init.cpp
libkwalacoin_node_a_CPPFLAGS += $(BDB_CPPFLAGS)
endif
if !ENABLE_WALLET
libkwalacoin_node_a_SOURCES += dummywallet.cpp
endif
#

# zmq #
if ENABLE_ZMQ
libkwalacoin_zmq_a_CPPFLAGS = $(AM_CPPFLAGS) $(KWALACOIN_INCLUDES) $(ZMQ_CFLAGS)
libkwalacoin_zmq_a_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS)
libkwalacoin_zmq_a_SOURCES = \
  zmq/zmqabstractnotifier.cpp \
  zmq/zmqnotificationinterface.cpp \
  zmq/zmqpublishnotifier.cpp \
  zmq/zmqrpc.cpp \
  zmq/zmqutil.cpp
endif
#

# wallet #
libkwalacoin_wallet_a_CPPFLAGS = $(AM_CPPFLAGS) $(KWALACOIN_INCLUDES) $(BOOST_CPPFLAGS) $(BDB_CPPFLAGS) $(SQLITE_CFLAGS)
libkwalacoin_wallet_a_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS)
libkwalacoin_wallet_a_SOURCES = \
  wallet/coincontrol.cpp \
  wallet/context.cpp \
  wallet/crypter.cpp \
  wallet/db.cpp \
  wallet/dump.cpp \
  wallet/external_signer_scriptpubkeyman.cpp \
  wallet/feebumper.cpp \
  wallet/fees.cpp \
  wallet/interfaces.cpp \
  wallet/load.cpp \
  wallet/migrate.cpp \
  wallet/receive.cpp \
  wallet/rpc/addresses.cpp \
  wallet/rpc/backup.cpp \
  wallet/rpc/coins.cpp \
  wallet/rpc/encrypt.cpp \
  wallet/rpc/spend.cpp \
  wallet/rpc/signmessage.cpp \
  wallet/rpc/transactions.cpp \
  wallet/rpc/util.cpp \
  wallet/rpc/wallet.cpp \
  wallet/scriptpubkeyman.cpp \
  wallet/spend.cpp \
  wallet/transaction.cpp \
  wallet/wallet.cpp \
  wallet/walletdb.cpp \
  wallet/walletutil.cpp \
  wallet/coinselection.cpp \
  $(KWALACOIN_CORE_H)

if USE_SQLITE
libkwalacoin_wallet_a_SOURCES += wallet/sqlite.cpp
endif
if USE_BDB
libkwalacoin_wallet_a_SOURCES += wallet/bdb.cpp wallet/salvage.cpp
endif
#

# wallet tool #
libkwalacoin_wallet_tool_a_CPPFLAGS = $(AM_CPPFLAGS) $(KWALACOIN_INCLUDES) $(BOOST_CPPFLAGS)
libkwalacoin_wallet_tool_a_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS)
libkwalacoin_wallet_tool_a_SOURCES = \
  wallet/wallettool.cpp \
  $(KWALACOIN_CORE_H)
#

# crypto #

# crypto_base contains the unspecialized (unoptimized) versions of our
# crypto functions. Functions that require custom compiler flags and/or
# runtime opt-in are omitted.
crypto_libkwalacoin_crypto_base_la_CPPFLAGS = $(AM_CPPFLAGS)

# Specify -static in both CXXFLAGS and LDFLAGS so libtool will only build a
# static version of this library. We don't need a dynamic version, and a dynamic
# version can't be used on windows anyway because the library doesn't currently
# export DLL symbols.
crypto_libkwalacoin_crypto_base_la_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS) -static
crypto_libkwalacoin_crypto_base_la_LDFLAGS = $(AM_LDFLAGS) -static

crypto_libkwalacoin_crypto_base_la_SOURCES = \
  crypto/aes.cpp \
  crypto/aes.h \
  crypto/chacha20.h \
  crypto/chacha20.cpp \
  crypto/chacha20poly1305.h \
  crypto/chacha20poly1305.cpp \
  crypto/common.h \
  crypto/hex_base.cpp \
  crypto/hex_base.h \
  crypto/hkdf_sha256_32.cpp \
  crypto/hkdf_sha256_32.h \
  crypto/hmac_sha256.cpp \
  crypto/hmac_sha256.h \
  crypto/hmac_sha512.cpp \
  crypto/hmac_sha512.h \
  crypto/poly1305.h \
  crypto/poly1305.cpp \
  crypto/muhash.h \
  crypto/muhash.cpp \
  crypto/ripemd160.cpp \
  crypto/ripemd160.h \
  crypto/sha1.cpp \
  crypto/sha1.h \
  crypto/sha256.cpp \
  crypto/sha256.h \
  crypto/sha256_sse4.cpp \
  crypto/sha3.cpp \
  crypto/sha3.h \
  crypto/sha512.cpp \
  crypto/sha512.h \
  crypto/siphash.cpp \
  crypto/siphash.h \
  support/cleanse.cpp

# See explanation for -static in crypto_libkwalacoin_crypto_base_la's LDFLAGS and
# CXXFLAGS above
crypto_libkwalacoin_crypto_sse41_la_LDFLAGS = $(AM_LDFLAGS) -static
crypto_libkwalacoin_crypto_sse41_la_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS) -static
crypto_libkwalacoin_crypto_sse41_la_CPPFLAGS = $(AM_CPPFLAGS)
crypto_libkwalacoin_crypto_sse41_la_CXXFLAGS += $(SSE41_CXXFLAGS)
crypto_libkwalacoin_crypto_sse41_la_CPPFLAGS += -DENABLE_SSE41
crypto_libkwalacoin_crypto_sse41_la_SOURCES = crypto/sha256_sse41.cpp

# See explanation for -static in crypto_libkwalacoin_crypto_base_la's LDFLAGS and
# CXXFLAGS above
crypto_libkwalacoin_crypto_avx2_la_LDFLAGS = $(AM_LDFLAGS) -static
crypto_libkwalacoin_crypto_avx2_la_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS) -static
crypto_libkwalacoin_crypto_avx2_la_CPPFLAGS = $(AM_CPPFLAGS)
crypto_libkwalacoin_crypto_avx2_la_CXXFLAGS += $(AVX2_CXXFLAGS)
crypto_libkwalacoin_crypto_avx2_la_CPPFLAGS += -DENABLE_AVX2
crypto_libkwalacoin_crypto_avx2_la_SOURCES = crypto/sha256_avx2.cpp

# See explanation for -static in crypto_libkwalacoin_crypto_base_la's LDFLAGS and
# CXXFLAGS above
crypto_libkwalacoin_crypto_x86_shani_la_LDFLAGS = $(AM_LDFLAGS) -static
crypto_libkwalacoin_crypto_x86_shani_la_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS) -static
crypto_libkwalacoin_crypto_x86_shani_la_CPPFLAGS = $(AM_CPPFLAGS)
crypto_libkwalacoin_crypto_x86_shani_la_CXXFLAGS += $(X86_SHANI_CXXFLAGS)
crypto_libkwalacoin_crypto_x86_shani_la_CPPFLAGS += -DENABLE_SSE41 -DENABLE_X86_SHANI
crypto_libkwalacoin_crypto_x86_shani_la_SOURCES = crypto/sha256_x86_shani.cpp

# See explanation for -static in crypto_libkwalacoin_crypto_base_la's LDFLAGS and
# CXXFLAGS above
crypto_libkwalacoin_crypto_arm_shani_la_LDFLAGS = $(AM_LDFLAGS) -static
crypto_libkwalacoin_crypto_arm_shani_la_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS) -static
crypto_libkwalacoin_crypto_arm_shani_la_CPPFLAGS = $(AM_CPPFLAGS)
crypto_libkwalacoin_crypto_arm_shani_la_CXXFLAGS += $(ARM_SHANI_CXXFLAGS)
crypto_libkwalacoin_crypto_arm_shani_la_CPPFLAGS += -DENABLE_ARM_SHANI
crypto_libkwalacoin_crypto_arm_shani_la_SOURCES = crypto/sha256_arm_shani.cpp
#

# consensus #
libkwalacoin_consensus_a_CPPFLAGS = $(AM_CPPFLAGS) $(KWALACOIN_INCLUDES)
libkwalacoin_consensus_a_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS)
libkwalacoin_consensus_a_SOURCES = \
  arith_uint256.cpp \
  arith_uint256.h \
  consensus/amount.h \
  consensus/merkle.cpp \
  consensus/merkle.h \
  consensus/params.h \
  consensus/tx_check.cpp \
  consensus/validation.h \
  hash.cpp \
  hash.h \
  prevector.h \
  primitives/block.cpp \
  primitives/block.h \
  primitives/transaction.cpp \
  primitives/transaction.h \
  pubkey.cpp \
  pubkey.h \
  script/interpreter.cpp \
  script/interpreter.h \
  script/script.cpp \
  script/script.h \
  script/script_error.cpp \
  script/script_error.h \
  serialize.h \
  span.h \
  tinyformat.h \
  uint256.cpp \
  uint256.h
#

# common #
libkwalacoin_common_a_CPPFLAGS = $(AM_CPPFLAGS) $(KWALACOIN_INCLUDES) $(BOOST_CPPFLAGS)
libkwalacoin_common_a_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS)
libkwalacoin_common_a_SOURCES = \
  addresstype.cpp \
  base58.cpp \
  bech32.cpp \
  chainparamsbase.cpp \
  chainparams.cpp \
  coins.cpp \
  common/args.cpp \
  common/bloom.cpp \
  common/config.cpp \
  common/init.cpp \
  common/interfaces.cpp \
  common/messages.cpp \
  common/run_command.cpp \
  common/settings.cpp \
  common/signmessage.cpp \
  common/system.cpp \
  common/url.cpp \
  compressor.cpp \
  core_read.cpp \
  core_write.cpp \
  deploymentinfo.cpp \
  external_signer.cpp \
  init/common.cpp \
  kernel/chainparams.cpp \
  key.cpp \
  key_io.cpp \
  merkleblock.cpp \
  net_types.cpp \
  netaddress.cpp \
  netbase.cpp \
  net_permissions.cpp \
  outputtype.cpp \
  policy/feerate.cpp \
  policy/policy.cpp \
  protocol.cpp \
  psbt.cpp \
  rpc/external_signer.cpp \
  rpc/rawtransaction_util.cpp \
  rpc/request.cpp \
  rpc/util.cpp \
  scheduler.cpp \
  script/descriptor.cpp \
  script/miniscript.cpp \
  script/parsing.cpp \
  script/sign.cpp \
  script/signingprovider.cpp \
  script/solver.cpp \
  $(KWALACOIN_CORE_H)
#

# util #
libkwalacoin_util_a_CPPFLAGS = $(AM_CPPFLAGS) $(KWALACOIN_INCLUDES)
libkwalacoin_util_a_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS)
libkwalacoin_util_a_SOURCES = \
  support/lockedpool.cpp \
  clientversion.cpp \
  logging.cpp \
  random.cpp \
  randomenv.cpp \
  streams.cpp \
  sync.cpp \
  util/asmap.cpp \
  util/batchpriority.cpp \
  util/bip32.cpp \
  util/bytevectorhash.cpp \
  util/chaintype.cpp \
  util/check.cpp \
  util/exception.cpp \
  util/feefrac.cpp \
  util/fs.cpp \
  util/fs_helpers.cpp \
  util/hasher.cpp \
  util/sock.cpp \
  util/syserror.cpp \
  util/moneystr.cpp \
  util/rbf.cpp \
  util/readwritefile.cpp \
  util/signalinterrupt.cpp \
  util/thread.cpp \
  util/threadinterrupt.cpp \
  util/threadnames.cpp \
  util/serfloat.cpp \
  util/strencodings.cpp \
  util/string.cpp \
  util/time.cpp \
  util/tokenpipe.cpp \
  $(KWALACOIN_CORE_H)
#

# cli #
libkwalacoin_cli_a_CPPFLAGS = $(AM_CPPFLAGS) $(KWALACOIN_INCLUDES)
libkwalacoin_cli_a_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS)
libkwalacoin_cli_a_SOURCES = \
  compat/stdin.h \
  compat/stdin.cpp \
  rpc/client.cpp \
  $(KWALACOIN_CORE_H)

nodist_libkwalacoin_util_a_SOURCES = $(srcdir)/obj/build.h
#

# kwalacoind & kwalacoin-node binaries #
kwalacoin_daemon_sources = kwalacoind.cpp
kwalacoin_bin_cppflags = $(AM_CPPFLAGS) $(KWALACOIN_INCLUDES)
kwalacoin_bin_cxxflags = $(AM_CXXFLAGS) $(PIE_FLAGS)
kwalacoin_bin_ldflags = $(RELDFLAGS) $(AM_LDFLAGS) $(LIBTOOL_APP_LDFLAGS) $(PTHREAD_FLAGS)

if TARGET_WINDOWS
kwalacoin_daemon_sources += kwalacoind-res.rc
endif

kwalacoin_bin_ldadd = \
  $(LIBKWALACOIN_WALLET) \
  $(LIBKWALACOIN_COMMON) \
  $(LIBKWALACOIN_UTIL) \
  $(LIBUNIVALUE) \
  $(LIBKWALACOIN_ZMQ) \
  $(LIBKWALACOIN_CONSENSUS) \
  $(LIBKWALACOIN_CRYPTO) \
  $(LIBLEVELDB) \
  $(LIBMEMENV) \
  $(LIBSECP256K1)

kwalacoin_bin_ldadd += $(BDB_LIBS) $(MINIUPNPC_LIBS) $(NATPMP_LIBS) $(EVENT_PTHREADS_LIBS) $(EVENT_LIBS) $(ZMQ_LIBS) $(SQLITE_LIBS)

kwalacoind_SOURCES = $(kwalacoin_daemon_sources) init/kwalacoind.cpp
kwalacoind_CPPFLAGS = $(kwalacoin_bin_cppflags)
kwalacoind_CXXFLAGS = $(kwalacoin_bin_cxxflags)
kwalacoind_LDFLAGS = $(kwalacoin_bin_ldflags)
kwalacoind_LDADD = $(LIBKWALACOIN_NODE) $(kwalacoin_bin_ldadd)

kwalacoin_node_SOURCES = $(kwalacoin_daemon_sources) init/kwalacoin-node.cpp
kwalacoin_node_CPPFLAGS = $(kwalacoin_bin_cppflags)
kwalacoin_node_CXXFLAGS = $(kwalacoin_bin_cxxflags)
kwalacoin_node_LDFLAGS = $(kwalacoin_bin_ldflags)
kwalacoin_node_LDADD = $(LIBKWALACOIN_NODE) $(kwalacoin_bin_ldadd) $(LIBKWALACOIN_IPC) $(LIBMULTIPROCESS_LIBS)

# kwalacoin-cli binary #
kwalacoin_cli_SOURCES = kwalacoin-cli.cpp
kwalacoin_cli_CPPFLAGS = $(AM_CPPFLAGS) $(KWALACOIN_INCLUDES) $(EVENT_CFLAGS)
kwalacoin_cli_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS)
kwalacoin_cli_LDFLAGS = $(RELDFLAGS) $(AM_LDFLAGS) $(LIBTOOL_APP_LDFLAGS) $(PTHREAD_FLAGS)

if TARGET_WINDOWS
kwalacoin_cli_SOURCES += kwalacoin-cli-res.rc
endif

kwalacoin_cli_LDADD = \
  $(LIBKWALACOIN_CLI) \
  $(LIBUNIVALUE) \
  $(LIBKWALACOIN_COMMON) \
  $(LIBKWALACOIN_UTIL) \
  $(LIBKWALACOIN_CRYPTO)

kwalacoin_cli_LDADD += $(EVENT_LIBS)
#

# kwalacoin-tx binary #
kwalacoin_tx_SOURCES = kwalacoin-tx.cpp
kwalacoin_tx_CPPFLAGS = $(AM_CPPFLAGS) $(KWALACOIN_INCLUDES)
kwalacoin_tx_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS)
kwalacoin_tx_LDFLAGS = $(RELDFLAGS) $(AM_LDFLAGS) $(LIBTOOL_APP_LDFLAGS) $(PTHREAD_FLAGS)

if TARGET_WINDOWS
kwalacoin_tx_SOURCES += kwalacoin-tx-res.rc
endif

kwalacoin_tx_LDADD = \
  $(LIBUNIVALUE) \
  $(LIBKWALACOIN_COMMON) \
  $(LIBKWALACOIN_UTIL) \
  $(LIBKWALACOIN_CONSENSUS) \
  $(LIBKWALACOIN_CRYPTO) \
  $(LIBSECP256K1)
#

# kwalacoin-wallet binary #
kwalacoin_wallet_SOURCES = kwalacoin-wallet.cpp
kwalacoin_wallet_SOURCES += init/kwalacoin-wallet.cpp
kwalacoin_wallet_CPPFLAGS = $(kwalacoin_bin_cppflags)
kwalacoin_wallet_CXXFLAGS = $(kwalacoin_bin_cxxflags)
kwalacoin_wallet_LDFLAGS = $(kwalacoin_bin_ldflags)
kwalacoin_wallet_LDADD = \
  $(LIBKWALACOIN_WALLET_TOOL) \
  $(LIBKWALACOIN_WALLET) \
  $(LIBKWALACOIN_COMMON) \
  $(LIBKWALACOIN_UTIL) \
  $(LIBUNIVALUE) \
  $(LIBKWALACOIN_CONSENSUS) \
  $(LIBKWALACOIN_CRYPTO) \
  $(LIBSECP256K1) \
  $(BDB_LIBS) \
  $(SQLITE_LIBS)

if TARGET_WINDOWS
kwalacoin_wallet_SOURCES += kwalacoin-wallet-res.rc
endif
#

# kwalacoin-util binary #
kwalacoin_util_SOURCES = kwalacoin-util.cpp
kwalacoin_util_CPPFLAGS = $(AM_CPPFLAGS) $(KWALACOIN_INCLUDES)
kwalacoin_util_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS)
kwalacoin_util_LDFLAGS = $(RELDFLAGS) $(AM_LDFLAGS) $(LIBTOOL_APP_LDFLAGS) $(PTHREAD_FLAGS)

if TARGET_WINDOWS
kwalacoin_util_SOURCES += kwalacoin-util-res.rc
endif

kwalacoin_util_LDADD = \
  $(LIBKWALACOIN_COMMON) \
  $(LIBKWALACOIN_UTIL) \
  $(LIBUNIVALUE) \
  $(LIBKWALACOIN_CONSENSUS) \
  $(LIBKWALACOIN_CRYPTO) \
  $(LIBSECP256K1)
#

# kwalacoin-chainstate binary #
kwalacoin_chainstate_SOURCES = kwalacoin-chainstate.cpp
kwalacoin_chainstate_CPPFLAGS = $(AM_CPPFLAGS) $(KWALACOIN_INCLUDES) $(BOOST_CPPFLAGS)
kwalacoin_chainstate_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS)

kwalacoin_chainstate_LDFLAGS = $(RELDFLAGS) $(AM_LDFLAGS) $(PTHREAD_FLAGS) $(LIBTOOL_APP_LDFLAGS) -static
kwalacoin_chainstate_LDADD = $(LIBKWALACOINKERNEL)

# libtool is unable to calculate this indirect dependency, presumably because it's a subproject.
# libsecp256k1 only needs to be linked in when libkwalacoinkernel is static.
kwalacoin_chainstate_LDADD += $(LIBSECP256K1)
#

# kwalacoinkernel library #
if BUILD_KWALACOIN_KERNEL_LIB
lib_LTLIBRARIES += $(LIBKWALACOINKERNEL)

libkwalacoinkernel_la_LDFLAGS = $(AM_LDFLAGS) -no-undefined $(RELDFLAGS) $(PTHREAD_FLAGS)
libkwalacoinkernel_la_LIBADD = $(LIBKWALACOIN_CRYPTO) $(LIBLEVELDB) $(LIBMEMENV) $(LIBSECP256K1)
libkwalacoinkernel_la_CPPFLAGS = $(AM_CPPFLAGS) -I$(builddir)/obj -I$(srcdir)/secp256k1/include $(BOOST_CPPFLAGS) $(LEVELDB_CPPFLAGS)

# libkwalacoinkernel requires default symbol visibility, explicitly specify that
# here so that things still work even when user configures with
#   --enable-reduce-exports
#
# Note this is a quick hack that will be removed as we incrementally define what
# to export from the library.
libkwalacoinkernel_la_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS) -fvisibility=default

# TODO: libkwalacoinkernel is a work in progress consensus engine library, as more
#       and more modules are decoupled from the consensus engine, this list will
#       shrink to only those which are absolutely necessary.
libkwalacoinkernel_la_SOURCES = \
  kernel/kwalacoinkernel.cpp \
  arith_uint256.cpp \
  chain.cpp \
  clientversion.cpp \
  coins.cpp \
  compressor.cpp \
  consensus/merkle.cpp \
  consensus/tx_check.cpp \
  consensus/tx_verify.cpp \
  core_read.cpp \
  dbwrapper.cpp \
  deploymentinfo.cpp \
  deploymentstatus.cpp \
  flatfile.cpp \
  hash.cpp \
  kernel/chain.cpp \
  kernel/checks.cpp \
  kernel/chainparams.cpp \
  kernel/coinstats.cpp \
  kernel/context.cpp \
  kernel/cs_main.cpp \
  kernel/disconnected_transactions.cpp \
  kernel/mempool_removal_reason.cpp \
  logging.cpp \
  node/blockstorage.cpp \
  node/chainstate.cpp \
  node/utxo_snapshot.cpp \
  policy/feerate.cpp \
  policy/packages.cpp \
  policy/policy.cpp \
  policy/rbf.cpp \
  policy/settings.cpp \
  policy/truc_policy.cpp \
  pow.cpp \
  primitives/block.cpp \
  primitives/transaction.cpp \
  pubkey.cpp \
  random.cpp \
  randomenv.cpp \
  script/interpreter.cpp \
  script/script.cpp \
  script/script_error.cpp \
  script/sigcache.cpp \
  script/solver.cpp \
  signet.cpp \
  streams.cpp \
  support/lockedpool.cpp \
  sync.cpp \
  txdb.cpp \
  txmempool.cpp \
  uint256.cpp \
  util/chaintype.cpp \
  util/check.cpp \
  util/feefrac.cpp \
  util/fs.cpp \
  util/fs_helpers.cpp \
  util/hasher.cpp \
  util/moneystr.cpp \
  util/rbf.cpp \
  util/serfloat.cpp \
  util/signalinterrupt.cpp \
  util/strencodings.cpp \
  util/string.cpp \
  util/syserror.cpp \
  util/threadnames.cpp \
  util/time.cpp \
  util/tokenpipe.cpp \
  validation.cpp \
  validationinterface.cpp \
  versionbits.cpp

# Required for obj/build.h to be generated first.
# More details: https://www.gnu.org/software/automake/manual/html_node/Built-Sources-Example.html
libkwalacoinkernel_la-clientversion.l$(OBJEXT): obj/build.h
endif # BUILD_KWALACOIN_KERNEL_LIB
#

CTAES_DIST =  crypto/ctaes/bench.c
CTAES_DIST += crypto/ctaes/ctaes.c
CTAES_DIST += crypto/ctaes/ctaes.h
CTAES_DIST += crypto/ctaes/README.md
CTAES_DIST += crypto/ctaes/test.c

CLEANFILES = $(EXTRA_LIBRARIES)

CLEANFILES += *.gcda *.gcno
CLEANFILES += compat/*.gcda compat/*.gcno
CLEANFILES += consensus/*.gcda consensus/*.gcno
CLEANFILES += crc32c/src/*.gcda crc32c/src/*.gcno
CLEANFILES += crypto/*.gcda crypto/*.gcno
CLEANFILES += index/*.gcda index/*.gcno
CLEANFILES += interfaces/*.gcda interfaces/*.gcno
CLEANFILES += node/*.gcda node/*.gcno
CLEANFILES += policy/*.gcda policy/*.gcno
CLEANFILES += primitives/*.gcda primitives/*.gcno
CLEANFILES += rpc/*.gcda rpc/*.gcno
CLEANFILES += script/*.gcda script/*.gcno
CLEANFILES += support/*.gcda support/*.gcno
CLEANFILES += univalue/*.gcda univalue/*.gcno
CLEANFILES += util/*.gcda util/*.gcno
CLEANFILES += wallet/*.gcda wallet/*.gcno
CLEANFILES += wallet/test/*.gcda wallet/test/*.gcno
CLEANFILES += zmq/*.gcda zmq/*.gcno
CLEANFILES += obj/build.h

EXTRA_DIST = $(CTAES_DIST)


config/kwalacoin-config.h: config/stamp-h1
	@$(MAKE) -C $(top_builddir) $(subdir)/$(@)
config/stamp-h1: $(top_srcdir)/$(subdir)/config/kwalacoin-config.h.in $(top_builddir)/config.status
	$(AM_V_at)$(MAKE) -C $(top_builddir) $(subdir)/$(@)
$(top_srcdir)/$(subdir)/config/kwalacoin-config.h.in:  $(am__configure_deps)
	$(AM_V_at)$(MAKE) -C $(top_srcdir) $(subdir)/config/kwalacoin-config.h.in

clean-local:
	-$(MAKE) -C secp256k1 clean
	-rm -f leveldb/*/*.gcda leveldb/*/*.gcno leveldb/helpers/memenv/*.gcda leveldb/helpers/memenv/*.gcno
	-rm -f config.h
	-rm -rf test/__pycache__

.rc.o:
	@test -f $(WINDRES) || (echo "windres $(WINDRES) not found, but is required to compile windows resource files"; exit 1)
	## FIXME: How to get the appropriate modulename_CPPFLAGS in here?
	$(AM_V_GEN) $(WINDRES) $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(CPPFLAGS) -DWINDRES_PREPROC -i $< -o $@

check-symbols: $(bin_PROGRAMS)
	@echo "Running symbol and dynamic library checks..."
	$(AM_V_at) $(PYTHON) $(top_srcdir)/contrib/devtools/symbol-check.py $(bin_PROGRAMS)

check-security: $(bin_PROGRAMS)
if HARDEN
	@echo "Checking binary security..."
	$(AM_V_at) $(PYTHON) $(top_srcdir)/contrib/devtools/security-check.py $(bin_PROGRAMS)
endif

libkwalacoin_ipc_mpgen_input = \
  ipc/capnp/echo.capnp \
  ipc/capnp/init.capnp
EXTRA_DIST += $(libkwalacoin_ipc_mpgen_input)
%.capnp:

# Explicitly list dependencies on generated headers as described in
# https://www.gnu.org/software/automake/manual/html_node/Built-Sources-Example.html#Recording-Dependencies-manually
ipc/capnp/libkwalacoin_ipc_a-protocol.$(OBJEXT): $(libkwalacoin_ipc_mpgen_input:=.h)

if BUILD_MULTIPROCESS
LIBKWALACOIN_IPC=libkwalacoin_ipc.a
libkwalacoin_ipc_a_SOURCES = \
  ipc/capnp/common-types.h \
  ipc/capnp/context.h \
  ipc/capnp/init-types.h \
  ipc/capnp/protocol.cpp \
  ipc/capnp/protocol.h \
  ipc/context.h \
  ipc/exception.h \
  ipc/interfaces.cpp \
  ipc/process.cpp \
  ipc/process.h \
  ipc/protocol.h
libkwalacoin_ipc_a_CPPFLAGS = $(AM_CPPFLAGS) $(KWALACOIN_INCLUDES) $(BOOST_CPPFLAGS)
libkwalacoin_ipc_a_CXXFLAGS = $(AM_CXXFLAGS) $(PIE_FLAGS) $(LIBMULTIPROCESS_CFLAGS)

include $(MPGEN_PREFIX)/include/mpgen.mk
libkwalacoin_ipc_mpgen_output = \
  $(libkwalacoin_ipc_mpgen_input:=.c++) \
  $(libkwalacoin_ipc_mpgen_input:=.h) \
  $(libkwalacoin_ipc_mpgen_input:=.proxy-client.c++) \
  $(libkwalacoin_ipc_mpgen_input:=.proxy-server.c++) \
  $(libkwalacoin_ipc_mpgen_input:=.proxy-types.c++) \
  $(libkwalacoin_ipc_mpgen_input:=.proxy-types.h) \
  $(libkwalacoin_ipc_mpgen_input:=.proxy.h)
nodist_libkwalacoin_ipc_a_SOURCES = $(libkwalacoin_ipc_mpgen_output)
CLEANFILES += $(libkwalacoin_ipc_mpgen_output)
endif

%.raw.h: %.raw
	@$(MKDIR_P) $(@D)
	$(AM_V_GEN) { \
	 echo "static unsigned const char $(*F)_raw[] = {" && \
	 $(HEXDUMP) -v -e '8/1 "0x%02x, "' -e '"\n"' $< | $(SED) -e 's/0x  ,//g' && \
	 echo "};"; \
	} > "$@.new" && mv -f "$@.new" "$@"

include Makefile.minisketch.include

include Makefile.crc32c.include
include Makefile.leveldb.include

include Makefile.test_util.include
include Makefile.test_fuzz.include

include Makefile.test.include

if ENABLE_BENCH
include Makefile.bench.include
endif

if ENABLE_QT
include Makefile.qt.include
endif

if ENABLE_QT_TESTS
include Makefile.qttest.include
endif

include Makefile.univalue.include
