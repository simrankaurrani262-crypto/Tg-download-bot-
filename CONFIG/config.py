"""
Render-friendly config — all required values are read from environment variables.
Copy .env.example to .env for local development, or set env vars in Render dashboard.
"""
import os

from CONFIG.commands import CommandsConfig
from CONFIG.messages import Messages, safe_get_messages
from CONFIG.domains import DomainsConfig
from CONFIG.limits import LimitsConfig


def _int(name, default=0):
    try:
        return int(os.environ.get(name, ""))
    except (ValueError, TypeError):
        return default


def _int_list(name, default=None):
    """Parse a comma-separated list of integers, e.g. '123456,789012'"""
    val = os.environ.get(name, "").strip()
    if not val:
        return default or []
    result = []
    for part in val.split(","):
        try:
            result.append(int(part.strip()))
        except (ValueError, TypeError):
            pass
    return result


def _str(name, default=""):
    return os.environ.get(name, default)


def _bool(name, default=False):
    val = os.environ.get(name, "").strip().lower()
    if val in ("1", "true", "yes"):
        return True
    if val in ("0", "false", "no"):
        return False
    return default


class Config(object):
    # -------------------------------------------------------
    # REQUIRED
    # -------------------------------------------------------
    BOT_NAME = _str("BOT_NAME", "tgytdlp_bot")
    BOT_NAME_FOR_USERS = _str("BOT_NAME_FOR_USERS", _str("BOT_NAME", "tgytdlp_bot"))

    # Telegram Pyrogram credentials — get from https://my.telegram.org
    API_ID = _int("API_ID")
    API_HASH = _str("API_HASH")

    # Bot token from @BotFather
    BOT_TOKEN = _str("BOT_TOKEN")

    # Admin user IDs — comma-separated list of integers
    ADMIN = _int_list("ADMIN")
    ADMIN_USERNAME = _str("ADMIN_USERNAME", "@")

    # Groups that bypass limits (comma-separated negative ints)
    ADMIN_GROUP = _int_list("ADMIN_GROUP")
    ALLOWED_GROUP = _int_list("ALLOWED_GROUP")

    # Logging channels — can all point to the same channel
    LOGS_ID = _int("LOGS_ID")
    LOGS_VIDEO_ID = _int("LOGS_VIDEO_ID") or _int("LOGS_ID")
    LOGS_NSFW_ID = _int("LOGS_NSFW_ID") or _int("LOGS_ID")
    LOGS_IMG_ID = _int("LOGS_IMG_ID") or _int("LOGS_ID")
    LOGS_PAID_ID = _int("LOGS_PAID_ID") or _int("LOGS_ID")
    LOG_EXCEPTION = _int("LOG_EXCEPTION") or _int("LOGS_ID")

    # Subscription channel
    SUBSCRIBE_CHANNEL = _int("SUBSCRIBE_CHANNEL")
    SUBSCRIBE_CHANNEL_URL = _str("SUBSCRIBE_CHANNEL_URL", "")

    # Mini-app URL (optional)
    MINIAPP_URL = _str("MINIAPP_URL", "")

    # Session string for reading admin logs channel (optional)
    CHANNEL_GUARD_SESSION_STRING = _str("CHANNEL_GUARD_SESSION_STRING", "")

    # -------------------------------------------------------
    # FIREBASE (optional — disabled by default)
    # -------------------------------------------------------
    USE_FIREBASE = _bool("USE_FIREBASE", False)
    BOT_DB_PATH = _str("BOT_DB_PATH", f"bot/{_str('BOT_NAME_FOR_USERS', 'tgytdlp_bot')}/")
    VIDEO_CACHE_DB_PATH = _str("VIDEO_CACHE_DB_PATH", "bot/video_cache")
    PLAYLIST_CACHE_DB_PATH = _str("PLAYLIST_CACHE_DB_PATH", "bot/video_cache/playlists")
    IMAGE_CACHE_DB_PATH = _str("IMAGE_CACHE_DB_PATH", "bot/video_cache/images")

    FIREBASE_USER = _str("FIREBASE_USER", "")
    FIREBASE_PASSWORD = _str("FIREBASE_PASSWORD", "")
    FIREBASE_CONF = {
        "apiKey": _str("FIREBASE_API_KEY", ""),
        "authDomain": _str("FIREBASE_AUTH_DOMAIN", ""),
        "projectId": _str("FIREBASE_PROJECT_ID", ""),
        "storageBucket": _str("FIREBASE_STORAGE_BUCKET", ""),
        "messagingSenderId": _str("FIREBASE_MESSAGING_SENDER_ID", ""),
        "appId": _str("FIREBASE_APP_ID", ""),
        "databaseURL": _str("FIREBASE_DATABASE_URL", ""),
    }

    # Optional: path to Firebase service account JSON file
    FIREBASE_SERVICE_ACCOUNT = _str("FIREBASE_SERVICE_ACCOUNT", "")

    FIREBASE_CACHE_FILE = _str("FIREBASE_CACHE_FILE", "dump.json")
    RELOAD_CACHE_EVERY = _int("RELOAD_CACHE_EVERY", 1)
    DOWNLOAD_FIREBASE_SCRIPT_PATH = "DATABASE/download_firebase.py"
    AUTO_CACHE_RELOAD_ENABLED = _bool("AUTO_CACHE_RELOAD_ENABLED", True)

    # -------------------------------------------------------
    # COOKIE URLS (optional — needed for age-restricted / private content)
    # -------------------------------------------------------
    COOKIE_URL = _str("COOKIE_URL", "")
    YOUTUBE_COOKIE_URL = _str("YOUTUBE_COOKIE_URL", "")
    YOUTUBE_COOKIE_URL_1 = _str("YOUTUBE_COOKIE_URL_1", "")
    YOUTUBE_COOKIE_URL_2 = _str("YOUTUBE_COOKIE_URL_2", "")
    YOUTUBE_COOKIE_URL_10 = _str("YOUTUBE_COOKIE_URL_10", "")
    YOUTUBE_COOKIE_ORDER = _str("YOUTUBE_COOKIE_ORDER", "round_robin")
    YOUTUBE_COOKIE_TEST_URL = _str(
        "YOUTUBE_COOKIE_TEST_URL",
        "https://www.youtube.com/watch?v=_GuOjXYl5ew"
    )
    INSTAGRAM_COOKIE_URL = _str("INSTAGRAM_COOKIE_URL", "")
    TIKTOK_COOKIE_URL = _str("TIKTOK_COOKIE_URL", "")
    FACEBOOK_COOKIE_URL = _str("FACEBOOK_COOKIE_URL", "")
    TWITTER_COOKIE_URL = _str("TWITTER_COOKIE_URL", "")
    VK_COOKIE_URL = _str("VK_COOKIE_URL", "")

    COOKIE_FILE_PATH = "TXT/cookie.txt"
    PIC_FILE_PATH = "pic.jpg"

    # -------------------------------------------------------
    # PROXY (optional)
    # -------------------------------------------------------
    PROXY_TYPE = _str("PROXY_TYPE", "http")
    PROXY_IP = _str("PROXY_IP", "")
    PROXY_PORT = _int("PROXY_PORT", 3128)
    PROXY_USER = _str("PROXY_USER", "")
    PROXY_PASSWORD = _str("PROXY_PASSWORD", "")

    PROXY_2_TYPE = _str("PROXY_2_TYPE", "socks5")
    PROXY_2_IP = _str("PROXY_2_IP", "")
    PROXY_2_PORT = _int("PROXY_2_PORT", 3128)
    PROXY_2_USER = _str("PROXY_2_USER", "")
    PROXY_2_PASSWORD = _str("PROXY_2_PASSWORD", "")

    PROXY_SELECT = _str("PROXY_SELECT", "round_robin")

    # -------------------------------------------------------
    # PO TOKEN PROVIDER (YouTube anti-bot bypass)
    # -------------------------------------------------------
    YOUTUBE_POT_ENABLED = _bool("YOUTUBE_POT_ENABLED", False)
    YOUTUBE_POT_BASE_URL = _str("YOUTUBE_POT_BASE_URL", "http://localhost:4416")
    YOUTUBE_POT_DISABLE_INNERTUBE = _bool("YOUTUBE_POT_DISABLE_INNERTUBE", False)

    # -------------------------------------------------------
    # DASHBOARD (optional internal web dashboard)
    # -------------------------------------------------------
    DASHBOARD_PORT = _int("DASHBOARD_PORT", 5555)
    DASHBOARD_USERNAME = _str("DASHBOARD_USERNAME", "admin")
    DASHBOARD_PASSWORD = _str("DASHBOARD_PASSWORD", "admin123")
    ACTIVE_SESSIONS_FILE = "CONFIG/.active_sessions.json"

    STAR_RECEIVER = _int("STAR_RECEIVER", 0)

    # -------------------------------------------------------
    # COMMANDS (from CommandsConfig — do not change)
    # -------------------------------------------------------
    DOWNLOAD_COOKIE_COMMAND = CommandsConfig.DOWNLOAD_COOKIE_COMMAND
    PROXY_COMMAND = CommandsConfig.PROXY_COMMAND
    SUBS_COMMAND = CommandsConfig.SUBS_COMMAND
    CHECK_COOKIE_COMMAND = CommandsConfig.CHECK_COOKIE_COMMAND
    SAVE_AS_COOKIE_COMMAND = CommandsConfig.SAVE_AS_COOKIE_COMMAND
    AUDIO_COMMAND = CommandsConfig.AUDIO_COMMAND
    UNCACHE_COMMAND = CommandsConfig.UNCACHE_COMMAND
    PLAYLIST_COMMAND = CommandsConfig.PLAYLIST_COMMAND
    FORMAT_COMMAND = CommandsConfig.FORMAT_COMMAND
    MEDIINFO_COMMAND = CommandsConfig.MEDIINFO_COMMAND
    SETTINGS_COMMAND = CommandsConfig.SETTINGS_COMMAND
    COOKIES_FROM_BROWSER_COMMAND = CommandsConfig.COOKIES_FROM_BROWSER_COMMAND
    BLOCK_USER_COMMAND = CommandsConfig.BLOCK_USER_COMMAND
    UNBLOCK_USER_COMMAND = CommandsConfig.UNBLOCK_USER_COMMAND
    IGNORE_USER_COMMAND = CommandsConfig.IGNORE_USER_COMMAND
    UNIGNORE_USER_COMMAND = CommandsConfig.UNIGNORE_USER_COMMAND
    BAN_TIME_COMMAND = CommandsConfig.BAN_TIME_COMMAND
    RUN_TIME = CommandsConfig.RUN_TIME
    GET_USER_LOGS_COMMAND = CommandsConfig.GET_USER_LOGS_COMMAND
    CLEAN_COMMAND = CommandsConfig.CLEAN_COMMAND
    USAGE_COMMAND = CommandsConfig.USAGE_COMMAND
    TAGS_COMMAND = CommandsConfig.TAGS_COMMAND
    BROADCAST_MESSAGE = CommandsConfig.BROADCAST_MESSAGE
    GET_USER_DETAILS_COMMAND = CommandsConfig.GET_USER_DETAILS_COMMAND
    SPLIT_COMMAND = CommandsConfig.SPLIT_COMMAND
    RELOAD_CACHE_COMMAND = CommandsConfig.RELOAD_CACHE_COMMAND
    AUTO_CACHE_COMMAND = CommandsConfig.AUTO_CACHE_COMMAND
    SEARCH_COMMAND = CommandsConfig.SEARCH_COMMAND
    KEYBOARD_COMMAND = CommandsConfig.KEYBOARD_COMMAND
    LINK_COMMAND = CommandsConfig.LINK_COMMAND
    IMG_COMMAND = CommandsConfig.IMG_COMMAND
    ADD_BOT_TO_GROUP_COMMAND = CommandsConfig.ADD_BOT_TO_GROUP_COMMAND
    NSFW_COMMAND = CommandsConfig.NSFW_COMMAND
    ARGS_COMMAND = CommandsConfig.ARGS_COMMAND
    LIST_COMMAND = CommandsConfig.LIST_COMMAND

    # -------------------------------------------------------
    # MESSAGES (dynamic, per-user language)
    # -------------------------------------------------------
    @classmethod
    def get_messages(cls, user_id=None, language_code=None):
        return safe_get_messages(user_id, language_code)

    @classmethod
    def get_message(cls, message_key, user_id=None, language_code=None):
        msgs = cls.get_messages(user_id, language_code)
        return getattr(msgs, message_key, f"[{message_key}]")

    # -------------------------------------------------------
    # DOMAINS (all attributes from DomainsConfig)
    # -------------------------------------------------------
    GREYLIST = DomainsConfig.GREYLIST
    BLACK_LIST = DomainsConfig.BLACK_LIST
    PORN_DOMAINS_FILE = DomainsConfig.PORN_DOMAINS_FILE
    PORN_KEYWORDS_FILE = DomainsConfig.PORN_KEYWORDS_FILE
    SUPPORTED_SITES_FILE = DomainsConfig.SUPPORTED_SITES_FILE
    UPDATE_PORN_SCRIPT_PATH = DomainsConfig.UPDATE_PORN_SCRIPT_PATH
    WHITELIST = DomainsConfig.WHITELIST
    WHITE_KEYWORDS = DomainsConfig.WHITE_KEYWORDS
    NO_COOKIE_DOMAINS = DomainsConfig.NO_COOKIE_DOMAINS
    NO_FILTER_DOMAINS = DomainsConfig.NO_FILTER_DOMAINS
    PROXY_DOMAINS = DomainsConfig.PROXY_DOMAINS
    PROXY_2_DOMAINS = DomainsConfig.PROXY_2_DOMAINS
    TIKTOK_DOMAINS = DomainsConfig.TIKTOK_DOMAINS
    YTDLP_ONLY_DOMAINS = DomainsConfig.YTDLP_ONLY_DOMAINS
    GALLERYDL_ONLY_DOMAINS = DomainsConfig.GALLERYDL_ONLY_DOMAINS
    GALLERYDL_ONLY_PATH = DomainsConfig.GALLERYDL_ONLY_PATH
    GALLERYDL_FALLBACK_DOMAINS = DomainsConfig.GALLERYDL_FALLBACK_DOMAINS
    CLEAN_QUERY = DomainsConfig.CLEAN_QUERY
    PIPED_DOMAIN = DomainsConfig.PIPED_DOMAIN

    # -------------------------------------------------------
    # LIMITS (all attributes from LimitsConfig)
    # -------------------------------------------------------
    TURN_OFF_LIMITS_FOR_ADMINS = LimitsConfig.TURN_OFF_LIMITS_FOR_ADMINS
    MAX_FILE_SIZE_GB = LimitsConfig.MAX_FILE_SIZE_GB
    DOWNLOAD_TIMEOUT = LimitsConfig.DOWNLOAD_TIMEOUT
    MAX_SUB_QUALITY = LimitsConfig.MAX_SUB_QUALITY
    MAX_SUB_DURATION = LimitsConfig.MAX_SUB_DURATION
    MAX_SUB_SIZE = LimitsConfig.MAX_SUB_SIZE
    MAX_PLAYLIST_COUNT = LimitsConfig.MAX_PLAYLIST_COUNT
    MAX_TIKTOK_COUNT = LimitsConfig.MAX_TIKTOK_COUNT
    MAX_IMG_FILES = LimitsConfig.MAX_IMG_FILES
    MAX_VIDEO_DURATION = LimitsConfig.MAX_VIDEO_DURATION
    MAX_IMG_RANGE_WAIT_TIME = LimitsConfig.MAX_IMG_RANGE_WAIT_TIME
    MAX_IMG_TOTAL_WAIT_TIME = LimitsConfig.MAX_IMG_TOTAL_WAIT_TIME
    MAX_IMG_INACTIVITY_TIME = LimitsConfig.MAX_IMG_INACTIVITY_TIME
    ENABLE_LIVE_STREAM_BLOCKING = LimitsConfig.ENABLE_LIVE_STREAM_BLOCKING
    SPLIT_LIVE_STREAM_BY_HOURS = LimitsConfig.SPLIT_LIVE_STREAM_BY_HOURS
    MAX_LIVE_STREAM_DURATION = LimitsConfig.MAX_LIVE_STREAM_DURATION
    MAX_ANIMATION_DURATION = LimitsConfig.MAX_ANIMATION_DURATION
    MAX_HTTP_CONNECTION_LIFETIME = LimitsConfig.MAX_HTTP_CONNECTION_LIFETIME
    HTTP_REQUEST_TIMEOUT = LimitsConfig.HTTP_REQUEST_TIMEOUT
    COOKIE_CACHE_DURATION = LimitsConfig.COOKIE_CACHE_DURATION
    COOKIE_CACHE_MAX_LIFETIME = LimitsConfig.COOKIE_CACHE_MAX_LIFETIME
    COOKIE_CACHE_REQUEST_TIMEOUT = LimitsConfig.COOKIE_CACHE_REQUEST_TIMEOUT
    YOUTUBE_COOKIE_RETRY_LIMIT_PER_HOUR = LimitsConfig.YOUTUBE_COOKIE_RETRY_LIMIT_PER_HOUR
    YOUTUBE_COOKIE_RETRY_WINDOW = LimitsConfig.YOUTUBE_COOKIE_RETRY_WINDOW
    RATE_LIMIT_PER_MINUTE = LimitsConfig.RATE_LIMIT_PER_MINUTE
    RATE_LIMIT_PER_HOUR = LimitsConfig.RATE_LIMIT_PER_HOUR
    RATE_LIMIT_PER_DAY = LimitsConfig.RATE_LIMIT_PER_DAY
    RATE_LIMIT_COOLDOWN_MINUTE = LimitsConfig.RATE_LIMIT_COOLDOWN_MINUTE
    RATE_LIMIT_COOLDOWN_HOUR = LimitsConfig.RATE_LIMIT_COOLDOWN_HOUR
    RATE_LIMIT_COOLDOWN_DAY = LimitsConfig.RATE_LIMIT_COOLDOWN_DAY
    COMMAND_LIMIT_PER_MINUTE = LimitsConfig.COMMAND_LIMIT_PER_MINUTE
    COMMAND_COOLDOWN_INITIAL = LimitsConfig.COMMAND_COOLDOWN_INITIAL
    COMMAND_COOLDOWN_MULTIPLIER = LimitsConfig.COMMAND_COOLDOWN_MULTIPLIER
    GROUP_MULTIPLIER = LimitsConfig.GROUP_MULTIPLIER
    MAX_MULTI_URL_LIMIT = LimitsConfig.MAX_MULTI_URL_LIMIT
    NSFW_STAR_COST = LimitsConfig.NSFW_STAR_COST
    # Anti-bot protection
    ANTI_BOT_PROTECTION_ENABLED = LimitsConfig.ANTI_BOT_PROTECTION_ENABLED
    ANTI_BOT_DUPLICATE_URL_LIMIT = LimitsConfig.ANTI_BOT_DUPLICATE_URL_LIMIT
    ANTI_BOT_DUPLICATE_URL_WINDOW = LimitsConfig.ANTI_BOT_DUPLICATE_URL_WINDOW
    ANTI_BOT_TIMER_INTERVAL_WINDOW = LimitsConfig.ANTI_BOT_TIMER_INTERVAL_WINDOW
    ANTI_BOT_TIMER_INTERVAL_TOLERANCE = LimitsConfig.ANTI_BOT_TIMER_INTERVAL_TOLERANCE
    ANTI_BOT_TIMER_INTERVAL_MIN_COUNT = LimitsConfig.ANTI_BOT_TIMER_INTERVAL_MIN_COUNT
    ANTI_BOT_TIMER_INTERVAL_MIN_INTERVAL = LimitsConfig.ANTI_BOT_TIMER_INTERVAL_MIN_INTERVAL
    ANTI_BOT_DUPLICATE_COMMAND_LIMIT = LimitsConfig.ANTI_BOT_DUPLICATE_COMMAND_LIMIT
    ANTI_BOT_DUPLICATE_COMMAND_WINDOW = LimitsConfig.ANTI_BOT_DUPLICATE_COMMAND_WINDOW
    ANTI_BOT_24H_WINDOW = LimitsConfig.ANTI_BOT_24H_WINDOW
    ANTI_BOT_24H_ACTIVITY_FREQUENCY = LimitsConfig.ANTI_BOT_24H_ACTIVITY_FREQUENCY
    ANTI_BOT_FLOOD_MESSAGES_PER_SECOND = LimitsConfig.ANTI_BOT_FLOOD_MESSAGES_PER_SECOND
    ANTI_BOT_FLOOD_WINDOW = LimitsConfig.ANTI_BOT_FLOOD_WINDOW
    ANTI_BOT_DUPLICATE_MESSAGE_LIMIT = LimitsConfig.ANTI_BOT_DUPLICATE_MESSAGE_LIMIT
    ANTI_BOT_DUPLICATE_MESSAGE_WINDOW = LimitsConfig.ANTI_BOT_DUPLICATE_MESSAGE_WINDOW
    ANTI_BOT_BLOCK_NUMBERS_ONLY = LimitsConfig.ANTI_BOT_BLOCK_NUMBERS_ONLY
    ANTI_BOT_BLOCK_SPECIAL_ONLY = LimitsConfig.ANTI_BOT_BLOCK_SPECIAL_ONLY
    ANTI_BOT_PATTERN_MIN_LENGTH = LimitsConfig.ANTI_BOT_PATTERN_MIN_LENGTH
