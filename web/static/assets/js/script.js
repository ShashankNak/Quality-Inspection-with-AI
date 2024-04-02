async function uploadVideo() {

    var fileInput = document.getElementById('videoInput');
    var videoContainer = document.getElementById('videoPlayer');
    if (videoContainer.src != '') {
        return;
    }



    var modelSelect = document.getElementById('model');
    var videoFile = fileInput.files[0];
    var model = modelSelect.value;

    if (!videoFile) {
        alert('Please select a video file');
        return;
    }

    var formData = new FormData();
    formData.append('video', videoFile);
    formData.append('model', model);


    try {
        const response = await fetch('/predictVideo', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error uploading video');
        }

        const data = await response.json();

        var outputVideoUrl = data.output_video_url;
        console.log(outputVideoUrl);
        if (outputVideoUrl) {
            videoContainer.innerHTML = '<source src="../../../' + outputVideoUrl + '" type="video/mp4">';
        } else {
            throw new Error('Error: No output video URL received');
        }
    } catch (error) {
        alert(error.message);
        location.reload();
    }

}




// Event listener for file input change event
document.getElementById('videoInput').addEventListener('change', function () {
    const fileInfoContainer = document.getElementById('fileInfo');
    const fileInputContainer = document.getElementById('videoInputContainer');
    const fileOutputContainer = document.getElementById('videoOutputContainer');
    const fileName = this.files[0].name;

    // Hide the file input and show the file name and restart button
    fileInputContainer.style.display = 'none';
    fileOutputContainer.style.display = 'flex';
    fileInfoContainer.style.display = 'flex';
    fileInfoContainer.textContent = 'Selected file: ' + fileName;
    document.getElementById('restartButton').style.display = 'inline';
});

// Function to restart file input
function restartFileInput() {
    const fileInfoContainer = document.getElementById('fileInfo');
    const fileInputContainer = document.getElementById('videoInputContainer');
    const fileOutputContainer = document.getElementById('videoOutputContainer');
    const videoPlayer = document.getElementById('videoPlayer');


    // Show the file input and hide the file name and restart button
    fileInputContainer.style.display = 'flex';
    fileInfoContainer.style.display = 'none';
    fileOutputContainer.style.display = 'none';
    videoPlayer.src = '';
    videoPlayer.innerHTML = '';

    document.getElementById('restartButton').style.display = 'none';
    location.reload();


    // Clear the file input value
    document.getElementById('videoInput').value = '';
}

class videoFile{
    constructor(fileName){
        this.fileName = fileName;
    }

}

async function samplevideoPlay(str) {
    const videoPlayer = document.getElementById("sampleVideoPlayer");
    const selectedProduct = document.getElementById("selectedProduct");
    if (videoPlayer.innerHTML == "") {
        videoPlayer.innerHTML = '<source src="../../../static/input/' + str + '_test.mp4" type="video/mp4">';
        selectedProduct.innerHTML = str
    } else {
        location.reload();
    }
}


function outputvideoPlay() {
    const videoPlayer = document.getElementById("sampleVideoPlayerOutput");
    const product = document.getElementById("selectedProduct");
    videoPlayer.innerHTML = '<source src="../../../static/output/' + product.innerHTML + '_test.mp4" type="video/mp4">';
}
