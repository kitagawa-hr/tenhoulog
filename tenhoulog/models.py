from dataclasses import dataclass
from datetime import datetime, tzinfo
from typing import List, Set, Tuple, Optional

import japanize_matplotlib  # noqa
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from pydantic import BaseModel


class GameResult(BaseModel):
    """1試合の結果

    nodocchi.moeのAPI形式に準拠
    datetimeはUTCとなっているので注意
    """

    lobby: str  # 個室ID
    player1: str  # 1位のプレイヤーの名前
    player1ptr: float  # 1位のプレイヤーの得点
    player1shuugi: Optional[int]  # 1位のプレイヤーの祝儀
    player2: str
    player2ptr: float
    player2shuugi: Optional[int]
    player3: str
    player3ptr: float
    player3shuugi: Optional[int]
    starttime: datetime  # 開始時刻(UTC)

    def to_records(self) -> List["Record"]:
        rank_to_attrs = [(1, "player1"), (2, "player2"), (3, "player3")]
        return [
            Record(
                player_name=getattr(self, attr),
                point=getattr(self, attr + "ptr"),
                tip=getattr(self, attr + "shuugi"),
                rank=rank,
            )
            for (rank, attr) in rank_to_attrs
        ]


class APIResponse(BaseModel):
    """nodocchi.moeのAPIレスポンス"""

    earliest: datetime  # 最も古い対戦の開戦時刻(UTC)
    lobby: str  # 個室ID
    list: List[GameResult]


class Record(BaseModel):
    """プレイヤーの1試合分の成績"""

    player_name: str  # 名前
    point: float  # 得点
    tip: Optional[int]  # 祝儀
    rank: int  # 順位


@dataclass
class ResultBook:
    """複数試合の結果をまとめた帳簿"""

    scores: pd.DataFrame  # 得点
    ranks: pd.DataFrame  # 順位
    tips: pd.DataFrame  # 祝儀

    @property
    def player_names(self) -> Set[str]:
        return set(self.scores.columns) - {"starttime"}

    def __add__(self, other: "ResultBook") -> "ResultBook":
        """他のBookとの結合"""
        columns = self.player_names.union(other.player_names).union({"starttime"})
        base_df = pd.DataFrame([], columns=columns)
        return ResultBook(
            pd.concat([base_df, self.scores, other.scores]),
            pd.concat([base_df, self.ranks, other.ranks]),
            pd.concat([base_df, self.tips, other.tips]),
        )

    @classmethod
    def _filter_df_by_period(cls, df: pd.DataFrame, time_period: Tuple[datetime, datetime]) -> pd.DataFrame:
        return df[(time_period[0] <= df["starttime"]) & (df["starttime"] < time_period[1])]

    def filter_by_period(self, time_period: Tuple[datetime, datetime]) -> "ResultBook":
        """指定した期間内の結果にフィルタする"""
        return ResultBook(
            self._filter_df_by_period(self.scores, time_period),
            self._filter_df_by_period(self.ranks, time_period),
            self._filter_df_by_period(self.tips, time_period),
        )

    def aggregate(self) -> pd.DataFrame:
        """集計結果をテーブルオブジェクトとして返す"""
        rows = []
        for player in self.player_names:
            score_sum = self.scores[player].sum()
            times = self.scores[player].notnull().sum()
            rank_counts = self.ranks[player].value_counts().to_dict()
            ranks = [rank_counts.get(rank, 0) for rank in (1, 2, 3)]
            rank_avg = self.ranks[player].mean()
            tip = int(self.tips[player].sum())
            rows.append([player, times, score_sum, "-".join(map(str, ranks)), rank_avg, tip])
        return pd.DataFrame(rows, columns=["名前", "回数", "得点", "順位分布", "平均順位", "祝儀"])

    def plot_cumsum(self, attr: str = "scores") -> Figure:
        """得点または祝儀の推移を可視化

        Args:
            - attr (str): ``scores`` or ``tips``を選択. Default to ``scores``.
        """
        target_df: pd.DataFrame = getattr(self, attr)
        fig, ax = plt.subplots()
        shifted_cumsum = target_df[self.player_names].apply(lambda x: pd.Series(x.dropna().values)).cumsum()
        shifted_cumsum.plot(ax=ax)
        ax.set_title("得点推移")
        ax.legend(loc="upper left")
        return fig


def results2book(results: List[GameResult], player_names: List[str], tz: tzinfo) -> ResultBook:
    """試合結果をDataFrameに変換

    player_namesで指定したプレイヤーの結果だけが対象
    (scoreを表すdf, rankを表すdf)を返す
    """
    scores = []
    ranks = []
    tips = []
    columns = player_names + ["starttime"]
    for result in results:
        starttime = result.starttime.astimezone(tz)
        records = result.to_records()
        score = dict({record.player_name: record.point for record in records}, starttime=starttime)
        rank = dict({record.player_name: record.rank for record in records}, starttime=starttime)
        tip = dict({record.player_name: record.tip for record in records}, starttime=starttime)
        scores.append(score)
        ranks.append(rank)
        tips.append(tip)
    return ResultBook(
        pd.DataFrame(scores, columns=columns),
        pd.DataFrame(ranks, columns=columns),
        pd.DataFrame(tips, columns=columns),
    )
