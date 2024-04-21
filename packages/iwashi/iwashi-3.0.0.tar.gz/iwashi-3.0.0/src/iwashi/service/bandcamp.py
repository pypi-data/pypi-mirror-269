from __future__ import annotations

import json
import re
from typing import List, TypedDict

import bs4

from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, Service

DATA_REGEX = r"preloadLink\s?=\s(?P<json>{[^;]+)"


class Bandcamp(Service):
    def __init__(self):
        super().__init__(
            name="Bandcamp",
            regex=re.compile(
                HTTP_REGEX + r"(?P<id>[\w-]+)?\.bandcamp\.com", re.IGNORECASE
            ),
        )

    async def visit(self, context: Context, id: str) -> None:
        url = f"https://{id}.bandcamp.com"
        res = await context.session.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        script = soup.select_one("script[data-band]")
        if script is None:
            raise Exception("No script found")

        data: Root = json.loads(script.attrs["data-band"])
        description_element = soup.select_one(".signed-out-artists-bio-text")
        profile_picture_element = soup.select_one(".band-photo")
        context.create_result(
            self,
            id=id,
            url=url,
            name=data["name"],
            description=description_element.text.strip()
            if description_element
            else None,
            profile_picture=profile_picture_element.attrs["src"]
            if profile_picture_element
            else None,
        )

        for site in data["sites"]:
            context.enqueue_visit(site["url"])


class Site(TypedDict):
    url: str
    title: str


class Root(TypedDict):
    sites: List[Site]
    name: str
