import pytest
from iwashi.service.note import Note
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_note():
    service = Note()
    correct = Result(
        service=service,
        id="pocketpair",
        url="https://note.com/pocketpair",
        name="ポケットペア",
        description="最高のゲームを作っています",
        profile_picture="https://assets.st-note.com/production/uploads/images/127793817/profile_28ad4f05e11a0fc2d9117a7e530bc6bf.jpg?fit=bounds&format=jpeg&quality=85&width=330",
        links={"https://twitter.com/Palworld_JP"},
    )
    await _test_service(service, correct, "https://note.com/pocketpair")
