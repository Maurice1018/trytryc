document.addEventListener("DOMContentLoaded", () => {
    const refreshButton = document.getElementById("refreshButton");
    const resultElement = document.getElementById("result");

    refreshButton.addEventListener("click", async () => {
        resultElement.textContent = "Refreshing...";
        try {
            const response = await fetch('/api/refresh-session');
            const result = await response.json();
            resultElement.textContent = `Message: ${result.message}`;
        } catch (error) {
            resultElement.textContent = `Error: ${error.message}`;
        }
    });
});
