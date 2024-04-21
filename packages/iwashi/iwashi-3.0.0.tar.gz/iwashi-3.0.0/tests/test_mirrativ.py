import pytest
from iwashi.service.mirrativ import Mirrativ
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_mirrativ():
    service = Mirrativ()
    correct = Result(
        service=service,
        id="495308",
        url="https://www.mirrativ.com/user/495308",
        name="ごはんちゃんねる",
        description="YouTubeでゲーム実況やプラモ制作をしています！",
        profile_picture="https://cdn.mirrativ.com/mirrorman-prod/image/profile_image/c9780b3765e11280b17cc0a9c1f2138d32af7e27295beae3a4f1c23304d4f3e4_m.jpeg?1697778608",
        links={"https://www.youtube.com/channel/UCyA5Im3h7KNmq02ccT0KhiQ"},
    )
    await _test_service(service, correct, "https://www.mirrativ.com/user/495308")
