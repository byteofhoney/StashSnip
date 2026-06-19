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

// Close modal on overlay click
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("deleteModal").addEventListener("click", function(e) {
        if (e.target === this) closeModal();
    });
});