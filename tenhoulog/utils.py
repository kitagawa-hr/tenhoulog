from datetime import datetime, tzinfo

import pandas as pd
from beautifultable import BeautifulTable


def start_of_today(tz: tzinfo) -> datetime:
    """指定したtimezoneにおける, 当日の00:00を表すdatetime"""
    now = datetime.now(tz=tz)
    return datetime(year=now.year, month=now.month, day=now.day, hour=0, second=0, tzinfo=tz)


def df2table(df: pd.DataFrame) -> BeautifulTable:
    """データフレームを可読性の高いテーブルに変換"""
    table = BeautifulTable()
    table.columns.header = df.columns
    for row in df.values:
        table.rows.append(row)
    return table
