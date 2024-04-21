import pytest
from iwashi.service.instagram import Instagram
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_instagram():
    service = Instagram()
    correct = Result(
        service=service,
        id="ismsx_",
        url="https://www.instagram.com/ismsx_",
        name="いっしん",
        description="Isshin Tanaka\nmotion designer / visual artist",
        profile_picture="https://scontent-nrt1-2.cdninstagram.com/v/t51.2885-19/252132732_925276874749701_2338460024889750642_n.jpg?stp=dst-jpg_s150x150&_nc_ht=scontent-nrt1-2.cdninstagram.com&_nc_cat=109&_nc_ohc=9zhwfo0l1JUAb4kjQ9-&edm=AOQ1c0wBAAAA&ccb=7-5&oh=00_AfDFhH0vtf75VqtZ6MXSNkczWc-WMtJzVm9xxF2rIrbN8Q&oe=66293E40&_nc_sid=8b3546",
        links={"https://ismsx.jp/"},
    )
    await _test_service(service, correct)
