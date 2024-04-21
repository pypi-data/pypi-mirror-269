import re
from typing import List, TypedDict

from loguru import logger

from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, Service


class Fanbox(Service):
    def __init__(self) -> None:
        super().__init__(
            name="Fanbox",
            regex=re.compile(HTTP_REGEX + r"(?P<id>[\w-]+)\.fanbox\.cc", re.IGNORECASE),
        )

    async def visit(self, context: Context, id: str):
        url = f"https://{id}.fanbox.cc"
        creator_res = await context.session.get(
            f"https://api.fanbox.cc/creator.get?creatorId={id}",
            headers={
                "accept": "application/json",
                "origin": f"https://{id}.fanbox.cc",
                "referer": f"https://{id}.fanbox.cc/",
            },
        )
        creator_res.raise_for_status()
        if creator_res.status // 100 == 4:
            logger.warning(f"[Fanbox] Could not find user for {url}")
            return

        info: Root = await creator_res.json()
        if "error" in info:
            logger.warning(f"[Fanbox] Could not find user for {url}")
            return
        context.create_result(
            self,
            id=id,
            url=url,
            name=info["body"]["user"]["name"],
            description=info["body"]["description"],
            profile_picture=info["body"]["user"]["iconUrl"],
        )

        for link in info["body"]["profileLinks"]:
            context.enqueue_visit(link)


class User(TypedDict):
    userId: str
    name: str
    iconUrl: str


class ProfileItemsItem0(TypedDict):
    id: str
    type: str
    imageUrl: str
    thumbnailUrl: str


class Body(TypedDict):
    user: User
    creatorId: str
    description: str
    hasAdultContent: bool
    coverImageUrl: str
    profileLinks: List[str]
    profileItems: List[ProfileItemsItem0]
    isFollowed: bool
    isSupported: bool
    isStopped: bool
    isAcceptingRequest: bool
    hasBoothShop: bool


class Root(TypedDict):
    body: Body
