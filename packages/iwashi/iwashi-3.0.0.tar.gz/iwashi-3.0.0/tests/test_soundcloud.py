import pytest
from iwashi.service.soundcloud import Soundcloud
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_soundcloud():
    service = Soundcloud()
    correct = Result(
        service=service,
        id="speder2",
        url="https://soundcloud.com/speder2",
        name="Speder2",
        description="ゲーム製作サークルの音楽・SEを担当しています",
        profile_picture="https://i1.sndcdn.com/avatars-000125467778-jpowym-large.jpg",
        links={
            "http://kohada.ushimairi.com/",
        },
    )
    await _test_service(
        service,
        correct,
        "https://soundcloud.com/speder2",
        "https://soundcloud.com/speder2/tracks",
    )
