document.addEventListener("DOMContentLoaded", function() {
    const contentArea = document.getElementById("content");
    if (!contentArea) return;

    const simplemde = new SimpleMDE({
        element: contentArea,
        spellChecker: true,
        placeholder: "Write your article here using Markdown...",
        autosave: { enabled: false },
        status: false,
    });

    const form = contentArea.closest("form");
    if (form) {
        form.addEventListener("submit", function() {
            contentArea.value = simplemde.value();
        });
    }
});