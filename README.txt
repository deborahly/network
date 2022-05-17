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
(+) Fields: post, liked_by, active
(+) post: many-to-one relationship with models.Post id
(+) liked_by: many-to-one relationship with models.User id
(+) active: True by default, when a like is created

---
URLs

GET network/login
Sending a GET request to /login will return "network/login.html" where user can fill and submit the login form

POST network/login
Sending a POST request to /login will attempt to sign user in
    If authentication not successful, server will return "network/login.html" passing message "Invalid username and/or password."
    If authentication successful, server will log user in and redirect user to index
Request body:
{
    "username": <str>,
    "password": <str>
}

GET network/logout
Sending a GET request to /logout will log user out and redirect user to index

GET network/register
Sending a GET request to /register will return "network/register.html" where user can fill and submit the register form

POST network/register
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

GET network/index
Sending a GET request to network/index requesting to retrieve All page posts will return "index.html" passing context:
{
    "posts": [<str>]
}

PUT network/index
Sending a PUT request to network/index requesting to update posts on next/previous page will return a JsonResponse as below:
{
    "posts": [<str>]
}
Request body:
{
    "page": <int>
}

GET network/<str:username>
Sending a GET request to network/<str:username> will return "profile.html" passing context:
{
    "username": <str>,
    "followers": [<int>],
    "following": [<int>],
    "posts": [<str>]
}

PUT network/<str:username>
Sending a PUT request to network/<str:username> requesting to update follow/unfollow will return the HttpResponse(status=204)
Request body:
{
    "active": "True"/"False"
}

GET network/following
Sending a GET request to network/following requesting to retrieve Following page posts will return "index.html" passing context:
{
    "posts": [<str>]
}

PUT network/following
Sending a PUT request to network/posts requesting to update posts on next/previous page will return a JsonResponse as below:
{
    "posts": [<str>]
}
Request body:
{
    "page": <int>
}

POST network/new-post
Sending a POST request to network/new-post requesting to create a post will return a JsonResponse as below:
{
    "message": "Post created successfully.",
    status=201
}
Request body:
{
    "content": <str>
}

PUT network/<int:post_id>
Sending a PUT request to network/<int:post_id> requesting to update a post will return a JsonResponse as below:
{
    "message": "Post edited successfully.",
    status=204
}
Request body:
{
    "content": <str>
}

PUT network/<int:post_id>
Sending a PUT request to network/<int:post_id> requesting to update like/unlike will return the HttpResponse(status=204)
Request body:
{
    "active": "True"/"False"
}