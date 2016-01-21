# BEGIN: TRADEWAVE MOVING AVERAGE CROSSOVER EXAMPLE
THRESHOLD = 0.005
INTERVAL = 43200
SHORT = 10
LONG = 90


def initialize():
    storage.invested = storage.get('invested', False)


def tick():
    short_term = data(interval=INTERVAL).btc_usd.ma(SHORT)
    long_term = data(interval=INTERVAL).btc_usd.ma(LONG)
    diff = 100 * (short_term - long_term) / ((short_term + long_term) / 2)

    if diff >= THRESHOLD and not storage.invested:
        buy(pairs.btc_usd)
        storage.invested = True
    elif diff <= -THRESHOLD and storage.invested:
        sell(pairs.btc_usd)
        storage.invested = False

    plot('short_term', short_term)
    plot('long_term', long_term)
    # END: TRADEWAVE MOVING AVERAGE CROSSOVER EXAMPLE
    ##############################################################

    ##############################################################
    # BEGIN MAX DRAW DOWN by litepresence
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    dd()


ROLLING = 30  # days


def dd():
    dd, storage.max_dd = max_dd(0)
    bnh_dd, storage.max_bnh_dd = bnh_max_dd(0)
    rolling_dd, storage.max_rolling_dd = max_dd(
        ROLLING * 86400 / info.interval)
    rolling_bnh_dd, storage.max_rolling_bnh_dd = bnh_max_dd(
        ROLLING * 86400 / info.interval)

    plot('dd', dd, secondary=True)
    plot('bnh_dd', bnh_dd, secondary=True)
    plot('rolling_dd', rolling_dd, secondary=True)
    plot('rolling_bnh_dd', rolling_bnh_dd, secondary=True)
    plot('zero', 0, secondary=True)
    if info.tick == 0:
        plot('dd_floor', -200, secondary=True)


def max_dd(rolling):
    port_value = float(portfolio.usd + portfolio.btc * data.btc_usd.price)
    max_value = 'max_value_' + str(rolling)
    values_since_max = 'values_since_max_' + str(rolling)
    max_dd = 'max_dd_' + str(rolling)
    storage[max_value] = storage.get(max_value, [port_value])
    storage[values_since_max] = storage.get(values_since_max, [port_value])
    storage[max_dd] = storage.get(max_dd, [0])
    storage[max_value].append(port_value)
    if port_value > max(storage[max_value]):
        storage[values_since_max] = [port_value]
    else:
        storage[values_since_max].append(port_value)
    storage[max_value] = storage[max_value][-rolling:]
    storage[values_since_max] = storage[values_since_max][-rolling:]
    dd = -100 * (max(storage[max_value]) - storage[values_since_max][-1]
                 ) / max(storage[max_value])
    storage[max_dd].append(float(dd))
    storage[max_dd] = storage[max_dd][-rolling:]
    max_dd = min(storage[max_dd])

    return (dd, max_dd)


def bnh_max_dd(rolling):
    coin = data.btc_usd.price
    bnh_max_value = 'bnh_max_value_' + str(rolling)
    bnh_values_since_max = 'bnh_values_since_max_' + str(rolling)
    bnh_max_dd = 'bnh_max_dd_' + str(rolling)
    storage[bnh_max_value] = storage.get(bnh_max_value, [coin])
    storage[bnh_values_since_max] = storage.get(bnh_values_since_max, [coin])
    storage[bnh_max_dd] = storage.get(bnh_max_dd, [0])
    storage[bnh_max_value].append(coin)
    if coin > max(storage[bnh_max_value]):
        storage[bnh_values_since_max] = [coin]
    else:
        storage[bnh_values_since_max].append(coin)
    storage[bnh_max_value] = storage[bnh_max_value][-rolling:]
    storage[bnh_values_since_max] = storage[bnh_values_since_max][-rolling:]
    bnh_dd = -100 * (max(storage[bnh_max_value]) - storage[bnh_values_since_max][-1]
                     ) / max(storage[bnh_max_value])
    storage[bnh_max_dd].append(float(bnh_dd))
    storage[bnh_max_dd] = storage[bnh_max_dd][-rolling:]
    bnh_max_dd = min(storage[bnh_max_dd])

    return (bnh_dd, bnh_max_dd)


def stop():
    log('MAX DD......: %.2f pct' % storage.max_dd)
    log('R MAX DD....: %.2f pct' % storage.max_rolling_dd)
    log('MAX BNH DD..: %.2f pct' % storage.max_bnh_dd)
    log('R MAX BNH DD: %.2f pct' % storage.max_rolling_bnh_dd)
