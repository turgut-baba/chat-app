document.getElementById('socket').addEventListener('click', async () => {
    const resultElement = document.getElementById('result');
    const url = "http://localhost:8000/interviewmq/publish/"; // Replace with your server URL

    try {
        const response = await fetch(url, {
            method: 'POST', // Change to the appropriate method
            headers: {
                'Content-Type': 'application/json', // Adjust as required
            },
            body: JSON.stringify({ 
                topic: 'foo',
                msg: 'Hello Stryker!'
             }), // Include the payload if needed
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        resultElement.textContent = `Message: ${data.status}`;
    } catch (error) {
        resultElement.textContent = `Error: ${error.message}`;
    }
});

document.getElementById('backend').addEventListener('click', async () => {
    fetch('/send_backend')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse JSON from the response
    })
    .then(data => {
        // Display the JSON response message in the resultElement
        const resultElement = document.getElementById('result'); // Ensure this element exists in your HTML
        resultElement.textContent = `Message: ${data.message}`;
    })
    .catch(err => console.error('Error:', err))
});