// 17-437 Team30
// Headliner App
// global.js

"use strict";

const CONFIGURATION = {
    "ctaTitle": "Checkout",
    "mapOptions": {"center":{"lat":37.4221,"lng":-122.0841},"fullscreenControl":true,"mapTypeControl":false,"streetViewControl":true,"zoom":11,"zoomControl":true,"maxZoom":22,"mapId":""},
    "mapsApiKey": "AIzaSyCuDct23hJWRLXJsCyc-W6szXDj3swI8Kc",
    "capabilities": {"addressAutocompleteControl":true,"mapDisplayControl":true,"ctaControl":true}
  };

function getList(searchTerm, byLocation) {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return
        updatePage(xhr, searchTerm, byLocation)
    }

    xhr.open("GET", "/headliner/get-global", true)
    xhr.send()
}

function updatePage(xhr, searchTerm, byLocation) {
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText)
        updateList(response, searchTerm, byLocation)
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

function updateList(items, searchTerm, byLocation) {
    let list = document.getElementById("events-container");
    list.innerHTML = ''; // Clear previous events
    // items.u
    let filteredEvents = items.events.filter(event => {
        if (byLocation) {
            return event.location.toLowerCase().includes(searchTerm);
        } else {
            return event.title.toLowerCase().includes(searchTerm);
        }
    });

    for (let event of filteredEvents) {
        list.prepend(makeEventElement(event, items.user_id));
    }
}

//makes the post element
function makeEventElement(item, userID) {
    // Build Event element
    let element = document.createElement('div');
    element.className = 'event-div rounded-4';
    element.id = 'id_event_div_' + item.id;
    let format = { hour: 'numeric', minute: 'numeric' };
    let date = new Date(item.creation_time);
    let localDateString = date.toLocaleDateString();
    //  let localTimeString = date.toLocaleTimeString('en-US', format);
    let pictureElement = '';
    let profileElement = '';
    if (item.picture) {
        pictureElement = `<img src="${item.picture}" alt="Event Picture" class="card-img-top event-picture rounded-5 p-2">`;
    }
    console.log(item.userID, userID)
    if (item.userID == userID) {

        profileElement = `<a href="/editevent/${item.id}" class="btn btn-danger text-white fw-bold link-underline link-underline-opacity-0">Edit Event</a>`;
    } else {
        profileElement = `<a href="/otherprofile/${item.userID}" class="btn btn-dark text-white fw-bold link-underline link-underline-opacity-0">Event by ${item.first_name} ${item.last_name}</a>`;
    }
    element.innerHTML = `
         <div class="post-container text-white">
            <div class="title row">
                <a href="/event/${item.id}" class="h2 fw-bold text-white link-underline link-underline-opacity-0" id="id_event_link_${item.id}">${item.title}</a>
            </div>
            <div class="image-container">
                ${pictureElement}
            </div>
            <div class="title m-3">
                ${profileElement}
            </div>
            <div class="title">
                <span id="id_event_date_time_${item.id}" class="event-date">Posted on: ${localDateString } </span>
            </div>
        </div>
    `;

    return element
}

function fillInAddress(place) {
    const addressComponents = place.address_components || [];
    let formattedAddress = '';

    // Concatenate all address components into a single string
    for (const component of addressComponents) {
      formattedAddress += component.long_name + ', ';
    }

    // Remove trailing comma and space
    formattedAddress = formattedAddress.replace(/,\s*$/, '');

    // Set the value of the input field to the formatted address
    document.getElementById('id_location').value = formattedAddress;
  }

function renderAddress(place, map, marker) {
    if (place.geometry && place.geometry.location) {
      map.setCenter(place.geometry.location);
      marker.position = place.geometry.location;
    } else {
      marker.position = null;
    }
  }

async function initMap() {
  const {Map} = google.maps;
  const {AdvancedMarkerElement} = google.maps.marker;
  const {Autocomplete} = google.maps.places;

  const mapOptions = CONFIGURATION.mapOptions;
  mapOptions.mapId = mapOptions.mapId || 'DEMO_MAP_ID';
  mapOptions.center = mapOptions.center || {lat: 37.4221, lng: -122.0841};

  const map = new Map(document.getElementById('gmp-map'), mapOptions);
  const marker = new AdvancedMarkerElement({map});
  const autocomplete = new Autocomplete(document.getElementById('id_location'), {
    fields: ['address_components', 'geometry', 'name'],
    types: ['address'],
  });

  autocomplete.addListener('place_changed', () => {
    const place = autocomplete.getPlace();
    if (!place.geometry) {
      // User entered the name of a Place that was not suggested and
      // pressed the Enter key, or the Place Details request failed.
      window.alert(`No details available for input: '${place.name}'`);
      return;
    }
    renderAddress(place, map, marker);
    fillInAddress(place);
  });
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


function loadMessages() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return
        updateEventPage(xhr)
    }

    xhr.open("GET", "/headliner/get-event", true)
    xhr.send()
}


function updateEventPage(xhr) {
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText)
        updateMessages(response)
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


function updateMessages(data) {
    let msgList = document.getElementById("message-list")
    let msgIdBase = "id_message_div_"

    if (!data.hasOwnProperty('allMessages')) return

    data['allMessages'].forEach((currMsg) => {
        if (!document.getElementById(msgIdBase + currMsg.id)) {
            let msgBlock = document.createElement("div")
            msgBlock.append(makeMessageHTML(currMsg))
            msgList.append(msgBlock)
        }
    })
}


function addMessage(eventID) {
    let newMessageElement = document.getElementById("id_message_input_text")
    let newMessageText = newMessageElement.value

    newMessageElement.value = ''
    displayError('')

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState !== 4) return
        updateMessages(xhr)
    }

    xhr.open("POST", addChatURL, true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhr.send(`message_text=${newMessageText}&csrfmiddlewaretoken=${getCSRFToken()}&event_id=${eventID}`)
}


function makeMessageHTML(msg) {
    let newMsg = document.createElement("div")
    newMsg.id = "id_message_div_" + msg.id
    newMsg.className = "message"

    newMsg.innerHTML = `
        <a href="/otherprofile/${msg.created_by}" id="id_msg_profile_${msg.id}"> Sent by ${msg.username}:</a>
        <p id="id_msg_text_${msg.id}" class="message"> ${sanitize(msg.text)} </p>
        <p id="id_msg_date_time_${msg.id}"> ${msg.creation_time} </p>
        <br>
    `

    return newMsg
}


function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}