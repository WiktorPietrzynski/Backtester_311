# cython: language_level=3
# cython: nonecheck=False
# cython: cdivision=True
# cython: boundscheck=False
# cython: wraparound=False
import numpy as np
cimport numpy as np
np.import_array()

# basic_backtest
cpdef list advanced_backtest(np.ndarray[double, ndim=2] candles_np_array, list backtest_settings, bint summary, int years):
    cdef int candles_len = candles_np_array.shape[0]
    cdef double[:, :] candles_array = candles_np_array
    cdef double stop_loss_type = backtest_settings[0]
    cdef double stop_loss_value = backtest_settings[1]
    cdef double take_profit_type = backtest_settings[2]
    cdef double take_profit_value = backtest_settings[3]
    cdef double fees = backtest_settings[4]/100
    cdef list returns_list = calc_advanced_backtest(candles_array, candles_len, stop_loss_type, stop_loss_value, take_profit_type, take_profit_value, fees)
    if summary:
        return make_summary(returns_list, years)
    else:
        return returns_list


# backtest
cdef list calc_advanced_backtest(double[:, :] candles, int candles_len, double stop_loss_type, double stop_loss_value, double take_profit_type, double take_profit_value, double fees):
    cdef list returns_list = []
    cdef int candle_id
    cdef double profit = 0.00
    cdef int side = 0
    cdef double open_price, candle_open, candle_high, candle_low, stop_loss_price, liquidation_price, take_profit_price
    for candle_id in range(candles_len):
        # candle_open, candle_high, candle_low, go_long, go_short, exit_long, exit_short = candles[candle_id]
        if side == 0:
            if candles[candle_id, 3]:
                # open long
                open_price = candles[candle_id, 0]
                candle_high = candles[candle_id, 1]
                candle_low = candles[candle_id, 2]
                side = 1
                stop_loss_price = set_stop_loss_price(side, open_price, stop_loss_type, stop_loss_value)
                liquidation_price = set_liquidation_price(side, open_price)
                take_profit_price = set_take_profit_price(side, open_price, take_profit_type, take_profit_value)
                # calc long
                profit = calc_trade_long(open_price, stop_loss_price, liquidation_price, take_profit_price, candle_high, candle_low, fees)
                if profit:
                    returns_list.append(profit)
                    profit = 0.0
                    side = 0
                else:
                    stop_loss_price = update_stop_loss_price_long(open_price, stop_loss_type, stop_loss_value, stop_loss_price, candle_high)
            elif candles[candle_id, 4]:
                # open short
                open_price = candles[candle_id, 0]
                candle_high = candles[candle_id, 1]
                candle_low = candles[candle_id, 2]
                side = 2
                stop_loss_price = set_stop_loss_price(side, open_price, stop_loss_type, stop_loss_value)
                liquidation_price = set_liquidation_price(side, open_price)
                take_profit_price = set_take_profit_price(side, open_price, take_profit_type, take_profit_value)
                # calc short
                profit = calc_trade_short(open_price, stop_loss_price, liquidation_price, take_profit_price, candle_high, candle_low, fees)
                if profit:
                    returns_list.append(profit)
                    profit = 0.0
                    side = 0
                else:
                    stop_loss_price = update_stop_loss_price_short(open_price, stop_loss_type, stop_loss_value, stop_loss_price, candle_low)
            else:
                continue
        elif side == 1:
            candle_high = candles[candle_id, 1]
            candle_low = candles[candle_id, 2]
            if candles[candle_id, 5]:
                # exit long
                candle_open = candles[candle_id, 0]
                profit = calc_profit_long(open_price, candle_open, fees)
                returns_list.append(profit)
                profit = 0.0
                side = 0
                if candles[candle_id, 4]:
                    # open short
                    open_price = candle_open
                    side = 2
                    stop_loss_price = set_stop_loss_price(side, open_price, stop_loss_type, stop_loss_value)
                    liquidation_price = set_liquidation_price(side, open_price)
                    take_profit_price = set_take_profit_price(side, open_price, take_profit_type, take_profit_value)
                    # calc short
                    profit = calc_trade_short(open_price, stop_loss_price, liquidation_price, take_profit_price, candle_high, candle_low, fees)
                    if profit:
                        returns_list.append(profit)
                        profit = 0.0
                        side = 0
                    else:
                        stop_loss_price = update_stop_loss_price_short(open_price, stop_loss_type, stop_loss_value, stop_loss_price, candle_low)
            else:
                # calc long
                profit = calc_trade_long(open_price, stop_loss_price, liquidation_price, take_profit_price, candle_high, candle_low, fees)
                if profit:
                    returns_list.append(profit)
                    profit = 0.0
                    side = 0
                else:
                    stop_loss_price = update_stop_loss_price_long(open_price, stop_loss_type, stop_loss_value, stop_loss_price, candle_high)
        elif side == 2:
            candle_high = candles[candle_id, 1]
            candle_low = candles[candle_id, 2]
            if candles[candle_id, 6]:
                # exit short
                candle_open = candles[candle_id, 0]
                profit = calc_profit_short(open_price, candle_open, fees)
                returns_list.append(profit)
                profit = 0.0
                side = 0
                if candles[candle_id, 3]:
                    # open long
                    open_price = candle_open
                    side = 1
                    stop_loss_price = set_stop_loss_price(side, open_price, stop_loss_type, stop_loss_value)
                    liquidation_price = set_liquidation_price(side, open_price)
                    take_profit_price = set_take_profit_price(side, open_price, take_profit_type, take_profit_value)
                    # calc long
                    profit = calc_trade_long(open_price, stop_loss_price, liquidation_price, take_profit_price, candle_high, candle_low, fees)
                    if profit:
                        returns_list.append(profit)
                        profit = 0.0
                        side = 0
                    else:
                        stop_loss_price = update_stop_loss_price_long(open_price, stop_loss_type, stop_loss_value, stop_loss_price, candle_high)
            else:
                # calc short
                profit = calc_trade_short(open_price, stop_loss_price, liquidation_price, take_profit_price, candle_high, candle_low, fees)
                if profit:
                    returns_list.append(profit)
                    profit = 0.0
                    side = 0
                else:
                    stop_loss_price = update_stop_loss_price_short(open_price, stop_loss_type, stop_loss_value, stop_loss_price, candle_low)
    return returns_list




