document.addEventListener('DOMContentLoaded', function() {
    // Set page index
    var page_index = 1;
    
    // Set page title
    var title = document.title;
    
    // Load page 1 of All Posts by default and only once
    var loadIndexOnce = (function() {
        var executed = false;
        return function() {
            if (!executed) {
                executed = true;
                loadPosts('all', page_index, '');
            }
        };
    })();
    
    if (title == 'Index') {
        loadIndexOnce();
    }

    // Load page 1 of Profile Posts when a profile is clicked on
    // let user = document.querySelector('#user');
    // let username = user.innerHTML;
    // user.addEventListener('click', loadPosts('profile', page_index, username), false);

    document.querySelector('#user').addEventListener('click', (event) => {
        username = event.target.innerHTML;
        loadPosts('profile', page_index, username);
    })

    // Create post when form is submitted
    if (document.title === 'Index') {
        document.querySelector('#new-post-form').addEventListener('submit', (event) => {
            event.preventDefault();
            savePost();
        });
    }

    // Request posts when next/previous button is clicked
    document.querySelector('#previous').addEventListener('click', (event) => {
        event.preventDefault();
        page_index--;
        if (document.title === 'Index') {
            loadPosts('all', page_index, '');
        }
        if (document.title === 'Profile') {
            loadPosts('profile', page_index, username);
        }
    })

    document.querySelector('#next').addEventListener('click', (event) => {
        event.preventDefault();
        page_index++;
        if (document.title === 'Index') {
            loadPosts('all', page_index, '');
        }
        if (document.title === 'Profile') {
            loadPosts('profile', page_index, username);
        }
    })
});


// function loadPosts(page) {
//     // Clear out
//     document.querySelector('#posts-list').innerHTML = '';
    
//     fetch(`http://127.0.0.1:8000/posts/${page}`)
//     .then(response => response.json())
//     .then(data => {

//         for (let i = 0; i < data.posts.length; i++) {
//             const card = document.createElement('div');
//             card.classList.add("card");

//             const card_header = document.createElement('div');
//             card_header.classList.add("card-header");

//             const card_body = document.createElement('div');
//             card_body.classList.add("card-body");

//             const posts_list = document.querySelector('#posts-list');            

//             card.append(card_header);
//             card.append(card_body);
//             posts_list.append(card);

//             card_header.innerHTML = data.posts[i]['poster'];
//             card_body.innerHTML = data.posts[i]['content'];
//         }

//         if (data.page.has_previous === false) {
//             document.querySelector('#previous').setAttribute('disabled', 'true');
//         } else {
//             document.querySelector('#previous').removeAttribute('disabled');
//         }

//         if (data.page.has_next === false) {
//             document.querySelector('#next').setAttribute('disabled', 'true');
//         } else {
//             document.querySelector('#next').removeAttribute('disabled');
//         }
//     });
// }

function loadPosts(view, page, username) {    
    // Clear out
    document.querySelector('.posts-list').innerHTML = '';

    fetch(`http://127.0.0.1:8000/posts/?view=${view}&page=${page}&username=${username}`)
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
            console.log(data.posts[i]);
        }
        
        if (data.page.has_previous === false) {
            document.querySelector('#previous').setAttribute('disabled', 'true');
        } else {
            document.querySelector('#previous').removeAttribute('disabled');
        }

        if (data.page.has_next === false) {
            document.querySelector('#next').setAttribute('disabled', 'true');
        } else {
            document.querySelector('#next').removeAttribute('disabled');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function loadPosts(view, page, username) {    
    // Clear out
    document.querySelector('.posts-list').innerHTML = '';

    fetch(`http://127.0.0.1:8000/posts/?view=${view}&page=${page}&username=${username}`)
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
            console.log(data.posts[i]);
        }
        
        if (data.page.has_previous === false) {
            document.querySelector('#previous').setAttribute('disabled', 'true');
        } else {
            document.querySelector('#previous').removeAttribute('disabled');
        }

        if (data.page.has_next === false) {
            document.querySelector('#next').setAttribute('disabled', 'true');
        } else {
            document.querySelector('#next').removeAttribute('disabled');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
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