document.addEventListener("DOMContentLoaded", function() {
    document.querySelector('#edit-post').style.display = 'none';
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function formSubmit(event) {
    event.preventDefault()
    const myForm = event.target
    const myFormData = new FormData(myForm)

    const json = {
        "content": myFormData.get('content')
    }

    const url = myForm.getAttribute("action")
    const method = myForm.getAttribute("method")
    const xhr = new XMLHttpRequest()
    const csrftoken = getCookie('csrftoken');

    xhr.open(method, url)

    // xhr.setRequestHeader("Content-Type", "application/json")
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest")
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)

    xhr.onload = function() {
        myForm.reset()
        if (xhr.status === 201) {
            if (myForm.getAttribute("id") == "new-post-form") {
                const newPost = JSON.parse(xhr.response)
                allPosts = document.getElementById("all-posts")
                const postsContainer = document.getElementById("all-posts").innerHTML
                allPosts.innerHTML =  formatPost(newPost) + postsContainer
                getLikes(newPost.id)
            } 

        } else if (xhr.status === 400) {
            const errorJson = xhr.response
            console.log(errorJson)
        }
    }
    xhr.onerror = function() {
        alert("Error! Please try again :( ")
    }

    if (myForm.getAttribute("id") == "new-post-form") {
        xhr.send(myFormData)
    } else {
        xhr.send(JSON.stringify(json))
        
        document.querySelector('#main').style.display = 'block';
        document.querySelector('#pagination').style.display = 'block';
        document.querySelector('#edit-post').style.display = 'none';

        //Update post without reloading of the page
        postId = myForm.getAttribute("action").slice(-3)
        document.querySelector(`#content${postId}`).innerHTML = json.content;
        document.querySelector('#submitbtn').value = "Post"
        document.querySelector('#textarea').value = ""
    }
}

function editPost(post_id) {
    const post_content = document.getElementById(`content${post_id}`)
    const initial_content = post_content.innerText
    
    // Hide all, but the edit form
    document.querySelector('#main').style.display = 'none';
    document.querySelector('#pagination').style.display = 'none';
    document.querySelector('#edit-post').style.display = 'block';

    // Edit post form
    document.querySelector('#edit-post-form').setAttribute("action", `/post/${post_id}`)
    document.querySelector('#content-edit').innerText = `${initial_content}`    
    document.querySelector('#submitbtn').value = "Save"
    
    //Submit the form
    document.querySelector("#edit-post-form").addEventListener("submit", formSubmit)
}

function like(post_id){
    const current_user = document.getElementById("current_user").textContent
    const url = `/post-like/${post_id}`
    const method = "POST"
    const xhr = new XMLHttpRequest()
    const csrftoken = getCookie('csrftoken');
    xhr.open(method, url)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
    
    xhr.onload = function() {
        getLikes(post_id)
    }
    xhr.send()
}

function getLikes(post_id) {
    
    fetch(`/post/${post_id}`)
    .then(response => response.json())
    .then(post => {
        const likeIcon = document.getElementById(`likeIcon${post.id}`)
        const current_user = document.getElementById("current_user").textContent
        const likes = post.likes.length
        counter = document.getElementById(`counter${post.id}`)
        counter.innerHTML = likes
        // Update like icon
        likers = post.likes
        if (likers.includes(current_user)) {
            likeIcon.innerText = "favorite"
        } else {
            likeIcon.innerText = "favorite_border"
        }
        })
}

function follow(username){
    const current_user = document.getElementById("current_user").textContent
    const url = `/profile/${username}`
    const method = "POST"
    const xhr = new XMLHttpRequest()
    const csrftoken = getCookie('csrftoken');
    xhr.open(method, url)
    xhr.setRequestHeader("Content-Type", "application/json")
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
    
    xhr.onload = function() {
       const followers = document.getElementById("followers")
       const followbtn = document.getElementById("follow")
       counter = parseInt(followers.innerHTML)
       if (followbtn.value == 'Follow') {
           counter ++
           followers.innerHTML = counter
           followbtn.value = 'Unfollow'
       } else {
           counter --
           followers.innerHTML = counter
           followbtn.value = 'Follow'
       }
       
    }
    xhr.send()
}
