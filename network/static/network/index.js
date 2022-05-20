document.addEventListener('DOMContentLoaded', function() {
    // Load page 1 of All Posts by default
    var page_index = 1;
    loadPosts(page_index);

    // Create post when form is submitted
    document.querySelector('#new-post-form').addEventListener('submit', (event) => {
        event.preventDefault();
        savePost();
    });

    // Require posts when next/previous button is clicked
    document.querySelector('#previous').addEventListener('click', (event) => {
        event.preventDefault();
        page_index--;
        loadPosts(page_index);
    })

    document.querySelector('#next').addEventListener('click', (event) => {
        event.preventDefault();
        page_index++;
        loadPosts(page_index);
    })
});

function loadPosts(page) {
    // Clear out
    document.querySelector('#posts-list').innerHTML = '';
    
    fetch(`http://127.0.0.1:8000/posts/${page}`)
    .then(response => response.json())
    .then(data => {

        for (let i = 0; i < data.posts.length; i++) {
            const card = document.createElement('div');
            card.classList.add("card");

            const card_header = document.createElement('div');
            card_header.classList.add("card-header");

            const card_body = document.createElement('div');
            card_body.classList.add("card-body");

            const posts_list = document.querySelector('#posts-list');            

            card.append(card_header);
            card.append(card_body);
            posts_list.append(card);

            card_header.innerHTML = data.posts[i]['poster'];
            card_body.innerHTML = data.posts[i]['content'];  
        }
    });
}

function savePost() {
    const csrftoken = getCookie('csrftoken');
    
    const content = document.querySelector('#new-post-content').value;
    
    const json_body = {
        content: content
    }
    
    const requestOptions = {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json_body),
        mode: 'same-origin'
    }

    fetch('http://127.0.0.1:8000/new', requestOptions)
    .then(response => response.json())
    .then(data => {
        document.querySelector('#new-post-message').innerHTML = data['message'];
    })
    .catch(error => {
        console.log('Error:', error);
    });

    document.querySelector('#new-post-content').value = '';
}

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