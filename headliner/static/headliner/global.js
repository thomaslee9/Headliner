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

var prevChatId = -1;
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

async function updateList(items, searchTerm, byLocation) {
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

    if (byLocation){
        list.innerHTML = '';
        initGlobalMap(searchTerm, filteredEvents, items.user_id)
    } else {
        let map = document.getElementById("map")
        let map_event = document.getElementById("map-event")
        map.innerHTML = ''
        map_event.innerHTML = ''
        const searchBox = document.getElementById("search-input");
        const newSearchBox = searchBox.cloneNode(true);
        searchBox.parentNode.replaceChild(newSearchBox, searchBox);
        for (let event of filteredEvents) {
            list.prepend(makeEventElement(event, items.user_id));
        }
    }
}

async function initGlobalMap(searchTerm, events, userID) {
  const { Map } = await google.maps.importLibrary("maps");
  const { InfoWindow } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
  const { PinElement } = await google.maps.importLibrary("marker");

  const firstEventCoordinates = await getLocationCoordinates(events[0].location);

  const map = new Map(document.getElementById("map"), {
    zoom: 12,
    center: firstEventCoordinates,
    mapId: "185b2b60fd97243d",
  });

  const input = document.getElementById("search-input");
  const searchBox = new google.maps.places.SearchBox(input);

  searchBox.addListener("places_changed", () => {
    const places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

    // For each place, get the icon, name and location.
    const bounds = new google.maps.LatLngBounds();

    places.forEach((place) => {
      if (!place.geometry || !place.geometry.location) {
        console.log("Returned place contains no geometry");
        return;
      }

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });

  // Create an info window to share between markers.
  const infoWindow = new InfoWindow();

  // Iterate over each event and create a marker for it.
  events.forEach(async (event, i) => {
    // Convert event location to coordinates (you need to implement this)
    const coordinates = await getLocationCoordinates(event.location);
    // Create a pin element for the marker.
    const pin = new PinElement({
      glyph: `${i + 1}`,
    });

    // Create the marker.
    const marker = new AdvancedMarkerElement({
      position: coordinates,
      map,
      title: `${i + 1}. ${event.location}`,
      content: pin.element,
    });

    // Add a click listener for each marker, and set up the info window.
    marker.addListener("click", ({ domEvent, latLng }) => {
      const { target } = domEvent;

      infoWindow.close();
      infoWindow.setContent(event.title);
      infoWindow.open(marker.map, marker);
      let map_event = document.getElementById("map-event")
      map_event.innerHTML = ""
      map_event.prepend(makeEventElement(event, userID))
    });
  });
}

function createMarker(place) {
  if (!place.geometry || !place.geometry.location) return;

  const marker = new google.maps.Marker({
    map,
    position: place.geometry.location,
  });
}

// Function to convert location string to coordinates (geocoding).
async function getLocationCoordinates(location) {
  // You need to implement this function using a geocoding service.
  // This could involve making a request to a geocoding API.
  // For example, using Google Maps Geocoding API:

  const response = await fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(location)}&key=AIzaSyCuDct23hJWRLXJsCyc-W6szXDj3swI8Kc`);
  const data = await response.json();
  console.log(data.results[0].geometry.location)
  return data.results[0].geometry.location;
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


function loadMessages(event_id, chat_id) {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return
        updateEventPage(xhr, chat_id)
    }

    xhr.open("GET", "/headliner/get-event/" + event_id + "/", true);
    xhr.send()
}


function updateEventPage(xhr, chat_id) {
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText)
        updateMessages(response, chat_id)
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


function updateMessages(data, chat_id) {
    let msgList = document.getElementById("message-list")
    let msgIdBase = "id_message_div_"
    if (chat_id !== prevChatId){
        prevChatId = chat_id
        msgList.innerHTML = ''
    }

    if (Object.keys(data).length === 0) return

    data[chat_id].forEach((currMsg) => {
        if (!document.getElementById(msgIdBase + currMsg.id)) {
            let msgBlock = document.createElement("div")
            msgBlock.append(makeMessageHTML(currMsg))
            msgList.append(msgBlock)
        }
    })
}


function addMessage(eventID, chatID) {
    let newMessageElement = document.getElementById("id_message_input_text")
    let newMessageText = newMessageElement.value

    newMessageElement.value = ''
    displayError('')

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState !== 4) return
        updateMessages(xhr, chatID)
    }
    xhr.open("POST", addChatURL, true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhr.send(`message_text=${newMessageText}&csrfmiddlewaretoken=${getCSRFToken()}&event_id=${eventID}&chat_id=${chatID}`)
}


function makeMessageHTML(msg) {
    let newMsg = document.createElement("div")
    newMsg.id = "id_message_div_" + msg.id
    newMsg.className = "message"

    let pictureElement = '';
    if (msg.picture) {
      pictureElement = `<img src="${msg.picture}" alt="Prof Picture" class="img-fluid rounded-5">`;
    }

    newMsg.innerHTML = `
      <div class="row text-white msg-div bg-opacity-50">
        <div class="col-md-4">
          <a href="/otherprofile/${msg.created_by}" class="fw-bold text-white link-underline link-underline-opacity-0" id="id_msg_profile_${msg.id}">${msg.username}:</a>
          <div class="prof-picture m-2">
            ${pictureElement}
          </div>
          <p id="id_msg_date_time_${msg.id}" class="text-white timestamp"> ${msg.creation_time} </p>
        </div>
        <div class="text-white col-md-8 p-3">
          <p id="id_msg_text_${msg.id}" class="text-white msg-text fw-bold text-white"> ${sanitize(msg.text)} </p>
        </div>
      </div>
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