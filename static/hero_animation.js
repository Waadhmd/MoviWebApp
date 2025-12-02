document.addEventListener("DOMContentLoaded", function () {
  const titleElement = document.getElementById("cineshelf-title");
  const iconElement = document.getElementById("popcorn-icon");
  const fullText = "CineShelf";
  let charIndex = 0;
  const typingDelay = 150; // Delay in milliseconds between each letter

  if (!titleElement) return;

  function typeTitle() {
    if (charIndex < fullText.length) {
      let char = fullText.charAt(charIndex);

      // Apply accent color to 'Shelf'
      if (charIndex >= 4) {
        // 'Cine' is 0-3, 'Shelf' starts at 4
        titleElement.innerHTML += `<span class="text-accent-js">${char}</span>`;
      } else {
        titleElement.innerHTML += char;
      }

      charIndex++;
      setTimeout(typeTitle, typingDelay);
    } else {
      // Typing finished, show the popcorn icon with a delay
      setTimeout(showPopcorn, 500);
    }
  }

  function showPopcorn() {
    if (iconElement) {
      // Remove the 'hidden-icon' class which triggers the CSS transition
      iconElement.classList.remove("hidden-icon");
      iconElement.classList.add("visible-icon");
    }
  }

  // Start the animation after a short initial pause
  setTimeout(typeTitle, 500);
});
