
document.addEventListener("DOMContentLoaded", function() {
    const input = document.getElementById('images');
    const preview = document.getElementById('preview');

    input.addEventListener('change', function() {
        preview.innerHTML = ''; 
        const files = input.files;

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            if (!file.type.startsWith('image/')) continue;

            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.width = 150; 
                img.style.margin = '5px';
                preview.appendChild(img);
            }
            reader.readAsDataURL(file);
        }
    });
});