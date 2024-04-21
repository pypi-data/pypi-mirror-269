import pytest
from iwashi.service.litlink import LitLink
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_litlink():
    service = LitLink()
    correct = Result(
        service=service,
        id="leftpory5n",
        url="https://lit.link/leftpory5n",
        name="左ポリ５ン",
        description="ひだりぽりごんと読みます。",
        profile_picture="https://prd.storage.lit.link/images/creators/3f1f9feb-8603-46ff-a038-b2a29021beaa/687f1d68-9516-4e61-b38f-7a4377657687.png",
        links={
            "https://skeb.jp/@leftpory5n",
            "https://twitter.com/leftpory5n",
            "https://giftee.com/u/odenpo",
            "https://odaibako.net/u/leftpory5n",
            "https://www.pixiv.net/users/259841",
        },
    )
    await _test_service(service, correct, "https://lit.link/leftpory5n")
