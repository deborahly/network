document.addEventListener('DOMContentLoaded', function() {
    // Set page index
    var page_index = 1;
    
    // Set page title
    const title = document.title;
    
    // When Index page is loaded 
    if (title === 'Index') {
        loadPosts('all', page_index, '');
        // Create post when form is submitted
        if (document.querySelector('#new-post-form')) {
            document.querySelector('#new-post-form').addEventListener('submit', (event) => {
                event.preventDefault();
                const content = document.querySelector('#new-post-content').value;
                savePost(content, ''); 
                document.querySelector('#new-post-content').value = '';
            });
        }
    }

    // When Following page is loaded
    if (title === 'Following') {
        // loadPosts('following', page_index, ''); 
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
});

function loadPosts(view, page, username) {    
    // Clear out
    document.querySelector('.posts-list').innerHTML = '';

    fetch(`http://127.0.0.1:8000/posts/?view=${view}&page=${page}&username=${username}`)
    .then(response => response.json()) 
    .then(data => {
        for (let i = 0; i < data.posts.length; i++) {
            // Update page index
            const page_index = document.querySelector('#page-index');
            page_index.dataset.page = data.page['current'];
            
            // Create card elements
            const card = document.createElement('div');
            card.classList.add("card", "my-card");
            
            const card_body = document.createElement('div');
            card_body.classList.add('card-body');
            card_body.dataset.id = `body-${data.posts[i]['id']}`;
            
            const card_title = document.createElement('h5');
            card_title.classList.add('card-title', 'my-card-title');
            
            const profile_link = document.createElement('a');
            profile_link.setAttribute('href', `/profile/${data.posts[i]['poster']}`);
            profile_link.innerHTML = data.posts[i]['poster'];
            
            const date = document.createElement('span');
            date.classList.add('date');
            date.innerHTML = ` at ${data.posts[i]['created_on']}`;
            
            const card_text = document.createElement('p');
            card_text.classList.add('card-text', 'my-card-text');
            card_text.dataset.id = `text-${data.posts[i]['id']}`;
            card_text.innerHTML = data.posts[i]['content'];

            const posts_list = document.querySelector('#posts-list'); 
            posts_list.append(card);           
            card.append(card_body);
            card_title.append(profile_link);
            card_body.append(card_title);
            card_body.append(date);
            card_body.append(card_text);

            // Display number of likes
            const likes_indication = document.createElement('span');
            likes_indication.innerHTML = 'Likes '
            const likes = document.createElement('span');
            likes.innerHTML = `${data.posts[i]['likes']}`;
            likes.dataset.id = `likes-${data.posts[i]['id']}`;
            card_body.append(likes_indication);
            likes_indication.append(likes);

            // If user is logged in and is not the post's author, add like link
            if (data.posts[i]['user_is_author'] != null) {
                const like_link = document.createElement('a');
                like_link.classList.add('like-link');
                like_link.setAttribute('href', '#');
                like_link.dataset.id = `like-${data.posts[i]['id']}`;
                
                // Update like/unlike link
                if (data.posts[i]['user_is_author'] === true) {
                    like_link.style.display = 'none';
                } else {
                    if (data.posts[i]['liked_by_user'] === true) {
                        like_link.innerHTML = ' Unlike';
                    } else {
                        like_link.innerHTML = ' Like';
                    }
                }

                // Append link
                card_body.append(like_link);
        
                // Add event listener for like link
                like_link.addEventListener('click', (event) => {
                    event.preventDefault();
                    like(data.posts[i]['id']);
                })
            }

            // Display edit and delete link
            if (data.posts[i]['user_is_author'] === true) {
                const edit_link = document.createElement('a');
                edit_link.classList.add('edit-link');
                edit_link.setAttribute('href', '#');
                edit_link.dataset.id = `edit-${data.posts[i]['id']}`;
                edit_link.innerHTML = ' Edit ';
                card_body.append(edit_link);

                const delete_link = document.createElement('a');
                delete_link.classList.add('delete-link');
                delete_link.setAttribute('href', '#');
                delete_link.dataset.id = `delete-${data.posts[i]['id']}`;
                delete_link.innerHTML = ' Delete';
                card_body.append(delete_link);

                // Add event listener for both links
                edit_link.addEventListener('click', (event) => {
                    event.preventDefault();
                    editPost(data.posts[i]['id']);
                })

                delete_link.addEventListener('click', (event) => {
                    event.preventDefault();
                    deletePost(data.posts[i]['id']);
                })
            }
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

function savePost(content, post_id) {
    const csrftoken = getCookie('csrftoken');
    
    const json_body = {
        content: content,
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

    fetch('http://127.0.0.1:8000/save', requestOptions)
    .then(response => response.json())
    .then(data => {
        if (data.edited === true) {
            const page_index = document.querySelector('#page-index').dataset.page;
            if (document.title == 'Index') {
                loadPosts('all', page_index, '');
            } else {
                const username = document.querySelector('#profile-username').innerHTML;
                loadPosts('profile', page_index, username);
            }
        } else {   
            if (document.title == 'Index') {
                loadPosts('all', 1, '');
            } else {
                const username = document.querySelector('#profile-username').innerHTML;
                loadPosts('profile', 1, username);
            }
        }
    })
    .catch(error => {
        console.log('Error:', error);
    });
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
    .then(data => {
        var likes_count = parseInt(document.querySelector(`[data-id="likes-${post_id}"]`).innerHTML);
        var like_link = document.querySelector(`[data-id="like-${post_id}"]`);

        if (data.like_status === 'liked') {
            likes_count += 1;
            document.querySelector(`[data-id="likes-${post_id}"]`).innerHTML = likes_count;
            like_link.innerHTML = ' Unlike';
        } else if (data.like_status === 'unliked') {
            likes_count -= 1;
            document.querySelector(`[data-id="likes-${post_id}"]`).innerHTML = likes_count;
            like_link.innerHTML = ' Like';
        }
    })
    .catch(error => {
        console.log('Error:', error);
    });
}

function editPost(post_id) {
    const card_text = document.querySelector(`[data-id="text-${post_id}"]`);

    const textarea = document.createElement('textarea');
    textarea.id = 'textarea'
    textarea.innerHTML = card_text.innerHTML; 

    card_text.innerHTML = '';
    card_text.append(textarea);

    const edit_link = document.querySelector(`[data-id="edit-${post_id}"]`);
    edit_link.remove();

    const card_body = document.querySelector(`[data-id="body-${post_id}"]`);

    const save_link = document.createElement('a');
    save_link.classList.add('save-link');
    save_link.setAttribute('href', '#');
    save_link.innerHTML = ' Save';
    card_body.append(save_link);

    // Add event listener for save link
    save_link.addEventListener('click', (event) => {
        event.preventDefault();
        const content = document.querySelector('#textarea').value;
        savePost(content, post_id);
    })
}

function deletePost(post_id) {
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

    fetch('http://127.0.0.1:8000/delete', requestOptions)
    .then(response => response.json())
    .then(data => {
        if (data.deleted = true) {
            const page = document.querySelector('#page-index').dataset.page
            
            if (document.title ==='Index') {
                loadPosts('all', page, '')
            } else if (document.title === 'Profile') {
                const username = document.querySelector('#profile-username').innerHTML
                loadPosts('profile', page, username)
            }
        }
    })
}