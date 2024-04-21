from __future__ import annotations

import json
import re
from typing import List, TypedDict

import bs4

from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, Service


class Note(Service):
    def __init__(self):
        super().__init__(
            name="Note",
            regex=re.compile(HTTP_REGEX + r"note\.com/(?P<id>[^/]+)", re.IGNORECASE),
        )

    async def visit(self, context: Context, id: str):
        url = f"https://note.com/{id}"
        res = await context.session.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")

        data_element = soup.select_one("script[type='application/ld+json']")
        if data_element is None:
            return
        data_root: Root = json.loads(data_element.text)
        if len(data_root) != 1:
            raise Exception("Root element is not unique")
        data = data_root[0]["mainEntity"]

        context.create_result(
            self,
            id=id,
            url=url,
            name=data["name"],
            description=data["description"],
            profile_picture=data["image"]["url"],
        )

        links: set[str] = set()
        for element in soup.select(".m-creatorSocialLinks__item"):
            link = element.select_one("a")
            if link is None:
                continue
            if "href" not in link.attrs:
                continue
            links.add(link.attrs["href"])
        for link in links:
            context.enqueue_visit(link)


Image = TypedDict(
    "Image", {"@type": "str", "url": "str", "width": "int", "height": "int"}
)
Mainentity = TypedDict(
    "Mainentity",
    {
        "@type": "str",
        "name": "str",
        "url": "str",
        "image": "Image",
        "description": "str",
    },
)
RootItem = TypedDict(
    "RootItem",
    {
        "@context": "str",
        "@type": "str",
        "dateCreated": "str",
        "mainEntity": "Mainentity",
    },
)
Root = List[RootItem]
