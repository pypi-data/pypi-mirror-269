import re
from typing import List, TypedDict

from loguru import logger

from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, Service


class Instagram(Service):
    def __init__(self) -> None:
        super().__init__(
            name="Instagram",
            regex=re.compile(HTTP_REGEX + r"instagram\.com/(?P<id>\w+)", re.IGNORECASE),
        )

    async def visit(self, context: Context, id: str):
        url = f"https://www.instagram.com/{id}"
        res = await context.session.get(url)
        res.raise_for_status()
        match = re.search(r"\"X-IG-App-ID\": ?\"(?P<id>\d{15})\"", await res.text())
        if match is None:
            raise Exception(f"[Instagram] No X-IG-App-ID found in {url}")
        context.session.headers["x-ig-app-id"] = match.group("id")

        info_res = await context.session.get(
            f"https://www.instagram.com/api/v1/users/web_profile_info/?username={id}",
        )
        info_res.raise_for_status()
        if info_res.status // 100 != 2 or info_res.history:
            logger.warning("[Instagram] Blocked by Instagram")
            context.create_result(
                self,
                id=id,
                url=url,
                name=id,
                description="Blocked by Instagram",
            )
            return
        info: Root = await info_res.json()
        user = info["data"]["user"]
        context.create_result(
            self,
            id=id,
            url=url,
            name=user["full_name"],
            profile_picture=user["profile_pic_url"],
            description=user["biography"],
        )

        for link in user["bio_links"]:
            context.enqueue_visit(link["url"])


class FriendshipStatus(TypedDict):
    following: bool
    blocking: bool
    is_bestie: bool
    is_feed_favorite: bool
    is_restricted: bool
    muting: bool
    is_muting_reel: bool
    outgoing_request: bool
    followed_by: bool
    incoming_request: bool


class HdProfilePicUrlInfo(TypedDict):
    url: str


class BiographyWithEntities(TypedDict):
    entities: List


class BioLinksItem(TypedDict):
    link_type: str
    lynx_url: str
    title: str
    url: str


class User(TypedDict):
    friendship_status: FriendshipStatus
    full_name: str
    gating: None
    is_memorialized: bool
    is_private: bool
    has_story_archive: None
    username: str
    is_regulated_c18: bool
    regulated_news_in_locations: List
    text_post_app_badge_label: str
    show_text_post_app_badge: bool
    eligible_for_text_app_activation_badge: bool
    hide_text_app_activation_badge_on_text_app: bool
    pk: str
    live_broadcast_visibility: None
    live_broadcast_id: None
    profile_pic_url: str
    hd_profile_pic_url_info: HdProfilePicUrlInfo
    is_unpublished: bool
    mutual_followers_count: int
    profile_context_links_with_user_ids: List
    biography_with_entities: BiographyWithEntities
    account_badges: List
    bio_links: List[BioLinksItem]
    external_lynx_url: str
    external_url: str
    ai_agent_type: None
    has_chaining: bool
    fbid_v2: str
    supervision_info: None
    interop_messaging_user_fbid: str
    account_type: int
    biography: str
    is_embeds_disabled: bool
    show_account_transparency_details: bool
    is_verified: bool
    is_professional_account: None
    follower_count: int
    address_street: str
    city_name: str
    is_business: bool
    zip: str
    category: str
    should_show_category: bool
    pronouns: List
    transparency_label: None
    transparency_product: None
    following_count: int
    media_count: int
    latest_reel_media: int
    total_clips_count: int
    latest_besties_reel_media: int
    reel_media_seen_timestamp: int
    id: str


class User0(TypedDict):
    pk: str
    id: str
    can_see_organic_insights: bool
    has_onboarded_to_text_post_app: bool


class Viewer(TypedDict):
    user: User0


class Data(TypedDict):
    user: User
    viewer: Viewer


class Extensions(TypedDict):
    is_final: bool


class Root(TypedDict):
    data: Data
    extensions: Extensions
