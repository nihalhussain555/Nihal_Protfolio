import json
import os
import re
import time
from datetime import datetime, timezone
from html import unescape

import requests
from bs4 import BeautifulSoup


# ============================================================
# USERNAMES
# ============================================================

LEETCODE_USERNAME = "Nihal_555"
CODECHEF_USERNAME = "kit28csb106"
CODEFORCES_USERNAME = "nihalhussain555"
HACKERRANK_USERNAME = "kit28_24bcs106"
GITHUB_USERNAME = "nihalhussain555"
CODOLIO_PROFILE = "NihalHussain"


# ============================================================
# CONFIG
# ============================================================

OUTPUT_FILE = "coding-stats.json"
TIMEOUT = 25

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/153.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


# ============================================================
# SESSION
# ============================================================

session = requests.Session()
session.headers.update(HEADERS)


# ============================================================
# HELPERS
# ============================================================

def get_text(url, headers=None):
    try:
        response = session.get(
            url,
            headers=headers or {},
            timeout=TIMEOUT,
        )

        print(f"[GET] {response.status_code} {url}")

        if response.status_code != 200:
            return None

        return response.text

    except Exception as exc:
        print(f"[ERROR] {url}")
        print(exc)
        return None


def get_json(url, headers=None):
    try:
        response = session.get(
            url,
            headers=headers or {},
            timeout=TIMEOUT,
        )

        print(f"[JSON] {response.status_code} {url}")

        if response.status_code != 200:
            return None

        return response.json()

    except Exception as exc:
        print(f"[JSON ERROR] {url}")
        print(exc)
        return None


def post_json(url, payload, headers=None):
    try:
        response = session.post(
            url,
            json=payload,
            headers=headers or {},
            timeout=TIMEOUT,
        )

        print(f"[POST] {response.status_code} {url}")

        if response.status_code != 200:
            print(response.text[:500])
            return None

        return response.json()

    except Exception as exc:
        print(f"[POST ERROR] {url}")
        print(exc)
        return None


def number(value):
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return int(value) if float(value).is_integer() else value

    text = unescape(str(value))
    text = text.replace(",", "").strip()

    match = re.search(r"-?\d+(?:\.\d+)?", text)

    if not match:
        return None

    value = float(match.group())

    return int(value) if value.is_integer() else value


def first_number(*values):
    for value in values:
        result = number(value)

        if result is not None:
            return result

    return None


def rounded(value):
    """Platform ratings are only ever shown as whole numbers."""

    result = number(value)

    if result is None:
        return None

    return int(result)


def put(data, key, value):
    if value is not None and value != "":
        data[key] = value


def clean_rank(value):
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return int(value)

    text = str(value).strip()

    if not text:
        return None

    numeric = number(text)

    if numeric is not None and re.fullmatch(
        r"#?\s*[\d,]+",
        text,
    ):
        return numeric

    return text


# ============================================================
# OUTPUT
# ============================================================

output = {
    "updatedAt": datetime.now(timezone.utc).isoformat(),

    "sourceStatus": {},

    "codolio": {
        "totalProblems": None,
        "cScore": None,
        "globalRank": None,
    },

    "platforms": {
        "leetcode": {
            "direct": {},
            "codolio": {},
            "final": {},
        },

        "codechef": {
            "direct": {},
            "codolio": {},
            "final": {},
        },

        "codeforces": {
            "direct": {},
            "codolio": {},
            "final": {},
        },

        "hackerrank": {
            "direct": {},
            "codolio": {},
            "final": {},
        },

        "github": {
            "direct": {},
            "codolio": {},
            "final": {},
        },
    },
}


def set_status(platform, source, success, message=""):
    output["sourceStatus"].setdefault(platform, {})

    output["sourceStatus"][platform][source] = {
        "ok": success,
        "message": message,
    }


# ============================================================
# CODOLIO
# ============================================================

CODOLIO_API = "https://api.codolio.com/profile"

CODOLIO_LEADERBOARD = (
    "https://node.codolio.com/api/leaderboard/v1/"
    "get-user-leaderboard"
)

CODOLIO_HEADERS = {
    "Accept": "application/json",
    "Origin": "https://codolio.com",
    "Referer": (
        "https://codolio.com/profile/"
        f"{CODOLIO_PROFILE}"
    ),
}

