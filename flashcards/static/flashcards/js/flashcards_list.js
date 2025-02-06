document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector("input");
    const paragraph = document.querySelector("p");

    let frontText = window.pageData.front;
    let backText = window.pageData.back;

    paragraph.textContent = frontText;
    let isFront = true;

    button.addEventListener("click", () => {
        isFront = !isFront;
        paragraph.textContent = isFront ? frontText : backText;
    });
});