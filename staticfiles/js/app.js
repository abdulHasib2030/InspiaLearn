//  ------------ input search field navber ------------ //
const searchBar = document.getElementById('search-icon')
const navSearch = document.getElementById('nav-search');

searchBar.addEventListener('click', function(){
    setTimeout(() => {
        navSearch.classList.add('hidden')
        document.getElementById('input-search').classList = 'block'
    }, 300)


})

const closeSearch = document.getElementById('close-search')

closeSearch.addEventListener('click', function(){
   setTimeout(() =>{
    document.getElementById('input-search').classList = 'hidden'
    navSearch.classList.remove('hidden')
   }, 300)

})

// ------------ responsive menu bar --------------------//
// const isAuthenticated = document.getElementById('menu-button').getAttribute('data-authenticated') === 'true';
// if (!isAuthenticated){
//     const menuButton = document.getElementById('menu-button');
//     const menuContent = document.getElementById('menu-content');
    
//     // Toggle dropdown visibility when the menu button is clicked
//     menuButton.addEventListener('click', function() {
//         menuContent.classList.toggle('hidden');
//     });
    
//     // Close the menu when clicking outside of it
//     document.addEventListener('click', function(event) {
//         if (!menuButton.contains(event.target) && !menuContent.contains(event.target)) {
//             menuContent.classList.add('hidden');
//         }
//     });

// }


//  ------------ carosoul banner section ---------------- //
const bannerCarousel = document.getElementById('carouselSlides');
const bannerPrevButton = document.getElementById('prevButton');
const bannerNextButton = document.getElementById('nextButton');
let currentSlide = 0;
const totalSlides = 2; // Two slides

// Handle Next button click
bannerNextButton.addEventListener('click', () => {
  moveToNextSlide()
});


setInterval(() => {
    moveToPrevSlide()
}, 2000);

const moveToNextSlide =()=>{
    if (currentSlide < totalSlides - 1) {
        currentSlide++;
    } else {
        currentSlide = 0; // Loop back to the first slide
    
    }
    updateCarousel();
}

// Handle Previous button click
bannerPrevButton.addEventListener('click', () => {
    moveToPrevSlide()
});

const moveToPrevSlide = () =>{
    if (currentSlide > 0) {
        currentSlide--;
    } else {
        currentSlide = totalSlides - 1; // Loop to the last slide
    }
    updateCarousel();
}

// Update Carousel Slide
function updateCarousel() {
const offset = currentSlide * -100; // Move to the current slide
bannerCarousel.style.transform = `translateX(${offset}%)`;
}


// ------------ carosul main section start --------------//

document.querySelectorAll('.carousel-wrapper').forEach(wrapper =>{

    const carousel = wrapper.querySelector('.carousel-id');
   
    const prevBtn = wrapper.querySelector('.prev');
    const nextBtn = wrapper.querySelector('.next');
    let scrollAmount = 0;

    prevBtn.style.display = 'none';

    function updateButtonVisibility(){
        if (carousel.scrollLeft === 0) {
            prevBtn.style.display = 'none';
        } else {
            prevBtn.style.display = 'block';
        }

        if (carousel.scrollWidth - carousel.clientWidth === carousel.scrollLeft) {
            nextBtn.style.display = 'none';
        } else {
            nextBtn.style.display = 'block';
        }
    }

    // Handle Next Button
    nextBtn.addEventListener('click', () => {
      const maxScrollLeft = carousel.scrollWidth - carousel.clientWidth;
      scrollAmount = Math.min(maxScrollLeft, scrollAmount + carousel.clientWidth);
      carousel.scrollTo({
        left: scrollAmount,
        behavior: 'smooth'
      });
      setTimeout(updateButtonVisibility, 500)
    });

    // Handle Prev Button
    prevBtn.addEventListener('click', () => {
      scrollAmount = Math.max(0, scrollAmount - carousel.clientWidth);
      carousel.scrollTo({
        left: scrollAmount,
        behavior: 'smooth'
      });
      setTimeout(updateButtonVisibility, 500);
    });
})

