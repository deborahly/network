document.addEventListener('DOMContentLoaded', function() {
    // Set page index
    var page_index = 1;
    
    // Set page title
    var title = document.title;
    
    // Load Index's page 1 by default and only once
    var loadIndexOnce = (function() {
        var executed = false;
        return function() {
            if (!executed) {
                executed = true;
                loadPosts('all', 1, '');
            }
        };
    })();
    
    if (title == 'Index') {
        loadIndexOnce();
    }

    // When Index page is loaded 
    if (title === 'Index') {
        // Create post when form is submitted
        document.querySelector('#new-post-form').addEventListener('submit', (event) => {
            event.preventDefault();
            savePost();
        });
    }

    // When Following page is loaded
    if (title === 'Following') {
        loadPosts('following', page_index, ''); 
    }

    // When Profile page is loaded   
    if (title == 'Profile') { 
        username = document.querySelector('#profile-username').innerHTML;
        loadPosts('profile', page_index, username); 
        
        // Follow/unfollow when requested
        document.querySelector('#follow-btn').addEventListener('click', (event) => {
            active = event.target.dataset.active;
            follow(username, active);
        });
    }

    // Request posts when previous button is clicked
    document.querySelector('#previous').addEventListener('click', (event) => {
        event.preventDefault();
        page_index--;
        if (title === 'Index') {
            loadPosts('all', page_index, '');
        }
        if (title === 'Following') {
            loadPosts('following', page_index, '');
        }
        if (title === 'Profile') {
            loadPosts('profile', page_index, username);
        }
    })

    // Request posts when next button is clicked
    document.querySelector('#next').addEventListener('click', (event) => {
        event.preventDefault();
        page_index++;
        if (title === 'Index') {
            loadPosts('all', page_index, '');
        }
        if (title === 'Following') {
            loadPosts('following', page_index, '');
        }
        if (title === 'Profile') {
            loadPosts('profile', page_index, username);
        }
    })

    // When like/unlike link is clicked, request server a response
    const links = document.querySelectorAll('.like-link');

    links.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            console.log('ok');
            like(post_id);
        })
    })
});

function loadPosts(view, page, username) {    
    // Clear out
    document.querySelector('.posts-list').innerHTML = '';

    fetch(`http://127.0.0.1:8000/posts/?view=${view}&page=${page}&username=${username}`)
    .then(response => response.json()) 
    .then(data => {
        for (let i = 0; i < data.posts.length; i++) {
            // Create elements
            const card = document.createElement('div');
            card.classList.add("card");
            
            const card_body = document.createElement('div');
            card_body.classList.add('card-body');
            
            const card_title = document.createElement('h5');
            card_title.classList.add('card-title');
            
            const profile_link = document.createElement('a');
            profile_link.setAttribute('href', `/profile/${data.posts[i]['poster']}`);
            profile_link.innerHTML = data.posts[i]['poster'];
            
            const card_subtitle = document.createElement('h7');
            card_subtitle.classList.add('card-subtitle', 'mb-2', 'text-muted');
            card_subtitle.innerHTML = `at ${data.posts[i]['created_on']}`;
            
            const card_text = document.createElement('p');
            card_text.classList.add('card-text');
            card_text.innerHTML = data.posts[i]['content'];
            
            const like_link = document.createElement('a');
            like_link.classList.add('card-link', 'like-link');
            like_link.setAttribute('href', '#');
            like_link.dataset.id = data.posts[i]['id'];

            // Adjust like links
            if (data.posts[i]['user_is_author'] === true) {
                like_link.style.display = 'none';
            } else {
                if (data.posts[i]['liked_by_user'] === true) {
                    like_link.innerHTML = 'Unlike';
                } else {
                    like_link.innerHTML = 'Like';
                }
            }

            // Append everything under posts list
            const posts_list = document.querySelector('#posts-list'); 
            posts_list.append(card);           
            card.append(card_body);
            card_body.append(card_title);
            card_body.append(card_subtitle);
            card_body.append(card_text);
            card_body.append(like_link);
            card_title.append(profile_link);

            // Add event listener
            like_link.addEventListener('click', (event) => {
                event.preventDefault();
                like(data.posts[i]['id']);
            })
        }
        
        // Display previous/next buttons, when applicable
        if (data.page.has_previous === false && data.page.has_next === false) {
            document.querySelector('.pagination').innerHTML = '';
        }
        
        if (data.page.has_previous === false && data.page.has_next === true) {
            document.querySelector('#previous').setAttribute('disabled', 'true');
        } else {
            document.querySelector('#previous').removeAttribute('disabled');
        }

        if (data.page.has_previous === true && data.page.has_next === false) {
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

    loadPosts('all', 1, '');
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

function follow(username, active) {
    const csrftoken = getCookie('csrftoken');
    
    const json_body = {
        active: active
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

    fetch(`http://127.0.0.1:8000/profile/${username}`, requestOptions)
    .then(response => response.json()) 
    .then(data => {
        console.log(data['message']);
        if (data['active'] == 'True') {
            const follow_btn = document.querySelector('#follow-btn');
            follow_btn.innerHTML = 'Unfollow';
            follow_btn.dataset.active = 'True';
            let followers_count = parseInt(document.querySelector('#followers-count').innerHTML);
            followers_count += 1;
            document.querySelector('#followers-count').innerHTML = followers_count;
        }

        if (data['active'] == 'False') {
            const follow_btn = document.querySelector('#follow-btn');
            follow_btn.innerHTML = 'Follow';
            follow_btn.dataset.active = 'False';
            let followers_count = parseInt(document.querySelector('#followers-count').innerHTML);
            followers_count -= 1;
            document.querySelector('#followers-count').innerHTML = followers_count;
        }
    })
    .catch(error => {
        console.log('Error:', error);
    });
}

function like(post_id) {
    const csrftoken = getCookie('csrftoken');
    
    const json_body = {
        post_id: post_id
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

    fetch('http://127.0.0.1:8000/like', requestOptions)
    .then(response => response.json()) 
    .then(_ => {
        like_link = document.querySelector(`[data-id="${post_id}"]`);

        if (like_link.innerHTML === 'Like') {
            like_link.innerHTML = 'Unlike';
        } else {
            like_link.innerHTML = 'Like';
        }
    })
    .catch(error => {
        console.log('Error:', error);
    });
}