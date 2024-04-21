import pytest
from iwashi.visitor import Result
from iwashi.service.booth import Booth
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_booth():
    service = Booth()
    correct = Result(
        service=service,
        id="miluda",
        url="https://miluda.booth.pm",
        name="Sunshine Mill 太陽光工場",
        description="Welcome to 太陽光工場.\r\nMiludaと申します。同人初心者アメリカ人ですけどどうぞよろしくお願いします。メインは東方や艦これです。\r\n\r\nよろしくお願いします！",
        profile_picture="https://booth.pximg.net/c/128x128/users/274/icon_image/41f84dbd-19af-49b9-8cf5-888eb389e500_base_resized.jpg",
        links={
            "https://miluda.com",
            "https://twitter.com/Miluda",
            "https://www.pixiv.net/users/161480",
        },
    )
    await _test_service(
        service,
        correct,
        "https://miluda.booth.pm/",
        "https://miluda.booth.pm/items/397",
    )
