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
    let list = document.getElementById("posts-container")
    
    let existingPostIds = new Set();
    let existingPosts = document.querySelectorAll('.post-div');
    existingPosts.forEach(post => {
        let postId = post.id.replace('id_post_div_', '');
        existingPostIds.add(parseInt(postId));
    });

    let existingCommentIds = new Set();
    let existingComments = document.querySelectorAll('.comment-div');
    existingComments.forEach(comment => {
        let commentId = comment.id.replace('id_comment_div_', '');
        existingCommentIds.add(parseInt(commentId));
    });

    for(let post of items['posts']) {
        if (!existingPostIds.has(post.id)){
            let element = document.createElement('div');
            element.className = 'comment-form-div';
    
            element.innerHTML = `
                <label>Comment:</label>
                <input type="text" id="id_comment_input_text_${post.id}">
                <button id="id_comment_button_${post.id}" onclick="addComment(${post.id})">Submit</button>
            `;
            list.prepend(element)
        }
        if (!existingPostIds.has(post.id)){
            list.prepend(makePostElement(post))
        }
        let comment_id = "comments-for-post-" + post.id
        let comment_list = document.getElementById(comment_id)
        for(let comment of items['comments']){
            if(comment.post_id == post.id && !existingCommentIds.has(comment.id)){
                comment_list.append(makeCommentElement(comment))
            }
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
function makeCommentElement(item) {
    let element = document.createElement('div');
    element.className = 'comment-div';
    element.id = 'id_comment_div_' + item.id;
    let format = { hour: 'numeric', minute: 'numeric' };
    let date = new Date(item.creation_time);
    let localDateString = date.toLocaleDateString();
    let localTimeString = date.toLocaleTimeString('en-US', format);
    element.innerHTML = `
        <a href="${`/other_profile/${item.username}/`}" class="comment-name" id="id_comment_profile_${ item.id }">Comment by ${item.first_name} ${item.last_name}</a>
        <span id="id_comment_text_${ item.id }" class="comment-text">${item.text}</span>
        <span id="id_comment_date_time_${item.id}" class="comment-date">${ localDateString } ${localTimeString}</span>
    `;
    return element
}

function addComment(id) {
    id_full = "id_comment_input_text_" + id
    let itemTextElement = document.getElementById(id_full)
    let itemTextValue   = itemTextElement.value

    itemTextElement.value = ''
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState !== 4) return
        updatePage(xhr)
    }
    xhr.open("POST", "/socialnetwork/add-comment", true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhr.send(`comment_text=${itemTextValue}&csrfmiddlewaretoken=${getCSRFToken()}&post_id=${id}&comment-type=global`)
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