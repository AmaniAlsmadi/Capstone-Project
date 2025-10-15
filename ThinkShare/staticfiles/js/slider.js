const sliders = {};

function nextSlide(articleId) {
    const container = document.getElementById(`slider-${articleId}`);
    const slides = container.querySelector('.slides');
    const total = slides.children.length;
    if (!sliders[articleId]) sliders[articleId] = 0;
    sliders[articleId] = (sliders[articleId] + 1) % total;
    slides.style.transform = `translateX(-${sliders[articleId] * 100}%)`;
}

function prevSlide(articleId) {
    const container = document.getElementById(`slider-${articleId}`);
    const slides = container.querySelector('.slides');
    const total = slides.children.length;
    if (!sliders[articleId]) sliders[articleId] = 0;
    sliders[articleId] = (sliders[articleId] - 1 + total) % total;
    slides.style.transform = `translateX(-${sliders[articleId] * 100}%)`;
}