# The leaderboard ranks each score type separately; this category
# is the C-Score ranking the profile page shows as "Global Rank".
CODOLIO_CSCORE_CATEGORY = "1"


def codolio_platform_stats(profile):

    if not isinstance(profile, dict):
        return {}

    result = {}

    question_stats = (
        profile.get("totalQuestionStats")
        or {}
    )

    if isinstance(question_stats, dict):

        put(
            result,
            "totalSolved",
            first_number(
                question_stats.get(
                    "totalQuestionCounts"
                ),
                question_stats.get(
                    "totalSolved"
                ),
                question_stats.get(
                    "solved"
                ),
            ),
        )

    user_stats = (
        profile.get("userStats")
        or {}
    )

    put(
        result,
        "rating",
        first_number(
            user_stats.get("currentRating"),
            user_stats.get("rating"),
        ),
    )

    put(
        result,
        "maxRating",
        number(
            user_stats.get("maxRating")
        ),
    )

    put(
        result,
        "rank",
        clean_rank(
            user_stats.get("rank")
            or user_stats.get("maxRank")
        ),
    )

    return result


def load_codolio():

    profiles = []

    payload = get_json(
        f"{CODOLIO_API}?userKey={CODOLIO_PROFILE}",
        CODOLIO_HEADERS,
    )

    data = (
        payload.get("data")
        if isinstance(payload, dict)
        else None
    )

    if not isinstance(data, dict):

        set_status(
            "codolio",
            "public",
            False,
            "Codolio profile API could not be loaded.",
        )

        return profiles

    nested = data.get("platformProfiles")

    if isinstance(nested, dict):
        nested = nested.get("platformProfiles")

    if isinstance(nested, list):
        profiles = nested

    user_id = data.get("id")

    if user_id:

        leaderboard = get_json(
            f"{CODOLIO_LEADERBOARD}?userId={user_id}",
            CODOLIO_HEADERS,
        )

        entry = (
            (
                (leaderboard or {}).get("data") or {}
            ).get("global") or {}
        ).get(CODOLIO_CSCORE_CATEGORY)

        if isinstance(entry, dict):

            put(
                output["codolio"],
                "cScore",
                rounded(entry.get("score")),
            )

            put(
                output["codolio"],
                "globalRank",
                number(entry.get("rank")),
            )

    set_status(
        "codolio",
        "public",
        bool(profiles),
        f"Loaded {len(profiles)} platform records.",
    )

    return profiles


codolio_profiles = load_codolio()


def platform_name(value):

    value = str(
        value or ""
    ).lower().strip()

    aliases = {
        "leetcode": "leetcode",
        "leetcode.com": "leetcode",

        "codechef": "codechef",

        "codeforces": "codeforces",

        "hackerrank": "hackerrank",
        "hacker rank": "hackerrank",
    }

    return aliases.get(
        value,
        value,
    )


for profile in codolio_profiles:

    name = platform_name(
        profile.get("platform")
        or profile.get("platformName")
        or profile.get("name")
    )

    if name in output["platforms"]:

        output["platforms"][name][
            "codolio"
        ] = codolio_platform_stats(
            profile
        )


# ============================================================
# LEETCODE
# ============================================================

