from __future__ import annotations
from typing import TypedDict, List
import asyncio
import time
import re

from loguru import logger

from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, Service


class Github(Service):
    def __init__(self) -> None:
        super().__init__(
            name="Github",
            regex=re.compile(HTTP_REGEX + r"github\.com/(?P<id>[\w-]+)", re.IGNORECASE),
        )

    async def wait_for_rate_limit(self, context: Context) -> None:
        res = await context.session.get("https://api.github.com/rate_limit")
        res.raise_for_status()
        data: RateLimit = await res.json()
        if data["rate"]["remaining"] == 0:
            reset = data["rate"]["reset"]
            logger.info(f"Rate limit reached. Waiting until {reset}")
            await asyncio.sleep(reset - time.time())

    async def visit(self, context: Context, id: str):
        await self.wait_for_rate_limit(context)
        url = f"https://github.com/{id}"
        info_res = await context.session.get(f"https://api.github.com/users/{id}")
        info_res.raise_for_status()
        info: UserInfo = await info_res.json()
        links_res = await context.session.get(
            f"https://api.github.com/users/{id}/social_accounts"
        )
        links_res.raise_for_status()
        links: List[SocialLink] = await links_res.json()

        context.create_result(
            self,
            id=id,
            url=url,
            name=info["name"],
            description=info["bio"],
            profile_picture=info["avatar_url"],
        )

        for link in links:
            context.enqueue_visit(link["url"])


class UserInfo(TypedDict):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool
    name: str
    company: None
    blog: str
    location: str
    email: None
    hireable: None
    bio: None
    twitter_username: str
    public_repos: int
    public_gists: int
    followers: int
    following: int
    created_at: str
    updated_at: str


class SocialLink(TypedDict):
    provider: str
    url: str


class Core(TypedDict):
    limit: int
    remaining: int
    reset: int
    used: int
    resource: str


class Resources(TypedDict):
    core: Core
    graphql: Core
    integration_manifest: Core
    search: Core


class RateLimit(TypedDict):
    resources: Resources
    rate: Core
