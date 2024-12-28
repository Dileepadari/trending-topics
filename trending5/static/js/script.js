async function get_trending(param) {
    const loadingElem = document.getElementById('loading');
    const contentElem = document.getElementById('content');
    const buttons = document.querySelectorAll('button');

    // Show loading and disable buttons
    loadingElem.style.display = 'block';
    buttons.forEach(button => button.disabled = true);

    const contentBlock = document.createElement('div');
    contentBlock.classList.add('content-block');  // New block for each query result
    contentElem.appendChild(contentBlock);  // Append the new block to the content

    try {
        let response;

        if (param === 'scrape') {
            response = await fetch('/api/trending');
        } else {
            response = await fetch('/api/lasttrending');
        }
        const total_data = await response.json();

        if (!response.ok) {
            throw new Error(total_data.message || 'Failed to fetch data');
        }

        if (total_data.message !== "Scraping successful") {
            throw new Error(total_data.message || 'Scraping not complete');
        }

        const data = total_data.data;
        const ipAddress = JSON.parse(data.ip_address).origin;

        // Display timestamp
        const timestampElem = document.createElement('h2');
        timestampElem.innerHTML = `These are the most happening topics as on ${data.timestamp} IST`;
        contentBlock.appendChild(timestampElem);

        // Create a list of trends
        const list = document.createElement('ul');
        list.classList.add('trend-list');

        for (let i = 1; i <= 5; i++) {
            let trendName = data[`nameoftrend${i}`];

            if (trendName) {
                trendName = trendName.replace(/\n/g, '<br>').replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;');
                trendName = trendName.replace(/<br>/, ' ').replace(/<br>/, ' ');

                const li = document.createElement('li');
                li.innerHTML = trendName;
                list.appendChild(li);
            }
        }

        if (!list.hasChildNodes()) {
            const li = document.createElement('li');
            li.textContent = "No trends available.";
            list.appendChild(li);
        }

        contentBlock.appendChild(list);

        // Display IP address
        const ipElem = document.createElement('p');
        ipElem.innerHTML = `The IP address used for this query was: <strong>${ipAddress}</strong>`;
        contentBlock.appendChild(ipElem);

        // Display MongoDB ID
        const mongodbIdElem = document.createElement('p');
        mongodbIdElem.innerHTML = `MongoDB ID of the entry: <pre>${JSON.stringify(data._id, null, 4)}</pre>`;
        contentBlock.appendChild(mongodbIdElem);

        const jsonElem = document.createElement('div');

        // Parse and clean the JSON data
        const cleanData = {
            ...data,
            ip_address: JSON.parse(data.ip_address), // Parse `ip_address` to a proper JSON object
            nameoftrend1: data.nameoftrend1
                .replace(/\n·\n/g, " · ")
                .replace(/\n/g, "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"), // Increased spaces
            nameoftrend2: data.nameoftrend2
                .replace(/\n·\n/g, " · ")
                .replace(/\n/g, "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"), // Increased spaces
            nameoftrend3: data.nameoftrend3
                .replace(/\n·\n/g, " · ")
                .replace(/\n/g, "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"), // Increased spaces
            nameoftrend4: data.nameoftrend4
                .replace(/\n·\n/g, " · ")
                .replace(/\n/g, "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"), // Increased spaces
            nameoftrend5: data.nameoftrend5
                .replace(/\n·\n/g, " · ")
                .replace(/\n/g, "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"), // Increased spaces
        };


        // Ensure proper newline preservation for nameoftrend fields
        // Display the cleaned and formatted JSON
        jsonElem.innerHTML = `<pre>Here’s a JSON extract of this record from the MongoDB:<br>[<br>  ${JSON.stringify(cleanData, null, 4).replace(/}/g, '  }')}<br>]</pre>`;

        contentBlock.appendChild(jsonElem);

        // Add the "run the script again" button
        const button = document.createElement('button');
        button.textContent = 'Click here to run the query again';
        button.onclick = () => get_trending('again');
        contentBlock.appendChild(button);

        // Scroll to the bottom
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });

    } catch (error) {
        console.error("Error fetching trending topics:", error);
        loadingElem.textContent = "Failed to load data. Please try again later.";
    } finally {
        // Hide loading and enable buttons
        loadingElem.style.display = 'none';
        buttons.forEach(button => button.disabled = false);
    }
}
