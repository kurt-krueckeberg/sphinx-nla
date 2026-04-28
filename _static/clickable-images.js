document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelectorAll("img.image-override, img.img-override")
    .forEach(function (img) {
      const imageUrl = img.currentSrc || img.src;

      if (!imageUrl) return;

      const link = document.createElement("a");
      link.href = imageUrl;
      link.target = "_blank";
      link.rel = "noopener";
      link.title = "Open image in new tab";

      img.parentNode.insertBefore(link, img);
      link.appendChild(img);

      img.style.cursor = "zoom-in";
    });
});
