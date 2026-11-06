# Polylang-Blog

Simple blog application in different programming languages with Docker, Redis, Meilisearch, and RabbitMQ.

---

## Summary

* **`MVC`** pattern for the pages
* **`Repository`** pattern for db actions (MySQL)
* **`Service`** pattern for business logic
* **`Event-Listener`** pattern for decoupling side-effects and event-driven actions (e.g., syncing search index, triggering emails)
* **`Command / Worker`** pattern for scheduled and queue-based background tasks
* **`Infrastructure`**: Docker environment integrating MySQL, Redis, Meilisearch, and RabbitMQ

---

## Routes

* **`GET /`** -> `FrontController@index` (List of latest posts, cached via Redis)
* **`GET /search`** -> `FrontController@search` (Full-text search via Meilisearch)
* **`GET /authors`** -> `FrontController@authors` (List of users with posts)
* **`GET /post/{id}`** -> `FrontController@showPost` (Show single post with comments)
* **`GET /login`** -> `AuthenticationController@login` (Show login form)
* **`POST /login`** -> `AuthenticationController@login` (Process login, store session in Redis)
* **`GET /auth/github`** -> `AuthenticationController@githubRedirect` (Redirect user to GitHub OAuth authorization)
* **`GET /auth/github/callback`** -> `AuthenticationController@githubCallback` (Handle GitHub callback, login or auto-register user, store session in Redis)
* **`GET /logout`** -> `AuthenticationController@logout` (Logout user, destroy Redis session)
* **`GET /register`** -> `AuthenticationController@register` (Show registration form)
* **`POST /register`** -> `AuthenticationController@register` (Process registration, trigger UserRegistered event)
* **`GET /verify`** -> `AuthenticationController@verifyUser` (Verify user email via token)
* **`GET /forgot-password`** -> `AuthenticationController@forgotPassword` (Show forgot password form)
* **`POST /forgot-password`** -> `AuthenticationController@sendPasswordResetLink` (Push reset email task to RabbitMQ)
* **`GET /reset-password`** -> `AuthenticationController@resetPassword` (Show reset password form)
* **`POST /reset-password`** -> `AuthenticationController@updatePassword` (Save new password)
* **`GET /admin/posts`** -> `AdminController@myPosts` (List logged-in user posts)
* **`GET /admin/posts/new`** -> `AdminController@newPost` (Show create post form)
* **`POST /admin/posts`** -> `AdminController@savePost` (Save post, triggers PostCreated event)
* **`GET /admin/posts/{id}/edit`** -> `AdminController@editPost` (Show edit post form)
* **`POST /admin/posts/{id}/update`** -> `AdminController@updatePost` (Update post, triggers PostUpdated event)
* **`POST /admin/posts/{id}/delete`** -> `AdminController@deletePost` (Delete post, triggers PostDeleted event)
* **`GET /admin/comments`** -> `AdminController@myComments` (List user comments)
* **`POST /admin/posts/{postId}/comments`** -> `AdminController@saveComment` (Save new comment from frontend post view or admin)
* **`GET /admin/comments/{id}/edit`** -> `AdminController@editComment` (Show edit comment form)
* **`POST /admin/comments/{id}/update`** -> `AdminController@updateComment` (Update comment)
* **`POST /admin/comments/{id}/delete`** -> `AdminController@deleteComment` (Delete comment)

---

## DB tables (MySQL)

* `posts`id, user_id, image_url, title, content, created_at, updated_at
* `users`id, firstname, lastname, email, password, github_id, created_at, updated_at, verified_at, reset_token, reset_expires_at
* `comments`id, user_id, post_id, content, created_at, updated_at

---

## Models

* **`Post`**
* **`User`**
* **`Comment`**

---

## Controllers

* **`FrontController`**
    * **`index`** returns list of latest posts paginated. Uses **`RedisCache`** to cache the result. Gets optional author_id to filter posts by author.
    * **`search`** queries **`Meilisearch`** for fast full-text post search based on keyword query parameter.
    * **`authors`** returns list of users with posts paginated.
    * **`showPost(id)`** returns post by id and related author(user), image and comments.
* **`AuthenticationController`**
    * **`login`** user logs with email and password, creates session in **`Redis`** and gets redirected to AdminController index.
    * **`githubRedirect`** initializes OAuth flow and redirects to GitHub.
    * **`githubCallback`** handles GitHub response, retrieves profile info, checks if user exists in database (or creates one automatically), creates session in **`Redis`**, and redirects.
    * **`logout`** destroys session in **`Redis`** and gets redirected to FrontController index.
    * **`register`** user types firstname, lastname, email, password, confirm_password. Triggers `UserRegistered` event. User is redirected to verification pending page.
    * **`verifyMessage`** returns view **`verify_message`**.
    * **`forgotPassword`** returns **`password_forgot`** view.
    * **`sendPasswordResetLink`** receives POST request from **`password_forgot`** view. Checks via **`UserRepository`** if user exists. If user exists, generates new token via **`AuthService generatePasswordResetToken`**, saves it in users table with **`reset_expires_at`** valid for 1h via **`UserRepository`**. Pushes reset email job to **`RabbitMQ`**. Redirects to **`AuthenticationController verifyMessage`**.
    * **`resetPassword`** returns view **`password_reset`**.
    * **`updatePassword`** receives POST request from **`password_reset`** view with fields **`reset_token, user_id, password, password_confirm`**. Validates token, hashes password, saves it, and redirects to login.
