async function fetchData() {
    const url = 'https://instagram-scraper-api2.p.rapidapi.com/v1/followers?username_or_id_or_url=mrbeast';
    const options = {
        method: 'GET',
        headers: {
            'x-rapidapi-key': '6164c8f5admshe4f1e3b5e0375d8p1828c8jsn0afb6d1540d8',
            'x-rapidapi-host': 'instagram-scraper-api2.p.rapidapi.com'
        }
    };

    try {
        const response = await fetch(url, options);
        const result = await response.json();
        console.log(result);
        document.getElementById("concerts").innerHTML = result.data.items.map(item => '<li>' + item.full_name + '</li>').join('');
    } catch (error) {
        console.error(error);
    }
}

fetchData();