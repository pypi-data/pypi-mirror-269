import pytest
from iwashi.visitor import Result
from iwashi.service.fanbox import Fanbox
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_fanbox():
    service = Fanbox()
    correct = Result(
        service=service,
        id="masahiro-emotion",
        url="https://masahiro-emotion.fanbox.cc",
        name="Masahiro Emoto",
        description="English text is shown below\r\n\r\n私はアニメーション監督、キャラクターデザイナー、作画監督、イラスレーター、ロボットのビヘイビアデザインなど活動しているクリエイターです。\r\n参加作品は\r\n・攻殻機動隊\r\n・カウボーイビバップ\r\n・Animatrix\r\n・REDLINE\r\n・BLEACH\r\n\r\nなど様々なプロジェクトに参加してました。\r\n\r\nI am a creator involved in various roles such as animation director, character designer, animation supervisor, illustrator, and robot behavior design.\r\nI have contributed to projects such as Ghost in the Shell, Cowboy Bebop, Animatrix, REDLINE, BLEACH, and many others.",
        profile_picture="https://pixiv.pximg.net/c/160x160_90_a2_g5/fanbox/public/images/user/91970939/icon/aAE8bJoSKtAtHhWK17NUmMFI.jpeg",
        links={"https://x.com/masahiroemotion/"},
    )
    await _test_service(
        service,
        correct,
        "https://masahiro-emotion.fanbox.cc/",
        "https://masahiro-emotion.fanbox.cc/posts/7382756",
    )
