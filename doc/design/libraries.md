# Libraries

| Name                     | Description |
|--------------------------|-------------|
| *libkwalacoin_cli*         | RPC client functionality used by *kwalacoin-cli* executable |
| *libkwalacoin_common*      | Home for common functionality shared by different executables and libraries. Similar to *libkwalacoin_util*, but higher-level (see [Dependencies](#dependencies)). |
| *libkwalacoin_consensus*   | Stable, backwards-compatible consensus functionality used by *libkwalacoin_node* and *libkwalacoin_wallet*. |
| *libkwalacoin_crypto*      | Hardware-optimized functions for data encryption, hashing, message authentication, and key derivation. |
| *libkwalacoin_kernel*      | Consensus engine and support library used for validation by *libkwalacoin_node*. |
| *libkwalacoinqt*           | GUI functionality used by *kwalacoin-qt* and *kwalacoin-gui* executables. |
| *libkwalacoin_ipc*         | IPC functionality used by *kwalacoin-node*, *kwalacoin-wallet*, *kwalacoin-gui* executables to communicate when [`--enable-multiprocess`](multiprocess.md) is used. |
| *libkwalacoin_node*        | P2P and RPC server functionality used by *kwalacoind* and *kwalacoin-qt* executables. |
| *libkwalacoin_util*        | Home for common functionality shared by different executables and libraries. Similar to *libkwalacoin_common*, but lower-level (see [Dependencies](#dependencies)). |
| *libkwalacoin_wallet*      | Wallet functionality used by *kwalacoind* and *kwalacoin-wallet* executables. |
| *libkwalacoin_wallet_tool* | Lower-level wallet functionality used by *kwalacoin-wallet* executable. |
| *libkwalacoin_zmq*         | [ZeroMQ](../zmq.md) functionality used by *kwalacoind* and *kwalacoin-qt* executables. |

## Conventions

- Most libraries are internal libraries and have APIs which are completely unstable! There are few or no restrictions on backwards compatibility or rules about external dependencies. An exception is *libkwalacoin_kernel*, which, at some future point, will have a documented external interface.

- Generally each library should have a corresponding source directory and namespace. Source code organization is a work in progress, so it is true that some namespaces are applied inconsistently, and if you look at [`libkwalacoin_*_SOURCES`](../../src/Makefile.am) lists you can see that many libraries pull in files from outside their source directory. But when working with libraries, it is good to follow a consistent pattern like:

  - *libkwalacoin_node* code lives in `src/node/` in the `node::` namespace
  - *libkwalacoin_wallet* code lives in `src/wallet/` in the `wallet::` namespace
  - *libkwalacoin_ipc* code lives in `src/ipc/` in the `ipc::` namespace
  - *libkwalacoin_util* code lives in `src/util/` in the `util::` namespace
  - *libkwalacoin_consensus* code lives in `src/consensus/` in the `Consensus::` namespace

## Dependencies

- Libraries should minimize what other libraries they depend on, and only reference symbols following the arrows shown in the dependency graph below:

<table><tr><td>

```mermaid

%%{ init : { "flowchart" : { "curve" : "basis" }}}%%

graph TD;

kwalacoin-cli[kwalacoin-cli]-->libkwalacoin_cli;

kwalacoind[kwalacoind]-->libkwalacoin_node;
kwalacoind[kwalacoind]-->libkwalacoin_wallet;

kwalacoin-qt[kwalacoin-qt]-->libkwalacoin_node;
kwalacoin-qt[kwalacoin-qt]-->libkwalacoinqt;
kwalacoin-qt[kwalacoin-qt]-->libkwalacoin_wallet;

kwalacoin-wallet[kwalacoin-wallet]-->libkwalacoin_wallet;
kwalacoin-wallet[kwalacoin-wallet]-->libkwalacoin_wallet_tool;

libkwalacoin_cli-->libkwalacoin_util;
libkwalacoin_cli-->libkwalacoin_common;

libkwalacoin_consensus-->libkwalacoin_crypto;

libkwalacoin_common-->libkwalacoin_consensus;
libkwalacoin_common-->libkwalacoin_crypto;
libkwalacoin_common-->libkwalacoin_util;

libkwalacoin_kernel-->libkwalacoin_consensus;
libkwalacoin_kernel-->libkwalacoin_crypto;
libkwalacoin_kernel-->libkwalacoin_util;

libkwalacoin_node-->libkwalacoin_consensus;
libkwalacoin_node-->libkwalacoin_crypto;
libkwalacoin_node-->libkwalacoin_kernel;
libkwalacoin_node-->libkwalacoin_common;
libkwalacoin_node-->libkwalacoin_util;

libkwalacoinqt-->libkwalacoin_common;
libkwalacoinqt-->libkwalacoin_util;

libkwalacoin_util-->libkwalacoin_crypto;

libkwalacoin_wallet-->libkwalacoin_common;
libkwalacoin_wallet-->libkwalacoin_crypto;
libkwalacoin_wallet-->libkwalacoin_util;

libkwalacoin_wallet_tool-->libkwalacoin_wallet;
libkwalacoin_wallet_tool-->libkwalacoin_util;

classDef bold stroke-width:2px, font-weight:bold, font-size: smaller;
class kwalacoin-qt,kwalacoind,kwalacoin-cli,kwalacoin-wallet bold
```
</td></tr><tr><td>

**Dependency graph**. Arrows show linker symbol dependencies. *Crypto* lib depends on nothing. *Util* lib is depended on by everything. *Kernel* lib depends only on consensus, crypto, and util.

</td></tr></table>

- The graph shows what _linker symbols_ (functions and variables) from each library other libraries can call and reference directly, but it is not a call graph. For example, there is no arrow connecting *libkwalacoin_wallet* and *libkwalacoin_node* libraries, because these libraries are intended to be modular and not depend on each other's internal implementation details. But wallet code is still able to call node code indirectly through the `interfaces::Chain` abstract class in [`interfaces/chain.h`](../../src/interfaces/chain.h) and node code calls wallet code through the `interfaces::ChainClient` and `interfaces::Chain::Notifications` abstract classes in the same file. In general, defining abstract classes in [`src/interfaces/`](../../src/interfaces/) can be a convenient way of avoiding unwanted direct dependencies or circular dependencies between libraries.

- *libkwalacoin_crypto* should be a standalone dependency that any library can depend on, and it should not depend on any other libraries itself.

- *libkwalacoin_consensus* should only depend on *libkwalacoin_crypto*, and all other libraries besides *libkwalacoin_crypto* should be allowed to depend on it.

- *libkwalacoin_util* should be a standalone dependency that any library can depend on, and it should not depend on other libraries except *libkwalacoin_crypto*. It provides basic utilities that fill in gaps in the C++ standard library and provide lightweight abstractions over platform-specific features. Since the util library is distributed with the kernel and is usable by kernel applications, it shouldn't contain functions that external code shouldn't call, like higher level code targeted at the node or wallet. (*libkwalacoin_common* is a better place for higher level code, or code that is meant to be used by internal applications only.)

- *libkwalacoin_common* is a home for miscellaneous shared code used by different KwalaCoins applications. It should not depend on anything other than *libkwalacoin_util*, *libkwalacoin_consensus*, and *libkwalacoin_crypto*.

- *libkwalacoin_kernel* should only depend on *libkwalacoin_util*, *libkwalacoin_consensus*, and *libkwalacoin_crypto*.

- The only thing that should depend on *libkwalacoin_kernel* internally should be *libkwalacoin_node*. GUI and wallet libraries *libkwalacoinqt* and *libkwalacoin_wallet* in particular should not depend on *libkwalacoin_kernel* and the unneeded functionality it would pull in, like block validation. To the extent that GUI and wallet code need scripting and signing functionality, they should be get able it from *libkwalacoin_consensus*, *libkwalacoin_common*, *libkwalacoin_crypto*, and *libkwalacoin_util*, instead of *libkwalacoin_kernel*.

- GUI, node, and wallet code internal implementations should all be independent of each other, and the *libkwalacoinqt*, *libkwalacoin_node*, *libkwalacoin_wallet* libraries should never reference each other's symbols. They should only call each other through [`src/interfaces/`](../../src/interfaces/) abstract interfaces.

## Work in progress

- Validation code is moving from *libkwalacoin_node* to *libkwalacoin_kernel* as part of [The libkwalacoinkernel Project #27587](https://github.com/bitcoin/bitcoin/issues/27587)
