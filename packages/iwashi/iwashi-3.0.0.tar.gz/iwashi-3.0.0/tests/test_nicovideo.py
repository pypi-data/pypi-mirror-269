import pytest
from iwashi.service.nicovideo import Nicovideo
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_nicovideo():
    service = Nicovideo()
    correct = Result(
        service=service,
        id="128134532",
        url="https://www.nicovideo.jp/user/128134532",
        name="ラベンダーP",
        description="鉄道、東方、艦これ、ボカロ、ボイロ、野球、応援歌、阪神タイガース、千葉ロッテマリーンズ、埼玉西武ライオンズ、オリックスバファローズ、東方のすくすく白沢、艦これの連装砲ちゃんが好きな人です<br><br>2006年4月17日生まれで岡山県備前市日生町(カキオコで有名な町)に住んでます",
        profile_picture="https://secure-dcdn.cdn.nimg.jp/nicoaccount/usericon/12813/128134532.jpg?1710066983",
        links={
            "https://www.youtube.com/channel/UC4jehnRY1GBPBpg-Np4WFNg",
            "https://twitter.com/lavenderp2018",
        },
    )
    await _test_service(service, correct, "https://www.nicovideo.jp/user/128134532")
