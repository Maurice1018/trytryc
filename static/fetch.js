document.addEventListener("DOMContentLoaded", () => {
    const refreshButton = document.getElementById("fetchButton");
    const resultElement = document.getElementById("result");

    refreshButton.addEventListener("click", async () => {
        resultElement.textContent = "Fetching...";
        try {
            const response = await fetch('/api/fetch-data');
            const result = await response.json();
            resultElement.textContent = `Message: ${result.message}`;
        } catch (error) {
            resultElement.textContent = `Error: ${error.message}`;
        }
    });
});
