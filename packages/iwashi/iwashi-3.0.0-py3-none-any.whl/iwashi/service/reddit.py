from __future__ import annotations

import json
import re
from typing import List, TypedDict

import bs4

from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, Service


class Reddit(Service):
    def __init__(self):
        super().__init__(
            name="Reddit",
            regex=re.compile(
                HTTP_REGEX + r"reddit\.com/user/(?P<id>[\w-]+)", re.IGNORECASE
            ),
        )

    async def visit(self, context: Context, id: str):
        url = f"https://www.reddit.com/user/{id}"
        res = await context.session.get(f"https://www.reddit.com/user/{id}/about.json")
        res.raise_for_status()
        info: Root = await res.json()

        context.create_result(
            self,
            id=id,
            url=url,
            name=info["data"]["name"],
            description=info["data"]["subreddit"]["public_description"],
            profile_picture=info["data"]["icon_img"],
        )

        res = await context.session.get(f"https://www.reddit.com/user/{id}/")
        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        # noun="social_link"
        for element in soup.select('[noun="social_link"]'):
            data: SocialLink = json.loads(
                element.attrs["data-faceplate-tracking-context"]
            )
            context.enqueue_visit(data["social_link"]["url"])


class Subreddit(TypedDict):
    default_set: bool
    user_is_contributor: None
    banner_img: str
    allowed_media_in_comments: List
    user_is_banned: None
    free_form_reports: bool
    community_icon: None
    show_media: bool
    icon_color: str
    user_is_muted: None
    display_name: str
    header_img: None
    title: str
    previous_names: List
    over_18: bool
    icon_size: List[int]
    primary_color: str
    icon_img: str
    description: str
    submit_link_label: str
    header_size: None
    restrict_posting: bool
    restrict_commenting: bool
    subscribers: int
    submit_text_label: str
    is_default_icon: bool
    link_flair_position: str
    display_name_prefixed: str
    key_color: str
    name: str
    is_default_banner: bool
    url: str
    quarantine: bool
    banner_size: None
    user_is_moderator: None
    accept_followers: bool
    public_description: str
    link_flair_enabled: bool
    disable_contributor_requests: bool
    subreddit_type: str
    user_is_subscriber: None


class Data(TypedDict):
    is_employee: bool
    is_friend: bool
    subreddit: Subreddit
    snoovatar_size: None
    awardee_karma: int
    id: str
    verified: bool
    is_gold: bool
    is_mod: bool
    awarder_karma: int
    has_verified_email: bool
    icon_img: str
    hide_from_robots: bool
    link_karma: int
    is_blocked: bool
    total_karma: int
    pref_show_snoovatar: bool
    name: str
    created: int
    created_utc: int
    snoovatar_img: str
    comment_karma: int
    accept_followers: bool
    has_subscribed: bool


class Root(TypedDict):
    kind: str
    data: Data


class SocialLinkData(TypedDict):
    type: str
    url: str
    name: str


class SocialLink(TypedDict):
    social_link: SocialLinkData
