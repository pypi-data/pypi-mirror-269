from __future__ import annotations
from typing import Dict, Union

import json
import re
from typing import List, TypedDict

import bs4

from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, Service


class TikTok(Service):
    def __init__(self) -> None:
        super().__init__(
            name="TikTok",
            regex=re.compile(
                HTTP_REGEX + r"tiktok\.com/@(?P<id>[-\w]+)", re.IGNORECASE
            ),
        )

    async def visit(self, context: Context, id: str) -> None:
        url = f"https://www.tiktok.com/@{id}"
        res = await context.session.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        element = soup.select_one("script#__UNIVERSAL_DATA_FOR_REHYDRATION__")
        if element is None:
            raise Exception(f"Cound not find data for {url}")
        data: Root = json.loads(element.text)
        default_scope = data["__DEFAULT_SCOPE__"]
        user_detail = default_scope["webapp.user-detail"]
        user_info = user_detail["userInfo"]
        user = user_info["user"]
        context.create_result(
            self,
            id=id,
            url=url,
            name=user["nickname"],
            description=user["signature"],
            profile_picture=user["avatarLarger"],
        )


class WebappSwitchAccount(TypedDict):
    vid: str


class SearchVideo(TypedDict):
    vid: str
    botVid: str


class AbTag(TypedDict):
    merge_risk_event: int


class Vid(TypedDict):
    isCreatorCenterContextEnabled: bool
    isInsightV2Enabled: bool
    isOfflineI18nEnabled: bool
    isParallelIframeEnabled: bool
    isPhase2Enabled: bool
    isPrefetchIframeResourceEnabled: bool
    isServerSideTranslationEnabled: bool


class CcPerfPhase1(TypedDict):
    vid: Vid


class Tiktok(TypedDict):
    private_account_prompt_for_u18: int
    use_aligned_copies: int


class TiktokWeb(TypedDict):
    capcut_entry_group: int
    enable_new_playlist: str
    post_polling_version: int
    show_aigc_toggle: int
    tts_product_anchor: int
    web_creation_cover_tool: int


class Webcast(TypedDict):
    web_drawer_show_explore: bool
    web_follow_guide_strategy_group: int


class Parameters(TypedDict):
    webapp_switch_account: WebappSwitchAccount
    mobile_consumption_limit_logged_in: WebappSwitchAccount
    last_login_method: WebappSwitchAccount
    video_bitrate_adapt: WebappSwitchAccount
    one_column_player_size: WebappSwitchAccount
    confirm_logout: WebappSwitchAccount
    webapp_login_email_phone: WebappSwitchAccount
    non_logged_in_comments: WebappSwitchAccount
    video_serverpush: WebappSwitchAccount
    xgplayer_preload_config: WebappSwitchAccount
    enable_ml_model: WebappSwitchAccount
    login_modal_ui_revamp: WebappSwitchAccount
    periodic_login_popup_interval: WebappSwitchAccount
    xg_volume_test: WebappSwitchAccount
    enable_odin_id: WebappSwitchAccount
    login_option_order_by_metrics: WebappSwitchAccount
    mobile_consumption_limit_non_logged_in: WebappSwitchAccount
    login_modal_image: WebappSwitchAccount
    share_button_part1_test: WebappSwitchAccount
    creator_center_connect: WebappSwitchAccount
    mobile_predictive_data: WebappSwitchAccount
    remove_bottom_banner: WebappSwitchAccount
    browser_mode_encourage_login: WebappSwitchAccount
    mobile_search_test: WebappSwitchAccount
    browser_login_redirect: WebappSwitchAccount
    use_inbox_notice_count_api: WebappSwitchAccount
    use_follow_v2: WebappSwitchAccount
    search_video: SearchVideo
    sign_up_webapp_region_change: WebappSwitchAccount
    volume_normalize: WebappSwitchAccount
    should_highlight_hashtag: WebappSwitchAccount
    qr_sso_popup: WebappSwitchAccount
    mobile_consumption_limit_v2: WebappSwitchAccount
    remove_poi_anchor_mobile: WebappSwitchAccount
    video_feed_redesign: WebappSwitchAccount
    mobile_vodkit: WebappSwitchAccount
    mobile_consumption_limit_login: WebappSwitchAccount
    ab_tag: AbTag
    add_kap_entry: WebappSwitchAccount
    add_profile_left_bar: WebappSwitchAccount
    add_transcript: WebappSwitchAccount
    auto_scroll: WebappSwitchAccount
    browse_mode_autoplay_test: WebappSwitchAccount
    browser_mode_creator_tab_3: WebappSwitchAccount
    cc_perf_phase1: CcPerfPhase1
    comment_refactor_test: WebappSwitchAccount
    creator_center_connect_global: WebappSwitchAccount
    creator_center_global_comment_management: WebappSwitchAccount
    creator_center_test: WebappSwitchAccount
    desktop_ui_opt: WebappSwitchAccount
    desktop_ui_reply: WebappSwitchAccount
    digital_wellbeing_web: WebappSwitchAccount
    enable_about_this_ad: WebappSwitchAccount
    enable_continue_play: WebappSwitchAccount
    enable_fb_sdk: WebappSwitchAccount
    enable_not_interested: WebappSwitchAccount
    enable_profile_pinned_video: WebappSwitchAccount
    enhance_video_consumption_test: WebappSwitchAccount
    exchange_retention_popup: WebappSwitchAccount
    expand_item_tag: WebappSwitchAccount
    explore_test: WebappSwitchAccount
    favorite_test: WebappSwitchAccount
    fix_tea_session: WebappSwitchAccount
    following_display_live: WebappSwitchAccount
    friends_tab: WebappSwitchAccount
    increase_detail_page_cover_quantity_test: WebappSwitchAccount
    kep_new_ui_login: WebappSwitchAccount
    live_abr_version: WebappSwitchAccount
    live_csr: WebappSwitchAccount
    live_csr_insert_context: WebappSwitchAccount
    live_csr_skeleton: WebappSwitchAccount
    live_end_improved_metrics: WebappSwitchAccount
    live_event_aggregation: WebappSwitchAccount
    live_feed_preload: WebappSwitchAccount
    live_feed_style: WebappSwitchAccount
    live_golive_entrance: WebappSwitchAccount
    live_lcp_perf_optimize: WebappSwitchAccount
    live_new_discover: WebappSwitchAccount
    live_player_h265: WebappSwitchAccount
    live_player_icon: WebappSwitchAccount
    live_player_mute_text: WebappSwitchAccount
    live_player_switch_button: WebappSwitchAccount
    live_preview_web: WebappSwitchAccount
    live_pro_show: WebappSwitchAccount
    live_recharge_by_amount: WebappSwitchAccount
    live_recharge_homescreen: WebappSwitchAccount
    live_room_age_restriction: WebappSwitchAccount
    live_room_match: WebappSwitchAccount
    live_room_non_streaming: WebappSwitchAccount
    live_room_seamless_switch: WebappSwitchAccount
    live_studio_download_refactor_pc: WebappSwitchAccount
    live_subscription_cashier: WebappSwitchAccount
    live_top_viewers: WebappSwitchAccount
    live_wallet_performance_packup: WebappSwitchAccount
    new_item_tag: WebappSwitchAccount
    optimise_browser_mode: WebappSwitchAccount
    pc_video_playlist_test: WebappSwitchAccount
    photo_mode_yml: WebappSwitchAccount
    photo_test: WebappSwitchAccount
    profile_follow_info: WebappSwitchAccount
    promote_qr_code: WebappSwitchAccount
    reverse_expand_item_tag: WebappSwitchAccount
    search_add_live: WebappSwitchAccount
    search_add_related_search: WebappSwitchAccount
    search_bar_style_opt: WebappSwitchAccount
    search_entry_comment_top: WebappSwitchAccount
    search_entry_comment_word: WebappSwitchAccount
    search_entry_search_bar: WebappSwitchAccount
    search_keep_sug_show: WebappSwitchAccount
    search_transfer_guesssearch: WebappSwitchAccount
    search_transfer_history: WebappSwitchAccount
    search_video_lab: WebappSwitchAccount
    seo_breadcrumb_detail: WebappSwitchAccount
    seo_desktop: WebappSwitchAccount
    should_recom_reduce_icon_risk: WebappSwitchAccount
    show_aigc_label_web: WebappSwitchAccount
    sidenav_test: WebappSwitchAccount
    studio_web_eh_entrance: WebappSwitchAccount
    studio_web_eh_entrance_v2: WebappSwitchAccount
    tiktok: Tiktok
    tiktok_web: TiktokWeb
    translation_reduce: WebappSwitchAccount
    ttlive_broadcast_topic_version_two: WebappSwitchAccount
    ui_layout_alignment: WebappSwitchAccount
    use_aligned_copies: WebappSwitchAccount
    use_error_boundary: WebappSwitchAccount
    video_detail_related_refetch: WebappSwitchAccount
    video_detail_search_bar: WebappSwitchAccount
    web_player_refactor: WebappSwitchAccount
    webapp_explore_category: WebappSwitchAccount
    webapp_preview_cover: WebappSwitchAccount
    webapp_recommend_language: WebappSwitchAccount
    webapp_seo_photomode_user_exp: WebappSwitchAccount
    webapp_video_detail_page_related_mask: WebappSwitchAccount
    webcast: Webcast


class Parameters0(TypedDict):
    tiktok: Dict


class Abtestapp(TypedDict):
    parameters: Parameters0


class Abtestversion(TypedDict):
    versionName: str
    parameters: Parameters
    abTestApp: Abtestapp


class WebappDotAppDashContext(TypedDict):
    language: str
    region: str
    appId: int
    appType: str
    wid: str
    webIdCreatedTime: str
    odinId: str
    nonce: str
    botType: str
    requestId: str
    clusterRegion: str
    abTestVersion: Abtestversion
    csrfToken: str
    userAgent: str
    encryptedWebid: str
    host: str


class ChildrenItem(TypedDict):
    title: str
    href: str


class NavlistItem(TypedDict):
    title: str
    children: List[ChildrenItem]


class ChildrenItem0(TypedDict):
    title: str
    key: str
    href: str


class NavlistItem0(TypedDict):
    title: str
    children: List[ChildrenItem0]


class ChildrenItem1(TypedDict):
    lang: List[str]
    links: List[ChildrenItem]


class KaplinksItem(TypedDict):
    title: str
    children: List[ChildrenItem1]


class Featureflags(TypedDict):
    feature_bar: bool
    business_account_open: bool
    feature_tt4b_ads: bool
    support_multiline_desc: bool
    pc_video_playlist: bool
    feature_mobile_ui_opt_stage2: bool
    add_recipe_card: bool
    desktop_app_survey: bool
    collapse_seo_header: bool
    collapse_seo_header_mobile: bool
    seo_enable_new_poi_page: bool
    enable_privacy_center: bool
    hashtag_viewcount: bool


class Desktopappdownloadlink(TypedDict):
    mac: str
    win: str


class Resource(TypedDict):
    prefix: str
    themes: List[str]
    esm: str
    nomodule: str
    version: str


class I18n(TypedDict):
    cookieBannerTitle: str
    cookieBannerTitleNew: str
    cookieBannerSubTitle: str
    cookieBannerSubTitleNew: str
    cookieBannerSubTitleV2: str
    cookieBannerBtnManage: str
    cookieBannerBtnAccept: str
    cookieBannerBtnDecline: str
    cookiesBannerDetails: str
    cookiesBannerCookiesPolicy: str
    cookiesBannerAccept: str
    webDoNotSellSettingsSavedToast: str
    cookieSettingManageYourCookieTitle: str
    cookieSettingSave: str
    cookieSettingAnalyticsAndMarketing: str
    cookieSettingNecessary: str
    cookieSettingNecessarySubtitle: str
    cookieSettingNecessaryV2: str
    cookieSettingNecessarySubtitleV2: str
    cookieSettingAnalyticsAndMarketingSubtitle: str
    cookieSettingAnalyticsAndMarketingSubtitleV2: str
    cookieManageTip: str


class Cookiebanner(TypedDict):
    load_dynamically: bool
    decline_btn_staged_rollout_area: List[str]
    resource: Resource
    i18n: I18n


class Desktopappsurveylink(TypedDict):
    default: str
    vn: str


