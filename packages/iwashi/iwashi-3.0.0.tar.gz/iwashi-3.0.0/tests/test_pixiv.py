import pytest
from iwashi.service.pixiv import Pixiv
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_pixiv():
    service = Pixiv()
    correct = Result(
        service=service,
        id="137796",
        url="https://www.pixiv.net/users/137796",
        name="画力欠乏症／妄想屋（仮名）",
        description="属性はロボ娘系。『日常』とか『らき☆すた』、『えす☆えふ』（らき☆すた二次創作）、『けものフレンズ』とかやってます。よろしくお願いします。\r\n\r\nメインのＨＮの略称は、「がけつ」または「ＧＫ２」。\r\nなお、状況？によってＨＮを変えてますが、なんとゆーか、けじめのようなものです(ぉ\r\nコメント、評価等大歓迎でございます。お気軽にお声がけください（￣▽￣)ノ\r\n\r\nマイピクにつきましては、作品を投稿されている方に限らせていただいております。悪しからずご了承ください。\r\n（その代わりといってはなんですが、マイピク限定での投稿はしておりません）\r\n\r\n※オリキャラ(二次創作含む)については、基本的に『描いてもいいのよ』、というか『描いてほしいのよ』ということでお願いします。\r\n※なお、拙作の無断転載および改変はご遠慮ください。",
        profile_picture="https://i.pximg.net/user-profile/img/2014/08/13/23/24/44/8259429_6f34e70e29290fdb5f0f8a66bc429203_170.jpg",
        links={
            "http://www.lares.dti.ne.jp/~gaketsu",
            "https://pawoo.net/oauth_authentications/137796?provider=pixiv",
            "https://sketch.pixiv.net/@gaketsu_gk2",
            "https://twitter.com/gaketsu_gk2",
        },
    )
    await _test_service(service, correct, "https://www.pixiv.net/users/137796")
