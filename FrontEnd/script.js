document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("analyze-btn");
    const output = document.getElementById("output");

    button.addEventListener("click", function () {
        chrome.tabs.query({ active: true, currentWindow: true }, async function (tabs) {
            const currentUrl = tabs[0].url;
            const apiUrl = `http://192.168.37.69:50000/start_orchestration/?url=${encodeURIComponent(currentUrl)}`;

            try {
                const response = await fetch(apiUrl, { method: "GET" });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const result = await response.json();
                console.log(result);

                const prediction = result.execution_output.prediction.toLowerCase();
                const confidence = result.execution_output.confidence;
                
                if (prediction === "legitimate") {
                    output.className = "legitimate";
                    output.innerHTML = `✅ <strong>Safe Website</strong> <br> Confidence: ${confidence}%`;
                } else {
                    output.className = "fraudulent";
                    output.innerHTML = `❌ <strong>Fraudulent Website</strong> <br> Confidence: ${confidence}%`;
                }

            } catch (error) {
                console.error(error);
                output.className = "error";
                output.innerHTML = `⚠️ Error: ${error.message}`;
            }

            output.style.display = "block";
            output.style.opacity = "1";
        });
    });
});