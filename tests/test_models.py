from datetime import datetime, timedelta, timezone, date

import pytest
import pandas as pd

from tenhoulog import models
from tenhoulog.models import GameResult

JST = timezone(timedelta(hours=+9), "JST")


@pytest.fixture
def player_names():
    return [
        "アカギ",
        "ワシズ",
        "黒服A",
        "黒服B",
        "黒服C",
        "黒服D",
    ]


@pytest.fixture
def game_results_3():
    """
    +--------+--------+-------+--------+--------+--------+
    | アカギ  | ワシズ  | 黒服A  | 黒服B  |  黒服C  | 黒服D   |
    +--------+--------+-------+--------+--------+--------+
    | 100.0  | -88.2  | -11.8 |  nan   |  nan   |  nan   |
    +--------+--------+-------+--------+--------+--------+
    | 290.4  |  nan   |  nan  | -160.4 |  nan   | -130.0 |
    +--------+--------+-------+--------+--------+--------+
    |  nan   | 380.0  |  nan  | -220.0 | -160.0 |  nan   |
    +--------+--------+-------+--------+--------+--------+
    |  nan   |  nan   | 45.6  |  0.0   | -45.6  |  nan   |
    +--------+--------+-------+--------+--------+--------+

    """
    fields = [
        {
            "lobby": "1111",
            "playernum": 3,
            "player1": "アカギ",
            "player1ptr": 100.0,
            "player1shuugi": 10,
            "player2": "黒服A",
            "player2ptr": -11.8,
            "player2shuugi": -2,
            "player3": "ワシズ",
            "player3ptr": -88.2,
            "player3shuugi": -8,
            "starttime": datetime(1978, 11, 22),
        },
        {
            "lobby": "1111",
            "playernum": 3,
            "player1": "アカギ",
            "player1ptr": 290.4,
            "player1shuugi": None,
            "player2": "黒服D",
            "player2ptr": -130.0,
            "player2shuugi": None,
            "player3": "黒服B",
            "player3ptr": -160.4,
            "player3shuugi": None,
            "starttime": datetime(1978, 11, 23),
        },
        {
            "lobby": "1111",
            "playernum": 3,
            "player1": "ワシズ",
            "player1ptr": 380,
            "player1shuugi": 140,
            "player2": "黒服C",
            "player2ptr": -160,
            "player2shuugi": -70,
            "player3": "黒服B",
            "player3ptr": -220,
            "player3shuugi": -70,
            "starttime": datetime(1978, 11, 23),
        },
        {
            "lobby": "1111",
            "playernum": 3,
            "player1": "黒服A",
            "player1ptr": 45.6,
            "player1shuugi": None,
            "player2": "黒服B",
            "player2ptr": 0,
            "player2shuugi": None,
            "player3": "黒服C",
            "player3ptr": -45.6,
            "player3shuugi": None,
            "starttime": datetime(1978, 11, 24),
        },
    ]
    return [GameResult(**field) for field in fields]


@pytest.fixture
def game_results_4():
    """
    +--------+--------+-------+--------+--------+--------+
    | アカギ  | ワシズ  | 黒服A  | 黒服B  |  黒服C  | 黒服D   |
    +--------+--------+-------+--------+--------+--------+
    | 100.0  | -88.2  | -8.3  |  3.5   |  nan   |  nan   |
    +--------+--------+-------+--------+--------+--------+
    | 290.4  |  nan   |  0.0  | -160.4 |  nan   | -130.0 |
    +--------+--------+-------+--------+--------+--------+
    |  nan   | 380.0  |  -50  | -220.0 | -110.0 |  nan   |
    +--------+--------+-------+--------+--------+--------+
    |  nan   |  nan   | 55.6  |  0.0   | -45.6  |  -10   |
    +--------+--------+-------+--------+--------+--------+

    """
    fields = [
        {
            "lobby": "1111",
            "playernum": 4,
            "player1": "アカギ",
            "player1ptr": 100.0,
            "player1shuugi": 10,
            "player2": "黒服B",
            "player2ptr": 3.5,
            "player2shuugi": 0,
            "player3": "黒服A",
            "player3ptr": -8.3,
            "player3shuugi": -2,
            "player4": "ワシズ",
            "player4ptr": -88.2,
            "player4shuugi": -8,
            "starttime": datetime(1978, 11, 22),
        },
        {
            "lobby": "1111",
            "playernum": 4,
            "player1": "アカギ",
            "player1ptr": 290.4,
            "player1shuugi": None,
            "player2": "黒服A",
            "player2ptr": 0,
            "player2shuugi": None,
            "player3": "黒服D",
            "player3ptr": -130.0,
            "player3shuugi": None,
            "player4": "黒服B",
            "player4ptr": -160.4,
            "player4shuugi": None,
            "starttime": datetime(1978, 11, 23),
        },
        {
            "lobby": "1111",
            "playernum": 4,
            "player1": "ワシズ",
            "player1ptr": 380,
            "player1shuugi": 140,
            "player2": "黒服A",
            "player2ptr": -50,
            "player2shuugi": -20,
            "player3": "黒服C",
            "player3ptr": -110,
            "player3shuugi": -50,
            "player4": "黒服B",
            "player4ptr": -220,
            "player4shuugi": -70,
            "starttime": datetime(1978, 11, 23),
        },
        {
            "lobby": "1111",
            "playernum": 4,
            "player1": "黒服A",
            "player1ptr": 55.6,
            "player1shuugi": None,
            "player2": "黒服B",
            "player2ptr": 0,
            "player2shuugi": None,
            "player3": "黒服D",
            "player3ptr": -10.0,
            "player3shuugi": None,
            "player4": "黒服C",
            "player4ptr": -45.6,
            "player4shuugi": None,
            "starttime": datetime(1978, 11, 24),
        },
    ]
    return [GameResult(**field) for field in fields]


