from .bandcamp import Bandcamp
from .booth import Booth
from .fanbox import Fanbox
from .instagram import Instagram
from .linktree import Linktree
from .litlink import LitLink
from .mirrativ import Mirrativ
from .nicovideo import Nicovideo
from .note import Note
from .pixiv import Pixiv
from .reddit import Reddit
from .sketch import Sketch
from .soundcloud import Soundcloud
from .tiktok import TikTok
from .twitcasting import TwitCasting
from .twitch import Twitch
from .twitter import Twitter
from .youtube import Youtube
from .spotify import Spotify
from .github import Github
from .itchio import Itchio
from .kofi import Kofi
from .patreon import Patreon

__all__ = [
    "Bandcamp",
    "Booth",
    "Fanbox",
    "Instagram",
    "Linktree",
    "LitLink",
    "Mirrativ",
    "Nicovideo",
    "Note",
    "Pixiv",
    "Reddit",
    "Sketch",
    "Soundcloud",
    "TikTok",
    "TwitCasting",
    "Twitch",
    "Twitter",
    "Youtube",
    "Spotify",
    "Github",
    "Itchio",
    "Kofi",
    "Patreon",
]

SERVICES = {
    Bandcamp(),
    Booth(),
    Fanbox(),
    Instagram(),
    Linktree(),
    LitLink(),
    Mirrativ(),
    Nicovideo(),
    Note(),
    Pixiv(),
    Reddit(),
    Sketch(),
    Soundcloud(),
    TikTok(),
    TwitCasting(),
    Twitch(),
    Twitter(),
    Youtube(),
    Spotify(),
    Github(),
    Itchio(),
    Kofi(),
    Patreon(),
}
