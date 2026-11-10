// Copyright (c) 2011-2020 The Bitcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef KWALACOIN_QT_KWALACOINADDRESSVALIDATOR_H
#define KWALACOIN_QT_KWALACOINADDRESSVALIDATOR_H

#include <QValidator>

/** Base58 entry widget validator, checks for valid characters and
 * removes some whitespace.
 */
class KwalaCoinsAddressEntryValidator : public QValidator
{
    Q_OBJECT

public:
    explicit KwalaCoinsAddressEntryValidator(QObject *parent);

    State validate(QString &input, int &pos) const override;
};

/** KwalaCoins address widget validator, checks for a valid kwalacoin address.
 */
class KwalaCoinsAddressCheckValidator : public QValidator
{
    Q_OBJECT

public:
    explicit KwalaCoinsAddressCheckValidator(QObject *parent);

    State validate(QString &input, int &pos) const override;
};

#endif // KWALACOIN_QT_KWALACOINADDRESSVALIDATOR_H
