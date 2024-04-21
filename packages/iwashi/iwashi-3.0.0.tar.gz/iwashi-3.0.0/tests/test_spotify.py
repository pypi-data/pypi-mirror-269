import pytest
from iwashi.service.spotify import Spotify
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_spotify():
    service = Spotify()
    correct = Result(
        service=service,
        id="0CLW5934vy2XusynS1px1S",
        url="https://open.spotify.com/artist/0CLW5934vy2XusynS1px1S",
        name="Flyana Boss",
        description="Two besties, one duo! Reporting to you live from LA.\nTEXT US (310) 742-0879 &#x1f643;",
        profile_picture="https://i.scdn.co/image/ab6761610000e5ebcd0271f5501c3e4064d0f6ec",
        links={
            "https://facebook.com/Flyanaboss-1100179700191258",
            "https://instagram.com/flyanaboss",
        },
    )
    await _test_service(
        service,
        correct,
        "https://open.spotify.com/artist/0CLW5934vy2XusynS1px1S",
        "https://open.spotify.com/intl-ja/artist/0CLW5934vy2XusynS1px1S",
    )
