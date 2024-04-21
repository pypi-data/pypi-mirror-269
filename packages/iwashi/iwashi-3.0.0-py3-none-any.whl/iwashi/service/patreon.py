from __future__ import annotations
import json
import re
from typing import List, TypedDict

import bs4
from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, Service


class Patreon(Service):
    def __init__(self) -> None:
        super().__init__(
            name="Patreon",
            regex=re.compile(
                HTTP_REGEX + r"patreon\.com/(?P<id>[\w-]+)",
                re.IGNORECASE,
            ),
        )

    async def visit(self, context: Context, id: str):
        url = f"https://www.patreon.com/{id}"
        res = await context.session.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        # <script type="application/ld+json">
        data_element = soup.select_one("script[type='application/ld+json']")
        if data_element is None:
            raise Exception("Could not find ld+json")
        data_root: Root = json.loads(data_element.text)

        context.create_result(
            self,
            id=id,
            url=url,
            name=data_root["author"]["name"],
            description=data_root["about"]["description"],
            profile_picture=data_root["author"]["image"]["contentUrl"],
        )

        for link in data_root["sameAs"]:
            context.enqueue_visit(link)


class Image(TypedDict):
    contentUrl: str
    thumbnailUrl: str


class Author(TypedDict):
    name: str
    image: Image


class About(TypedDict):
    description: str


class Primaryimageofpage(TypedDict):
    representativeOfPage: bool
    contentUrl: str
    thumbnailUrl: str


class Root(TypedDict):
    author: Author
    about: About
    primaryImageOfPage: Primaryimageofpage
    datePublished: str
    sameAs: List[str]