class Desktopwebsurveylink(TypedDict):
    new: str
    old: str


class Config(TypedDict):
    featureFlags: Featureflags
    desktopAppDownloadLink: Desktopappdownloadlink
    signUpOpen: bool
    cookieBanner: Cookiebanner
    isGrayFilter: bool
    nickNameControlDay: str
    desktopAppSurveyLink: Desktopappsurveylink
    desktopWebSurveyLink: Desktopwebsurveylink


class Domains(TypedDict):
    kind: str
    captcha: str
    imApi: str
    imFrontier: str
    mTApi: str
    rootApi: str
    secSDK: str
    slardar: str
    starling: str
    tea: str
    teaChannel: str
    teaChannelType: str
    libraWebSDK: str
    webcastApi: str
    webcastRootApi: str
    pipoApi: str
    tcc: str
    locationApi: str


class Microsoft(TypedDict):
    visible: bool
    normal: str


class Downloadlink(TypedDict):
    microsoft: Microsoft
    apple: Microsoft
    amazon: Microsoft
    google: Microsoft


class OriginalsubdivisionsItem(TypedDict):
    GeoNameID: str
    ASCIName: str
    Name: str


class Geocity(TypedDict):
    City: str
    Subdivisions: str
    OriginalSubdivisions: List[OriginalsubdivisionsItem]
    SubdivisionsArr: List[str]


Longdateformat = TypedDict(
    "Longdateformat",
    {
        "LT": "str",
        "LTS": "str",
        "L": "str",
        "LL": "str",
        "LLL": "str",
        "LLLL": "str",
        "l": "str",
        "ll": "str",
        "lll": "str",
        "llll": "str",
        "LL-Y": "str",
    },
)


class Meridiem(TypedDict):
    am: str
    pm: str
    AM: str
    PM: str


class Datefmtlocale(TypedDict):
    name: str
    months: List[str]
    monthsShort: List[str]
    weekdays: List[str]
    weekdaysShort: List[str]
    weekdaysMin: List[str]
    longDateFormat: Longdateformat
    meridiem: Meridiem


class Videoplayerconfig(TypedDict):
    fallback: bool


class Playbacknormalizepath(TypedDict):
    path: List[str]


class Bitrateconfig(TypedDict):
    bitrateLower: int
    bitrateRange: List[int]
    bitrateUpper: int
    mode: str
    paramBf: float
    paramBp: float
    paramLower: float
    paramUpper: float
    paramUpperBl: float
    paramVl1: float
    paramVl2: int
    paramVlLower: float
    paramVlUpper: float
    slidingWindowCountThreshold: int
    slidingWindowExtraction: str
    slidingWindowType: str
    slidingWindowWeight: str
    slidingWindowWeightThreshold: int


class Studiodownloadentrance(TypedDict):
    regions: List[str]
    userRegions: List[str]
    allRegions: bool
    userBlockRegions: List[str]
    userBlockGeoNameIDs: List[str]


class Livesuggestconfig(TypedDict):
    isBlockedArea: bool
    isRiskArea: bool


class Liveanchorentrance(TypedDict):
    liveCenter: bool
    creatorHub: bool
    liveStudio: bool


class Xgplayerinithost(TypedDict):
    group1: List[str]
    group2: List[str]


class VideoorderItem(TypedDict):
    property: str
    detail: List[int]


class VideoorderItem0(TypedDict):
    property: str
    order: str


class Videoorder(TypedDict):
    videoOrder: List[Union[VideoorderItem0, VideoorderItem]]


class Autobitrateparams(TypedDict):
    paramA: int
    paramB: float
    paramC: float
    paramD: int
    minBitrate: int


class ConfigsItem(TypedDict):
    paramBf: float
    paramBp: float
    paramUpper: float
    paramLower: float
    paramUpperBl: float
    paramVl1: float
    paramVl2: int
    paramVlUpper: float
    paramVlLower: float
    bitrateUpper: int
    bitrateLower: int
    slidingWindowType: str
    slidingWindowWeight: str
    slidingWindowWeightThreshold: int
    slidingWindowCountThreshold: int
    slidingWindowExtraction: str
    bitrateRange: List[int]
    mode: str
    quality_filter: Dict
    white_list: List
    autoBitrateParams: Autobitrateparams
    defaultBitrate: int


class Bitrateselectorconfigs(TypedDict):
    configs: List[ConfigsItem]


class Videocoversettings(TypedDict):
    format: int
    acceptHeader: str
    _ssrCount: int


class Hevcrobustness(TypedDict):
    useHevcRobustTest: bool
    forceRobustTest: List[str]


class Apikeys(TypedDict):
    firebase: str


class WebappDotBizDashContext(TypedDict):
    os: str
    isMobile: bool
    isAndroid: bool
    isIOS: bool
    jumpType: str
    navList: List[Union[NavlistItem, NavlistItem0]]
    kapLinks: List[KaplinksItem]
    config: Config
    domains: Domains
    downloadLink: Downloadlink
    deviceLimitRegisterExpired: bool
    subdivisions: List[str]
    geo: List[str]
    geoCity: Geocity
    isGoogleBot: bool
    isBingBot: bool
    isBot: bool
    isSearchEngineBot: bool
    isTTP: bool
    dateFmtLocale: Datefmtlocale
    videoPlayerConfig: Videoplayerconfig
    playbackNormalizePath: Playbacknormalizepath
    bitrateConfig: Bitrateconfig
    searchVideoForLoggedin: bool
    studioDownloadEntrance: Studiodownloadentrance
    liveSuggestConfig: Livesuggestconfig
    liveAnchorEntrance: Liveanchorentrance
    liveStudioEnable: bool
    xgplayerInitHost: Xgplayerinithost
    videoOrder: Videoorder
    searchLiveForLoggedin: bool
    canUseQuery: bool
    bitrateSelectorConfigs: Bitrateselectorconfigs
    idc: str
    vregion: str
    vgeo: str
    videoCoverSettings: Videocoversettings
    hevcRobustness: Hevcrobustness
    apiKeys: Apikeys


