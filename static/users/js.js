function updateValue() {
    const URL = "http://localhost:8000/api/combined-data/"
    fetch(URL)
        .then(response => {
            // Check if the response status is OK (status code 200-299)
            if (!response.ok) {
                throw new Error(`Network response was not ok (status ${response.status})`);
            }

            return response.json();
        })
        .then(data => {
            console.log(data)
            // Check if the expected data is received
            if (!data) {
                throw new Error('Invalid data received');
            }
            const rawDate = new Date(data.voltage.date);
            const formattedDate = rawDate.toLocaleString()

            // Update the value on the page
            document.getElementById('voltage').innerHTML = data.voltage.voltage;
            document.getElementById('voltage-date').innerHTML = `latest updated at: ${formattedDate}`;

        })
        .catch(error => {
            // Handle errors here
            console.error('Error:', error.message);
            // Optionally, display an error message on the page
            document.getElementById('voltage').innerHTML = 'Error fetching data';
        });
}

// Set interval to call the updateValue function every 5000 milliseconds (5 seconds)
setInterval(updateValue, 5000);


