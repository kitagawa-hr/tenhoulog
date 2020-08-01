from tenhoulog import utils

import pandas as pd


def test_df2table():
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [5, 4, 3, 2, 1]})
    table = utils.df2table(df)
    assert table.columns.header.value == ["A", "B"]
    expected_rows = [[1, 5], [2, 4], [3, 3], [4, 2], [5, 1]]
    for actual_row, expected_row in zip(table.rows, expected_rows):
        assert actual_row.value == expected_row