Webapp = TypedDict(
    "Webapp",
    {
        "suggested_search_feedback1": "str",
        "suggested_search_feedback2": "str",
        "suggested_search_feedback3": "str",
        "suggested_search_feedback4": "str",
        "suggested_search_feedback5": "str",
        "suggested_search_feedback6": "str",
        "suggested_search_feedback7": "str",
        "suggested_search_feedback8": "str",
        "suggested_search_feedback9": "str",
        "suggested_search_feedback10": "str",
        "suggested_search_feedback11": "str",
        "suggested_search_feedback12": "str",
        "suggested_search_feedback13": "str",
        "Share to": "str",
        "friends": "str",
        "following": "str",
        "messages": "str",
        "Web_logout_modal_header": "str",
        "Web_logout_modal_body": "str",
        "Inbox_New": "str",
        "Log out": "str",
        "Web_loginDropdown_switchAccount": "str",
        "Web_removeAccount_modal_header": "str",
        "Web_removeAccount_modal_body": "str",
        "Cancel": "str",
        "Web_removeAccount_btn": "str",
        "Web_switchAccount_modal_manageAccount": "str",
        "Web_switchAccount_modal_addAccount": "str",
        "Web_removeAccount_doneEditing_btn": "str",
        "pcWeb_survey_popup_header": "str",
        "pcWeb_survey_popup_body": "str",
        "pcWeb_survey_popup_cta1": "str",
        "pcWeb_survey_popup_cta2": "str",
        "grid": "str",
        "accessibilityLabels_link_userProfile": "str",
        "server_error_title": "str",
        "server_error_sub": "str",
        "refresh": "str",
        "SEO_homepage_title": "str",
        "SEO_homepage_desc": "str",
        "Home": "str",
        "personalisedSearch_searchResults_moreOptions_listItem4": "str",
        "Thank you for your feedback": "str",
        "pc_web_more_btn": "str",
        "Report": "str",
        "search_rs_report_not_relevant": "str",
        "others_searched_for": "str",
        "Sorry, something wrong with the server, please try again.": "str",
        "try_again_btn": "str",
        "no_results": "str",
        "no_results_for": "str",
        "no_results_desc": "str",
        "sms_NGO": "str",
        "Followers": "str",
        "search_account": "str",
        "search_see_more": "str",
        "pm_main_live_entry_final": "str",
        "search_top": "str",
        "search_video": "str",
        "search_nomoreresults_text": "str",
        "incorrect_code": "str",
        "common_login_panel_title": "str",
        "webapp_coin_recharge_login": "str",
        "WebApp_coin_recharge_9": "str",
        "login_to_search": "str",
        "nonloggedinsearch_popup_header_v1": "str",
        "classifyV1AWeb_webAppDesktop_maskLayer_bodyDesc": "str",
        "seo_pcweb_logIn_header": "str",
        "delete": "str",
        "reactivate_h1": "str",
        "reactivate_btn": "str",
        "optimize_web_open_notnow_cta": "str",
        "optimize_web_open_tiktok_cta": "str",
        "optimize_web_full_app_header": "str",
        "optimize_web_full_app_body": "str",
        "pcWeb_guestLogin_without": "str",
        "pcWeb_guestLogin_withoutSignup": "str",
        "login_popup_modal_header": "str",
        "guestmode_signup_or": "str",
        "encouragePreviousLoginPlatform_loginPage_loginBadge_body": "str",
        "qr_code_login_prompt_popup_header": "str",
        "tiktoktv_login_modal_loginscreen_scanqr1": "str",
        "tiktoktv_login_modal_loginscreen_scanqr2": "str",
        "login_fb_phoneLinked_toast": "str",
        "login_fb_emailLinked_toast": "str",
        "accessibilityLabels_login_modal_eyeClosedIcon": "str",
        "accessibilityLabels_login_modal_eyeOpenIcon": "str",
        "tv_webLogin_login_header": "str",
        "accessibilityLabels_login_form_placeholder_countryCode": "str",
        "webapp_orContinueWith": "str",
        "tv_webLogin_enterCode_bodyv2": "str",
        "tv_webLogin_enterCode_altMethod": "str",
        "tiktok_instant_app_loading_status_header": "str",
        "accessibilityLabels_search_button": "str",
        "regionOption_selectCountry_list_description": "str",
        "regionOption_selectCountry_list_title": "str",
        "accessibilityLabels_signup_form_placeholder_month": "str",
        "accessibilityLabels_signup_form_placeholder_day": "str",
        "accessibilityLabels_signup_form_placeholder_year": "str",
        "webapp_loginModal_qrCode": "str",
        "HUToS_signupConsent_halfSheet_headline": "str",
        "HUToS_signupConsent_halfSheet_par1": "str",
        "HUToS_signupConsent_halfSheet_par1tos": "str",
        "HUToS_signupConsent_halfSheet_par1pp": "str",
        "HUToS_signupConsent_halfSheet_par1cp": "str",
        "HUToS_signupConsent_halfSheet_par2": "str",
        "HUToS_signupConsent_halfSheet_par2sot": "str",
        "HUToS_signupConsent_halfSheet_par2ph": "str",
        "HUToS_signupConsent_halfSheet_declineButton": "str",
        "HUToS_signupConsent_halfSheet_acceptButton": "str",
        "regionOption_signUp_COdisclaimer_description": "str",
        "regionOption_signUp_disclaimer_description": "str",
        "regionOption_signUp_disclaimer_placeholder": "str",
        "regionOption_signUp_nonEUdisclaimer_description": "str",
        "common_notification_unlogged_button": "str",
        "title_private_on": "str",
        "descrip_private_on_signup": "str",
        "link_learn_more_private_accounts_signup": "str",
        "button_signup_private_on": "str",
        "OK": "str",
        "login_fb_noLonger_LinkPhoneReminder": "str",
        "login_fb_noLonger_LoginWithPhoneNextTime": "str",
        "login_fb_noLonger_phone_send_cta": "str",
        "login_fb_noLonger_can'tVerifyPhone": "str",
        "login_fb_noLonger_can'tVerifyPhone_useEmail": "str",
        "login_fb_link_cta": "str",
        "login_fb_noLonger_LinkEmailAddress": "str",
        "login_fb_noLonger_EmailLoginAlternative": "str",
        "login_fb_noLonger_GiveFeedback": "str",
        "login_fb_noLonger_can'tVerifyEmail": "str",
        "login_fb_noLonger_can'tVerifyEmail_usePhone": "str",
        "login_fb_noLonger_LinkPhoneNumber": "str",
        "login_fb_noLonger_LinkPhoneNumberReminder": "str",
        "login_fb_noLonger_LinkPhone": "str",
        "login_fb_noLonger_notNow_cta": "str",
        "reactivate_toast": "str",
        "regionOption_selectCountry_list_confirmation": "str",
        "accessibilityLabels_signup_form_back": "str",
        "accessibilityLabels_login_form_back": "str",
        "No videos with this hashtag yet": "str",
        "Looking for videos? Try browsing our trending creators, hashtags, and sounds.": "str",
        "playlist_webapp_profileview_playlists_numberviews": "str",
        "views": "str",
        "playlist_webapp_profileview_playlists_numbervid": "str",
        "posts": "str",
        "playlist_webapp_toast_error_cheatPlaylist": "str",
        "playlist_webapp_toast_error_tryagain": "str",
        "playlist_webapp_toast_created": "str",
        "playlist_webapp_creation_backBtn": "str",
        "playlist_webapp_creation_header_create": "str",
        "playlist_webapp_creation_desc": "str",
        "playlist_webapp_upload_dropdown_nameaplaylist": "str",
        "videos": "str",
        "playlist_webapp_upload_addtoplaylist": "str",
        "playlist_webapp_creation_selectvid_desc": "str",
        "playlist_webapp_creation_btn_cancel": "str",
        "playlist_webapp_creation_btn_create": "str",
        "blue_v_change_username_review_modal_desc": "str",
        "blue_v_change_name_review_modal_desc": "str",
        "blue_v_webapp_change_name_review_modal_desc": "str",
        "blue_v_change_name_review_modal_title": "str",
        "blue_v_change_name_review_cancel_btn": "str",
        "blue_v_change_name_review_submit_btn": "str",
        "profile_personal_no_content_title": "str",
        "profile_personal_no_content_body": "str",
        "profile_no_content_title": "str",
        "profile_no_content_des": "str",
        "fc_view_empty_videos_title": "str",
        "fc_view_fav_empty_videos_desc": "str",
        "profile_public_nolikes_title": "str",
        "profile_self_public_nolikes": "str",
        "profile_others_public_nolikes": "str",
        "cancel": "str",
        "editprofile_editpage_error_photofail_others": "str",
        "editprofile_editpage_photo_editphoto": "str",
        "editprofile_editimage_zoom": "str",
        "editprofile_cancel": "str",
        "editprofile_editpage_photo_apply": "str",
        "editprofile_editpage_username_confirmtitle": "str",
        "editprofile_editpage_username_confirmtext": "str",
        "nickname_change_pop_up_title": "str",
        "nickname_change_pop_up_description": "str",
        "nickname_username_change_pop_up_title": "str",
        "nickname_username_change_pop_up_description": "str",
        "nickname_username_change_pop_up_cta_2": "str",
        "blue_v_change_username_modal_title": "str",
        "blue_v_change_username_modal_desc": "str",
        "blue_v_change_username_modal_desc_2": "str",
        "blue_v_change_name_modal_title": "str",
        "blue_v_change_name_modal_desc": "str",
        "blue_v_change_name_modal_desc_2": "str",
        "blue_v_change_username_name_modal_title": "str",
        "blue_v_webapp_change_name_modal_desc": "str",
        "blue_v_webapp_change_name_modal_desc_2": "str",
        "blue_v_change_name_modal_submit_request_btn": "str",
        "blue_v_change_name_modal_change_btn": "str",
        "blue_v_change_username_lose_badge_modal_title": "str",
        "blue_v_change_name_lose_badge_modal_title": "str",
        "blue_v_webapp_change_name_lose_badge_modal_title": "str",
        "blue_v_change_name_lose_badge_modal_desc": "str",
        "blue_v_change_name_lose_badge_confirm_btn": "str",
        "editprofile_editpage_error_row": "str",
        "editprofile_editpage_bio": "str",
        "editprofile_editpage_error_namenotavail": "str",
        "editprofile_editpage_error_max": "str",
        "editprofile_editpage_name": "str",
        "nickname_change_1st_time_description": "str",
        "nickname_change_description": "str",
        "editprofile_editpage_error_notavailable": "str",
        "editprofile_editpage_error_tryagain": "str",
        "editprofile_editpage_error_min2char": "str",
        "editprofile_editpage_error_username_max": "str",
        "editprofile_editpage_username": "str",
        "editprofile_editpage_username_subtext1": "str",
        "editprofile_editpage_username_subtext2": "str",
        "editprofile_editpage_error_photofail_max": "str",
        "editprofile_editpage_error_image_cantuse": "str",
        "editprofile_editpage_error_cantmodify_others": "str",
        "editprofile_editpage_error_cantmodify_review": "str",
        "editprofile_editpage_error_username_cantchange": "str",
        "alert_user_update_profile_limited_toast": "str",
        "account_status_banned": "str",
        "nickname_change_fail_toast": "str",
        "ecom_changename_web": "str",
        "editprofile_editprofile": "str",
        "editprofile_editpage_photo": "str",
        "editprofile_save": "str",
        "editprofile_close": "str",
        "editprofile_tooltip_title": "str",
        "editprofile_tooltip_subtitle": "str",
        "webdm_message_button": "str",
        "profile_page_message_btn": "str",
        "sug_accounts": "str",
        "profile_page_followerList_private_header": "str",
        "profile_page_followerList_private_body": "str",
        "profile_page_profile_follower_tab": "str",
        "profile_page_profile_follower_view_desc": "str",
        "profile_page_followingList_private_header": "str",
        "profile_page_followingList_private_body": "str",
        "profile_page_profile_following_tab": "str",
        "profile_page_profile_following_view_desc": "str",
        "profile_page_profile_follower_desc": "str",
        "profile_page_profile_following_desc": "str",
        "profile_page_suggested_tab": "str",
        "profile_page_profile_friends_desc": "str",
        "profile_page_friends_tab": "str",
        "user_action_unfollow": "str",
        "profile_self_link_unavailable": "str",
        "nonpersonalizedFeeds_profile_suggestedAccounts_info_body": "str",
        "nonpersonalizedFeeds_profile_suggestedAccounts_info_bodyManagePersonFeedsVariable": "str",
        "nonpersonalizedFeeds_profile_suggestedAccounts_info_bodyPrivacyVariable": "str",
        "Privacy": "str",
        "nonpersonalizedFeeds_modal_allScenarios_body_learnMore_articleLink": "str",
        "Learn more": "str",
        "nonpersonalizedFeeds_turnOn_modal_toggle_CTA": "str",
        "No bio yet.": "str",
        "Following": "str",
        "followers": "str",
        "Likes": "str",
        "playlist_webapp_profileview_btn_changeorder": "str",
        "playlist_webapp_profile_entry_create": "str",
        "playlist_webapp_changeorder_header": "str",
        "playlist_webapp_upload_nameplaylist_btn": "str",
        "playlist_webapp_profileview_playlists": "str",
        "Videos": "str",
        "pm_mt_multiguest_enlarge_host_tag": "str",
        "LIVE": "str",
        "webLIVE_personalPage_LIVEbanner_title": "str",
        "profile_others_blocked_post_body": "str",
        "profile_others_block_post_body": "str",
        "This account is private": "str",
        "profile_others_private_body": "str",
        "profile_others_like_private_title": "str",
        "profile_others_like_private_body": "str",
        "sortbyvv_profile_tab_text_favorites": "str",
        "liked": "str",
        "webLIVE_personalPage_LIVEbanner_numViewerDesc": "str",
        "webapp_profile": "str",
        "podcasts_linkFullEpisodes_publishEpisodePage_confirmationBanner": "str",
        "editprofile_toast": "str",
        "blue_v_change_name_toast_request_submitted": "str",
        "online": "str",
        "Users": "str",
        "keywords_expand_title_hashtags": "str",
        "Hashtags": "str",
        "keywords_expand_title_sounds": "str",
        "Sounds": "str",
        "Page not available": "str",
        "playlist_invalid_error_code": "str",
        "videos_": "str",
        "No videos with this sound yet": "str",
        "topic_foryou_topics_toast_unavailable": "str",
        "Promote_PC_popup_title": "str",
        "Promote_PC_popup_content": "str",
        "qapage_webapp_askby": "str",
        "qapage_empty_title": "str",
        "qapage_empty_desc": "str",
        "follows": "str",
        "video_detail": "str",
        "creator": "str",
        "video_label_private": "str",
        "Friends only": "str",
        "comment_disable_notfollow": "str",
        "video_details_page_comment_header": "str",
        "ad_comment_close_des": "str",
        "comment_off": "str",
        "scheduled_video_comment_unavailable": "str",
        "Close": "str",
        "asr_transcript_onpc_kebab_menu_ab_transcript_button": "str",
        "Share": "str",
        "share": "str",
        "cc_webapp_age_video_details_title": "str",
        "classifyV1AWeb_webAppDesktop_maskLayer_headerTitle": "str",
        "cc_webapp_age_video_details_body": "str",
        "classifyV1AWeb_webAppDesktop_maskLayer_button": "str",
        "photosensitive_skepped_toast": "str",
        "pcWeb_floatingPlayer_on": "str",
        "pcWeb_multitaskPlayer_on": "str",
        "pcWeb_miniPlayer_turnOff_cta": "str",
        "ad_not_support": "str",
        "pc_web_keyboard_btn": "str",
        "video_details_page_morevideos_btn": "str",
        "Log In": "str",
        "pc_web_you_may_like": "str",
        "about": "str",
        "seo_pcWeb_recipe_about_header": "str",
        "seo_pcWeb_recipe_ingredient_header": "str",
        "seo_pcWeb_recipe_step_header": "str",
        "seo_pcWeb_recipe_hint_header": "str",
        "seo_internalLink_mayBeInterested": "str",
        "seo_aggre_related_to": "str",
        "Analytics": "str",
        "Upload": "str",
        "TikTok": "str",
        "SEO TikTok Description": "str",
        "SEO TikTok Keyword": "str",
        "feedback_pc_back": "str",
        "feedback_and_help_seo_title": "str",
        "Is your problem resolved?": "str",
        "backend_settings_yes": "str",
        "backend_settings_no": "str",
        "backend_settings_stillhaveproblem": "str",
        "Help Center": "str",
        "backend_settings_topictitle": "str",
        "Feedback and help": "str",
        "backend_settings_faqtitle": "str",
        "Report a problem": "str",
        "feedback_pc_history": "str",
        "Tell us your feedback": "str",
        "Please provide as much detail as possible": "str",
        "feedback_pc_upload": "str",
        "Submit": "str",
        "Network error. Please try again.": "str",
        "com_mig_your_support_tickets": "str",
        "Description must be at least 2 characters": "str",
        "Couldn't upload image. Please try again": "str",
        "setting_feedback_delete_picture": "str",
        "setting_feedback_delete_history": "str",
        "Video": "str",
        "webapp_unblocked_button1": "str",
        "webdm_block": "str",
        "webapp_privacy_and_safety_blocked_accounts": "str",
        "BA_onboarding_welcome_title": "str",
        "ttba_switch": "str",
        "ttelite_switch_title": "str",
        "ttelite_switch_intro": "str",
        "ttelite_switch_action_yes": "str",
        "ttelite_switch_action_no": "str",
        "stop_seller_remove_pop_context": "str",
        "stop_seller_remove_pop_context_hyperlink": "str",
        "stop_seller_remove_pop_title": "str",
        "manage_account": "str",
        "acc_control": "str",
        "delete_acc": "str",
        "delete_btn": "str",
        "changeRegistrationLocation_account_accountInformation": "str",
        "changeRegistrationLocation_account_accountInformation_title": "str",
        "changeRegistrationLocation_account_accountInformation_subtitle": "str",
        "Confirm": "str",
        "bc_account_private_enable_notice_content": "str",
        "bc_account_private_enable_notice_contenturl": "str",
        "ba": "str",
        "caba_no_private": "str",
        "caba_no_private_desc": "str",
        "private_acc_ads": "str",
        "switch_public_h1": "str",
        "switch_public_desc": "str",
        "bc_account_private_enable_notice_title": "str",
        "disallowSwitchAccount_privacy_popUp_title": "str",
        "disallowSwitchAccount_privacy_popUp_description": "str",
        "disallowSwitchAccount_privacy_popUp_placeholder": "str",
        "disallowSwitchAccount_privacy_popUp_placeholder2": "str",
        "disallowSwitchAccount_privacy_popUp_button2": "str",
        "toast_restricted_fam_pairing": "str",
        "privacy_h1": "str",
        "discoverability": "str",
        "private_acc": "str",
        "private_acc_desc": "str",
        "feedback_webform_dropdown_tt4b_opt_2": "str",
        "download_data_entry_point": "str",
        "datadownload_process_download_your_data": "str",
        "dyd_desc": "str",
        "ok_btn": "str",
        "privacy": "str",
        "Language": "str",
        "datadownload_screentitle": "str",
        "Privacy and settings": "str",
        "WebApp_coin_recharge_1": "str",
        "desktop_push_turn_on_tips_text1": "str",
        "accessibilityLabels_settings_pushNotifs_modal_lockIcon": "str",
        "desktop_push_turn_on_tips_text2": "str",
        "push_notifications": "str",
        "desktop_notifications": "str",
        "allow_in_browser": "str",
        "desktop_push_tips": "str",
        "desktop_push_turn_on_tips_title": "str",
        "push_preferences": "str",
        "push_preferences_tips": "str",
        "interactions": "str",
        "push_likes_description": "str",
        "push_likes": "str",
        "push_comments": "str",
        "push_new_followers": "str",
        "push_mentions": "str",
        "screentimedash_digitalwellbeing_summary_timespent_graph_yaxis_hours_1": "str",
        "screentimedash_digitalwellbeing_summary_timespent_graph_yaxis_minutes_1": "str",
        "screentimedash_digitalwellbeing_summary_day_label_sun": "str",
        "screentimedash_digitalwellbeing_summary_day_label_mon": "str",
        "screentimedash_digitalwellbeing_summary_day_label_tue": "str",
        "screentimedash_digitalwellbeing_summary_day_label_wed": "str",
        "screentimedash_digitalwellbeing_summary_day_label_thu": "str",
        "screentimedash_digitalwellbeing_summary_day_label_fri": "str",
        "screentimedash_digitalwellbeing_summary_day_label_sat": "str",
        "screentimedash_digitalwellbeing_summary_month_label_jan": "str",
        "screentimedash_digitalwellbeing_summary_month_label_feb": "str",
        "screentimedash_digitalwellbeing_summary_month_label_mar": "str",
        "screentimedash_digitalwellbeing_summary_month_label_apr": "str",
        "screentimedash_digitalwellbeing_summary_month_label_may": "str",
        "screentimedash_digitalwellbeing_summary_month_label_jun": "str",
        "screentimedash_digitalwellbeing_summary_month_label_jul": "str",
        "screentimedash_digitalwellbeing_summary_month_label_aug": "str",
        "screentimedash_digitalwellbeing_summary_month_label_sep": "str",
        "screentimedash_digitalwellbeing_summary_month_label_oct": "str",
        "screentimedash_digitalwellbeing_summary_month_label_nov": "str",
        "screentimedash_digitalwellbeing_summary_month_label_dec": "str",
        "screentimedash_digitalwellbeing_summary_timespent_day": "str",
        "screentimedash_digitalwellbeing_summary_timespent_hours_1": "str",
        "screentimedash_digitalwellbeing_summary_timespent_minutes_1": "str",
        "screentimedash_digitalwellbeing_summary_timespent_night": "str",
        "screentimedash_digitalwellbeing_summary_appopened_day_1": "str",
        "screentimedash_digitalwellbeing_summary_appopened_night_1": "str",
        "screentimedash_digitalwellbeing_summary_appopened_actionsheet_chooseweek_title": "str",
        "screentimedash_digitalwellbeing_summary_timespent_tab": "str",
        "screentimedash_digitalwellbeing_summary_appopened_tab": "str",
        "screentimedash_digitalwellbeing_summary_timespent_header_daytime": "str",
        "screentimedash_digitalwellbeing_summary_daytime_tip_desc": "str",
        "screentimedash_digitalwellbeing_summary_nighttime_tip_title": "str",
        "screentimedash_digitalwellbeing_summary_nighttime_tip_desc": "str",
        "screentimedash_digitalwellbeing_summary_appopened_header_total": "str",
        "screentime_settings_dailyscreentime_status_off": "str",
        "screentime_settings_title": "str",
        "screenTime_web_infoIcon_desc": "str",
        "screentimedash_digitalwellbeing_dailyscreentime_title": "str",
        "screentime_settings_screentimebreaks_title": "str",
        "screentime_settings_screentimebreaks_desc": "str",
        "nightscreentimemgmt_screentimesettings_sleepreminders_feature_name": "str",
        "nightscreentimemgmt_screentimesettings_sleepreminders_feature_desc": "str",
        "screentimedash_digitalwellbeing_weeklyscreentime_title": "str",
        "screentimedash_digitalwellbeing_weeklyscreentime_desc": "str",
        "screentimedash_digitalwellbeing_summary_header": "str",
        "screenTime_summarySection_desc": "str",
        "teenScreenTimeDashboard_familyPairing_header_helpAndResources": "str",
        "teenScreenTimeDashboard_familyPairing_screenTime_link": "str",
        "pa_ads_label": "str",
        "customizeSTM_screenTimeLimit_selectTime_minutes": "str",
        "customizeSTM_screenTimeLimit_selectTimeActionSheet": "str",
        "customizeSTM_screenTimeLimit_selectTime_hours": "str",
        "customizeSTM_dailyScreenTimeOn_header_notified": "str",
        "customizeSTM_dailyScreenTimeOn_desc_notified": "str",
        "customizeSTM_dailyScreenTimeOn_header_discuss": "str",
        "customizeSTM_dailyScreenTimeOn_desc_discuss": "str",
        "customizeSTM_dailyScreenTimeOn_header_time_minutes": "str",
        "customizeSTM_dailyScreenTimeOn_header_time_hours": "str",
        "customizeSTM_dailyScreenTimeOn_header_time_hoursMinutes": "str",
        "customizeSTM_teenDailyScreenTimeOn_header": "str",
        "customizeSTM_dailyScreenTimeOn_title": "str",
        "customizeSTM_dailyScreenTimeOff_title": "str",
        "dailyscreentime_featurescreen_heading": "str",
        "SEO_setting_title": "str",
        "Sub_emote_goback": "str",
        "webapp_block_experience_unblock_popup_header": "str",
        "webapp_block_experience_block_popup_header": "str",
        "webapp_block_experience_unblock_popup_body": "str",
        "webapp_block_experience_block_popup_body": "str",
        "webapp_unblocked_button2": "str",
        "unblock": "str",
        "support_webapp_sharing_chat_page_video_card_3": "str",
        "Feedback": "str",
        "support_webapp_sharing_chat_page_video_card_1": "str",
        "support_webapp_sharing_chat_page_video_card_2": "str",
        "photo_post_unavailable_title": "str",
        "subVideo_unavailableScreen_title": "str",
        "dm_stranger_delete_this_message_header": "str",
        "dm_stranger_delete_this_message_body": "str",
        "dm_tcm_request_link_report": "str",
        "dm_message_request_report": "str",
        "dm_tcm_request_desc_business_wants_send_msg": "str",
        "dm_message_request": "str",
        "dm_tcm_request_title_business_wants_send_msg": "str",
        "dm_message_request_title": "str",
        "dm_delete": "str",
        "dm_accept": "str",
        "webdm_unblock_this_account": "str",
        "webdm_inputbox_block_note": "str",
        "im_hint_send_msg": "str",
        "comment_tray_emoji": "str",
        "subVideo_nonsubs_webToast": "str",
        "dm_tcm_card_title_business_invitation": "str",
        "webdm_message_not_supported": "str",
        "direct_meaasge_sending_ban_feedback": "str",
        "direct_meaasge_sending_ban_notice": "str",
        "webdm_unlike": "str",
        "Like": "str",
        "webdm_report": "str",
        "Friends": "str",
        "Inbox_Follow_back": "str",
        "dm_tcm_banner_from_tcm": "str",
        "WBS_inbox_cc_view": "str",
        "wbs_inbox_msg_cctos_createcontacts": "str",
        "webdm_report_01_message_selected": "str",
        "webdm_report_n_message_selected": "str",
        "Back": "str",
        "Report_reason": "str",
        "dm_web_baLabel_filter": "str",
        "dm_web_baLabel_emptyLabel_state": "str",
        "dm_web_baLabel_apply_btn": "str",
        "dm_web_baLabel_unreadOnly_checkbox": "str",
        "privacy_and_safety_message_detail": "str",
        "setting_disabled_16": "str",
        "hint_dm_settings": "str",
        "option_everyone": "str",
        "option_friends": "str",
        "option_no_one": "str",
        "family_pairing_toast_parent_settings": "str",
        "webdm_message_settings": "str",
        "dm_who_can_send_you_direct_messages": "str",
        "dm_tcm_section_name_msg_preferences": "str",
        "dm_tcm_toggle_title_always_allow": "str",
        "dm_tcm_toggle_desc_tcm": "str",
        "webdm_cancel": "str",
        "save_settings": "str",
        "message_request_inbox": "str",
        "webdm_chatlist_head_messages": "str",
        "like_message": "str",
        "dm_multiple_messages": "str",
        "support_webapp_sharing_chat_page_status_2": "str",
        "support_webapp_sharing_chat_page_status_1": "str",
        "dm_left_swipe_unmute": "str",
        "dm_left_swipe_mute": "str",
        "no_top": "str",
        "webdm_pin_to_top": "str",
        "dm_tcm_label_business": "str",
        "dm_web_baLabel_noChatFound_header": "str",
        "dm_web_baLabel_noChatFound_body": "str",
        "im_message_list_empty": "str",
        "webdm_report_type": "str",
        "webdm_report_why": "str",
        "webdm_next": "str",
        "webdm_report_popup_title": "str",
        "webdm_report_popup_detail": "str",
        "webdm_done": "str",
        "dm_stranger_error_message_header": "str",
        "dm_stranger_error_message_body": "str",
        "SEO_dm_title": "str",
        "basicPoi_moreRelated": "str",
        "no_video_in_collection_error_title": "str",
        "no_video_in_collection_error_description": "str",
        "collection_not_availble_error": "str",
        "shared_collection_dmcard_title": "str",
        "shared_collection_dmcard_desc": "str",
        "login_fb_noLonger_title": "str",
        "login_fb_noLonger_body": "str",
        "login_fb_noLonger_cta1": "str",
        "login_fb_noLonger_cta2": "str",
        "pc_web_explorePage_topics_singing_dancing": "str",
        "pc_web_explorePage_topics_comedy": "str",
        "pc_web_explorePage_topics_sports": "str",
        "pc_web_explorePage_topics_anime_comics": "str",
        "pc_web_explorePage_topics_relationship": "str",
        "pc_web_explorePage_topics_shows": "str",
        "pc_web_explorePage_topics_lipsync": "str",
        "pc_web_explorePage_topics_daily_life": "str",
        "pc_web_explorePage_topics_beauty_care": "str",
        "pc_web_explorePage_topics_games": "str",
        "pc_web_explorePage_topics_society": "str",
        "pc_web_explorePage_topics_outfit": "str",
        "pc_web_explorePage_topics_cars": "str",
        "pc_web_explorePage_topics_food": "str",
        "pc_web_explorePage_topics_animals": "str",
        "pc_web_explorePage_topics_family": "str",
        "pc_web_explorePage_topics_drama": "str",
        "pc_web_explorePage_topics_fitness_health": "str",
        "pc_web_explorePage_topics_education": "str",
        "pc_web_explorePage_topics_technology": "str",
        "pc_web_empty_state_novid_header": "str",
        "pc_web_empty_state_novid_body": "str",
        "pc_web_explorePage_all": "str",
        "pcWeb_seasonal_tab_newYear": "str",
        "pcWeb_seasonal_tab_christmas": "str",
        "pc_web_explore_meta_title": "str",
        "pc_web_explore_meta_desc": "str",
        "seo_popular_disclaimer": "str",
        "seo_popular_disclaimer2_btn": "str",
        "feed": "str",
        "custom": "str",
        "website": "str",
        "comment_tray_reply_default": "str",
        "pcWeb_add_reply": "str",
        "comment_tray_default": "str",
        "seo_popular_faq": "str",
        "keys": "str",
        "playlist_webapp_profileView_error_header": "str",
        "playlist_webapp_profileView_error_desc": "str",
        "playlist_webapp_toast_deleted": "str",
        "playlist_webapp_profileview_btn_editname": "str",
        "playlist_webapp_profileview_btn_deleteplaylist": "str",
        "playlist_webapp_editname_header": "str",
        "playlist_webapp_deleteplaylist_header": "str",
        "playlist_webapp_editname_desc": "str",
        "playlist_webapp_deleteplaylist_desc": "str",
        "playlist_webapp_deleteplaylist_btn_cancel": "str",
        "playlist_webapp_editname_btn": "str",
        "playlist_webapp_deleteplaylist_btn_delete": "str",
        "playlist_webapp_profileview_btn_removevid": "str",
        "playlist_webapp_profileview_btn_addvid": "str",
        "embed": "str",
        "account": "str",
        "hide": "str",
        "update": "str",
        "Download": "str",
        "Caption": "str",
        "Open": "str",
        "net": "str",
        "ca": "str",
        "get_app": "str",
        "get_tt_desktop": "str",
        "get_tt_app": "str",
        "accessibilityLabels_forYou_scroll_btn": "str",
        "personalized_nonLogin_popup_header": "str",
        "personalized_nonLogin_popup_body": "str",
        "desktop_app_installScreen_tos": "str",
        "desktop_app_installScreen_pp": "str",
        "personalized_nonLogin_popup_cta2": "str",
        "personalized_nonLogin_popup_cta1": "str",
        "report_Prohibited_or_infringing": "str",
        "report_Right_owner": "str",
        "report_Prohibited_or_violence": "str",
        "report_Not_right_owner": "str",
        "Web_report_thanks_for_report": "str",
        "dsa_illegal_report_received_confirm_logout": "str",
        "dsa_illegal_report_received_confirm": "str",
        "pm_mt_live_done": "str",
        "Web_report_report_for_error": "str",
        "live_close": "str",
        "pm_mt_live_page_sth_wrong": "str",
        "pm_mt_live_page_try_again": "str",
        "report_inbox_retry_btn": "str",
        "Please select a scenario": "str",
        "Web_report_reason_select": "str",
        "dsa_illegal_placeholder_learnmore": "str",
        "Web_report_description": "str",
        "report_details_toast": "str",
        "attachment_upload_limit": "str",
        "report_img_toast": "str",
        "event_dm_share_message_card": "str",
        "pcWeb_youReposted_label": "str",
        "pcWeb_nickReposted_label": "str",
        "qapage_webapp_error_title": "str",
        "music_detail_unavailable_1": "str",
        "subVideo_viewing_lable": "str",
        "Web_report_hide_video": "str",
        "Web_report_show_video": "str",
        "scheduled_for": "str",
        "pc_web_playing_now": "str",
        "pc_web_fullscreen_btn": "str",
        "pc_web_speed_btn": "str",
        "who_can_view_public": "str",
        "public_desc": "str",
        "who_can_view_followers": "str",
        "followers_desc_for_private": "str",
        "who_can_view_friends": "str",
        "followers_desc": "str",
        "private_desc": "str",
        "commonStrings_privacySettings_option_friends": "str",
        "commonStrings_privacySettings_optionDescription_friends": "str",
        "commonStrings_privacySettings_option_onlyYou": "str",
        "commonStrings_privacySettings_option_everyone": "str",
        "commonStrings_privacySettings_option_onOffTikTok": "str",
        "useAlignedCopies_privacySettings_panel_description": "str",
        "new_video_status": "str",
        "pull_video_expl_available_for_ads": "str",
        "duet_stitch_minor": "str",
        "hint2": "str",
        "hint1": "str",
        "privacy_set": "str",
        "view_access": "str",
        "allow_comment": "str",
        "allow_duet": "str",
        "allow_stitch": "str",
        "privacy_settings_done": "str",
        "delete_confirm": "str",
        "cancel_settings": "str",
        "comment_at_search": "str",
        "comment_at_load": "str",
        "comment_at_tryagain": "str",
        "no_at_me": "str",
        "mention_privacy_toast_cant_mention": "str",
        "comment_tray_at": "str",
        "comment_tray_btn": "str",
        "comment_reply_success": "str",
        "comment_post_success": "str",
        "comment_banned_toast": "str",
        "comment_post_failed": "str",
        "comment_nointernet_toast": "str",
        "searchquerycomment_feedbackpanel_notinterested": "str",
        "searchquerycomment_feedbackpanel_unrelated": "str",
        "searchquerycomment_feedbackpanel_inappropriate": "str",
        "searchquerycomment_feedbackpanel_others": "str",
        "comment_delete_cancel": "str",
        "searchquerycomment_feedbackpanel_header": "str",
        "accessibilityLabels_forYou_btn_like": "str",
        "comment_delete_btn": "str",
        "comment_delete_des": "str",
        "comment_delete_confirm": "str",
        "following_acc": "str",
        "friends_acc": "str",
        "WebApp_comment_copyurl_id": "str",
        "comment_reply_btn": "str",
        "pcWeb_detailPage_comment_viewNumReply": "str",
        "pcWeb_detailPage_comment_viewNumMore": "str",
        "view_more_replies": "str",
        "comment_panel_zero": "str",
        "comment_turnoff_unlike": "str",
        "comment_turnoff_like": "str",
        "comment_delete_success": "str",
        "comment_delete_failed": "str",
        "Comment": "str",
        "Next": "str",
        "pc_web_previous_btn": "str",
        "pc_web_next_btn": "str",
        "pc_web_login": "str",
        "pc_web_login_to_comment": "str",
        "pcWeb_detailPage_backTop_btn": "str",
        "pc_web_browser_nowPlaying": "str",
        "fixed_comments": "str",
        "pc_web_browser_tabName_creatorVid": "str",
        "support_webapp_sharing_error_message": "str",
        "support_webapp_sharing_sent_toast_1": "str",
        "support_webapp_sharing_sent_toast_2": "str",
        "support_webapp_sharing_sent_toast_3": "str",
        "support_webapp_sharing_option_button": "str",
        "support_webapp_sharing_toast_2": "str",
        "support_webapp_sharing_toast_1": "str",
        "subVideo_share_note": "str",
        "support_webapp_sharing_searchbar_ghosttext": "str",
        "support_webapp_sharing_search_results": "str",
        "support_webapp_sharing_recent": "str",
        "support_webapp_sharing_following": "str",
        "support_webapp_sharing_write_a_message": "str",
        "support_webapp_sharing_send_button": "str",
        "pcWeb_NewFeatureFloating": "str",
        "pcWeb_NewFeatureMultitask": "str",
        "pcWeb_Floating": "str",
        "pcWeb_Multitask": "str",
        "embed_profile_popup_title": "str",
        "embed_profile_popup_desc": "str",
        "embeds_popup_hashtag_header": "str",
        "embeds_popup_hashtag_body": "str",
        "embeds_popup_sound_header": "str",
        "embeds_popup_sound_body": "str",
        "Embed video": "str",
        "embed_popup_embed_body": "str",
        "embeds_popup_tns": "str",
        "embed_profile_popup_bottom_desc_tos": "str",
        "embed_profile_card_desc_privacy_policy": "str",
        "By embedding this video, you confirm that you agree to our <a href={TermsHref}>Terms of Use</a> and acknowledge you have read and understood our <a href={PolicyHref}> Privacy Policy.</a>": "str",
        "embed_profile_popup_btn": "str",
        "web_sharing_disable_toast": "str",
        "Copied": "str",
        "embed_success": "str",
        "embed_profile_tooltip": "str",
        "accessibilityLabels_forYou_share_moreOptions_btn": "str",
        "masklayer_general_title": "str",
        "photosensitive_masklayer_title": "str",
        "photosensitive_masklayer_removed": "str",
        "masklayer_general_body": "str",
        "photosensitive_masklayer_body1": "str",
        "photosensitive_masklayer_body2": "str",
        "photosensitive_masklayer_removed_body1": "str",
        "photosensitive_masklayer_removed_body3": "str",
        "masklayer_general_skip": "str",
        "photosensitive_masklayer_watch": "str",
        "masklayer_general_watch": "str",
        "photosensitive_masklayer_skipall": "str",
        "Webapp_tooltips_Pause": "str",
        "Webapp_tooltips_play": "str",
        "pm_web_fullpage_entry": "str",
        "pm_web_fullpage_error_button": "str",
        "live_error_network_title": "str",
        "live_error_network_body": "str",
        "live_error_network_button": "str",
        "live_ending_title": "str",
        "pm_mt_livecard_end_subtitle_1": "str",
        "pm_web_fyp_homePage_entry": "str",
        "webapp_forYoufeed_notInterested_btn": "str",
        "pc_web_report_btn": "str",
        "about_this_ad_title": "str",
        "copy_link": "str",
        "webapp_share_btn": "str",
        "accessibilityLabels_forYou_btn_share": "str",
        "fixed_likes": "str",
        "comment_tray_exit_title": "str",
        "comment_tray_exit_des": "str",
        "comment_tray_exit_leave": "str",
        "comment_tray_exit_stay": "str",
        "pcWeb_login_browserMode": "str",
        "webapp_seekbar_tooltip": "str",
        "pc_web_browser_creatorVid_exit": "str",
        "pc_web_volume_btn": "str",
        "view_analytics": "str",
        "deleted": "str",
        "video_unavailable_deleted": "str",
        "webapp_feed_redesign_zerovideo": "str",
        "webapp_feed_redesign_retry": "str",
        "bc_likes": "str",
        "bc_comments": "str",
        "bc_shares": "str",
        "author": "str",
        "seo_aggre_see_more": "str",
        "seo_aggre_transcript_header": "str",
        "send_message": "str",
        "creatorCenter_content_actions": "str",
        "home_error_video_geofencing": "str",
        "music_detail_unavailable_2": "str",
        "qapage_webapp_error_subtitle": "str",
        "photo_post_unavailable_dec": "str",
        "disable_reuse_soundtrack_unavailable_page_body": "str",
        "poisharing_edgecase_one": "str",
        "poistore_detail_text": "str",
        "qa_reflow_page_empty_subtitle": "str",
        "ext_share_story_viewmore_btn": "str",
        "poisharing_cta_return": "str",
        "Couldn't find this account": "str",
        "Couldn't find this sound": "str",
        "disable_reuse_soundtrack_unavailable_mobile_body": "str",
        "embed_err_unavailable": "str",
        "Couldn't find this hashtag": "str",
        "desktop_error_video_geofencing": "str",
        "qa_page_reflow_page_blank_title": "str",
        "poisuggest_placeuna_title_1": "str",
        "err_feature_unavailable": "str",
        "playlist_unavailable": "str",
        "accessibilityLabels_forYou_videoCard_fullScreen": "str",
        "profile_page_pin": "str",
        "cover_notice_violation": "str",
        "official_tag": "str",
        "original_tag": "str",
        "seo_user_video_cover": "str",
        "or": "str",
        "accessibilityLabels_forYou_videoControls_videoProgress": "str",
        "accessibilityLabels_forYou_btn_comment": "str",
        "accessibilityLabels_feed_icon_favorite": "str",
        "comments": "str",
        "accessibilityLabels_forYou_videoControls_pause_btn": "str",
        "accessibilityLabels_forYou_videoControls_play_btn": "str",
        "pcWeb_firstTime_expand2_guide": "str",
        "accessibilityLabels_forYou_videoControls_volume_btn": "str",
        "accessibilityLabels_forYou_videoControls_report_btn": "str",
        "pc_web_scroll_header": "str",
        "pc_web_scroll_body": "str",
        "webapp_feed_redesign_allcomments": "str",
        "video_details_page_comment_field_cta": "str",
        "pc_web_less_btn": "str",
        "Expand": "str",
        "basicPoi_relatedTopics": "str",
        "playlist_webapp_creation_namePlaylist_characterCount_limit": "str",
        "yproject_playlist_name_toast": "str",
        "playlist_webapp_upload_nameplaylist_header": "str",
        "playlist_webapp_toast_error_vidlimit": "str",
        "playlist_webapp_selectvid_error_header": "str",
        "playlist_webapp_selectvid_error_desc": "str",
        "playlist_webapp_selectvid_header": "str",
        "playlist_webapp_selectvid_desc": "str",
        "playlist_webapp_selectvid_toast_alreadyadded": "str",
        "playlist_webapp_toast_error_cheatPlaylistCannotAdd": "str",
        "playlist_webapp_profileview_toast_vidremoved": "str",
        "pc_web_playpause_btn": "str",
        "pc_web_skip_forward_5_sec_btn": "str",
        "pc_web_skip_back_5_sec_btn": "str",
        "pc_web_muteunmute_btn": "str",
        "desktop_kb_shortcuts_tooltip_previous": "str",
        "desktop_kb_shortcuts_tooltip_next": "str",
        "start_time": "str",
        "discard": "str",
        "more": "str",
        "post_now": "str",
        "Follow": "str",
        "settings": "str",
        "end_live": "str",
        "follow": "str",
        "see_all": "str",
        "see_less": "str",
        "go_live": "str",
        "upload_fail": "str",
        "Search": "str",
        "inbox": "str",
        "select_file": "str",
        "load_error": "str",
        "privateAccountPrompt_manageAccount_privateAccount_title": "str",
        "privateAccountPrompt_account_permission_current_label": "str",
        "privateAccountPrompt_manageAccount_privateAccount_body": "str",
        "privateAccountPrompt_manageAccount_publicAccount_title": "str",
        "privateAccountPrompt_manageAccount_publicAccount_body2": "str",
        "privateAccountPrompt_stayPrivate_button": "str",
        "privateAccountPrompt_stayPublic_button": "str",
        "privateAccountPrompt_manageAccount_privateAccount_button2": "str",
        "privateAccountPrompt_switchPrivate_button": "str",
        "privateAccountPrompt_switchPublic_button": "str",
        "privateAccountPrompt_manageAccount_privateAccount_button3": "str",
        "privateAccountPrompt_manageAccount_privateAccount_button4": "str",
        "privateAccountPrompt_manageAccount_title": "str",
        "privateAccountPrompt_popUp_prompt_title": "str",
        "privateAccountPrompt_welcomePage_title": "str",
        "privateAccountPrompt_manageAccount_privateAccount_description3": "str",
        "privateAccountPrompt_popUp_prompt_description": "str",
        "privateAccountPrompt_account_permission_disclaimer": "str",
        "privateAccountPrompt_manageAccount_privateAccount_placeholder": "str",
        "pcWeb_miniPlayer_linkOpened_toast": "str",
        "pcWeb_miniPlayer_backToLogIn_toast": "str",
        "pcWeb_miniPlayer_linkCopied_toast": "str",
        "pcWeb_videoSkipped": "str",
        "pcWeb_NotSupportedFloating": "str",
        "pcWeb_NotSupportedMulti": "str",
        "TTweb_fyf_menuDownloadVideo_menuLink": "str",
        "TTweb_fyf_menuSendtoFriend_menuLink": "str",
        "TTweb_fyf_menuPictureinPicture_menuLink": "str",
        "changeRegistrationLocation_weakWarning_loseFeatures_toast": "str",
        "settings_privacy_interactions_comment": "str",
        "nonpersonalizedFeeds_feed_entrypoint_manageFeed": "str",
        "webAnalytics_videoDetail_viewPerformance": "str",
        "expansion_SEO_Vp": "str",
        "ls_view_details": "str",
        "webapp_mig_blocked": "str",
        "webapp_mig_unblocked": "str",
        "vid_mod_analytics_penalty_reason_minor_title": "str",
        "vid_mod_analytics_penalty_reason_minor_desc": "str",
        "vid_mod_analytics_penalty_reason_unoriginal_title": "str",
        "vid_mod_analytics_penalty_reason_unoriginal_desc": "str",
        "vid_mod_analytics_nr_vid_penalty_reason_unoriginal_title": "str",
        "vid_mod_analytics_nr_vid_penalty_reason_unoriginal_desc": "str",
        "vid_mod_analytics_nr_acct_penalty_reason_unoriginal_title": "str",
        "vid_mod_analytics_nr_acct_penalty_reason_unoriginal_desc": "str",
        "vid_mod_analytics_penalty_reason_spam_title": "str",
        "vid_mod_analytics_penalty_reason_spam_desc": "str",
        "vid_mod_analytics_penalty_reason_sexual_title": "str",
        "vid_mod_analytics_penalty_reason_sexual_desc": "str",
        "vid_mod_analytics_penalty_reason_tobacco_title": "str",
        "vid_mod_analytics_penalty_reason_tobacco_desc": "str",
        "vid_mod_analytics_penalty_reason_stunts_title": "str",
        "vid_mod_analytics_penalty_reason_stunts_desc": "str",
        "vid_mod_analytics_penalty_reason_graphic_title": "str",
        "vid_mod_analytics_penalty_reason_graphic_desc": "str",
        "vid_mod_analytics_penalty_reason_fyf_title": "str",
        "vid_mod_analytics_penalty_reason_fyf_desc": "str",
        "vidModAnalytics_detailPg_sectionHumanMod_sectionBody": "str",
        "vidModAnalytics_detailPg_sectionVideoDetails_sectionLabel": "str",
        "vidModAnalytics_detailPg_sectionDatePosted_sectionLabel": "str",
        "vid_mod_analytics_appeal_detailpg_reason_title": "str",
        "vid_mod_analytics_detail_pg_title": "str",
        "vid_mod_analytics_detail_pg_desc": "str",
        "vidModAnalytics_detailPg_sectionSuccess_header": "str",
        "vid_mod_analytics_appeal_success_detail_pg_desc": "str",
        "vid_mod_analytics_appeal_detail_pg_title": "str",
        "vid_mod_analytics_appeal_detail_pg_desc": "str",
        "vidModAnalytics_appealSubmitted_sectionTitle_header": "str",
        "vid_mod_analytics_appeal_rcv_detail_pg_desc": "str",
        "dsa_illegal_appeal_expired_header": "str",
        "dsa_illegal_appeal_expired_desc": "str",
        "dsa_illegal_appeal_button_ok": "str",
        "dsaCGWebapp_detailPg_sectionCG_body": "str",
        "dsaCGWebapp_detailPg_sectionCG_link": "str",
        "dsaCGWebapp_appealExpired_emptyState_body": "str",
        "appeal_btn_new": "str",
        "dsa_illegal_appeal_dropdown_title": "str",
        "dsa_illegal_appeal_explanation": "str",
        "dsa_illegal_appeal_alt_options": "str",
        "inbox_all_activity": "str",
        "system_notifications_inbox_channel_name_accountupdates": "str",
        "system_notifications_inbox_channel_name_tiktok": "str",
        "system_notifications_inbox_channel_name_creatormonetization": "str",
        "system_notifications_inbox_channel_name_adssupport": "str",
        "system_notifications_inbox_channel_name_businessaccount": "str",
        "promote_title": "str",
        "TTweb_inbox_systemNotificationchannel_brandActivity_name": "str",
        "TTweb_inbox_systemNotificationchannel_tiktokPlatform_name": "str",
        "TTweb_inbox_systemNotificationchannel_adsFeedback_name": "str",
        "TTweb_inbox_systemNotificationchannel_missions_name": "str",
        "system_notifications_inbox_channel_name_transactionassistant": "str",
        "TTweb_inbox_systemNotificationchannel_creatorProgram_name": "str",
        "system_notifications_inbox_channel_name_live": "str",
        "TTweb_inbox_systemNotificationchannel_screenTime_name": "str",
        "TTweb_inbox_systemNotificationchannel_mlbb_name": "str",
        "TTweb_inbox_systemNotificationchannel_series_name": "str",
        "TTweb_inbox_systemNotificationchannel_creatorMarketplace_name": "str",
        "TTweb_inbox_systemNotificationchannel_effects_name": "str",
        "report_inbox_status": "str",
        "report_inbox_inreview": "str",
        "report_inbox_violation": "str",
        "report_inbox_noviolation": "str",
        "dsa_report_pg_header": "str",
        "dsa_illegal_report_inbox_resubmit": "str",
        "tiktok_series_appeal_request_review_series_details_title": "str",
        "dailyscreentime_notifreminder_desc_minutes": "str",
        "familyPairing_dailyScreenTime_intervention_desc_minutes": "str",
        "dailyscreentime_notifreminder_desc_hours": "str",
        "familyPairing_dailyScreenTime_intervention_desc_hours": "str",
        "familyPairing_dailyScreenTime_intervention_desc_hoursMinutes": "str",
        "dailyscreentime_notifreminder_toast_incorrectpasscode": "str",
        "nightscreentimemgmt_sleepreminders_modal_readyforsleep_heading": "str",
        "nightscreentimemgmt_sleepreminders_modal_readyforsleep_firstreminder_desc": "str",
        "nightscreentimemgmt_sleepreminders_modal_readyforsleep_editreminder_link": "str",
        "nightscreentimemgmt_sleepreminders_modal_readyforsleep_ok_btn": "str",
        "nightscreentimemgmt_sleepreminders_modal_readyforsleep_delay_btn_variantone": "str",
        "screentime_breakreminder_modal_timetotakeabreak_title": "str",
        "screentime_breakreminder_modal_timetotakeabreak_desc_1": "str",
        "screentime_breakreminder_modal_editreminder_link": "str",
        "screentime_breakreminder_modal_ok_btn": "str",
        "screentime_breakreminder_modal_snooze_link": "str",
        "dailyscreentime_notifreminder_header_ready": "str",
        "familyPairing_dailyScreenTime_intervention_returnToTikTok_toast": "str",
        "dailyscreentime_notifreminder_button_returntotiktok": "str",
        "dailyscreentime_introsheet_minors_heading": "str",
        "dailyscreentime_introsheet_minors_firstbullet_logoff": "str",
        "dailyscreentime_introsheet_minors_secondbullet_settingsprivacy": "str",
        "dailyscreentime_introsheet_minors_firstbutton_gotit": "str",
        "dailyscreentime_introsheet_minors_secondbutton_manage": "str",
        "dailyscreentime_notifreminder_desc_hoursminutes": "str",
        "Got it": "str",
        "email_redesign_webapp_order_details_page_title": "str",
        "email_redesign_webapp_logistics_page_title": "str",
        "email_redesign_webapp_write_review_page_title": "str",
        "email_redesign_webapp_refund_detail_page_title": "str",
        "email_redesign_webapp_orders_title": "str",
        "email_redesign_webapp_vouchers_title": "str",
        "email_redesign_webapp_shopping_cart_title": "str",
        "seller_messages_email_webapp_reply_title": "str",
        "seller_messages_email_webapp_mute_title": "str",
        "seller_messages_email_webapp_setting_title": "str",
        "Ecom_email_pc_shoptab_homepage_title": "str",
        "Ecom_email_pc_pdp_shoptab_homepage_title": "str",
        "Ecom_email_pc_deal_page_shoptab_homepage_title": "str",
        "Ecom_email_pc_pdp_title": "str",
        "Ecom_email_pc_coupon_add_on_title": "str",
        "Ecom_email_pc_free_shipping_add_on_page_title": "str",
        "email_redesign_webapp_order_details_page_context": "str",
        "email_redesign_webapp_logistics_page_context": "str",
        "email_redesign_webapp_write_review_page_context": "str",
        "email_redesign_webapp_refund_detail_page_context": "str",
        "email_redesign_webapp_orders_context": "str",
        "email_redesign_webapp_vouchers_context": "str",
        "email_redesign_webapp_shopping_cart_context": "str",
        "seller_messages_email_webapp_reply_desc": "str",
        "seller_messages_email_webapp_mute_desc": "str",
        "seller_messages_email_webapp_setting_desc": "str",
        "Ecom_email_pc_shoptab_homepage_description": "str",
        "Ecom_email_pc_pdp_shoptab_homepage_description": "str",
        "Ecom_email_pc_deal_page_shoptab_homepage_description": "str",
        "Ecom_email_pc_pdp_description": "str",
        "Ecom_email_pc_coupon_add_on_description": "str",
        "Ecom_email_pc_free_shipping_add_on_page_description": "str",
        "terms": "str",
        "copyright": "str",
        "Legal": "str",
        "Privacy Policy": "str",
        "help": "str",
        "safety": "str",
        "privacyCenter_webFooter_resourcesPrivacy_navLink": "str",
        "help_center_creator_portal": "str",
        "Community Guidelines": "str",
        "hca_web_Company": "str",
        "hca_web_Program": "str",
        "hca_web_TermsAndPolicies": "str",
        "auto_play": "str",
        "for_you": "str",
        "TikTok i18n title": "str",
        "accessibilityLabels_forYou_nav_tiktok_btn": "str",
        "following_my_empty_desc": "str",
        "followers_my_empty_desc": "str",
        "common_registration_username_suggested": "str",
        "profile_suggested_empty_toast": "str",
        "feed_caption_see_more": "str",
        "desktop_logged_in_profile": "str",
        "sidenav_follow_hint": "str",
        "Discover": "str",
        "tteh_webapp_acquisitionBanner_1": "str",
        "tteh_webapp_acquisitionBanner_2": "str",
        "hca_web_Channels": "str",
        "pm_mt_obs_revoke_desc": "str",
        "pm_mt_revoke_duration": "str",
        "pm_mt_modal_revoke_confirm_btn": "str",
        "webLIVE_enableEvent_LIVEPage_eventStartNowReminder": "str",
        "webLIVE_enableEvent_LIVEPage_eventReminder": "str",
        "live_on_status": "str",
        "sidenav_login_cta": "str",
        "pc_web_explore_main_header": "str",
        "Profile": "str",
        "nonpersonalizedFeeds_LIVEfeed_navP_menuLink": "str",
        "pc_web_column_mode_tooltip": "str",
        "pc_web_browser_mode_btn": "str",
        "pc_web_column_mode_btn": "str",
        "network_error_title": "str",
        "network_error_sub": "str",
        "accessibilityLabels_home_skipContentFeed": "str",
        "accessibilityLabels_forYou_nav_messages_btn": "str",
        "wbs_goto_bc_modal_feature3_title": "str",
        "wbs_goto_bc_modal_feature3_content": "str",
        "wbs_goto_bc_modal_feature1_title": "str",
        "wbs_goto_bc_modal_feature1_content": "str",
        "wbs_goto_bc_modal_title": "str",
        "wbs_goto_bc_modal_btn": "str",
        "pc_web_dark_mode_popup_header": "str",
        "pc_web_dark_mode_popup_body": "str",
        "desktop_app_downloadPopup_header": "str",
        "pcWeb_desktopApp_maintainPopup_body": "str",
        "desktop_app_downloadPopup_cta": "str",
        "desktop_app_upToDate_toast": "str",
        "desktop_app_tab_settings": "str",
        "desktop_app_tab_updateTikTok": "str",
        "dsa_illegal_more_options_link": "str",
        "report_inbox_video": "str",
        "report_inbox_comment": "str",
        "report_inbox_account": "str",
        "report_inbox_live": "str",
        "report_inbox_livecomment": "str",
        "report_inbox_directmessage": "str",
        "report_inbox_sound": "str",
        "report_inbox_hashtag": "str",
        "shoutouts_detail_comment_report_title": "str",
        "tns_intro_reporter_title": "str",
        "profile_page_events_list": "str",
        "qareport_question": "str",
        "report_inbox_title": "str",
        "inbox_default_text": "str",
        "Inbox_Comments_on_your_videos": "str",
        "Inbox_When_someone_comments_on__one_of_your_videos_you_ll_see_it_here": "str",
        "Inbox_New_followers": "str",
        "Inbox_When_someone_new_follows_you_you_ll_see_it_here": "str",
        "Inbox_Likes_on_your_videos": "str",
        "Inbox_When_someone_likes_one_of_your_videos_you_ll_see_it_here": "str",
        "Inbox_Mentions_of_You": "str",
        "Inbox_When_someone_mentions_you_you_ll_see_it_here": "str",
        "Inbox_replied_to_your_comment": "str",
        "Inbox_commented": "str",
        "inbox_videoreply": "str",
        "Inbox_created_a_duet_with_you": "str",
        "Inbox_is_following_you": "str",
        "Inbox_started_following_you": "str",
        "photomode_inbox_liked": "str",
        "Inbox_liked_your_video": "str",
        "Inbox_liked_your_comment": "str",
        "Inbox_and": "str",
        "Inbox_others": "str",
        "in_app_push_mention_in_photo": "str",
        "Inbox_mentioned_you_in_a_video": "str",
        "Inbox_mentioned_you_in_a_comment": "str",
        "system_notifications_inbox_header": "str",
        "inbox_request_accept": "str",
        "Inbox_Follow_requests": "str",
        "Inbox_Today": "str",
        "Inbox_Yesterday": "str",
        "Inbox_This_Week": "str",
        "Inbox_This_Month": "str",
        "Inbox_Previous": "str",
        "Inbox_All": "str",
        "Inbox_Likes": "str",
        "Inbox_Comments": "str",
        "Inbox_Mentions": "str",
        "Inbox_Notifications": "str",
        "system_notifications_details_button": "str",
        "accessibilityLabels_forYou_btn_inbox": "str",
        "Inbox": "str",
        "live_creator_hub_home_desc": "str",
        "editprofile_feedtooltip_title": "str",
        "editprofile_feedtooltip_subtitle": "str",
        "tiktok_series_webapp_tooltip_get_started": "str",
        "accessibilityLabels_forYou_nav_language_back_btn": "str",
        "desktop_kb_shortcuts_menu": "str",
        "accessibilityLabels_settings_darkModeOn": "str",
        "accessibilityLabels_settings_darkModeOff": "str",
        "View profile": "str",
        "tiktok_series_webapp_option": "str",
        "ls_live_studio": "str",
        "web_business_suite_entry": "str",
        "live_center_title": "str",
        "live_creator_hub_name": "str",
        "desktop_app_accountSettings": "str",
        "accessibilityLabels_settings_language": "str",
        "pc_web_dark_mode": "str",
        "login_fb_noLonger_LogInEase": "str",
        "Log_out_sheet_2": "str",
        "login_fb_confirmLogOut_body": "str",
        "login_fb_confirmLogOut_stay_cta": "str",
        "scheduler_welcome_tooltip_title": "str",
        "scheduler_welcome_tooltip_des": "str",
        "tenMinPlusUpload_webPage_introduceToolTip_title": "str",
        "tenMinPlusUpload_webPage_introduceToolTip_body": "str",
        "new_feature_guidance_Upload": "str",
        "podcasts_linkFullEpisodes_linkPodcastPage_tooltip": "str",
        "accessibilityLabels_forYou_nav_upload_btn": "str",
        "accessibilityLabels_forYou_nav_settings_btn": "str",
        "push_popup_title": "str",
        "push_popup_content": "str",
        "push_popup_btn1": "str",
        "push_popup_btn2": "str",
        "about_this_ad_fallback_description1": "str",
        "about_this_ad_fallback_more_info_hyperlink_2": "str",
        "about_this_ad_fallback_adjust_settings": "str",
        "settings_updated": "str",
        "Settings_ads_page_adpersonalization_title": "str",
        "Adv_settings_warning_text": "str",
        "Adv_settings_warning_description": "str",
        "Adv_settings_page_help_text": "str",
        "Adv_settings_page_hide_adv_title": "str",
        "inbox_follow_failed_banned": "str",
        "inbox_follow_failed_noconnection": "str",
        "inbox_follow_failed_other": "str",
        "GENERAL": "str",
        "Explore": "str",
        "TRENDING": "str",
        "search_Submission_Failed_tips": "str",
        "sug_report_relevant": "str",
        "view_all_results": "str",
        "accessibilityLabels_search_suggestions": "str",
        "embed_music_card_see_more": "str",
        "web_search_clear_btn": "str",
        "personalisedSearch_searchResults_searchBlankPage_manageSearchLabel": "str",
        "web_search_recent_header": "str",
        "search_feedback_success_tips1": "str",
        "Web_report_report_detail": "str",
        "avia_law_report_received_confirm": "str",
        "dailyscreentime_featurescreen_toast_editedtime": "str",
        "screenTime_screenTimeBreaks_manageTime_editBreak_toast": "str",
        "error_toast": "str",
        "screenTime_sleepReminders_setSleepTime_toast": "str",
        "nightscreentimemgmt_sleepreminders_toast_editsleeptime": "str",
        "family_safety_mode_locked_mode_indicator": "str",
        "screentimedash_digitalwellbeing_dailyscreentime_desc": "str",
        "Web_report_block_who": "str",
        "Web_report_block_detail": "str",
        "copyright_check_post_popup_cancel": "str",
        "km_report_question": "str",
        "km_pick_reason": "str",
        "choosepassword_button": "str",
        "Web_report_description_NetzDG": "str",
        "Signature": "str",
        "Sign_here": "str",
        "Report_confirmation": "str",
        "avia_law_false_report_warning": "str",
        "Web_report_description_tips": "str",
        "Web_report_you_can_also": "str",
        "dsa_illegal_report_trustedflaggerlink": "str",
        "dsa_illegal_report_trustedflagger": "str",
        "dsa_report_penalty_reminder": "str",
        "dsa_illegal_report_email": "str",
        "dsa_illegal_report_fill_email": "str",
        "dsa_illegal_report_trustedflagger_fill_email": "str",
        "dsa_illegal_detail_country": "str",
        "dsa_illegal_detail_law": "str",
        "dsa_illegal_cite_law_desc": "str",
        "dsa_illegal_detail_explanation": "str",
        "dsa_illegal_report_explanation_desc": "str",
        "dsa_illegal_appeal_signature": "str",
        "dsa_illegal_sign_legal_name": "str",
        "dsa_illegal_confirm_accuracy": "str",
        "dsa_illegal_report_trustedflagger_email": "str",
        "dsa_illegal_select_region": "str",
        "Web_report_account_impersonated_search": "str",
        "Web_report_account_impersonated": "str",
        "Web_report_account_impersonated_description": "str",
        "dsa_illegal_select_country_optional": "str",
        "dailyscreentime_featurescreen_desc_balanceyourday": "str",
        "dailyscreentime_featurescreen_firstbullet_settime": "str",
        "dailyscreentime_featurescreen_firstbullet_settime_desc_choose": "str",
        "dailyscreentime_featurescreen_secondbullet_getnotified": "str",
        "dailyscreentime_featurescreen_secondbullet_getnotified_desc_close": "str",
        "screenTime_web_dailyscreentime_mainSetting_toggle_desc": "str",
        "customizeSTM_screenTimeLimit_option_sameLimit": "str",
        "screenTime_web_setting_customTime_option": "str",
        "customizeSTM_screenTimeLimit_option_customLimit": "str",
        "screenTime_web_dailyscreentime_manageTime_modal_done_btn": "str",
        "nightscreentimemgmt_setsleeptime_halfsheet_am_desc": "str",
        "nightscreentimemgmt_setsleeptime_halfsheet_pm_desc": "str",
        "nightscreentimemgmt_sleepreminders_sleeptime_on_secondline_teens": "str",
        "nightscreentimemgmt_sleepreminders_sleeptime_on_secondline_adults": "str",
        "nightscreentimemgmt_sleepreminders_defaultscreen_desc": "str",
        "nightscreentimemgmt_sleepreminders_defaultscreen_setsleeptimebullet_title": "str",
        "nightscreentimemgmt_sleepreminders_defaultscreen_setsleeptimebullet_desc": "str",
        "nightscreentimemgmt_sleepreminders_defaultscreen_pushnotifsbullet_title": "str",
        "nightscreentimemgmt_sleepreminders_defaultscreen_pushnotifsbullet_teens_desc": "str",
        "nightscreentimemgmt_sleepreminders_defaultscreen_pushnotifsbullet_adults_desc": "str",
        "screenTime_web_sleepReminders_mainSetting_toggle_desc": "str",
        "screentime_settings_screentimebreaks_intro_desc": "str",
        "screentime_settings_screentimebreaks_intro_schedulebreaks_heading": "str",
        "screentime_settings_screentimebreaks_actionsheet_desc_returninguser": "str",
        "screentime_settings_screentimebreaks_intro_tailoryourexp_heading": "str",
        "screentime_settings_screentimebreaks_intro_tailoryourexp_desc": "str",
        "screenTime_web_screenTimeBreaks_mainSetting_toggle_desc": "str",
        "pcWeb_guestLogin_contToVideo": "str",
        "pcWeb_guestLogin_guest": "str",
        "unit_week": "str",
        "unit_day": "str",
        "unit_hr": "str",
        "unit_min": "str",
        "unit_sec": "str",
        "time_ago": "str",
        "syntheticMedia_feed_bottomBanner_AIGCLabel": "str",
        "AIGC_FYP_descSection_label": "str",
        "pcWeb_autoScroll_on": "str",
        "pcWeb_autoScroll_off": "str",
        "desktop_kb_shortcuts_tooltip_like_vid": "str",
        "desktop_kb_shortcuts_tooltip_mute_unmute_vid": "str",
        "desktop_kb_shortcuts_modal": "str",
        "desktop_kb_shortcuts_tooltip_title": "str",
        "link_close_popup": "str",
        "bc_disclosure_tag_ecommerce_us": "str",
        "bc_disclosure_tag_ecommerce_uk": "str",
        "bc_new_disclosure": "str",
        "tcm_closedLoop_commercialContent_brandOrganic_videoTag": "str",
        "scm_label_and_appeal_modal_title": "str",
        "scm_label_and_appeal_modal_desc": "str",
        "scm_label_and_appeal_modal_button_learn_more": "str",
        "scm_label_and_appeal_modal_button_dismiss": "str",
        "ttba_ob_switchouterr_title": "str",
        "ttba_ob_switchouterr_title_lttfb": "str",
        "ttba_ob_switchouterr_title_lmp": "str",
        "ttba_ob_switchouterr_title_seller": "str",
        "ttba_ob_switchouterr_subtext": "str",
        "ttba_ob_switchouterr_subtext_lttfb": "str",
        "ttba_ob_switchouterr_subtext_lmp": "str",
        "ttba_ob_switchouterr_subtext_seller": "str",
        "switched_to_personal": "str",
        "add_windows_store_badge_download_app_stores": "str",
        "add_windows_store_badge_get_tiktok_app": "str",
        "add_windows_store_badge_scan_qr": "str",
        "engagement": "str",
        "direct_meaasge_sending_ban_feedback_again": "str",
        "nonpersonalizedFeeds_LIVEfeed_label_mainString_personalizationOn": "str",
        "nonpersonalizedFeeds_LIVEfeed_label_mainString": "str",
        "nonpersonalizedFeeds_turnOff_modal_toggle_bodyFull": "str",
        "nonpersonalizedFeeds_turnOn_modal_toggle_bodyFull": "str",
        "personalisedSearch_searchResults_actionSheet_bodyPara1": "str",
        "personalisedSearch_searchResults_actionSheet_bodyPara1V2": "str",
        "nonpersonalizedFeeds_turnOn_modal_toggle_headline": "str",
        "personalisedSearch_searchResults_actionSheet_header": "str",
        "personalisedSearch_searchResults_actionSheet_bodyPara2Bold1": "str",
        "nonpersonalizedFeeds_settings_contentPreferences_entrypoint": "str",
        "personalisedSearch_searchResults_actionSheet_toggle": "str",
        "personalisedSearch_searchResults_actionSheet_btn": "str",
        "search_videosearchbar_recommended_generic_1": "str",
        "please_input_search_keyword": "str",
        "seo_serp_expansion_num1": "str",
        "seo_aggre_metadesc2": "str",
        "SERP discover title": "str",
        "TikTok i18n keywords": "str",
        "SEO_discover_title": "str",
        "SEO_discover_desc": "str",
        "SEO_following_title": "str",
        "SEO_following_desc": "str",
        "hashtag_SEO_title2": "str",
        "hashtag_SEO_desc1": "str",
        "err_tag": "str",
        "SEO_qa_title_1": "str",
        "SEO_qa_desc_1": "str",
        "SEO_search_title": "str",
        "SEO_search_desc": "str",
        "SEO_Recharge_title": "str",
        "SEO_Recharge_desc": "str",
        "SEO_live_title": "str",
        "SEO_live_discover_title": "str",
        "SEO_live_discover_desc": "str",
        "SEO_live_desc": "str",
        "SEO_live_desc2": "str",
        "playlist_sharing_metatitle": "str",
        "playlist_sharing_metadescription": "str",
        "SEO_foryou_animals_title": "str",
        "SEO_foryou_animals_desc": "str",
        "SEO_foryou_beauty_title": "str",
        "SEO_foryou_beauty_desc": "str",
        "SEO_foryou_comedy_title": "str",
        "SEO_foryou_comedy_desc": "str",
        "SEO_foryou_dance_title": "str",
        "SEO_foryou_dance_desc": "str",
        "SEO_foryou_food_title": "str",
        "SEO_foryou_food_desc": "str",
        "SEO_foryou_gaming_title": "str",
        "SEO_foryou_gaming_desc": "str",
        "SEO_foryou_sports_title": "str",
        "SEO_foryou_sports_desc": "str",
        "share_live_event_title": "str",
        "share_live_event_desc": "str",
        "playlist_share_title": "str",
        "playlist_share_desc": "str",
        "user_SEO_official_title1": "str",
        "user_SEO_title1": "str",
        "share_effect_title": "str",
        "share_sticker_desc": "str",
        "share_sticker_preset": "str",
        "shared_collection_other_apps_title": "str",
        "shared_collection_other_apps_description": "str",
        "pm_mt_ls_download_button": "str",
        "TikTok | Make Your Day": "str",
        "serp_following_title": "str",
        "serp_following_desc": "str",
        "pc_web_skip_forward_5_sec": "str",
        "pc_web_skip_backward_5_sec": "str",
        "requested": "str",
        "Public": "str",
        "webapp_forYoufeed_videoRemoved_toast": "str",
        "QR CODE Text": "str",
        "pc_reflow_download": "str",
        "Get": "str",
        "seo_aggre_metadesc1": "str",
        "TikTok Trends": "str",
        "TikTok Trending": "str",
        "Trending Videos": "str",
        "Trending Hashtags": "str",
        "SEO_trending_title": "str",
        "SEO_trending_desc": "str",
        "seo_serp_hashtag_title": "str",
        "seo_serp_hashtag_desc": "str",
        "seo_serp_hashtag_desc1": "str",
        "TikTok i18n keywords for home": "str",
        "seo_serp_expansion_title": "str",
        "seo_serp_music_title": "str",
        "seo_serp_music_desc3": "str",
        "seo_serp_music_desc": "str",
        "seo_serp_music_desc1": "str",
        "seo_serp_music_desc2": "str",
        "err_sound": "str",
        "err_sound_copy": "str",
        "basicPoi_task2_metaTdk_title": "str",
        "basicPoi_task2_metaTdk_desc": "str",
        "basicPoi_task2_metaTdk_keyword": "str",
        "basicPoi_metaTdk_title": "str",
        "basicPoi_metaTdk_regional_desc": "str",
        "basicPoi_metaTdk_store_desc": "str",
        "basicPoi_metaTdk_keyword": "str",
        "basicPoi_metaTdk_storeSite": "str",
        "poidetails_tiktokplaces": "str",
        "poidetails_location_name_placehldtwo": "str",
        "music_SEO_desc3": "str",
        "seo_serp_user2_title": "str",
        "seo_serp_user1_title": "str",
        "seo_serp_user_desc": "str",
        "seo_serp_user_desc1": "str",
        "seo_serp_user_desc2": "str",
        "seo_serp_user_desc3": "str",
        "err_user": "str",
        "err_user_private": "str",
        "seo_serp_videotxt_desc1": "str",
        "seo_serp_videotxt_desc2": "str",
        "seo_serp_videotxt_desc3": "str",
        "seo_serp_searchQuery_desc": "str",
        "seo_serp_musicName_desc": "str",
        "serp_videoText_searchQuery_title": "str",
        "serp_videoText_searchQuery_title2": "str",
        "seo_serp_videotxt_title": "str",
        "seo_serp_videotxt_title2": "str",
        "err_vid_geo": "str",
        "err_vid": "str",
        "subVideo_outApp_sharing_title": "str",
        "basicPoi_toDoList_region": "str",
        "basicPoi_toDoList": "str",
        "seo_popular_sightseeing": "str",
        "basicPoi_sightSeeing": "str",
        "basicPoi_outdoorActivities": "str",
        "basicPoi_nightLife": "str",
        "basicPoi_familyFriendly": "str",
        "basicPoi_bestRestaurant_region": "str",
        "basicPoi_foodNDrinks": "str",
        "seo_popular_restaurant": "str",
        "basicPoi_brunchRestaurants": "str",
        "basicPoi_fineDining": "str",
        "basicPoi_seaFood": "str",
        "basicPoi_veganRestaurants": "str",
        "basicPoi_hotels_region": "str",
        "basicPoi_hotels": "str",
        "seo_popular_hotel": "str",
        "basicPoi_downtownHotels": "str",
        "basicPoi_petFriendly": "str",
        "basicPoi_airbnbs": "str",
        "basicPoi_luxuryHotels": "str",
        "basicPoi_parks_region": "str",
        "basicPoi_parks": "str",
        "seo_popular_park": "str",
        "basicPoi_amusementParks": "str",
        "basicPoi_dogParks": "str",
        "basicPoi_skateParks": "str",
        "basicPoi_indoorParks": "str",
        "basicPoi_shopping_region": "str",
        "basicPoi_shopping": "str",
        "seo_popular_shoppingMall": "str",
        "basicPoi_shoppingMalls": "str",
        "basicPoi_downtownShopping": "str",
        "basicPoi_vintageShopping": "str",
        "basicPoi_giftShops": "str",
    },
)