* **`AdminController`**
    * **`newPost`** returns form for writing new post from logged-in users.
    * **`editPost(id)`** finds user post by id, and opens form for editing post.
    * **`savePost`** receives post data, saves it into db, and dispatches `PostCreated` event.
    * **`updatePost(id)`** receives post data, updates it into db, and dispatches `PostUpdated` event.
    * **`deletePost(id)`** deletes post from db and dispatches `PostDeleted` event.
    * **`myPosts`** returns list of posts written by user with buttons for edit and delete.
    * **`myComments`** returns list of comments written by user.
    * **`newComment(postId)`** returns form for new comment for given postId.
    * **`editComment(id)`** returns form for editing comment by its id.
    * **`saveComment`** saves new comment in db.
    * **`updateComment`** updates comment in db.
    * **`deleteComment(id)`** deletes comment from db.

---

## Events & Listeners (Event-Listener Pattern)

* **`EventDispatcher`** - Central mechanism to dispatch application events.
* **`PostCreated` Event** -> Handled by **`SyncPostToMeilisearchListener`** (adds document to search index).
* **`PostUpdated` Event** -> Handled by **`SyncPostToMeilisearchListener`** (updates document in search index).
* **`PostDeleted` Event** -> Handled by **`SyncPostToMeilisearchListener`** (removes document from search index).
* **`UserRegistered` Event** -> Handled by **`SendVerificationEmailListener`** (pushes email job to RabbitMQ queue).

---

## Views

* **`front`**
    * **`navigation`** links for Latest Posts, Authors, Search bar. Buttons for login/register or logout/admin.
    * **`post_index`** pagination buttons top and bottom. List of divs with image on left, h3 title and p resume 50 characters at right. Each div is link to **`showPost`**.
    * **`post_authors`** list of links by author Firstname Lastname to posts from the author.
    * **`post_show`** renders a post. h2 title at top, image after, content after, author Firstname Lastname after content at right. Next list of comments as div. Form with textarea and button for adding comment from currently logged user.
* **`auth`**
    * **`login`** form with fields email, password, button Login. Includes a distinct **"Login with GitHub"** OAuth button.
    * **`register`** form with fields firstname, lastname, email, password, password_confirm, button register. Includes **"Sign up with GitHub"** option.
    * **`verify_message`** page returned after registration with message to user.
    * **`password_forgot`** form with field for email address and button "Send Link".
    * **`password_reset`** form with fields for password, password_confirm, button "Update".
* **`admin`**
    * **`navigation`** left sidebar with links "My posts", "My Comments", "Logout".
    * **`my_posts`** button "Add Post". Pagination. Table with posts.
    * **`my_comments`** Pagination. Table with comments.
    * **`new_edit_post`** form with upload of image, field for Title, textarea with tinymc editor for content, button for "Save", button for "Discard".
    * **`new_edit_comment`** form with textarea for comment.

---

## Repositories

* **`UserRepository`**
* **`PostRepository`**
* **`CommentRepository`**
* All have standard actions:
    * **`getAll()`** returns all as array of models. Empty array if no rows.
    * **`getById(id)`** returns single row by id, null if not found.
    * **`save(model data)`** saves single row in db, returns row id on success, false on error.
    * **`update(model data)`** updates single row in db, returns row id on success, false on error.
    * **`delete(id)`** deletes single row by id, returns true on success, false on error.
* **`SearchRepository`** (Meilisearch integration for indexing and full-text searching)

---

## External Drivers & Libraries

* **`RedisClient`** handles session storage and data caching.
* **`RabbitMQClient`** handles publishing background jobs (emails, reports).
* **`OAuthClient`** (e.g., Authlib / Socialite / Passport) handles GitHub OAuth2 protocol handshake.

---

## Services

* **`AuthService`**
* **`passwordHash`**(string plainPassword) - returns hashed password string.
* **`passwordVerify`**(int userId, string plainPassword) - verifies password.
* **`generatePasswordResetToken`** generates token for password reset.
* **`GenerateCSVSummaryForNewPosts`** generates CSV file for posts created in the last 24h.
* **`GeneratePDFSummaryForNewPosts`** generates PDF file for posts created in the last 24h.
* **`SendEmail`** sends email to given recipient with subject, content, attachment.
* **`SearchService`** coordinates syncing posts with Meilisearch.
* **`QueueService`** pushes jobs to RabbitMQ.

---

## Commands

* **`CleanUnverifiedUsers`** deletes all users where `created_at < NOW() - INTERVAL 24 HOUR` and `verified_at` is null.
* **`GenerateSitemap`** generates sitemap.xml with links to all posts.
* **`SendNotificationSummary`** generates csv and pdf attachments via services and sends them via email to all users.
* **`QueueWorker`** background daemon listening to **`RabbitMQ`** to process asynchronous tasks.