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
    }, 3000);
    
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
    

    
    // ------------- Category section start ------------------------//
    let storeCategoryData = []
    
        fetch('home/catgory/')
        .then(res => res.json())
        .then(data => {
      
            updataCategoryData(data)
        })
    
    function updataCategoryData(data){
        const dataCategoryAll =document.getElementById('data-category')
        dataCategoryAll.innerHTML = ''
       
        
    
        data?.map((item)=> {
            
            const div = document.createElement('div');
            const urlSet = `/course/${item.uid}/`
            
            div.classList ="carousel-item  md:w-1/3 lg:w-1/5 w-4/5 bg-white my-4 h-full  rounded-lg   duration-300 ease-in-out transition-transform transform hover:-translate-y-2 cursor-pointer"
            div.innerHTML = ` <a href="${urlSet}">
                 <div class="card card-compact h-full bg-base-100  border-2">
                <figure>
                    <img
                    src=${item.image}
                    alt="not found image" />
                </figure>
                <div class="card-body gap-0 ">
                    <h2 class="card-title ">${item.title}</h2>
                       <!-- Author Name -->
                        <p class=" text-sm text-gray-700">${item.instructor}</p>
    
                       
    
                        <!-- Price -->
                        <p class=" mt-2 font-bold gap-3"> <i class="fa-solid fa-bangladeshi-taka-sign"></i> ${item.after_discount} 
                        <del><i class="fa-solid fa-bangladeshi-taka-sign ml-3"></i> ${item.main_price}</del> <span>${item.percent}% off</span>
                        </p>
    
                        <!-- Add to Cart Button -->
                        <button class="mt-4 w-full bg-gradient-to-r from-[#1D72ED]  to-[#2ABAEE] font-semibold text-xl text-white py-2 rounded-md ">
                            Add to Cart
                        </button>
                </div>
            </div>
                </a>`;
            dataCategoryAll.appendChild(div);
        });
    
    
    }
    
    
    function dataNotFonnd(){
        const dataCategoryAll =document.getElementById('data-category')
        dataCategoryAll.innerHTML = `
        <h1 class="text-2xl font-bold text-center mx-auto ">
            We couldn't find any courses matching the selected category.
            
            </h1>
          
        `
    
    }
    
    const categoryBtnClik = (data) =>{
       const dataCategory = {category:data}
      fetch('home/catgory/', {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': getCookie('csrftoken') 
        },
        body: JSON.stringify(dataCategory)
      })
      .then(res => res.json())
      .then(data => {
        storeCategoryData = [];
        if (!data || data.length === 0) {
            dataNotFonnd()
        }
        else{
            
            updataCategoryData(data)
            
        }
      })
    
    }
    
    // console.log(storeCategoryData);
    
    function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.startsWith(name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
    
    // ------------ carosul main section start --------------//
    
    // document.querySelectorAll('.carousel-wrapper').forEach(wrapper =>{
    
    //     const carousel = wrapper.querySelector('.carousel-id');
       
    //     const prevBtn = wrapper.querySelector('.prev');
    //     const nextBtn = wrapper.querySelector('.next');
    //     let scrollAmount = 0;
    
    //     prevBtn.style.display = 'none';
    
    //     function updateButtonVisibility(){
    //         if (carousel.scrollLeft === 0) {
    //             prevBtn.style.display = 'none';
    //         } else {
    //             prevBtn.style.display = 'block';
    //         }
    
    //         if (carousel.scrollWidth - carousel.clientWidth === carousel.scrollLeft) {
    //             nextBtn.style.display = 'none';
    //         } else {
    //             nextBtn.style.display = 'block';
    //         }
    //     }
    
    //     // Handle Next Button
    //     nextBtn.addEventListener('click', () => {
    //       const maxScrollLeft = carousel.scrollWidth - carousel.clientWidth;
    //       scrollAmount = Math.min(maxScrollLeft, scrollAmount + carousel.clientWidth);
    //       carousel.scrollTo({
    //         left: scrollAmount,
    //         behavior: 'smooth'
    //       });
    //       setTimeout(updateButtonVisibility, 500)
    //     });
    
    //     // Handle Prev Button
    //     prevBtn.addEventListener('click', () => {
    //       scrollAmount = Math.max(0, scrollAmount - carousel.clientWidth);
    //       carousel.scrollTo({
    //         left: scrollAmount,
    //         behavior: 'smooth'
    //       });
    //       setTimeout(updateButtonVisibility, 500);
    //     });
    // })