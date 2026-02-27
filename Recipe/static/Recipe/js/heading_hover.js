document.addEventListener("DOMContentLoaded", function () {
    const jumpifyHeading = (el) => {
        if (!el || (el.dataset && el.dataset.jumpified === "1")) return;
        if (el.childElementCount > 0) return;

        const text = el.textContent || "";
        const label = text.trim();
        if (!label) return;

        el.dataset.jumpified = "1";
        el.classList.add("jump-heading");
        el.setAttribute("aria-label", label);
        el.textContent = "";

        Array.from(text).forEach((ch, index) => {
            const span = document.createElement("span");
            span.className = "jump-letter";
            span.setAttribute("aria-hidden", "true");
            span.style.setProperty("--i", index);
            if (ch === " ") {
                span.innerHTML = "&nbsp;";
            } else {
                span.textContent = ch;
            }
            el.appendChild(span);
        });
    };

    document.querySelectorAll("h1, h2, h3").forEach(jumpifyHeading);
});