# trades
cdef double set_liquidation_price(int side, double open_price) nogil:
    return open_price * 2.0 if side == 2 else 0.0


cdef double set_stop_loss_price(int side, double open_price, double stop_loss_type, double stop_loss_value) nogil:
    cdef double stop_loss_price = 0.0
    if stop_loss_value != 0:
        if side == 2:
            stop_loss_value = -stop_loss_value
        if stop_loss_type == 2.0 or stop_loss_type == 3.0:
            stop_loss_price = open_price * ((100 - stop_loss_value) / 100)
        else:
            stop_loss_price = open_price - stop_loss_value
    return stop_loss_price


cdef double set_take_profit_price(int side, double open_price, double take_profit_type, double take_profit_value) nogil:
    cdef double take_profit_price = 0.0
    if take_profit_value != 0:
        if side == 2:
            take_profit_value = -take_profit_value
        if take_profit_type == 2.0:
            take_profit_price = open_price * ((100 + take_profit_value) / 100)
        else:
            take_profit_price = open_price + take_profit_value
    return take_profit_price


cdef double calc_trade_long(double open_price, double stop_loss_price, double liquidation_price, double take_profit_price, double candle_high, double candle_low, double fees) nogil:
    cdef double profit = 0.0
    if stop_loss_long(candle_low, stop_loss_price):
        profit = calc_profit_long(open_price, stop_loss_price, fees)
    elif liquidation_long(candle_low, liquidation_price):
        profit = calc_profit_long(open_price, liquidation_price, fees)
    elif take_profit_long(candle_high, take_profit_price):
        profit = calc_profit_long(open_price, take_profit_price, fees)
    return profit


cdef double calc_trade_short(double open_price, double stop_loss_price, double liquidation_price, double take_profit_price, double candle_high, double candle_low, double fees) nogil:
    cdef double profit = 0.0
    if stop_loss_short(candle_high, stop_loss_price):
        profit = calc_profit_short(open_price, stop_loss_price, fees)
    elif liquidation_short(candle_high, liquidation_price):
        profit = calc_profit_short(open_price, liquidation_price, fees)
    elif take_profit_short(candle_low, take_profit_price):
        profit = calc_profit_short(open_price, take_profit_price, fees)
    return profit


