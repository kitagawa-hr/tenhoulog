import httpx

from .models import APIResponse


def fetch_lobby_log(lobby_id: str) -> APIResponse:
    """指定したロビーの対戦成績を取得する"""
    API_URL = "https://nodocchi.moe/api/lobby.php"
    resp = httpx.post(API_URL, data={"lobby": lobby_id})
    return APIResponse.parse_raw(resp.text)
