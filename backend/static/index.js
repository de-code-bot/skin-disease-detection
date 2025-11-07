document.addEventListener('DOMContentLoaded', () => {
    const image_upload = document.getElementById('imageUpload');
    const submit_button = document.getElementById('analyzeBtn');
    const result_field = document.getElementById('results');
    const result_text = document.getElementById('resultText')

    if (!(image_upload && submit_button && result_field && result_text)){
        alert('HTML invalid, missing required elements');
        return;
    }

    submit_button.addEventListener('click', async () => {
        const image = image_upload.files[0];
        const formData = new FormData();
        formData.append("image", image);

        result_field.style.display = 'block';
        const response = await fetch("/api/v1/predictions", {
            method : 'POST',
            body : formData
        });

        if (!response.ok){
            alert("Failed to analyse image");
            return;
        }

        const data = await response.json();
        result_text.innerText = data.result

        if (data.hasOwnProperty('additional')) {
            Object.entries(data.additional).forEach(([key, value]) => {
                console.info(`${key}: ${value}`);
            });
        }
    });
});