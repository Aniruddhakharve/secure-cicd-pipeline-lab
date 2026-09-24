function updateStatus(elementId, text, className) {
    const element = document.getElementById(elementId);

    element.textContent = text;
    element.classList.remove(
        "health-healthy",
        "health-unhealthy",
        "health-checking"
    );
    element.classList.add(className);
}


async function checkHealth() {
    try {
        const response = await fetch("/health", {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        const data = await response.json();

        if (response.ok && data.status === "healthy") {
            updateStatus(
                "application-status",
                "Healthy",
                "health-healthy"
            );

            updateStatus(
                "database-status",
                "Connected",
                "health-healthy"
            );

            return;
        }

        updateStatus(
            "application-status",
            "Degraded",
            "health-unhealthy"
        );

        updateStatus(
            "database-status",
            "Disconnected",
            "health-unhealthy"
        );

    } catch (error) {
        updateStatus(
            "application-status",
            "Unavailable",
            "health-unhealthy"
        );

        updateStatus(
            "database-status",
            "Unavailable",
            "health-unhealthy"
        );
    }
}


document.addEventListener("DOMContentLoaded", checkHealth);