class WebappDotI18nDashTranslation(TypedDict):
    Webapp: Webapp


class Parameters1(TypedDict):
    add_info_card_seo: WebappSwitchAccount
    add_transcript_seo: WebappSwitchAccount
    user_more_related_video: WebappSwitchAccount
    user_page_serp_compliance: WebappSwitchAccount


class SeoDotAbtest(TypedDict):
    canonical: str
    pageId: str
    vidList: List[str]
    parameters: Parameters1


class Commerceuserinfo(TypedDict):
    commerceUser: bool


class Profiletab(TypedDict):
    showMusicTab: bool
    showQuestionTab: bool
    showPlayListTab: bool


class User(TypedDict):
    id: str
    shortId: str
    uniqueId: str
    nickname: str
    avatarLarger: str
    avatarMedium: str
    avatarThumb: str
    signature: str
    createTime: int
    verified: bool
    secUid: str
    ftc: bool
    relation: int
    openFavorite: bool
    commentSetting: int
    commerceUserInfo: Commerceuserinfo
    duetSetting: int
    stitchSetting: int
    privateAccount: bool
    secret: bool
    isADVirtual: bool
    roomId: str
    uniqueIdModifyTime: int
    ttSeller: bool
    region: str
    downloadSetting: int
    profileTab: Profiletab
    followingVisibility: int
    recommendReason: str
    nowInvitationCardUrl: str
    nickNameModifyTime: int
    isEmbedBanned: bool
    canExpPlaylist: bool
    profileEmbedPermission: int
    language: str
    eventList: List
    suggestAccountBind: bool


class Stats(TypedDict):
    followerCount: int
    followingCount: int
    heart: int
    heartCount: int
    videoCount: int
    diggCount: int
    friendCount: int


class Userinfo(TypedDict):
    user: User
    stats: Stats
    itemList: List


class Sharemeta(TypedDict):
    title: str
    desc: str


class WebappDotUserDashDetail(TypedDict):
    userInfo: Userinfo
    shareMeta: Sharemeta
    statusCode: int
    statusMsg: str
    needFix: bool


class WebappDotADashB(TypedDict):
    b_c: str


_DefaultScope = TypedDict(
    "_DefaultScope",
    {
        "webapp.app-context": WebappDotAppDashContext,
        "webapp.biz-context": WebappDotBizDashContext,
        "webapp.i18n-translation": WebappDotI18nDashTranslation,
        "seo.abtest": SeoDotAbtest,
        "webapp.user-detail": WebappDotUserDashDetail,
        "webapp.a-b": WebappDotADashB,
    },
)


class Root(TypedDict):
    __DEFAULT_SCOPE__: _DefaultScope
