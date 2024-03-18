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
    
    let existingPostIds = new Set();
    let existingPosts = document.querySelectorAll('.event-div');
    existingPosts.forEach(post => {
        let postId = post.id.replace('id_event_div_', '');
        existingPostIds.add(parseInt(postId));
    });

    for(let event of items['events']) {
        if (!existingPostIds.has(event.id)){
            list.prepend(makePostElement(event))
        }

    }
}
//makes the post element
function makePostElement(item) {
    let element = document.createElement('div');
    element.className = 'post-div';
    element.id = 'id_post_div_' + item.id;
    let format = { hour: 'numeric', minute: 'numeric' };
    let date = new Date(item.creation_time);
    let localDateString = date.toLocaleDateString();
    let localTimeString = date.toLocaleTimeString('en-US', format);
    element.innerHTML = `
        <a href="${`/other_profile/${item.username}/`}" class="post-name" id="id_post_profile_${item.id}">Post by ${item.first_name} ${item.last_name}</a>
        <span id="id_post_text_${ item.id }" class="post-text">${item.text}</span>
        <span id="id_post_date_time_${item.id}" class="post-date">${ localDateString } ${localTimeString}</span>
        <div id=comments-for-post-${ item.id }></div>
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