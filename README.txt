(1) Add All Posts page
(+) Add link in the navigation bar for accessing the page
(+) Display all posts from all users, with the most recent posts first
(+) Add "Next" and "Previous" buttons. Posts should only be displayed 10 on a page
(+) Add Create Post function on top of the page. For writing content, display a textarea field. For submit, display a submit button

(2) Add Profile page
(+) Add link under any username display for accessing the page. When clicked, get required information from server and display Profile page
(+) Display user's posts, with the most recent posts first
(+) Display number of followers the user has
(+) Display number of people user follows
(+) Display "Follow" or "Unfollow" button when current user is visiting other users' profile page
(+) Add "Next" and "Previous" buttons. Posts should only be displayed 10 on a page

(3) Add Following page
(+) User has to be signed in
(+) Add link in the navigation bar for accessing the page
(+) Display posts from users the current user follows, with the most recent posts first
(+) Add "Next" and "Previous" buttons. Posts should only be displayed 10 on a page

(4) Post element
(+) Each post should include: username of the poster, the post content, date and time of post, number of "likes" the post received
(+) "Likes" count starts in 0 for each and every post
(+) Add "Like" or "Unlike" button. When clicked, update the like count on server and client without reloading the page

(5) Add Edit Post function
(+) User has to be signed in
(+) Display "Edit" button on current user's post
(+) When clicking the button, the content of the post should be replaced with a textarea pre-filled with current content
(+) Add "Save" button. When clicked, save new content on database without reloading the page
(+) Prevent users to edit posts that they do not own

(6) Create models.Post
(+) Fields: poster, content, created_on, edited
(+) poster: many-to-one relationship with models.User id
(+) content: textarea, max length of 150 characters
(+) created_on: date and time when post was submited
(+) edited: track if post was edited or not

(7) Create models.Follow
(+) Fields: follower, followed, active
(+) follower: many-to-one relationship with models.User id
(+) followed: many-to-one relationship with models.User id
(+) active: True by default, when a following is created

(8) Create models.Like
(+) Fields: post, liked_by
(+) post: many-to-one relationship with models.Post id
(+) liked_by: many-to-many relationship with models.User id

---
URLs

GET /login
Sending a GET request to /login will return "network/login.html" where user can fill and submit the login form

POST /login
Sending a POST request to /login will attempt to sign user in
    If authentication not successful, server will return "network/login.html" passing message "Invalid username and/or password."
    If authentication successful, server will log user in and redirect user to index
Request body:
{
    "username": <str>,
    "password": <str>
}

GET /logout
Sending a GET request to /logout will log user out and redirect user to index

GET /register
Sending a GET request to /register will return "network/register.html" where user can fill and submit the register form

POST /register
Sending a POST request to /register will attempt to register user
    If password and password confirmation do not match, server will return "network/register.html" passing message "Passwords must match."
    If unable to save new user for username already taken, server will return "network/register.html" passing message "Username already taken."
    If able to save new user, server will log user in and redirect user to index
Request body:
{
    "username": <str>,
    "email": <str>,
    "password": <str>,
    "confirmation": <str>
}

GET /index
Sending a GET request to network/index will return "index.html"

GET /posts/<int:page>
Sending a GET request to /posts requesting to retrieve posts will return a JsonResponse as below:
{
    "page": {
        "current": <int>,
        "has_next": <bool>,
        "has_previous": <bool>
    },
    "posts": [{
        "id": <int>,
        "poster": <str>,
        "content": <str>,
        "created_on": <str>,
        "edited": <bool>
    }],
}

GET /<str:username>
Sending a GET request to /<str:username> will return "profile.html" passing context:
{
    "username": <str>,
    "followers": <int>,
    "following": <int>
}

GET /<str:username>/posts
Sending a GET request to /<str:username>/posts requesting to retrieve posts by a certain user will return a JsonResponse as below:
{
    "page": {
        "current": <int>,
        "has_next": <bool>,
        "has_previous": <bool>
    },
    "posts": [{
        "id": <int>,
        "poster": <str>,
        "content": <str>,
        "created_on": <str>,
        "edited": <bool>
    }],
}

PUT /<str:username>
Sending a PUT request to /<str:username> requesting to update follow/unfollow will return the HttpResponse(status=204)
Request body:
{
    "active": "True"/"False"
}

GET /following
Sending a GET request to /following requesting to retrieve Following page posts will return "index.html" passing context:
{
    "posts": [<str>]
}

PUT /following
Sending a PUT request to /posts requesting to update posts on next/previous page will return a JsonResponse as below:
{
    "posts": [<str>]
}
Request body:
{
    "page": <int>
}

POST /new-post
Sending a POST request to /new-post requesting to create a post will return a JsonResponse as below:
{
    "message": "Post created successfully.",
    status=201
}
Request body:
{
    "content": <str>
}

PUT /<int:post_id>
Sending a PUT request to /<int:post_id> requesting to update a post will return a JsonResponse as below:
{
    "message": "Post edited successfully.",
    status=204
}
Request body:
{
    "content": <str>
}

PUT /<int:post_id>
Sending a PUT request to network/<int:post_id> requesting to update like/unlike will return the HttpResponse(status=204)
Request body:
{
    "active": "True"/"False"
}