// Copyright (c) 2023 KwalaCoins Developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include "logprintf.h"
#include "nontrivial-threadlocal.h"

#include <clang-tidy/ClangTidyModule.h>
#include <clang-tidy/ClangTidyModuleRegistry.h>

class KwalaCoinsModule final : public clang::tidy::ClangTidyModule
{
public:
    void addCheckFactories(clang::tidy::ClangTidyCheckFactories& CheckFactories) override
    {
        CheckFactories.registerCheck<kwalacoin::LogPrintfCheck>("kwalacoin-unterminated-logprintf");
        CheckFactories.registerCheck<kwalacoin::NonTrivialThreadLocal>("kwalacoin-nontrivial-threadlocal");
    }
};

static clang::tidy::ClangTidyModuleRegistry::Add<KwalaCoinsModule>
    X("kwalacoin-module", "Adds kwalacoin checks.");

volatile int KwalaCoinsModuleAnchorSource = 0;
