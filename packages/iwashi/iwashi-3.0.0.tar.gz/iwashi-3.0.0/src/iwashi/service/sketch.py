from __future__ import annotations
from typing import Dict, List, NotRequired, TypedDict

import json
import re

import bs4

from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, Service


class Sketch(Service):
    def __init__(self):
        super().__init__(
            name="Sketch",
            regex=re.compile(
                HTTP_REGEX + r"sketch\.pixiv\.net/@(?P<id>\w+)", re.IGNORECASE
            ),
        )

    async def visit(self, context: Context, id: str):
        url = f"https://sketch.pixiv.net/@{id}"
        res = await context.session.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        element = soup.select_one("script#__NEXT_DATA__")
        if element is None:
            raise Exception(f"__NEXT_DATA__ not found: {id}")
        next_data = json.loads(element.text)
        data: Root = json.loads(next_data["props"]["pageProps"]["initialState"])
        users = data["users"]["users"]
        if len(users) != 1:
            raise Exception(f"User is must be unique: {id}")
        user = users.popitem()[1]
        context.create_result(
            self,
            id=id,
            url=url,
            name=user["name"],
            description=user["description"],
            profile_picture=user["icon"]["photo"]["original"]["url"],
        )
        social_accounts = user["social_accounts"]
        if "twitter" in social_accounts:
            unique_name = social_accounts["twitter"]["unique_name"]
            context.enqueue_visit(f"https://twitter.com/{unique_name}")
            del social_accounts["twitter"]
        if "pixiv" in social_accounts:
            unique_name = social_accounts["pixiv"]["unique_name"]
            context.enqueue_visit(f"https://www.pixiv.net/users/{unique_name}")
            del social_accounts["pixiv"]
        if social_accounts:
            raise Exception(f"Unknown social accounts: {social_accounts}")


class Amountpoint(TypedDict):
    partial: bool
    input: str
    exchangeErrors: List


class Amountmoney(TypedDict):
    partial: bool
    input: str
    transferErrors: List


class Transfer(TypedDict):
    to: str
    amountPoint: Amountpoint
    amountMoney: Amountmoney
    confirmation: None


class Reward(TypedDict):
    balance: Dict
    provisionalRewards: Dict
    decrementHistories: Dict
    rewards: Dict
    rewardWallLink: Dict
    bankAccount: Dict
    transferring: bool
    historying: bool
    transfer: Transfer
    terms: None


class Temporarymedium(TypedDict):
    temporaryMedium: Dict


class Template(TypedDict):
    themes: Dict


class State(TypedDict):
    state: Dict


class Special(TypedDict):
    contestResults: Dict


class Feedback(TypedDict):
    feedbacks: Dict
    links: Dict


class Contest(TypedDict):
    contests: List


class Info(TypedDict):
    content: None
    hidden: bool


class Componentactionerror(TypedDict):
    alert: None
    info: Info


class Options(TypedDict):
    filterBy: None
    orderBy: str


class Livelist(TypedDict):
    ids: List
    ended: bool
    fetching: bool
    options: Options


class Live(TypedDict):
    lives: Dict
    liveAdStages: Dict
    liveAvailability: bool
    liveClosedAvailability: bool
    liveLogs: Dict
    liveCaptions: Dict
    liveChatErrorMessage: None
    liveArchiveLink: Dict
    liveGiftings: Dict
    liveGiftingSummaries: Dict
    liveGiftingRecommends: Dict
    liveGiftingRecommendsPaging: Dict
    liveGiftingHistories: Dict
    liveSummaryUrl: None
    liveList: Livelist
    unpresentedBlacklistedLiveChats: List


class Comment(TypedDict):
    comments: Dict
    commentWalls: Dict
    commentLinks: Dict
    heartWalls: Dict
    heartLinks: Dict


class Tag(TypedDict):
    endedTagCompletions: List
    tags: List
    tagWalls: Dict
    tagLinks: Dict
    tagUploadSuggested: Dict


class Item(TypedDict):
    items: Dict
    itemWalls: Dict
    itemLinks: Dict
    itemRepliesWall: Dict
    itemRepliesLink: Dict
    itemTopicIds: List


