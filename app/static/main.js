// Copy to clipboard
function copyCode() {
    const code = document.querySelector(".code-block code");
    const btn = document.querySelector(".copy-btn");

    if (!code || !btn) return;

    navigator.clipboard.writeText(code.innerText).then(() => {
        btn.textContent = "Copied!";
        btn.style.background = "#3ecf8e";
        btn.style.color = "#17140f";

        setTimeout(() => {
            btn.textContent = "Copy";
            btn.style.background = "";
            btn.style.color = "";
        }, 2000);
    });
}

// Auto dismiss flash messages
document.addEventListener("DOMContentLoaded", () => {
    const flashes = document.querySelectorAll(".flash");
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.transition = "opacity 0.5s";
            flash.style.opacity = "0";
            setTimeout(() => flash.remove(), 500);
        }, 3000);
    });
});


function openModal(id, title) {
    document.getElementById("modalSnipTitle").textContent = '"' + title + '"';
    document.getElementById("modalDeleteForm").action = "/delete/" + id;
    document.getElementById("deleteModal").classList.add("active");
}

function closeModal() {
    document.getElementById("deleteModal").classList.remove("active");
}


function openSidebar() {
    document.getElementById("sidebarOverlay").classList.add("active");
    document.getElementById("sidebarToggle").setAttribute("aria-expanded", "true");
}

function closeSidebar() {
    document.getElementById("sidebarOverlay").classList.remove("active");
    document.getElementById("sidebarToggle").setAttribute("aria-expanded", "false");
}

// Close sidebar on overlay click, same pattern as delete modal
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("sidebarOverlay").addEventListener("click", function(e) {
        if (e.target === this) closeSidebar();
    });
});

// Close sidebar on Escape key
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeSidebar();
});

// Close modal on overlay click
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("deleteModal").addEventListener("click", function(e) {
        if (e.target === this) closeModal();
    });
});

// ── Theme toggle ──
function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${value}; expires=${expires}; path=/`;
}

function getCookie(name) {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith(name + "="))
        ?.split("=")[1];
}

function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "light" ? "dark" : "light";
    applyTheme(next);
    setCookie("theme", next, 365);
}

function applyTheme(theme) {
    if (theme === "light") {
        document.documentElement.setAttribute("data-theme", "light");
    } else {
        document.documentElement.removeAttribute("data-theme");
    }
}

// Apply saved theme on load
document.addEventListener("DOMContentLoaded", () => {
    const saved = getCookie("theme");
    if (saved === "light") applyTheme("light");
});