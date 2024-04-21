import pytest
from iwashi.service.sketch import Sketch
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_sketch():
    service = Sketch()
    correct = Result(
        service=service,
        id="par1y",
        url="https://sketch.pixiv.net/@par1y",
        name="Paryi",
        description="お勉強と落書きがメイン\nフォロワーさんとまったり絡みたい\nhttps://twitter.com/par1y\n",
        profile_picture="https://img-sketch.pixiv.net/uploads/user_icon/file/1980676/5116648097160323811.jpg",
        links={"https://twitter.com/par1y", "https://www.pixiv.net/users/par1y"},
    )
    await _test_service(service, correct, "https://sketch.pixiv.net/@par1y")
