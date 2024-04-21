from __future__ import annotations
import re

import bs4


from iwashi.helper import HTTP_REGEX, traverse
from iwashi.visitor import Context, Service


class Kofi(Service):
    def __init__(self) -> None:
        super().__init__(
            name="Ko-fi",
            regex=re.compile(
                HTTP_REGEX + r"ko-fi\.com/(?P<id>[\w-]+)",
                re.IGNORECASE,
            ),
        )

    async def visit(self, context: Context, id: str):
        url = f"https://ko-fi.com/{id}"
        res = await context.session.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        name = (
            traverse(soup.select_one(".mob-profile-name"))
            .map(lambda x: x.text)
            .map(str.strip)
            .get()
        )
        avatar = (
            traverse(soup.select_one("#profilePicture2"))
            .map(lambda x: x.attrs.get("src"))
            .map(str)
            .get()
        )
        social_links = soup.select(".social-link a")

        context.create_result(
            self,
            id=id,
            url=url,
            name=name,
            profile_picture=avatar,
        )

        for link in social_links:
            href = link.attrs.get("href")
            if href is None:
                continue
            context.enqueue_visit(href)
