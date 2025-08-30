document.addEventListener('DOMContentLoaded', () => {
  // ===== MENU TOGGLE =====
  const menuButton = document.querySelector('.menu_button button');
  const navbar = document.querySelector('.navbar');

  if (menuButton) {
    menuButton.addEventListener('click', (e) => {
      e.stopPropagation();
      navbar.classList.toggle('active');
    });

    document.addEventListener('click', (e) => {
      if (!navbar.contains(e.target) && !menuButton.contains(e.target)) {
        navbar.classList.remove('active');
      }
    });
  }

  // ===== IMAGE POPUP =====
  const carImages = document.querySelectorAll('.highlighted-cars .car img');
  carImages.forEach(img => {
    img.addEventListener('click', () => {
      const overlay = document.createElement('div');
      overlay.classList.add('image-popup-overlay');

      const fullImage = document.createElement('img');
      fullImage.src = img.src;
      fullImage.classList.add('image-popup-full');

      overlay.appendChild(fullImage);
      document.body.appendChild(overlay);

      overlay.addEventListener('click', () => {
        overlay.remove();
      });
    });
  });

  // ===== VIEW DETAILS (Mobile only) =====
  const isMobile = window.matchMedia("(max-width: 600px)").matches;
  const carsModal = document.getElementById('carsModal');
  const detailButtons = document.querySelectorAll('.cars-details-btn');
  const closeCarsModalBtn = document.querySelector('.cars-close-btn');

  if (carsModal && detailButtons.length > 0 && closeCarsModalBtn) {
    if (isMobile) {
      detailButtons.forEach(button => {
        button.addEventListener('click', () => {
          carsModal.style.display = 'block';
        });
      });

      closeCarsModalBtn.addEventListener('click', () => {
        carsModal.style.display = 'none';
      });

      window.addEventListener('click', (event) => {
        if (event.target === carsModal) {
          carsModal.style.display = 'none';
        }
      });
    } else {
      detailButtons.forEach(button => {
        button.disabled = true;
        button.style.opacity = "0.5";
        button.style.cursor = "not-allowed";
        button.title = "Available only on mobile";
      });
    }
  }

  // ===== Fetch and display cars dynamically =====
  fetch('https://car-backend-4zsn.onrender.com/cars')  // Fetch cars from the Flask backend
    .then(response => response.json())  // Convert response to JSON
    .then(data => {
      const container = document.querySelector('.highlighted-cars');
      container.innerHTML = '';  // Clear existing cars

      // Loop through the fetched cars and display each one
     data.forEach(car => {
  const carDiv = document.createElement('div');
  carDiv.classList.add('car');

  carDiv.innerHTML = `
    <img src="${car.image}" alt="${car.name}">
    <p class="description">${car.name}</p>
    <p class="price">₱${car.price}</p>
  `;

  container.appendChild(carDiv);
});

    })
    .catch(error => console.error('Error fetching cars:', error));  // Handle any errors
});