def load_leetcode():

    result = {}

    endpoint = "https://leetcode.com/graphql"

    headers = {
        "Content-Type": "application/json",
        "Origin": "https://leetcode.com",
        "Referer": (
            f"https://leetcode.com/u/"
            f"{LEETCODE_USERNAME}/"
        ),
    }

    profile_query = """
    query userProfile($username: String!) {
        matchedUser(username: $username) {
            username

            profile {
                ranking
                reputation
            }

            submitStats: submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
        }
    }
    """

    data = post_json(
        endpoint,
        {
            "query": profile_query,
            "variables": {
                "username": LEETCODE_USERNAME
            },
        },
        headers,
    )

    matched = (
        data
        .get("data", {})
        .get("matchedUser")
        if isinstance(data, dict)
        else None
    )

    if matched:

        submit_stats = (
            matched.get("submitStats")
            or {}
        )

        counts = (
            submit_stats.get(
                "acSubmissionNum"
            )
            or []
        )

        for item in counts:

            difficulty = str(
                item.get("difficulty", "")
            ).lower()

            count = number(
                item.get("count")
            )

            if difficulty == "all":
                put(
                    result,
                    "totalSolved",
                    count,
                )

            elif difficulty == "easy":
                put(
                    result,
                    "easySolved",
                    count,
                )

            elif difficulty == "medium":
                put(
                    result,
                    "mediumSolved",
                    count,
                )

            elif difficulty == "hard":
                put(
                    result,
                    "hardSolved",
                    count,
                )

        profile = (
            matched.get("profile")
            or {}
        )

        put(
            result,
            "rank",
            number(
                profile.get("ranking")
            ),
        )

    # Contest rating.
    contest_query = """
    query userContestRanking($username: String!) {
        userContestRanking(username: $username) {
            rating
            globalRanking
        }
    }
    """

    contest = post_json(
        endpoint,
        {
            "query": contest_query,
            "variables": {
                "username": LEETCODE_USERNAME
            },
        },
        headers,
    )

    ranking = (
        contest
        .get("data", {})
        .get("userContestRanking")
        if isinstance(contest, dict)
        else None
    )

    if ranking:

        put(
            result,
            "rating",
            rounded(
                ranking.get("rating")
            ),
        )

        if result.get("rank") is None:

            put(
                result,
                "rank",
                number(
                    ranking.get(
                        "globalRanking"
                    )
                ),
            )

    # Max rating.
    history_query = """
    query userContestRankingHistory(
        $username: String!
    ) {
        userContestRankingHistory(
            username: $username
        ) {
            rating
            attended
        }
    }
    """

    history = post_json(
        endpoint,
        {
            "query": history_query,
            "variables": {
                "username": LEETCODE_USERNAME
            },
        },
        headers,
    )

    rows = (
        history
        .get("data", {})
        .get("userContestRankingHistory")
        if isinstance(history, dict)
        else None
    )

    ratings = []

    if isinstance(rows, list):

        for row in rows:

            if not isinstance(row, dict):
                continue

            if row.get("attended") is False:
                continue

            rating = number(
                row.get("rating")
            )

            if rating is not None:
                ratings.append(rating)

    if ratings:

        result["maxRating"] = int(
            max(
                ratings
            )
        )

    # HTML fallback.
    if not result.get("totalSolved"):

        html = get_text(
            f"https://leetcode.com/u/"
            f"{LEETCODE_USERNAME}/"
        )

        if html:

            soup = BeautifulSoup(
                html,
                "html.parser",
            )

            text = soup.get_text(
                " ",
                strip=True,
            )

            patterns = [
                r"([\d,]+)\s+problems solved",
                r"([\d,]+)\s+Problems Solved",
            ]

            for pattern in patterns:

                match = re.search(
                    pattern,
                    text,
                    re.I,
                )

                if match:

                    result["totalSolved"] = number(
                        match.group(1)
                    )

                    break

    # Community mirror fallback.
    #
    # leetcode.com sits behind Cloudflare, which frequently blocks
    # requests coming from cloud/CI IP ranges (GitHub Actions
    # included) even though the same query works fine from a
    # normal residential/browser IP. When our own GraphQL + HTML
    # attempts come back empty, fall back to a couple of
    # long-running community mirrors that do their own scraping
    # and are usually not blocked.
    if not result.get("totalSolved"):

        mirrors = [
            f"https://leetcode-stats-api.herokuapp.com/{LEETCODE_USERNAME}",
            f"https://leetcode-stats.tashif.codes/{LEETCODE_USERNAME}",
        ]

        for mirror_url in mirrors:

            mirror = get_json(mirror_url)

            if not isinstance(mirror, dict):
                continue

            if mirror.get("status") not in (None, "success"):
                continue

            put(result, "totalSolved", number(mirror.get("totalSolved")))
            put(result, "easySolved", number(mirror.get("easySolved")))
            put(result, "mediumSolved", number(mirror.get("mediumSolved")))
            put(result, "hardSolved", number(mirror.get("hardSolved")))

            if result.get("rank") is None:
                put(result, "rank", number(mirror.get("ranking")))

            if result.get("totalSolved") is not None:
                break

    set_status(
        "leetcode",
        "direct",
        bool(result),
        "LeetCode GraphQL + HTML fallback + community mirror fallback.",
    )

    return result


