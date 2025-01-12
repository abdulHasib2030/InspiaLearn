document.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById("customVideo");
    const playButton = document.getElementById("playButton");

    // Initially show the play button
    playButton.addEventListener("click", () => {
        video.play();
        // playButton.classList.add("hidden");
        video.setAttribute("controls", "controls");
        video.classList.add("show-controls");
    });

    // Show play button again when the video is paused
    video.addEventListener("pause", () => {
        playButton.classList.remove("hidden");
        // video.removeAttribute("controls");
        // video.classList.remove("show-controls");
    });

    // Keep controls visible during playback
    video.addEventListener("play", () => {
        playButton.classList.add("hidden");

        video.setAttribute("controls", "controls");
    });
});
