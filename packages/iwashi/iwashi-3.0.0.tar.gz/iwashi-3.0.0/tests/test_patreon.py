import pytest
from iwashi.service.patreon import Patreon
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_itchio():
    service = Patreon()
    correct = Result(
        service=service,
        id="sebastianlague",
        url="https://www.patreon.com/sebastianlague",
        name="Sebastian Lague",
        description="Hello! I create game development tutorials on a wide range of topics. These videos are all freely available on my youtube channel.If you'd like to support the creation of more content like this, you can set a monthly recurring pledge here. There are some small perks on offer in return for your generosity –– see the sidebar for more info.",
        profile_picture="https://c10.patreonusercontent.com/4/patreon-media/p/campaign/114575/0a25704faa914c03839a205f218d36f6/eyJ3Ijo2MjB9/1.jpg",
        links={
            "https://twitter.com/SebastianLague",
            "https://youtube.com/channel/UCmtyQOKKmrMVaKuRXz02jbQ",
        },
    )
    await _test_service(
        service,
        correct,
        "https://www.patreon.com/sebastianlague",
        "https://www.patreon.com/sebastianlague/about",
    )
