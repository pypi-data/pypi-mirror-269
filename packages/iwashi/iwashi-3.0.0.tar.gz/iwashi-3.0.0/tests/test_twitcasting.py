import pytest
from iwashi.service.twitcasting import TwitCasting
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_twitcasting():
    service = TwitCasting()
    correct = Result(
        service=service,
        id="kaizi0817",
        url="https://twitcasting.tv/kaizi0817",
        name="細貝直心",
        description="細貝直心 / 1996年8月17日24歳/2021年2月〜メンズスキンケアD2Cブランド@serra_adsonをリリース中‼︎/若い人達が挑戦するきっかけを作りたい/フォローお願いします/tiktokも始めました！",
        profile_picture="https://imagegw02.twitcasting.tv/image3s/pbs.twimg.com/profile_images/1412219689615302662/Gxz3711a_bigger.jpg",
        links={"https://twitter.com/kaizi0817"},
    )
    await _test_service(
        service,
        correct,
        "https://twitcasting.tv/kaizi0817",
        "https://twitcasting.tv/kaizi0817/archive/",
    )
