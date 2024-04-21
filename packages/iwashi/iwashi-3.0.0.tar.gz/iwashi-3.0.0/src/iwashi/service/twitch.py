import re
from typing import List, TypedDict

from loguru import logger

from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, Service


class Twitch(Service):
    def __init__(self) -> None:
        super().__init__(
            name="Twitch",
            regex=re.compile(HTTP_REGEX + r"twitch\.tv/(?P<id>\w+)", re.IGNORECASE),
        )

    async def visit(self, context: Context, id: str):
        url = f"https://www.twitch.tv/{id}"
        res = await context.session.get(url)
        res.raise_for_status()
        match = re.search(
            r'clientId ?= ?"(?P<token>kimne78kx3ncx6brgo4mv6wki5h1ko)"',
            await res.text(),
        )
        if match is None:
            logger.warning(f"[Twitch] Could not find token for {url}")
            return
        token = match.group("token")

        res = await context.session.post(
            "https://gql.twitch.tv/gql",
            json=[
                {
                    "operationName": "ChannelRoot_AboutPanel",
                    "variables": {"channelLogin": id, "skipSchedule": True},
                    "extensions": {
                        "persistedQuery": {
                            "version": 1,
                            "sha256Hash": "6089531acef6c09ece01b440c41978f4c8dc60cb4fa0124c9a9d3f896709b6c6",
                        }
                    },
                }
            ],
            headers={
                "Client-Id": token,
            },
        )
        res.raise_for_status()
        info: Root = await res.json()
        user = info[0]["data"]["user"]
        if user is None:
            logger.warning(f"[Twitch] Could not find user for {url}")
            return
        context.create_result(
            self,
            id=id,
            url=url,
            name=user["displayName"],
            description=user["description"],
            profile_picture=user["profileImageURL"],
        )

        for link in user["channel"]["socialMedias"]:
            context.enqueue_visit(link["url"])


class Followers(TypedDict):
    totalCount: int
    __typename: str


class SocialMediasItem0(TypedDict):
    id: str
    name: str
    title: str
    url: str
    __typename: str


class Channel(TypedDict):
    id: str
    socialMedias: List[SocialMediasItem0]
    __typename: str


class LastBroadcast(TypedDict):
    id: str
    game: None
    __typename: str


class Videos(TypedDict):
    edges: List
    __typename: str


class User(TypedDict):
    id: str
    description: str
    displayName: str
    isPartner: bool
    primaryColorHex: str
    profileImageURL: str
    followers: Followers
    channel: Channel
    lastBroadcast: LastBroadcast
    primaryTeam: None
    videos: Videos
    __typename: str


class Data(TypedDict):
    currentUser: None
    user: User


class Extensions(TypedDict):
    durationMilliseconds: int
    operationName: str
    requestID: str


class RootItem0(TypedDict):
    data: Data
    extensions: Extensions


Root = List[RootItem0]