cdef inline bint stop_loss_long(double candle_low, double stop_loss_price) nogil:
    if stop_loss_price:
        if stop_loss_price >= candle_low:
            return True
    return False


cdef inline bint stop_loss_short(double candle_high, double stop_loss_price) nogil:
    if stop_loss_price:
        if stop_loss_price <= candle_high:
            return True
    return False


cdef inline bint liquidation_long(double candle_low, double liquidation_price) nogil:
    return True if liquidation_price >= candle_low else False


cdef inline bint liquidation_short(double candle_high, double liquidation_price) nogil:
    return True if liquidation_price <= candle_high else False


cdef inline bint take_profit_long(double candle_high, double take_profit_price) nogil:
    if take_profit_price:
        if take_profit_price <= candle_high:
            return True
    return False


cdef inline bint take_profit_short(double candle_low, double take_profit_price) nogil:
    if take_profit_price:
        if take_profit_price >= candle_low:
            return True
    return False


cdef inline double calc_profit_long(double open_price, double exit_price, double fees) nogil:
    cdef double profit = 100 * (exit_price - open_price) / open_price
    cdef double total_fee = (100 * fees) + ((100 + profit) * fees)
    return profit - total_fee


cdef inline double calc_profit_short(double open_price, double exit_price, double fees) nogil:
    cdef double profit = 100 * (open_price - exit_price) / open_price
    cdef double total_fee = (100 * fees) + ((100 + profit) * fees)
    return profit - total_fee


cdef inline double update_stop_loss_price_long(double open_price, double stop_loss_type, double stop_loss_value, double stop_loss_price, double candle_high) nogil:
    cdef double trailing_stop_loss_price = 0.0
    if stop_loss_type == 3.0 and stop_loss_value:
        if candle_high > open_price:
            trailing_stop_loss_price = candle_high * ((100 - stop_loss_value) / 100)
            if stop_loss_price < trailing_stop_loss_price:
                stop_loss_price = trailing_stop_loss_price
    return stop_loss_price


cdef inline double update_stop_loss_price_short(double open_price, double stop_loss_type, double stop_loss_value, double stop_loss_price, double candle_low) nogil:
    cdef double trailing_stop_loss_price = 0.0
    if stop_loss_type == 3.0 and stop_loss_value:
        if candle_low < open_price:
            trailing_stop_loss_price = candle_low * ((100 + stop_loss_value) / 100)
            if stop_loss_price > trailing_stop_loss_price:
                stop_loss_price = trailing_stop_loss_price
    return stop_loss_price

# summary

cdef list make_summary(list returns_list, int years):
    if len(returns_list) == 0:
        return [0.0 for i in range(16)]
    else:
        return make_summary_cy(returns_list, years)

cdef make_summary_cy(list returns_list, int years):
    cdef np.ndarray[double, ndim=1] returns_array = np.array(returns_list)
    cdef int trade_count = returns_array.shape[0]
    cdef double total_profit, win_rate, avg_trade, total_profit_to_drawdown, mmar_ratio, volatility, avg_win, max_win, avg_loss, max_loss, max_drawdown, profit_factor, sharpe_ratio, sortino_ratio, total_win, total_loss, net_profit, net_profit_to_drawdown, rar, cagr, mar_ratio
    cdef np.ndarray[double, ndim=1] win_returns_array = returns_array[returns_array > 0]
    cdef np.ndarray[double, ndim=1] loss_returns_array = returns_array[returns_array < 0]
    cdef int win_trades_count = win_returns_array.shape[0]
    cdef int loss_trades_count = loss_returns_array.shape[0]
    cdef np.ndarray[double, ndim=1] total_profit_array = np.cumprod(1 + returns_array / 100)
    cdef np.ndarray[double, ndim=1] total_returns_array = np.diff(np.insert(total_profit_array, 0, 1.0))
    # stats
    avg_trade = np.mean(returns_array)
    volatility = np.std(returns_array)
    total_profit = (100 * (total_profit_array[trade_count - 1])) - 100
    max_drawdown = calc_max_drawdown(total_profit_array)
    if win_trades_count > 0:
        avg_win = np.mean(win_returns_array)
        max_win = np.max(win_returns_array)
        win_rate = win_trades_count * 100.0 / trade_count
    else:
        avg_win = 0.0
        max_win = 0.0
        win_rate = 0.
        total_win = 0.0
    if loss_trades_count > 0:
        avg_loss = np.mean(loss_returns_array)
        max_loss = np.min(loss_returns_array)
        total_profit_to_drawdown = total_profit / max_drawdown
        sortino_ratio = calc_sortino_ratio(loss_returns_array, avg_trade)
    else:
        avg_loss = 0.0
        max_loss = 0.0
        total_loss = 0.0
        total_profit_to_drawdown = 0.0
        sortino_ratio = 0.0

    sharpe_ratio = calc_sharpe_ratio(avg_trade, volatility)
    cagr = calc_cagr(returns_array, total_profit, years)
    rar = calc_rar(total_profit_array, trade_count, years)
    mar_ratio = calc_mar_ratio(cagr, max_drawdown)
    mmar_ratio = calc_mmar_ratio(rar, max_drawdown)
    return [total_profit, max_drawdown, total_profit_to_drawdown, trade_count, win_rate, avg_trade, avg_win, avg_loss, max_win, max_loss, sharpe_ratio, sortino_ratio, cagr, rar, mar_ratio, mmar_ratio]



