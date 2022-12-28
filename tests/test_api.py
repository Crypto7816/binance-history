import pytest
from pandas import Timestamp

from binance_history import fetch_klines, fetch_agg_trades, fetch_data


def test_fetch_klines_1m_one_month():
    asset_type = "spot"
    symbol = "BTCUSDT"
    start = "2022-1-2 5:29"
    end = "2022-1-5 11:31"
    tz = "Asia/Shanghai"

    klines = fetch_klines(
        asset_type=asset_type,
        symbol=symbol,
        timeframe="1m",
        start=start,
        end=end,
        tz=tz,
    )

    assert klines.index[0] == Timestamp(start, tz=tz)
    assert klines.close_datetime[0] == Timestamp("2022-1-2 5:29:59.999", tz=tz)
    assert klines.index[-1] == Timestamp(end, tz=tz)
    assert klines.close_datetime[-1] == Timestamp("2022-1-5 11:31:59.999", tz=tz)


def test_fetch_klines_1m_many_months():
    asset_type = "spot"
    symbol = "BTCUSDT"
    start = "2022-1-1 5:29"
    end = "2022-2-3 11:31"
    tz = "Asia/Shanghai"

    klines = fetch_klines(
        asset_type=asset_type,
        symbol=symbol,
        timeframe="1m",
        start=start,
        end=end,
        tz=tz,
    )

    assert klines.index[0] == Timestamp(start, tz=tz)
    assert klines.close_datetime[0] == Timestamp("2022-1-1 5:29:59.999", tz=tz)
    assert klines.index[-1] == Timestamp(end, tz=tz)
    assert klines.close_datetime[-1] == Timestamp("2022-2-3 11:31:59.999", tz=tz)


def test_fetch_klines_15m_many_months():
    asset_type = "spot"
    symbol = "BTCUSDT"
    start = "2022-1-1 5:29"
    end = "2022-2-3 11:31"
    tz = "Asia/Shanghai"

    klines = fetch_klines(
        asset_type=asset_type,
        symbol=symbol,
        timeframe="15m",
        start=start,
        end=end,
        tz=tz,
    )

    assert klines.index[0] == Timestamp("2022-1-1 5:30", tz=tz)
    assert klines.close_datetime[0] == Timestamp("2022-1-1 5:44:59.999", tz=tz)
    assert klines.index[-1] == Timestamp("2022-2-3 11:30", tz=tz)
    assert klines.close_datetime[-1] == Timestamp("2022-2-3 11:44:59.999", tz=tz)


def test_fetch_klines_1h_this_month():
    asset_type = "spot"
    symbol = "BTCUSDT"
    start = "2022-11-2 5:29"
    end = Timestamp.now().replace(day=2)
    tz = "Asia/Shanghai"

    klines = fetch_klines(
        asset_type=asset_type,
        symbol=symbol,
        timeframe="1h",
        start=start,
        end=end,
        tz=tz,
    )

    assert klines.index[0] == Timestamp("2022-11-2 6:00", tz=tz)
    assert klines.close_datetime[0] == Timestamp("2022-11-2 6:59:59.999", tz=tz)
    assert klines.index[-1] == Timestamp(
        year=end.year, month=end.month, day=end.day, hour=end.hour, tz=tz
    )
    assert klines.close_datetime[-1] == Timestamp(
        year=end.year,
        month=end.month,
        day=end.day,
        hour=end.hour,
        minute=59,
        second=59,
        microsecond=999000,
        tz=tz,
    )


def test_fetch_klines_missing_timezone():
    asset_type = "spot"
    symbol = "BTCUSDT"
    start = "2022-1-2 5:29"
    end = "2022-1-5 11:31"
    tz = "Asia/Shanghai"

    fetch_klines(
        asset_type=asset_type,
        symbol=symbol,
        timeframe="1m",
        start=Timestamp(start, tz=tz),
        end=Timestamp(end, tz=tz),
        tz=None,
    )

    fetch_klines(
        asset_type=asset_type,
        symbol=symbol,
        timeframe="1m",
        start=Timestamp(start, tz=None),
        end=Timestamp(end, tz=None),
        tz=tz,
    )


def test_fetch_agg_trades_one_month():
    asset_type = "spot"
    symbol = "ETCBTC"
    start = "2022-1-2 8:29"
    end = "2022-1-10 11:31"
    tz = "Asia/Shanghai"

    agg_trades = fetch_agg_trades(asset_type, symbol, start, end, tz)
    assert agg_trades.index[0].day == 2
    assert agg_trades.index[-1].day == 10


def test_fetch_data_with_wrong_data_type():
    data_type = "binance-btc-private-key"
    asset_type = "spot"
    symbol = "ETCBTC"
    start = "2022-1-2 8:29"
    end = "2022-1-10 11:31"
    tz = "Asia/Shanghai"

    with pytest.raises(ValueError):
        fetch_data(data_type, asset_type, symbol, start, end, tz)