class Browser(TypedDict):
    name: str
    version: str
    major: str
    native: bool
    uwp: bool


class Engine(TypedDict):
    name: str
    version: str


class Cpu(TypedDict):
    architecture: str


class Agent(TypedDict):
    ua: str
    browser: Browser
    engine: Engine
    os: Engine
    device: Dict
    cpu: Cpu


class App(TypedDict):
    agent: Agent
    locale: str
    mayPromptNotificationSubscription: bool
    renderingPreparedAt: int
    preparedSimpleDrawOnClient: bool
    uploadables: List[str]
    isInit: bool


class Gifting(TypedDict):
    lastGiftingItem: None
    giftingItems: List
    points: List


class Contact(TypedDict):
    faqCategories: List


class Announcement(TypedDict):
    announcements: List


class DescriptionFragmentsItem(TypedDict):
    type: str
    body: str
    normalized_body: str


class Twitter(TypedDict):
    unique_name: str
    expired: bool
    is_public: bool


class Pixiv(TypedDict):
    unique_name: str
    expired: bool
    show_on_pixiv: bool


class SocialAccounts(TypedDict):
    twitter: NotRequired[Twitter]
    pixiv: NotRequired[Pixiv]


class Color(TypedDict):
    hex: str
    r: int
    g: int
    b: int


class Pxsq60(TypedDict):
    width: int
    height: int
    url: str
    url2x: str


class Photo(TypedDict):
    pxsq60: Pxsq60
    pxw540: Pxsq60
    pxsq180: Pxsq60
    pxsq120: Pxsq60
    sq180: Pxsq60
    original: Pxsq60
    sq120: Pxsq60
    w240: Pxsq60
    sq60: Pxsq60
    w540: Pxsq60
    pxw240: Pxsq60


class Icon(TypedDict):
    id: int
    type: str
    color: Color
    photo: Photo


class Self(TypedDict):
    method: str
    href: str


class _Links(TypedDict):
    self: Self


class Stats(TypedDict):
    follower_count: int
    following_count: int
    heart_count: int
    resnap_count: int
    public_post_count: int


class User(TypedDict):
    description_fragments: List[DescriptionFragmentsItem]
    name: str
    followed: bool
    following: bool
    blocking: bool
    social_accounts: SocialAccounts
    icon: Icon
    unique_name: str
    post_ids: List
    _links: _Links
    id: str
    pixiv_user_id: str
    description: str
    stats: Stats


Users = Dict[str, User]
Usercolors = Dict[str, str]


class Users0(TypedDict):
    users: Users
    userWalls: Dict
    userLinks: Dict
    userColors: Usercolors
    usersRecommended: List
    usersBlockedWall: List
    usersBlockedWallLink: Dict
    account: Dict
    accountSetting: Dict


class Notifications(TypedDict):
    wall: List
    link: Dict
    types: List


class Privacypolicy(TypedDict):
    privacyPolicyIsAccepted: None
    privacyPolicyText: str
    privacyPolicyUrl: str
    privacyPolicyAcceptedVersion: str
    privacyPolicyUpdatedAt: str


class Params(TypedDict):
    id: str


class Navigation(TypedDict):
    name: str
    params: Params
    search: Dict


class Status(TypedDict):
    code: str
    message: None


class Route(TypedDict):
    historyState: None
    isNavigating: bool
    navigation: Navigation
    status: Status


class Root(TypedDict):
    reward: Reward
    temporaryMedium: Temporarymedium
    template: Template
    state: State
    special: Special
    feedback: Feedback
    contest: Contest
    componentActionError: Componentactionerror
    live: Live
    comment: Comment
    tag: Tag
    item: Item
    app: App
    gifting: Gifting
    contact: Contact
    announcement: Announcement
    users: Users0
    notifications: Notifications
    privacyPolicy: Privacypolicy
    route: Route


class Pageprops(TypedDict):
    initialState: str


class Props(TypedDict):
    pageProps: Pageprops
    __N_SSP: bool


class Query(TypedDict):
    id: str


class NEXT_DATA(TypedDict):
    props: Props
    page: str
    query: Query
    buildId: str
    isFallback: bool
    gssp: bool
    customServer: bool
    scriptLoader: List
