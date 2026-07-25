// Copy to clipboard (detail page)
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

// Copy snippet from card (index page)
function copyCardCode(btn) {
    const card = btn.closest(".snippet-card");
    const codeEl = card.querySelector("pre code, .card-code");
    if (!codeEl) return;
    const text = codeEl.innerText || codeEl.textContent;
    const label = btn.querySelector(".copy-label");

    navigator.clipboard.writeText(text)
        .then(() => flashCopy(btn, label))
        .catch(() => {
            const ta = document.createElement("textarea");
            ta.value = text;
            ta.style.position = "fixed";
            ta.style.opacity = "0";
            document.body.appendChild(ta);
            ta.select();
            document.execCommand("copy");
            document.body.removeChild(ta);
            flashCopy(btn, label);
        });
}

function flashCopy(btn, label) {
    const prev = label ? label.textContent : "";
    if (label) label.textContent = "Copied!";
    btn.classList.add("copied");
    setTimeout(() => {
        if (label) label.textContent = prev || "Copy";
        btn.classList.remove("copied");
    }, 2000);
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

// Close modal on overlay click
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("deleteModal").addEventListener("click", function(e) {
        if (e.target === this) closeModal();
    });
});
