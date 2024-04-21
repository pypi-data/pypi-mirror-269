from __future__ import annotations
import json

import re
from typing import Dict, List, Literal, TypedDict

import bs4

from iwashi.helper import HTTP_REGEX, BASE_HEADERS
from iwashi.visitor import Context, Service


class Spotify(Service):
    def __init__(self):
        super().__init__(
            name="Spotify",
            regex=re.compile(
                HTTP_REGEX
                + r"(open\.)?spotify\.com\/(intl-[\w]*\/)?artist\/(?P<id>[0-9a-zA-Z]+)",
                re.IGNORECASE,
            ),
        )

    async def extract_access_token(self, soup: bs4.BeautifulSoup) -> str:
        script = soup.select_one("script#session")
        if script is None:
            raise RuntimeError("Token not found")
        data = Session(**json.loads(script.text))
        return data["accessToken"]

    async def visit(self, context: Context, id: str):
        url = f"https://open.spotify.com/artist/{id}"
        response = await context.session.get(url, headers=BASE_HEADERS)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(await response.text(), "html.parser")
        access_token = await self.extract_access_token(soup)

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {access_token}",
            "content-type": "application/json",
        }
        params = {
            "operationName": "queryArtistOverview",
            "variables": json.dumps(
                {
                    "uri": f"spotify:artist:{id}",
                    "locale": "intl-ja",
                    "includePrerelease": True,
                }
            ),
            "extensions": '{"persistedQuery":{"version":1,"sha256Hash":"da986392124383827dc03cbb3d66c1de81225244b6e20f8d78f9f802cc43df6e"}}',
        }
        response = await context.session.get(
            "https://api-partner.spotify.com/pathfinder/v1/query",
            params=params,
            headers=headers | BASE_HEADERS,
        )
        response.raise_for_status()
        data: ArtistResponse = await response.json()
        profile = data["data"]["artistUnion"]["profile"]
        avatar_image = data["data"]["artistUnion"]["visuals"]["avatarImage"]
        if len(avatar_image["sources"]) == 0:
            avatar_url = None
        else:
            avatar_url = sorted(
                avatar_image["sources"], key=lambda x: x["width"] * x["height"]
            )[-1]["url"]

        context.create_result(
            self,
            id=id,
            url=url,
            name=profile["name"],
            description=profile["biography"]["text"],
            profile_picture=avatar_url,
        )

        for link in profile["externalLinks"]["items"]:
            context.enqueue_visit(link["url"])


class Session(TypedDict):
    accessToken: str  # [0-9a-zA-Z-_]{19}-[0-9a-zA-Z-_]{37}-[0-9a-zA-Z-_]{57}
    accessTokenExpirationTimestampMs: int  # Unix timestamp in milliseconds
    isAnonymous: bool  # true
    clientId: str  # [0-9a-f]{32}


class Biography(TypedDict):
    text: str
    title: Literal["AUTOBIOGRAPHY"]


class ExternalLinksItem(TypedDict):
    name: str
    url: str


class ExternalLinks(TypedDict):
    items: List[ExternalLinksItem]


class ImagesItemSource(TypedDict):
    width: int
    height: int
    url: str


class ImagesItem(TypedDict):
    sources: List[ImagesItemSource]


class Images(TypedDict):
    items: List[ImagesItem]


class OwnerV2Data(TypedDict):
    __typename: Literal["User"]
    name: str


class OwnerV2(TypedDict):
    data: OwnerV2Data


class PlaylistsV2ItemData(TypedDict):
    __typename: Literal["Playlist"]
    description: str
    images: Images
    name: str
    ownerV2: OwnerV2
    uri: str


class PlaylistsV2Item(TypedDict):
    data: PlaylistsV2ItemData


class PlaylistsV2(TypedDict):
    items: List[PlaylistsV2Item]


class Profile(TypedDict):
    biography: Biography
    externalLinks: ExternalLinks
    name: str
    pinnedItem: None
    playlistsV2: PlaylistsV2
    verified: bool


class ColorRaw(TypedDict):
    hex: str  # "#[0-9a-f]{6}"


class ExtractedColors(TypedDict):
    colorRaw: ColorRaw


class AvatarImage(ImagesItem):
    extractedColors: ExtractedColors


class Visuals(TypedDict):
    avatarImage: AvatarImage


class ArtistUnion(TypedDict):
    profile: Profile
    visuals: Visuals


class ArtistData(TypedDict):
    artistUnion: ArtistUnion


class ArtistResponse(TypedDict):
    data: ArtistData
    extensions: Dict