def test_game_result_to_records_3(game_results_3):
    for result in game_results_3:
        records = result.to_records()
        assert records == [
            models.Record(player_name=result.player1, point=result.player1ptr, tip=result.player1shuugi, rank=1),
            models.Record(player_name=result.player2, point=result.player2ptr, tip=result.player2shuugi, rank=2),
            models.Record(player_name=result.player3, point=result.player3ptr, tip=result.player3shuugi, rank=3),
        ]


def test_game_result_to_records_4(game_results_4):
    for result in game_results_4:
        records = result.to_records()
        assert records == [
            models.Record(player_name=result.player1, point=result.player1ptr, tip=result.player1shuugi, rank=1),
            models.Record(player_name=result.player2, point=result.player2ptr, tip=result.player2shuugi, rank=2),
            models.Record(player_name=result.player3, point=result.player3ptr, tip=result.player3shuugi, rank=3),
            models.Record(player_name=result.player4, point=result.player4ptr, tip=result.player4shuugi, rank=4),
        ]


@pytest.mark.parametrize(
    "log_str,game_result",
    [
        (
            "L1000 | 00:30 | 四般南喰赤－ | A(+45.0) B(+9.0) C(-20.0) D(-34.0)",
            models.GameResult(
                lobby="L1000",
                playernum=4,
                player1="A",
                player1ptr=45.0,
                player1shuugi=None,
                player2="B",
                player2ptr=9.0,
                player2shuugi=None,
                player3="C",
                player3ptr=-20.0,
                player3shuugi=None,
                player4="D",
                player4ptr=-34.0,
                player4shuugi=None,
                starttime=datetime(2020, 1, 1, 0, 30),
            ),
        )
    ],
)
def test_game_result_from_str(log_str, game_result):
    actual = models.GameResult.from_str(log_str, date(2020, 1, 1))
    assert actual == game_result


def test_book_from_results(game_results_3, player_names):
    book = models.ResultBook.from_results(game_results_3, player_names)
    scores = pd.DataFrame(
        [
            [100, -88.2, -11.8, None, None, None, datetime(1978, 11, 22),],
            [290.4, None, None, -160.4, None, -130, datetime(1978, 11, 23),],
            [None, 380.0, None, -220.0, -160.0, None, datetime(1978, 11, 23),],
            [None, None, 45.6, 0.0, -45.6, None, datetime(1978, 11, 24),],
        ],
        columns=player_names + ["starttime"],
    )
    pd.testing.assert_frame_equal(scores, book.scores, check_dtype=False)


@pytest.mark.parametrize(
    "record_str,name,point,tip",
    [
        ("A(+45.0)", "A", 45.0, None),
        ("A(0.0)", "A", 0, None),
        ("A(+45.0,+3枚)", "A", 45.0, 3),
        ("A(+45.0,0枚)", "A", 45.0, 0),
        ("あいうえお(+45.0,+21枚)", "あいうえお", 45.0, 21),
        ("hoge(+1945.8,-20枚)", "hoge", 1945.8, -20),
    ],
)
def test_parse_record_str(record_str, name, point, tip):
    assert models.Record._parse_record_str(record_str) == {"name": name, "point": point, "tip": tip}


@pytest.mark.parametrize(
    "records_str,records",
    [
        (
            "A(+45.0) B(+9.0) C(-20.0) D(-34.0)",
            [
                models.Record(player_name="A", point=45.0, tip=None, rank=1),
                models.Record(player_name="B", point=9.0, tip=None, rank=2),
                models.Record(player_name="C", point=-20.0, tip=None, rank=3),
                models.Record(player_name="D", point=-34.0, tip=None, rank=4),
            ],
        ),
        (
            "B(+9.0) A(+45.0) D(-34.0) C(-20.0)",
            [
                models.Record(player_name="A", point=45.0, tip=None, rank=1),
                models.Record(player_name="B", point=9.0, tip=None, rank=2),
                models.Record(player_name="C", point=-20.0, tip=None, rank=3),
                models.Record(player_name="D", point=-34.0, tip=None, rank=4),
            ],
        ),
        (
            "A(+64.0,+3枚) B(-8.0,-1枚) C(-56.0,-2枚)",
            [
                models.Record(player_name="A", point=64.0, tip=3, rank=1),
                models.Record(player_name="B", point=-8.0, tip=-1, rank=2),
                models.Record(player_name="C", point=-56.0, tip=-2, rank=3),
            ],
        ),
    ],
)
def test_from_str(records_str, records):
    assert models.Record.parse_str(records_str) == records
