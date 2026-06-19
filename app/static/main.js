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