from __future__ import annotations
import re

import bs4


from iwashi.helper import HTTP_REGEX, traverse
from iwashi.visitor import Context, Service


class Itchio(Service):
    def __init__(self) -> None:
        super().__init__(
            name="itch.io",
            regex=re.compile(
                HTTP_REGEX
                + r"((?P<id_subdomain>[\w-]+)\.itch\.io/|itch\.io/profile/(?P<id_profile>[\w-]+))",
                re.IGNORECASE,
            ),
        )

    async def resolve_id(self, context: Context, url: str) -> str | None:
        match = self.regex.match(url)
        if match is None:
            return None
        return match.group("id_profile") or match.group("id_subdomain")

    async def visit(self, context: Context, id: str):
        url = f"https://{id}.itch.io"
        res = await context.session.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        user_links = soup.select(".link_group a")

        res_profile = await context.session.get(f"https://itch.io/profile/{id}")
        res_profile.raise_for_status()
        soup_profile = bs4.BeautifulSoup(await res_profile.text(), "html.parser")
        # <meta property="og:title" content="Sebastian Lague">
        name_element = soup_profile.select_one('meta[property="og:title"]')
        name = traverse(name_element).map(lambda x: x.attrs.get("content")).get()
        # <div class="avatar" style="background-image: url('https://img.itch.zone/aW1nLzEwODg5MDY5LmpwZw==/80x80%23/rdXwL%2B.jpg')"></div>
        avatar_element = soup_profile.select_one(".avatar")
        avatar = (
            traverse(avatar_element)
            .map(lambda x: x.attrs.get("style"))
            .map(str)
            .map(lambda x: x.split("url('")[1].split("')")[0])
            .get()
        )

        context.create_result(
            self,
            id=id,
            url=url,
            name=name,
            profile_picture=avatar,
        )

        for link in user_links:
            href = link.attrs.get("href")
            if href is None:
                continue
            context.enqueue_visit(href)