output["platforms"]["leetcode"]["direct"] = (
    load_leetcode()
)


# ============================================================
# CODECHEF
# ============================================================

def load_codechef():

    result = {}

    url = (
        f"https://www.codechef.com/users/"
        f"{CODECHEF_USERNAME}"
    )

    html = get_text(url)

    if not html:

        set_status(
            "codechef",
            "direct",
            False,
            "CodeChef profile unavailable.",
        )

        return result

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    text = soup.get_text(
        " ",
        strip=True,
    )

    # ------------------------------------------------------------
    # Total problems solved.
    #
    # This one is still "label then number" on the current page,
    # e.g. "Total Problems Solved: 440".
    # ------------------------------------------------------------

    for expression in (
        r"Total Problems Solved\s*:?\s*([\d,]+)",
        r"Problems Solved\s*:?\s*([\d,]+)",
    ):

        match = re.search(expression, text, re.I)

        if match:

            value = number(match.group(1))

            if value is not None:
                result["totalSolved"] = value
                break

    # ------------------------------------------------------------
    # Rating / max rating / global rank.
    #
    # CodeChef redesigned this section of the profile page. Two
    # things changed that broke the old label-then-number regexes:
    #
    #   1. The current rating number and the global/country rank
    #      numbers now appear BEFORE their label in the page's
    #      text (e.g. "1069 ... CodeChef Rating" and
    #      "121862 Global Rank" instead of the old
    #      "CodeChef Rating ... 1069" / "Global Rank #121862").
    #
    #   2. The page now shows a second, near-identical block for
    #      "DSA Rating" right next to the CodeChef Rating block,
    #      so a generic "Global Rank" / "Rating" search can grab
    #      the DSA numbers instead of the CodeChef ones.
    #
    # To handle both, we anchor on the literal
    # "CodeChef Rating (Highest Rating <n>)" text (still label
    # order, and unique to this block), then look immediately
    # BEFORE it for the current rating number and immediately
    # AFTER it (but before the next "DSA Rating" block) for the
    # global/country rank numbers.
    # ------------------------------------------------------------

    window_start = text.find("Total Problems Solved")

    window = text[window_start:] if window_start != -1 else text

    cc_block = re.search(
        r"CodeChef Rating\s*\(Highest Rating\s*([\d,]+)\)",
        window,
        re.I,
    )

    if cc_block:

        put(result, "maxRating", number(cc_block.group(1)))

        # Current rating: nearest standalone number before this
        # block, ignoring anything inside parentheses (division
        # tags like "(Div 4)" also contain digits).
        before = window[:cc_block.start()]
        before = re.sub(r"\([^)]*\)", " ", before)

        numbers_before = re.findall(r"\d[\d,]*", before)

        if numbers_before:
            put(result, "rating", number(numbers_before[-1]))

        # Global/country rank: look after this block, but stop
        # before the DSA Rating block so we don't pick up its
        # numbers instead.
        after = window[cc_block.end():cc_block.end() + 600]

        dsa_index = after.find("DSA Rating")

        if dsa_index != -1:
            after = after[:dsa_index]

        rank_match = re.search(r"([\d,]+)\s*Global Rank", after, re.I)

        if rank_match:
            put(result, "rank", clean_rank(rank_match.group(1)))

    # Fallback for the old page layout, in case CodeChef reverts
    # or A/B tests the redesign.
    if result.get("rating") is None:

        match = re.search(
            r"CodeChef Rating\s*:?\s*([\d,]+)",
            window,
            re.I,
        )

        if match:
            put(result, "rating", number(match.group(1)))

    if result.get("maxRating") is None:

        match = re.search(r"Highest Rating\s*([\d,]+)", window, re.I)

        if match:
            put(result, "maxRating", number(match.group(1)))

    if result.get("rank") is None:

        match = re.search(r"Global Rank\s*#?\s*([\d,]+)", window, re.I)

        if match:
            put(result, "rank", clean_rank(match.group(1)))

    # Search embedded JSON if HTML text did not expose it.
    for script in soup.find_all("script"):

        raw = (
            script.string
            or script.get_text()
        )

        if not raw:
            continue

        mappings = {
            "rating": [
                "rating",
                "currentRating",
            ],

            "maxRating": [
                "highestRating",
                "maxRating",
            ],

            "totalSolved": [
                "totalSolved",
                "problemsSolved",
            ],
        }

        for field, keys in mappings.items():

            if field in result:
                continue

            for key in keys:

                match = re.search(
                    rf'"{re.escape(key)}"\s*:\s*"?('
                    rf'[\d,]+)',
                    raw,
                    re.I,
                )

                if match:

                    result[field] = number(
                        match.group(1)
                    )

                    break

    set_status(
        "codechef",
        "direct",
        bool(result),
        "CodeChef public profile scraper.",
    )

    return result


