import re

import bs4

from iwashi.helper import HTTP_REGEX, normalize_url
from iwashi.visitor import Context, Service


class Booth(Service):
    def __init__(self) -> None:
        super().__init__(
            name="Booth",
            regex=re.compile(HTTP_REGEX + r"(?P<id>[\w-]+)\.booth\.pm", re.IGNORECASE),
        )

    async def visit(self, context: Context, id: str) -> None:
        url = f"https://{id}.booth.pm"
        res = await context.session.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        name_element = soup.select_one(".shop-name")
        name = name_element.text if name_element is not None else None
        desc_element = soup.select_one(".booth-description .autolink")
        description = desc_element.text if desc_element is not None else None
        avater_element = soup.select_one(".avatar-image")

        context.create_result(
            self,
            id=id,
            url=url,
            name=name,
            description=description,
            profile_picture=avater_element.attrs["style"].split("url(")[1].split(")")[0]
            if avater_element is not None
            else None,
        )

        if desc_element is None:
            return
        for link in soup.select(".booth-description a"):
            if "href" not in link.attrs:
                continue
            normalized_url = normalize_url(link.attrs["href"])
            if normalized_url is None:
                continue
            context.enqueue_visit(normalized_url)
