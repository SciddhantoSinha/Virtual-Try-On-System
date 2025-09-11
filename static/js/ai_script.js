document.getElementById("predictBtn").addEventListener("click", () => {
    const fileInput = document.getElementById("fileInput");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/predict", {
        method: "POST",
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("predictionOutput").innerText = `Error: ${data.error}`;
            } else {
                document.getElementById("predictionOutput").innerText = `
                    Predicted Measurements:
                    Height: ${data.height.toFixed(2)} cm,
                    Weight: ${data.weight.toFixed(2)} kg,
                    Chest: ${data.chest.toFixed(2)} cm
                `;
                updateARVisualization(data.height, data.weight, data.chest);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById("predictionOutput").innerText = "An error occurred.";
        });
});