output["platforms"]["codechef"]["direct"] = (
    load_codechef()
)


# ============================================================
# CODEFORCES
# ============================================================

def load_codeforces():

    result = {}

    profile = get_json(
        "https://codeforces.com/api/user.info"
        f"?handles={CODEFORCES_USERNAME}"
    )

    if (
        isinstance(profile, dict)
        and profile.get("status") == "OK"
        and profile.get("result")
    ):

        user = profile["result"][0]

        put(
            result,
            "rating",
            number(
                user.get("rating")
            ),
        )

        put(
            result,
            "maxRating",
            number(
                user.get("maxRating")
            ),
        )

        put(
            result,
            "rank",
            clean_rank(
                user.get("rank")
            ),
        )

    # Codeforces asks clients to avoid excessive requests.
    time.sleep(2.2)

    submissions = get_json(
        "https://codeforces.com/api/user.status"
        f"?handle={CODEFORCES_USERNAME}"
        "&from=1&count=10000"
    )

    if (
        isinstance(submissions, dict)
        and submissions.get("status") == "OK"
    ):

        solved = set()

        for submission in (
            submissions.get("result")
            or []
        ):

            if submission.get(
                "verdict"
            ) != "OK":
                continue

            problem = (
                submission.get("problem")
                or {}
            )

            contest_id = submission.get(
                "contestId",
                "gym",
            )

            index = problem.get(
                "index"
            )

            if index:

                solved.add(
                    f"{contest_id}-{index}"
                )

        result["totalSolved"] = len(
            solved
        )

    set_status(
        "codeforces",
        "direct",
        bool(result),
        "Official Codeforces API.",
    )

    return result


output["platforms"]["codeforces"]["direct"] = (
    load_codeforces()
)


# ============================================================
# HACKERRANK
# ============================================================

# HackerRank's profile page is a client-rendered app and no longer
# prints any statistics into the HTML, so these are the JSON
# endpoints that page itself calls. They are public and need no
# authentication.
HACKERRANK_BADGES_API = (
    "https://www.hackerrank.com/rest/hackers/"
    f"{HACKERRANK_USERNAME}/badges"
)

HACKERRANK_CERTIFICATES_API = (
    "https://www.hackerrank.com/community/v1/"
    "test_results/hacker_certificate"
    f"?username={HACKERRANK_USERNAME}"
)

HACKERRANK_HEADERS = {
    "Accept": "application/json",
    "Referer": (
        "https://www.hackerrank.com/profile/"
        f"{HACKERRANK_USERNAME}"
    ),
}


def load_hackerrank():

    result = {}

    badges = get_json(
        HACKERRANK_BADGES_API,
        HACKERRANK_HEADERS,
    )

    models = (
        badges.get("models")
        if isinstance(badges, dict)
        else None
    )

    if isinstance(models, list) and models:

        solved = 0
        earned = 0

        for badge in models:

            if not isinstance(badge, dict):
                continue

            solved += int(badge.get("solved") or 0)

            if int(badge.get("stars") or 0) > 0:
                earned += 1

            if badge.get("badge_type") == "problem-solving":

                put(
                    result,
                    "rank",
                    number(badge.get("hacker_rank")),
                )

        put(result, "totalSolved", solved or None)
        put(result, "badgesEarned", earned or None)

    certificates = get_json(
        HACKERRANK_CERTIFICATES_API,
        HACKERRANK_HEADERS,
    )

    entries = (
        certificates.get("data")
        if isinstance(certificates, dict)
        else None
    )

    if isinstance(entries, list):

        passed = [
            entry
            for entry in entries
            if isinstance(entry, dict)
            and (entry.get("attributes") or {}).get(
                "status"
            )
            == "test_passed"
        ]

        put(
            result,
            "certifications",
            len(passed) or None,
        )

    set_status(
        "hackerrank",
        "direct",
        bool(result),
        (
            "HackerRank public badges and certificate APIs. "
            "HackerRank exposes no contest rating, so stars and "
            "badges are reported instead."
        ),
    )

    return result


