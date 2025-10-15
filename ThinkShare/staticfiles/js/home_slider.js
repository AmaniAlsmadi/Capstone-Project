let currentIndex = 0;

document.addEventListener("DOMContentLoaded", () => {
    const slidesContainer = document.querySelector(".slides");
    const slides = slidesContainer.querySelectorAll(".slide");

    function showSlide(index) {
        const total = slides.length;

        if (index >= total) currentIndex = 0;
        else if (index < 0) currentIndex = total - 1;
        else currentIndex = index;

        slidesContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    window.nextSlide = function() {
        showSlide(currentIndex + 1);
    }

    window.prevSlide = function() {
        showSlide(currentIndex - 1);
    }

    setInterval(() => nextSlide(), 5000);
});
