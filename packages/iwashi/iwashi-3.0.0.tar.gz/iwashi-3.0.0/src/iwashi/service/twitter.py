import json
import re
from typing import List, TypedDict

from loguru import logger

from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, Service


class Twitter(Service):
    def __init__(self) -> None:
        super().__init__(
            name="Twitter",
            regex=re.compile(
                HTTP_REGEX + r"(twitter|x)\.com/(#!/)?@?(?P<id>\w+)", re.IGNORECASE
            ),
        )
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ja",
        }
        self.bearer_token: str | None = None
        self.guest_token: str | None = None

    async def fetch_authorization(self, context: Context) -> str:
        if self.bearer_token:
            return self.bearer_token
        res = await context.session.get(
            "https://abs.twimg.com/responsive-web/client-web/main.28fc48ca.js"
        )
        res.raise_for_status()
        match = re.search('(AAAAA.*?)"', await res.text())
        assert match
        bearer_token = "Bearer " + match.group(1)
        self.bearer_token = bearer_token
        return bearer_token

    async def fetch_guest_token(self, context: Context) -> str:
        if self.guest_token:
            return self.guest_token
        res = await context.session.post(
            "https://api.twitter.com/1.1/guest/activate.json",
            headers=self.headers,
        )
        res.raise_for_status()
        data = await res.json()
        self.guest_token = data["guest_token"]
        return data["guest_token"]

    async def setup_headers(self, context: Context) -> None:
        self.headers["authorization"] = await self.fetch_authorization(context)
        self.headers["x-guest-token"] = await self.fetch_guest_token(context)

    async def visit(self, context: Context, id: str) -> None:
        url = f"https://twitter.com/{id}"
        await self.setup_headers(context)

        res = await context.session.get(
            "https://api.twitter.com/graphql/rePnxwe9LZ51nQ7Sn_xN_A/UserByScreenName",
            params={
                "variables": json.dumps(
                    {
                        "screen_name": id,
                        "withSafetyModeUserFields": True,
                        "withSuperFollowsUserFields": True,
                    }
                ),
                "features": json.dumps(
                    {
                        "responsive_web_twitter_blue_verified_badge_is_enabled": True,
                        "responsive_web_graphql_exclude_directive_enabled": True,
                        "verified_phone_label_enabled": False,
                        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                        "responsive_web_graphql_timeline_navigation_enabled": True,
                    }
                ),
            },
            headers=self.headers,
        )
        res.raise_for_status()
        info: Root = await res.json()
        if not info["data"]:
            logger.warning(f"[Twitter] Could not find data for {url}")
            return
        result = info["data"]["user"]["result"]
        if result["__typename"] == "UserUnavailable":
            context.create_result(
                self,
                id=id,
                url=url,
                name="<UserUnavailable>",
            )
            return

        data = result["legacy"]
        context.create_result(
            self,
            id=id,
            url=url,
            name=data["name"],
            description=data["description"],
            profile_picture=data["profile_image_url_https"],
        )

        if "url" not in data["entities"]:
            return

        for link in data["entities"]["url"]["urls"]:
            context.enqueue_visit(link["expanded_url"])

        for link in data["entities"]["description"]["urls"]:
            context.enqueue_visit(link["expanded_url"])


class LocationsItem0(TypedDict):
    line: int
    column: int


class Tracing(TypedDict):
    trace_id: str


class Extensions(TypedDict):
    name: str
    source: str
    code: int
    kind: str
    tracing: Tracing


class ErrorsItem0(TypedDict):
    message: str
    locations: List[LocationsItem0]
    path: List[str]
    extensions: Extensions
    code: int
    kind: str
    name: str
    source: str
    tracing: Tracing


class AffiliatesHighlightedLabel(TypedDict):
    pass


class UrlsItem0(TypedDict):
    display_url: str
    expanded_url: str
    url: str
    indices: List[int]


class Description(TypedDict):
    urls: List[UrlsItem0]


class Entities(TypedDict):
    description: Description
    url: Description


class Rgb(TypedDict):
    blue: int
    green: int
    red: int


class PaletteItem0(TypedDict):
    percentage: float
    rgb: Rgb


class Ok(TypedDict):
    palette: List[PaletteItem0]


class R(TypedDict):
    ok: Ok


class MediaColor(TypedDict):
    r: R


class ProfileBannerExtensions(TypedDict):
    mediaColor: MediaColor


class Legacy(TypedDict):
    created_at: str
    default_profile: bool
    default_profile_image: bool
    description: str
    entities: Entities
    fast_followers_count: int
    favourites_count: int
    followers_count: int
    friends_count: int
    has_custom_timelines: bool
    is_translator: bool
    listed_count: int
    location: str
    media_count: int
    name: str
    normal_followers_count: int
    pinned_tweet_ids_str: List[str]
    possibly_sensitive: bool
    profile_banner_extensions: ProfileBannerExtensions
    profile_banner_url: str
    profile_image_extensions: ProfileBannerExtensions
    profile_image_url_https: str
    profile_interstitial_type: str
    screen_name: str
    statuses_count: int
    translator_type: str
    url: str
    verified: bool
    withheld_in_countries: List


class Result(TypedDict):
    __typename: str
    id: str
    rest_id: str
    affiliates_highlighted_label: AffiliatesHighlightedLabel
    is_blue_verified: bool
    legacy: Legacy
    business_account: AffiliatesHighlightedLabel
    legacy_extended_profile: AffiliatesHighlightedLabel
    is_profile_translatable: bool
    verification_info: AffiliatesHighlightedLabel


class User(TypedDict):
    result: Result


class Data(TypedDict):
    user: User


class Root(TypedDict):
    errors: List[ErrorsItem0]
    data: Data