output["platforms"]["hackerrank"]["direct"] = (
    load_hackerrank()
)


# ============================================================
# GITHUB
# ============================================================

def load_github():

    result = {}

    headers = {
        "Accept": (
            "application/vnd.github+json"
        ),
        "X-GitHub-Api-Version": "2022-11-28",
    }

    profile = get_json(
        f"https://api.github.com/users/"
        f"{GITHUB_USERNAME}",
        headers,
    )

    if profile:

        put(
            result,
            "repositories",
            profile.get(
                "public_repos"
            ),
        )

        put(
            result,
            "followers",
            profile.get(
                "followers"
            ),
        )

        put(
            result,
            "following",
            profile.get(
                "following"
            ),
        )

    repositories = get_json(
        f"https://api.github.com/users/"
        f"{GITHUB_USERNAME}/repos"
        "?per_page=100&sort=updated",
        headers,
    )

    if isinstance(
        repositories,
        list,
    ):

        stars = 0
        forks = 0

        for repo in repositories:

            stars += int(
                repo.get(
                    "stargazers_count",
                    0,
                )
                or 0
            )

            forks += int(
                repo.get(
                    "forks_count",
                    0,
                )
                or 0
            )

        result["stars"] = stars
        result["forks"] = forks

    set_status(
        "github",
        "direct",
        bool(result),
        "Official GitHub REST API.",
    )

    return result


output["platforms"]["github"]["direct"] = (
    load_github()
)


# ============================================================
# MERGE
#
# DIRECT DATA ALWAYS WINS.
# CODOLIO ONLY FILLS MISSING VALUES.
# ============================================================

FIELDS = [
    "totalSolved",
    "rating",
    "maxRating",
    "rank",
    "easySolved",
    "mediumSolved",
    "hardSolved",
    "repositories",
    "followers",
    "following",
    "stars",
    "forks",
    "badgesEarned",
    "certifications",
]


for platform_name, platform in (
    output["platforms"].items()
):

    direct = (
        platform.get("direct")
        or {}
    )

    codolio = (
        platform.get("codolio")
        or {}
    )

    final = {}

    for field in FIELDS:

        if (
            direct.get(field)
            is not None
        ):

            final[field] = direct[field]

        elif (
            codolio.get(field)
            is not None
        ):

            final[field] = codolio[field]

    platform["final"] = final


# ============================================================
# CODOLIO TOTAL
# ============================================================

totals = []

for platform_name in [
    "leetcode",
    "codechef",
    "codeforces",
    "hackerrank",
]:

    value = (
        output["platforms"]
        [platform_name]
        ["final"]
        .get("totalSolved")
    )

    value = number(value)

    if value is not None:
        totals.append(value)


if totals:

    output["codolio"][
        "totalProblems"
    ] = sum(totals)


# ============================================================
# SAVE JSON
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8",
) as file:

    json.dump(
        output,
        file,
        indent=2,
        ensure_ascii=False,
    )


# ============================================================
# PRINT RESULT
# ============================================================

print()
print("=" * 60)
print("CODING PLATFORM STATISTICS")
print("=" * 60)

for platform_name in output["platforms"]:

    print()
    print(
        platform_name.upper()
    )

    print(
        json.dumps(
            output["platforms"]
            [platform_name]
            ["final"],
            indent=2,
        )
    )

print()
print("=" * 60)
print("CODOLIO")
print("=" * 60)

print(
    json.dumps(
        output["codolio"],
        indent=2,
    )
)

print()
print("=" * 60)
print(
    "UPDATED:",
    output["updatedAt"],
)
print("=" * 60)