
function searchDish() {
    const query = document.getElementById('searchInput').value.toLowerCase().trim();
    if (!query) {
        alert('Please enter a search term!');
        return;
    }

    const dishes = document.querySelectorAll('.dish-card');
    let found = false;

    // Remove previous highlights
    dishes.forEach(d => d.classList.remove('highlight'));

    for (let dish of dishes) {
        const dishName = dish.querySelector('h3').innerText.toLowerCase();
        if (dishName.includes(query)) {
            dish.classList.add('highlight');
            dish.scrollIntoView({ behavior: 'smooth', block: 'center' });
            found = true;
            break;
        }
    }
}
function showImage(btn) {
  const modal = document.getElementById('imageModal');
  const popupImage = document.getElementById('popupImage');

  // ✅ Read the image path from the button's data-src
  const imagePath = btn.getAttribute('data-src');
  popupImage.src = imagePath;

  modal.style.display = "block";
}

function closeImage() {
  document.getElementById('imageModal').style.display = "none";
}
