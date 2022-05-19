document.addEventListener('DOMContentLoaded', function() {
    // By default, load All Posts

    // Create post when form is submitted
    document.querySelector('#new-post-form').addEventListener('submit', (event) => {
        event.preventDefault();
        save_post();
    });
});

function save_post() {
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