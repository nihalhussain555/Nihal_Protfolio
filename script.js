document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       ELEMENTS
    ===================================================== */

    const body = document.body;

    const header =
        document.getElementById("header");

    const menu =
        document.getElementById("menu");

    const nav =
        document.querySelector(".nav-links");

    const themeToggle =
        document.getElementById("themeToggle");

    const scrollProgress =
        document.querySelector(".scroll-progress");

    const cursorGlow =
        document.querySelector(".cursor-glow");

    const typing =
        document.querySelector(".typing");


    /* =====================================================
       CURSOR GLOW
    ===================================================== */

    if (
        cursorGlow &&
        window.matchMedia("(pointer:fine)").matches
    ) {

        let mouseX = window.innerWidth / 2;
        let mouseY = window.innerHeight / 2;

        let currentX = mouseX;
        let currentY = mouseY;

        document.addEventListener("mousemove", (event) => {

            mouseX = event.clientX;
            mouseY = event.clientY;

        });

        function animateCursor() {

            currentX +=
                (mouseX - currentX) * 0.12;

            currentY +=
                (mouseY - currentY) * 0.12;

            cursorGlow.style.left =
                `${currentX}px`;

            cursorGlow.style.top =
                `${currentY}px`;

            requestAnimationFrame(
                animateCursor
            );
        }

        animateCursor();
    }


    /* =====================================================
       SCROLL PROGRESS
    ===================================================== */

    function updateScrollProgress() {

        const scrollTop =
            window.scrollY;

        const pageHeight =
            document.documentElement.scrollHeight -
            window.innerHeight;

        const percentage =
            pageHeight > 0
                ? (scrollTop / pageHeight) * 100
                : 0;

        if (scrollProgress) {

            scrollProgress.style.width =
                `${percentage}%`;
        }
    }

    window.addEventListener(
        "scroll",
        updateScrollProgress,
        { passive: true }
    );

    updateScrollProgress();


    /* =====================================================
       NAVBAR HIDE / SHOW
    ===================================================== */

    let lastScroll = 0;

    window.addEventListener(
        "scroll",
        () => {

            const currentScroll =
                window.scrollY;

            if (
                currentScroll > lastScroll &&
                currentScroll > 150
            ) {

                header.classList.add(
                    "hidden"
                );

            } else {

                header.classList.remove(
                    "hidden"
                );
            }

            lastScroll =
                Math.max(
                    currentScroll,
                    0
                );
        },
        { passive: true }
    );


    /* =====================================================
       MOBILE MENU
    ===================================================== */

    if (menu && nav) {

        menu.addEventListener(
            "click",
            () => {

                const opened =
                    nav.classList.toggle(
                        "active"
                    );

                menu.setAttribute(
                    "aria-expanded",
                    opened
                );

                const icon =
                    menu.querySelector("i");

                if (opened) {

                    icon.classList.remove(
                        "fa-bars"
                    );

                    icon.classList.add(
                        "fa-xmark"
                    );

                } else {

                    icon.classList.remove(
                        "fa-xmark"
                    );

                    icon.classList.add(
                        "fa-bars"
                    );
                }
            }
        );


        nav.querySelectorAll("a")
            .forEach(link => {

                link.addEventListener(
                    "click",
                    () => {

                        nav.classList.remove(
                            "active"
                        );

                        menu.setAttribute(
                            "aria-expanded",
                            "false"
                        );

                        const icon =
                            menu.querySelector("i");

                        icon.classList.remove(
                            "fa-xmark"
                        );

                        icon.classList.add(
                            "fa-bars"
                        );
                    }
                );
            });
    }


    /* =====================================================
       TYPING EFFECT
    ===================================================== */

    if (typing) {

        const words = [
            "AI / ML Engineer",
            "Full Stack Developer",
            "MERN Developer",
            "Software Developer",
            "C++ Developer"
        ];

        let wordIndex = 0;
        let charIndex = 0;
        let deleting = false;

        function typeEffect() {

            const currentWord =
                words[wordIndex];

            if (!deleting) {

                charIndex++;

                typing.textContent =
                    currentWord.substring(
                        0,
                        charIndex
                    );

                if (
                    charIndex >=
                    currentWord.length
                ) {

                    deleting = true;

                    setTimeout(
                        typeEffect,
                        1400
                    );

                    return;
                }

                setTimeout(
                    typeEffect,
                    80
                );

            } else {

                charIndex--;

                typing.textContent =
                    currentWord.substring(
                        0,
                        charIndex
                    );

                if (charIndex <= 0) {

                    deleting = false;

                    wordIndex =
                        (wordIndex + 1) %
                        words.length;

                    setTimeout(
                        typeEffect,
                        300
                    );

                    return;
                }

                setTimeout(
                    typeEffect,
                    45
                );
            }
        }

        typeEffect();
    }


    /* =====================================================
       SCROLL REVEAL
    ===================================================== */

    const revealElements =
        document.querySelectorAll(
            ".reveal"
        );

    const revealObserver =
        new IntersectionObserver(
            (entries, observer) => {

                entries.forEach(entry => {

                    if (
                        entry.isIntersecting
                    ) {

                        entry.target.classList
                            .add("active");

                        observer.unobserve(
                            entry.target
                        );
                    }
                });

            },
            {
                threshold: 0.12
            }
        );

    revealElements.forEach(
        element =>
            revealObserver.observe(element)
    );


    /* =====================================================
       ACTIVE NAVIGATION
    ===================================================== */

    const sections =
        document.querySelectorAll(
            "section[id]"
        );

    const navLinks =
        document.querySelectorAll(
            ".nav-links a"
        );

    const sectionObserver =
        new IntersectionObserver(
            entries => {

                entries.forEach(entry => {

                    if (
                        !entry.isIntersecting
                    ) {
                        return;
                    }

                    navLinks.forEach(link => {

                        link.classList.remove(
                            "active"
                        );

                        if (
                            link.getAttribute(
                                "href"
                            ) ===
                            `#${entry.target.id}`
                        ) {

                            link.classList.add(
                                "active"
                            );
                        }
                    });

                });

            },
            {
                rootMargin:
                    "-35% 0px -55% 0px"
            }
        );

    sections.forEach(
        section =>
            sectionObserver.observe(section)
    );


    /* =====================================================
       EXPERIENCE ACCORDION
    ===================================================== */

    const experienceToggle =
        document.querySelector(
            ".experience-toggle"
        );

    const experienceDetails =
        document.querySelector(
            ".experience-details"
        );

    if (
        experienceToggle &&
        experienceDetails
    ) {

        experienceToggle.addEventListener(
            "click",
            () => {

                const opened =
                    experienceDetails
                        .classList
                        .toggle("active");

                experienceToggle
                    .classList
                    .toggle(
                        "active",
                        opened
                    );
            }
        );
    }


    /* =====================================================
       THEME
    ===================================================== */

    const savedTheme =
        localStorage.getItem(
            "portfolio-theme"
        );

    if (savedTheme === "light") {

        body.classList.add(
            "light"
        );
    }

    function updateThemeIcon() {

        if (!themeToggle) {
            return;
        }

        const icon =
            themeToggle.querySelector(
                "i"
            );

        if (
            body.classList.contains(
                "light"
            )
        ) {

            icon.className =
                "fas fa-sun";

        } else {

            icon.className =
                "fas fa-moon";
        }
    }

    updateThemeIcon();

    if (themeToggle) {

        themeToggle.addEventListener(
            "click",
            () => {

                body.classList.toggle(
                    "light"
                );

                const theme =
                    body.classList.contains(
                        "light"
                    )
                        ? "light"
                        : "dark";

                localStorage.setItem(
                    "portfolio-theme",
                    theme
                );

                updateThemeIcon();
            }
        );
    }


    /* =====================================================
       MAGNETIC BUTTONS
    ===================================================== */

    if (
        window.matchMedia(
            "(pointer:fine)"
        ).matches
    ) {

        document
            .querySelectorAll(
                ".magnetic"
            )
            .forEach(button => {

                button.addEventListener(
                    "mousemove",
                    event => {

                        const rect =
                            button.getBoundingClientRect();

                        const x =
                            event.clientX -
                            rect.left -
                            rect.width / 2;

                        const y =
                            event.clientY -
                            rect.top -
                            rect.height / 2;

                        button.style.transform =
                            `translate(${x * .08}px, ${y * .08}px)`;
                    }
                );

                button.addEventListener(
                    "mouseleave",
                    () => {

                        button.style.transform =
                            "";
                    }
                );
            });
    }


    /* =====================================================
       CARD TILT
    ===================================================== */

    if (
        window.matchMedia(
            "(pointer:fine)"
        ).matches
    ) {

        const cards =
            document.querySelectorAll(
                ".project-card, .platform-card, .achievement-card"
            );

        cards.forEach(card => {

            card.addEventListener(
                "mousemove",
                event => {

                    const rect =
                        card.getBoundingClientRect();

                    const x =
                        (event.clientX -
                            rect.left) /
                        rect.width -
                        .5;

                    const y =
                        (event.clientY -
                            rect.top) /
                        rect.height -
                        .5;

                    card.style.transform =
                        `
                        perspective(900px)
                        rotateX(${y * -3}deg)
                        rotateY(${x * 3}deg)
                        translateY(-7px)
                        `;
                }
            );

            card.addEventListener(
                "mouseleave",
                () => {

                    card.style.transform =
                        "";
                }
            );
        });
    }


    /* =====================================================
       RIPPLE EFFECT
    ===================================================== */

    document
        .querySelectorAll(
            ".primary-btn, .secondary-btn, .project-links a"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                event => {

                    const rect =
                        button.getBoundingClientRect();

                    const ripple =
                        document.createElement(
                            "span"
                        );

                    ripple.className =
                        "ripple";

                    ripple.style.left =
                        `${event.clientX - rect.left}px`;

                    ripple.style.top =
                        `${event.clientY - rect.top}px`;

                    button.appendChild(
                        ripple
                    );

                    setTimeout(
                        () => ripple.remove(),
                        650
                    );
                }
            );
        });


    /* =====================================================
       CONTACT FORM
    ===================================================== */

    const contactForm =
        document.getElementById(
            "contactForm"
        );

    if (contactForm) {

        contactForm.addEventListener(
            "submit",
            event => {

                event.preventDefault();

                const button =
                    contactForm.querySelector(
                        ".form-submit"
                    );

                if (!button) {
                    return;
                }

                const original =
                    button.innerHTML;

                button.innerHTML =
                    `
                    <span>Message Ready ✓</span>
                    <i class="fas fa-check"></i>
                    `;

                button.style.background =
                    "#16a34a";

                setTimeout(
                    () => {

                        button.innerHTML =
                            original;

                        button.style.background =
                            "";
                    },
                    2200
                );

                contactForm.reset();
            }
        );
    }


    /* =====================================================
       COUNTER ANIMATION
    ===================================================== */

    const statNumbers =
        document.querySelectorAll(
            ".stat-number, .achievement-stats strong"
        );

    function animateCounter(element) {

        if (
            element.dataset.animated
        ) {
            return;
        }

        const text =
            element.textContent.trim();

        const match =
            text.match(
                /^([\d,.]+)(.*)$/
            );

        if (!match) {
            return;
        }

        const target =
            Number(
                match[1].replace(
                    /,/g,
                    ""
                )
            );

        const suffix =
            match[2];

        if (
            !Number.isFinite(target)
        ) {
            return;
        }

        element.dataset.animated =
            "true";

        const duration = 1000;

        const start =
            performance.now();

        function update(time) {

            const progress =
                Math.min(
                    (time - start) /
                    duration,
                    1
                );

            const eased =
                1 -
                Math.pow(
                    1 - progress,
                    3
                );

            const value =
                target * eased;

            if (
                Number.isInteger(
                    target
                )
            ) {

                element.textContent =
                    Math.floor(
                        value
                    ).toLocaleString() +
                    suffix;

            } else {

                element.textContent =
                    value.toFixed(2) +
                    suffix;
            }

            if (
                progress < 1
            ) {

                requestAnimationFrame(
                    update
                );
            }
        }

        requestAnimationFrame(
            update
        );
    }

    const counterObserver =
        new IntersectionObserver(
            entries => {

                entries.forEach(
                    entry => {

                        if (
                            entry.isIntersecting
                        ) {

                            animateCounter(
                                entry.target
                            );

                            counterObserver
                                .unobserve(
                                    entry.target
                                );
                        }
                    }
                );

            },
            {
                threshold: .7
            }
        );

    statNumbers.forEach(
        element =>
            counterObserver.observe(
                element
            )
    );

});