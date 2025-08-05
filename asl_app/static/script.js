const video = document.getElementById('webcam');
const canvas = document.getElementById('canvas');
const output = document.getElementById('output');
const ctx = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
    setInterval(sendFrame, 1000); // Every 1 second
  });

function sendFrame() {
  ctx.drawImage(video, 0, 0, 224, 224);
  canvas.toBlob(blob => {
    const formData = new FormData();
    formData.append('image', blob, 'frame.jpg');

    fetch('/predict', {
      method: 'POST',
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      output.innerText = data.prediction;
    })
    .catch(err => {
      console.error("Prediction error:", err);
    });
  }, 'image/jpeg');
}
