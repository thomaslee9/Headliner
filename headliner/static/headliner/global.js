function getList() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return
        updatePage(xhr)
    }

    xhr.open("GET", "/headliner/get-global", true)
    xhr.send()
}

function updatePage(xhr) {
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText)
        updateList(response)
        return
    }

    if (xhr.status === 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('content-type') === 'application/json') {
        displayError(`Received status = ${xhr.status}`)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}
function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}
function updateList(items) {
    let list = document.getElementById("events-container")
    
    let existingEventIds = new Set();
    let existingEvents = document.querySelectorAll('.event-div');
    existingEvents.forEach(event => {
        let eventId = event.id.replace('id_event_div_', '');
        existingEventIds.add(parseInt(eventId));
    });
    console.log(items['events'])
    for(let event of items['events']) {
        if (!existingEventIds.has(event.id)){
            list.prepend(makeEventElement(event))
        }

    }
}
//makes the post element
function makeEventElement(item) {
    let element = document.createElement('div');
    element.className = 'event-div';
    element.id = 'id_event_div_' + item.id;
    let format = { hour: 'numeric', minute: 'numeric' };
    let date = new Date(item.creation_time);
    let localDateString = date.toLocaleDateString();
    let localTimeString = date.toLocaleTimeString('en-US', format);
    let pictureElement = '';
    if (item.picture) {
        pictureElement = `<img src="${item.picture}" alt="Event Picture" class="event-picture">`;
    }
    element.innerHTML = `
        <div class="image-container">
            ${pictureElement}
        </div>
        <div class="post-container">
            <a href="${`/other_profile/${item.username}/`}" class="event-name" id="id_event_profile_${item.id}">Event by ${item.first_name} ${item.last_name}</a>
            <span id="id_event_text_${ item.id }" class="event-text">${item.text}</span>
            <span id="id_event_date_time_${item.id}" class="event-date">${ localDateString } ${localTimeString}</span>
            <div id=comments-for-event-${ item.id }></div>
        </div>
    `;
    return element
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}