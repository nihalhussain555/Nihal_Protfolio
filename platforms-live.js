(() => {
    "use strict";

    /*
     * =========================================================
     * PORTFOLIO CODING STATISTICS
     * =========================================================
     *
     * Data source:
     *
     * coding-stats.json
     *
     * The Python scraper updates this file.
     *
     * Priority:
     *
     * Direct platform data
     *          ↓
     * Codolio fallback
     *          ↓
     * Frontend
     *
     * Direct platform data ALWAYS wins.
     * =========================================================
     */

    const STATS_FILE = "./coding-stats.json";

    const REFRESH_TIME = 5 * 60 * 1000;


    // =========================================================
    // HELPERS
    // =========================================================

    function element(id) {
        return document.getElementById(id);
    }


    function isValid(value) {

        return (
            value !== undefined &&
            value !== null &&
            value !== "" &&
            value !== "—" &&
            value !== "Unavailable" &&
            value !== "Loading..."
        );
    }


    function hasAnyPlatformData(data) {

        const platforms = data.platforms || {};

        return Object.values(platforms).some(platform => {

            const buckets = [
                platform?.final,
                platform?.direct,
                platform?.codolio,
            ];

            return buckets.some(
                bucket =>
                    bucket &&
                    Object.values(bucket).some(isValid)
            );
        });
    }


    function formatNumber(value) {

        if (!isValid(value)) {
            return "—";
        }

        const parsed = Number(
            String(value)
                .replace(/,/g, "")
                .trim()
        );

        if (Number.isFinite(parsed)) {

            return parsed.toLocaleString(
                "en-IN"
            );
        }

        return String(value);
    }


    function setValue(id, value) {

        const target = element(id);

        if (!target) {
            return;
        }

        target.textContent =
            formatNumber(value);
    }


    // =========================================================
    // GET FINAL PLATFORM VALUE
    // =========================================================

    function getPlatformValue(
        platform,
        field
    ) {

        if (!platform) {
            return null;
        }


        /*
         * First priority:
         * Python-generated final value.
         */
        if (
            platform.final &&
            isValid(
                platform.final[field]
            )
        ) {

            return platform.final[field];
        }


        /*
         * Second priority:
         * Direct platform scraper.
         */
        if (
            platform.direct &&
            isValid(
                platform.direct[field]
            )
        ) {

            return platform.direct[field];
        }


        /*
         * Third priority:
         * Codolio.
         */
        if (
            platform.codolio &&
            isValid(
                platform.codolio[field]
            )
        ) {

            return platform.codolio[field];
        }


        return null;
    }


    // =========================================================
    // RENDER PLATFORM
    // =========================================================

    function renderPlatform(
        data,
        platformName,
        ids
    ) {

        const platform =
            data.platforms?.[
                platformName
            ] || {};


        if (ids.solved) {

            setValue(
                ids.solved,
                getPlatformValue(
                    platform,
                    "totalSolved"
                )
            );
        }


        if (ids.rating) {

            setValue(
                ids.rating,
                getPlatformValue(
                    platform,
                    "rating"
                )
            );
        }


        if (ids.maxRating) {

            setValue(
                ids.maxRating,
                getPlatformValue(
                    platform,
                    "maxRating"
                )
            );
        }


        if (ids.rank) {

            const rank =
                getPlatformValue(
                    platform,
                    "rank"
                );

            setValue(
                ids.rank,
                rank
            );
        }
    }


    // =========================================================
    // RENDER EVERYTHING
    // =========================================================

    function renderStats(data) {

        if (
            !data ||
            !data.platforms
        ) {

            console.error(
                "[Stats] Invalid coding-stats.json"
            );

            return;
        }


        // -----------------------------------------------------
        // LEETCODE
        // -----------------------------------------------------

        renderPlatform(
            data,
            "leetcode",
            {
                solved:
                    "leetcode-solved",

                rating:
                    "leetcode-rating",

                maxRating:
                    "leetcode-max-rating",

                rank:
                    "leetcode-rank",
            }
        );


        // -----------------------------------------------------
        // CODECHEF
        // -----------------------------------------------------

        renderPlatform(
            data,
            "codechef",
            {
                solved:
                    "codechef-solved",

                rating:
                    "codechef-rating",

                maxRating:
                    "codechef-max-rating",

                rank:
                    "codechef-rank",
            }
        );


        // -----------------------------------------------------
        // CODEFORCES
        // -----------------------------------------------------

        renderPlatform(
            data,
            "codeforces",
            {
                solved:
                    "codeforces-solved",

                rating:
                    "codeforces-rating",

                maxRating:
                    "codeforces-max-rating",

                rank:
                    "codeforces-rank",
            }
        );


        // -----------------------------------------------------
        // HACKERRANK
        // -----------------------------------------------------

        renderPlatform(
            data,
            "hackerrank",
            {
                solved:
                    "hackerrank-solved",

                rating:
                    "hackerrank-rating",

                maxRating:
                    "hackerrank-max-rating",

                rank:
                    "hackerrank-status",
            }
        );


        // -----------------------------------------------------
        // GITHUB
        // -----------------------------------------------------

        const github =
            data.platforms?.github || {};


        setValue(
            "github-repos",
            getPlatformValue(
                github,
                "repositories"
            )
        );


        setValue(
            "github-followers",
            getPlatformValue(
                github,
                "followers"
            )
        );


        setValue(
            "github-stars",
            getPlatformValue(
                github,
                "stars"
            )
        );


        setValue(
            "github-forks",
            getPlatformValue(
                github,
                "forks"
            )
        );


        // -----------------------------------------------------
        // CODOLIO
        // -----------------------------------------------------

        const codolio =
            data.codolio || {};


        setValue(
            "codolio-score",
            codolio.cScore ??
            codolio.score ??
            codolio.c_score
        );


        setValue(
            "codolio-rank",
            codolio.globalRank ??
            codolio.rank
        );


        setValue(
            "codolio-solved",
            codolio.totalProblems ??
            codolio.totalSolved ??
            codolio.total
        );


        // -----------------------------------------------------
        // STATUS
        // -----------------------------------------------------

        const status =
            element("codolio-status");

        if (status) {

            status.textContent =
                hasAnyPlatformData(data)
                    ? "SYNCED"
                    : "NOT SYNCED YET";
        }


        const liveText =
            element("platform-live-text");

        if (liveText) {

            let directCount = 0;

            Object.values(
                data.sourceStatus || {}
            ).forEach(
                platform => {

                    if (
                        platform?.direct?.ok
                    ) {

                        directCount++;
                    }
                }
            );


            if (directCount > 0) {

                liveText.textContent =
                    "LIVE DATA LOADED";

            } else if (hasAnyPlatformData(data)) {

                liveText.textContent =
                    "FALLBACK DATA LOADED";

            } else {

                liveText.textContent =
                    "STATS NOT AVAILABLE YET";
            }
        }


        // -----------------------------------------------------
        // LAST UPDATED
        // -----------------------------------------------------

        const updated =
            element("platform-updated");


        if (
            updated &&
            data.updatedAt
        ) {

            const date =
                new Date(
                    data.updatedAt
                );


            if (
                !Number.isNaN(
                    date.getTime()
                )
            ) {

                updated.textContent =
                    "UPDATED " +
                    date.toLocaleString(
                        "en-IN",
                        {
                            dateStyle:
                                "short",

                            timeStyle:
                                "medium",
                        }
                    );
            }
        }
    }


    // =========================================================
    // FALLBACK WHEN THE JSON CAN'T BE LOADED
    // =========================================================
    //
    // coding-stats.json is written by the GitHub Action, not by
    // this script. If it hasn't been generated yet (first-ever
    // run not triggered), was deleted, or the fetch times out,
    // every card would otherwise be stuck on the static
    // "Loading..." text from the HTML forever. Replace it with
    // something honest instead.

    const ALL_STAT_IDS = [
        "leetcode-solved", "leetcode-rating", "leetcode-max-rating", "leetcode-rank",
        "codechef-solved", "codechef-rating", "codechef-max-rating", "codechef-rank",
        "codeforces-solved", "codeforces-rating", "codeforces-max-rating", "codeforces-rank",
        "hackerrank-solved", "hackerrank-rating", "hackerrank-max-rating", "hackerrank-status",
        "github-repos", "github-followers", "github-stars", "github-forks",
        "codolio-score", "codolio-rank", "codolio-solved",
    ];

    function renderUnavailable() {

        ALL_STAT_IDS.forEach(id => {

            const target = element(id);

            if (target && target.textContent === "Loading...") {
                target.textContent = "Unavailable";
            }
        });

        const status = element("codolio-status");

        if (status) {
            status.textContent = "NOT SYNCED YET";
        }

        const liveText = element("platform-live-text");

        if (liveText) {
            liveText.textContent =
                "STATS NOT AVAILABLE YET";
        }

        const updated = element("platform-updated");

        if (updated) {
            updated.textContent =
                "Waiting for first sync";
        }
    }


    // =========================================================
    // LOAD JSON
    // =========================================================

    async function loadStats() {

        const controller = new AbortController();

        // Don't let a slow/hanging request keep the cards on
        // "Loading..." indefinitely.
        const timeoutId = setTimeout(
            () => controller.abort(),
            10000
        );

        try {

            const response =
                await fetch(
                    STATS_FILE +
                    "?v=" +
                    Date.now(),
                    {
                        method: "GET",
                        cache: "no-store",
                        signal: controller.signal,
                    }
                );


            if (!response.ok) {

                throw new Error(
                    `HTTP ${response.status}`
                );
            }


            const data =
                await response.json();


            renderStats(data);


            console.log(
                "[Portfolio Stats] Updated:",
                data
            );


        } catch (error) {

            console.error(
                "[Portfolio Stats] Failed:",
                error
            );

            renderUnavailable();

        } finally {

            clearTimeout(timeoutId);
        }
    }


    // =========================================================
    // START
    // =========================================================

    function startStats() {

        loadStats();


        setInterval(
            loadStats,
            REFRESH_TIME
        );
    }


    if (
        document.readyState ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            startStats
        );

    } else {

        startStats();
    }

})();