import pytest
from iwashi.service.youtube import Youtube
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_youtube():
    service = Youtube()
    correct = Result(
        service=service,
        id="TomScottGo",
        url="https://www.youtube.com/@TomScottGo",
        name="Tom Scott",
        description="Hi, I'm Tom Scott. These are some of the things I've made and done. They'll probably come back to haunt me in a few years' time.\n\nContact me: https://www.tomscott.com/contact/\n\n• • •\n\nThis channel is a production of Pad 26 Limited, registered in England and Wales, № 11662641.\nRegistered office: Amelia House, Crescent Road, Worthing, West Sussex, BN11 1QR\n(This address is only for legal documents; no other mail will be forwarded.)",
        profile_picture="https://yt3.googleusercontent.com/ytc/AIdro_k8W5CNSqxeITAoBY5JkpW3SVJlWitSOStGnvKYulDn21w=s900-c-k-c0x00ffffff-no-rj",
        links={"https://www.tomscott.com/"},
    )
    await _test_service(
        service,
        correct,
        "https://www.youtube.com/@TomScottGo",
        "https://www.youtube.com/@TomScottGo/community",
        "https://www.youtube.com/c/TomScottGo",
        "https://www.youtube.com/c/TomScottGo/community",
        "https://youtu.be/7DKv5H5Frt0",
        "https://www.youtube.com/watch?v=7DKv5H5Frt0",
    )