# cdef np.ndarray[double, ndim=1] remove_outliners(np.ndarray[double, ndim=1] returns_array):
#     cdef double top_threshold = np.percentile(returns_array, 90)
#     cdef double bottom_threshold = np.percentile(returns_array, 1)
#     # returns_array = returns_array[(returns_array <= top_threshold) & (returns_array >= bottom_threshold)]
#     returns_array = returns_array[(returns_array <= top_threshold)]
#     return returns_array


cdef double calc_max_drawdown(np.ndarray[double, ndim=1] total_profit_array):
    cdef np.ndarray[double, ndim=1] running_max_array = np.maximum.accumulate(total_profit_array)
    cdef np.ndarray[double, ndim=1] drawdown_array = (running_max_array - total_profit_array) / running_max_array * 100
    return np.max(drawdown_array)


cdef double calc_sharpe_ratio(double avg_trade, double volatility):
    if volatility == 0.0:
        return 100.0
    cdef double sharpe_ratio = avg_trade / volatility
    if sharpe_ratio > 100.0:
        return 100.0
    elif sharpe_ratio < -100:
        return -100.0
    else:
        return sharpe_ratio


cdef double calc_sortino_ratio(np.ndarray[double, ndim=1] loss_returns_array, double avg_trade):
    cdef double downside_dev = np.std(loss_returns_array)
    if downside_dev < 0.01:
        downside_dev = 0.01
    cdef double sortino_ratio = avg_trade / downside_dev
    return sortino_ratio

cdef double calc_rar(np.ndarray[double, ndim=1] total_profit_array, int trade_count, int years):
    cdef double rar_ratio
    if trade_count < 2:
        return 0.0
    total_profit_array = total_profit_array * 100.0
    cdef np.ndarray[double, ndim=1] x_values = np.arange(1.0, trade_count+1)
    # cdef np.ndarray[double, ndim=1] ab = np.polyfit(x_values, returns_array, deg=1)
    # return ab[0] * trade_count + ab[1]
    cdef np.ndarray[double, ndim=2] x_mat = np.vstack((np.ones(trade_count), x_values)).T
    cdef np.ndarray[double, ndim=1] beta_hat = np.linalg.inv(x_mat.T.dot(x_mat)).dot(x_mat.T).dot(total_profit_array)
    rar_ratio = beta_hat[1] * trade_count + beta_hat[0] - 100
    if years == 1:
        return rar_ratio
    else:
        return ((rar_ratio / 100) ** (1.0 / years) - 1) *100


cdef double calc_cagr(np.ndarray[double, ndim=1] returns_array, double total_profit, int years):
    # print(total_profit, years)
    if years == 1:
        return total_profit
    else:
        return ((total_profit/100) ** (1.0 / years) - 1) * 100

cdef double calc_mar_ratio(double cagr, double max_drawdown):
    if max_drawdown == 0.0:
        return 100.0
    else:
        return cagr / max_drawdown

cdef double calc_mmar_ratio(double rar, double max_drawdown):
    if max_drawdown == 0.0:
        return 100.0
    else:
        return rar / max_drawdown



