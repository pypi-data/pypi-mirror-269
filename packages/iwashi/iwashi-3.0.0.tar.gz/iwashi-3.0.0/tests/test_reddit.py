import pytest
from iwashi.service.reddit import Reddit
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_reddit():
    service = Reddit()
    correct = Result(
        service=service,
        id="MarcusFaze",
        url="https://www.reddit.com/user/MarcusFaze",
        name="MarcusFaze",
        description="I’m 18, I’m a Wrestling Fan,I’m from North Carolina",
        profile_picture="https://styles.redditmedia.com/t5_25b6em/styles/profileIcon_ym46r18i589b1.jpg?width=256&amp;height=256&amp;crop=256:256,smart&amp;s=7b7e1b4c208f847f36de445ebd5b8f0c32657071",
        links={"https://twitter.com/marcus_faze"},
    )
    await _test_service(service, correct, "https://www.reddit.com/user/MarcusFaze")
