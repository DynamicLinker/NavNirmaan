async function uploadImage() {
    const fileInput = document.getElementById('imageInput');
    const statusText = document.getElementById('statusText');

    if (fileInput.files.length === 0) {
        alert('Please select an image to upload.');
        return;
    }

    const formdata = new FormData();
    formdata.append("file", fileInput.files[0]);

    statusText.innerText = "analyzing floor plan... (this may take a minute)";

    try {
        const response = await fetch("http://localhost:8000/api/v1/generate-3d", {
            method: "POST",
            body: formdata
        });

        if (!response.ok) {
            if (response.status === 429){
                throw new Error("Too many requests. Server busy. Please try later.");
            }
            throw new Error("Failed to generate model. Please try again");
        }

        statusText.innerText = "Model Generated! Loading model...."


        const blob = await response.blob();


        const modelUrl = URL.createObjectURL(blob);


        const houseAsset = document.getElementById('house');
        const houseEntity = document.getElementById('house-entity');


        
        houseAsset.setAttribute("src", modelUrl);
        houseEntity.removeAttribute('gltf-model');

        setTimeout(() => {
            houseEntity.setAttribute('gltf-model', '#house');
            statusText.innerText = "click screen to walk around.";
        }, 50);

    } catch (error) {
        console.error(error);
        statusText.innerText = "error occured.";
    }

}