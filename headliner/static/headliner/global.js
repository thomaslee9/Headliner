"use strict";

const CONFIGURATION = {
    "ctaTitle": "Checkout",
    "mapOptions": {"center":{"lat":37.4221,"lng":-122.0841},"fullscreenControl":true,"mapTypeControl":false,"streetViewControl":true,"zoom":11,"zoomControl":true,"maxZoom":22,"mapId":""},
    "mapsApiKey": "AIzaSyCuDct23hJWRLXJsCyc-W6szXDj3swI8Kc",
    "capabilities": {"addressAutocompleteControl":true,"mapDisplayControl":true,"ctaControl":true}
  };

function getList(searchTerm) {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return
        updatePage(xhr, searchTerm)
    }

    xhr.open("GET", "/headliner/get-global", true)
    xhr.send()
}

function updatePage(xhr, searchTerm) {
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText)
        updateList(response, searchTerm)
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
function updateList(items, searchTerm) {
    let list = document.getElementById("events-container");
    list.innerHTML = ''; // Clear previous events
    
    let filteredEvents = items.events.filter(event => {
        return event.title.toLowerCase().includes(searchTerm.toLowerCase());
    });
    
    for (let event of filteredEvents) {
        list.prepend(makeEventElement(event));
    }
}

//makes the post element
function makeEventElement(item) {
    // Build Event element
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
            <a href="/event/${item.id}" class="event-text" id="id_event_link_${item.id}">${item.title}</a>
            <br>
            <a href="${`/other_profile/${item.username}/`}" class="event-name" id="id_event_profile_${item.id}">Event by ${item.first_name} ${item.last_name}</a>
            <br>
            <span id="id_event_text_${ item.id }" class="event-text">${item.text}</span>
            <br>
            <span id="id_event_date_time_${item.id}" class="event-date">Posted on: ${ localDateString } </span>
            <div id=comments-for-event-${ item.id }></div>
        </div>
    `;

    // Build Tag Element for this Event post
    let tagDiv = document.createElement('div');
    tagDiv.className = 'tag-div';
    tagDiv.id = 'id_tag_div_' + item.id;
    tagDiv.innerHTML = `
        <div> 🔥TRENDING🔥 </div>
    `;
    element.appendChild(tagDiv)

    // Build Upvote / Downvote Element for this Event post
    let voteDiv = document.createElement('div');
    voteDiv.className = 'vote-div';
    voteDiv.id = 'id_vote_div_' + item.id;
    voteDiv.innerHTML = `
        <div> Like: 👍  Dislike: 👎 </div>
    `;
    element.appendChild(voteDiv)

    // Build Comment Element for this Event post
    let commentDiv = document.createElement('div');
    commentDiv.className = 'comment-div';
    commentDiv.id = 'id_comment_div_' + item.id;
    commentDiv.innerHTML = `
        <div id="comments-for-event-${ item.id }"></div>
        <div id="comment-div">Comments go here...</div>
    `;
    element.appendChild(commentDiv)

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