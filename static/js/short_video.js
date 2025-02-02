let page = 1;
let loading = false;

const loadVideos = async () =>{
    if(loading){
        return
    }
    loading = true;
    try{
        const response = await fetch(`/videos/?page=${page}`)
        const data = await response.json()
        console.log(data.videos);
        renderVideos(data.videos)
        page++;
    }
    catch(error){
        console.log("Error loading videos", error);
    }
    finally{
        loading = false;
    }
}

const renderVideos = (videos) =>{
    const container = document.getElementById('video-container')
    videos.forEach(video =>{
        const videoWrapper = document.createElement('div')
        videoWrapper.className = 'video-item-wrapper';
        
        const videoElement = document.createElement('video')
        videoElement.src = video.video;
        videoElement.muted = true; // Mute video for hover playback
        videoElement.loop = true; // Enable looping
        videoElement.className = 'video-item';

        videoElement.addEventListener('mouseover', ()=>{
            videoElement.play()
        })

        videoElement.addEventListener('mouseleave', ()=>{
            videoElement.pause()
        })

        // const playButton = document.createElement("button");
        // playButton.className = "bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600";
        // playButton.textContent = "Play";

        videoElement.addEventListener('click', ()=>{
            console.log("clicked video");
            window.location.href =`/video/${video.id}`;
        })

        videoWrapper.appendChild(videoElement)
        // videoWrapper.appendChild(playButton)
        container.appendChild(videoElement)
        
    })
}

window.addEventListener('scroll', ()=>{
    if(window.innerHeight + window.scrollY >= document.body.offsetHeight){
        loadVideos()
    }
})

document.addEventListener('DOMContentLoaded', loadVideos)

// const observer = new IntersectionObserver((entries) => {
//     entries.forEach(entry => {
//         const video = entry.target;
//         if (entry.isIntersecting) {
//             video.play();
//         } else {
//             video.pause();
//         }
//     });
// });

// document.querySelectorAll('.video-item').forEach(video => {
//     observer.observe(video);
// });


let relatedPage = 1;
let relatedLoading = false;

// Load related videos
const loadRelatedVideos = async () => {
    if (relatedLoading) return;
    relatedLoading = true;

    try {
        const response = await fetch(`/related-videos/{{ video.id }}?page=${relatedPage}`);
        const data = await response.json();
        console.log(data.videos);
        renderRelatedVideos(data.videos);
        relatedPage++;
    } catch (error) {
        console.error("Error loading related videos:", error);
    } finally {
        relatedLoading = false;
    }
};

// Render related videos
const renderRelatedVideos = (videos) => {
    const container = document.getElementById("related-video-container");
    videos.forEach((video) => {
        const videoWrapper = document.createElement("div");
        videoWrapper.className = "related-video-wrapper flex items-center gap-4 rounded-lg shadow-lg p-4 bg-white";

        const videoElement = document.createElement("video");
        videoElement.src = video.video; // Video URL
        videoElement.muted = true;
        videoElement.loop = true;
        videoElement.className = "w-32 h-20 rounded-lg object-cover";
        videoElement.addEventListener("mouseover", () => videoElement.play());
        videoElement.addEventListener("mouseleave", () => videoElement.pause());

        const playButton = document.createElement("button");
        playButton.className = "bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600";
        playButton.textContent = "Play";
        playButton.addEventListener("click", () => {
            window.location.href = `/video/${video.id}`; // Navigate to a different video
        });

        videoWrapper.appendChild(videoElement);
        videoWrapper.appendChild(playButton);
        container.appendChild(videoWrapper);
    });
};

// Infinite scroll for related videos
window.addEventListener("scroll", () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        loadRelatedVideos();
    }
});

// Initial load
document.addEventListener("DOMContentLoaded", loadRelatedVideos);
