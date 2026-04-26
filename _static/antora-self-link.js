document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".antora-self-link img, img.antora-self-link").forEach(function (img) {
    if (img.closest("a")) return;

    const link = document.createElement("a");
    link.href = img.currentSrc || img.getAttribute("src");
    link.className = "image-reference antora-self-link-reference";

    img.parentNode.insertBefore(link, img);
    link.appendChild(img);
  });
});
