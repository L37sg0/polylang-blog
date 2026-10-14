# Polylang-Blog
Simple blog application in different programming languages with Docker, Redis, Meilisearch, and RabbitMQ.

---
## Summary
- **`MVC`** pattern for the pages
- **`Repository`** pattern for db actions (MySQL)
- **`Service`** pattern for business logic
- **`Command / Worker`** pattern for scheduled and queue-based background tasks
- **`Infrastructure`**: Docker environment integrating MySQL, Redis, Meilisearch, and RabbitMQ

---
## Routes
- **`GET /`** -> `FrontController@index` (List of latest posts, cached via Redis)
- **`GET /search`** -> `FrontController@search` (Full-text search via Meilisearch)
- **`GET /authors`** -> `FrontController@authors` (List of users with posts)
- **`GET /post/{id}`** -> `FrontController@showPost` (Show single post with comments)
- **`GET /login`** -> `AuthenticationController@login` (Show login form)
- **`POST /login`** -> `AuthenticationController@login` (Process login, store session in Redis)
- **`GET /logout`** -> `AuthenticationController@logout` (Logout user, destroy Redis session)
- **`GET /register`** -> `AuthenticationController@register` (Show registration form)
- **`POST /register`** -> `AuthenticationController@register` (Process registration, push email task to RabbitMQ)
- **`GET /verify`** -> `AuthenticationController@verifyUser` (Verify user email via token)
- **`GET /forgot-password`** -> `AuthenticationController@forgotPassword` (Show forgot password form)
- **`POST /forgot-password`** -> `AuthenticationController@sendPasswordResetLink` (Push reset email task to RabbitMQ)
- **`GET /reset-password`** -> `AuthenticationController@resetPassword` (Show reset password form)
- **`POST /reset-password`** -> `AuthenticationController@updatePassword` (Save new password)
- **`GET /admin/posts`** -> `AdminController@myPosts` (List logged-in user posts)
- **`GET /admin/posts/new`** -> `AdminController@newPost` (Show create post form)
- **`POST /admin/posts`** -> `AdminController@savePost` (Save post, sync to Meilisearch)
- **`GET /admin/posts/{id}/edit`** -> `AdminController@editPost` (Show edit post form)
- **`POST /admin/posts/{id}/update`** -> `AdminController@updatePost` (Update post, sync to Meilisearch)
- **`POST /admin/posts/{id}/delete`** -> `AdminController@deletePost` (Delete post, remove from Meilisearch)
- **`GET /admin/comments`** -> `AdminController@myComments` (List user comments)
- **`POST /admin/posts/{postId}/comments`** -> `AdminController@saveComment` (Save new comment from frontend post view or admin)
- **`GET /admin/comments/{id}/edit`** -> `AdminController@editComment` (Show edit comment form)
- **`POST /admin/comments/{id}/update`** -> `AdminController@updateComment` (Update comment)
- **`POST /admin/comments/{id}/delete`** -> `AdminController@deleteComment` (Delete comment)

---
## DB tables (MySQL)
- **`posts`** - id, user_id, image_url,  title, content, created_at, updated_at
- **`users`** - id, firstname, lastname, email, password, created_at, updated_at, verified_at, reset_token, reset_expires_at
- **`comments`** - id, user_id, post_id, content, created_at, updated_at

---
## Models
- **`Post`**
- **`User`**
- **`Comment`**

---
## Controllers
- **`FrontController`**
    - **`index`** - returns list of latest posts paginated. Uses **`RedisCache`** to cache the result. Gets optional author_id to filter posts by author.
    - **`search`** - queries **`Meilisearch`** for fast full-text post search based on keyword query parameter.
    - **`authors`** - returns list of users with posts paginated
    - **`showPost(id)`** - returns post by id and related author(user), image and comments
- **`AuthenticationController`**
    - **`login`** - user logs with email and password, creates session in **`Redis`** and gets redirected to AdminController index.
    - **`logout`** - destroys session in **`Redis`** and gets redirected to FrontController index.
    - **`register`** - user types firstname, lastname, email, password, confirm_password. Pushes an email job to **`RabbitMQ`** queue for async processing. Verification link is generated and send to user email. User is redirected to page with message. Your account is being created. Visit your email to verify and login. Visiting the verification link saves timestamp verified_at in users table and user is able to use his credentials to log into the system.
    - **`verifyMessage`** - returns view **`verify_message`**.
    - **`forgotPassword`** - returns **`password_forgot`** view.
    - **`sendPasswordResetLink`** - receives POST request from **`password_forgot`** view. Checks via **`UserRepository`** if user exists. If user exists, generates new token via **`AuthService generatePasswordResetToken`**, saves it in users table with **`reset_expires_at`** valid for 1h via **`UserRepository`**. Pushes reset email job to **`RabbitMQ`**. Sends email with `http://site.com/reset-password?token=XYZ` via **`SendEmail`** service. Redirects to **`AuthenticationController verifyMessage`**
    - **`resetPassword`** - returns view **`password_reset`**.
    - **`updatePassword`** - receives POST request from **`password_reset`** view with fields **`reset_token, user_id, password, password_confirm`**. Validates **`reset_token`** е валиден в таблицата `users`, паролите съвпадат, хешира я и я записва. Накрая редиректва към логин.
- **`AdminController`**
    - **`newPost`** - returns form for writing new post from logged-in users
    - **`editPost(id)`** - finds user post by id, and opens form for editing post
    - **`savePost`** - receives post data and saves it into db.
    - **`updatePost(id)`** - receives post data and updates it into db.
    - **`deletePost(id)`** - deletes post from db.
    - **`myPosts`** - returns list of posts written by user with buttons for edit and delete.
    - **`myComments`** - returns list of comments written by user.
    - **`newComment(postId)`** - returns form for new comment for given postId
    - **`editComment(id)`** - returns form for editing comment by its id.
    - **`saveComment`** - saves new comment in db.
    - **`updateComment`** - updates comment in db.
    - **`deleteComment(id)`** - deletes comment from db.
    - **`newPost`**, **`editPost(id)`**, **`savePost`**, **`updatePost(id)`**, **`deletePost(id)`** - manage posts and automatically trigger **`Meilisearch`** index updates (add/update/delete documents).

---
## Views
- **`front`**
    - **`navigation`** - links for Latest Posts, Authors, Search bar. Buttons for login/register or logout/admin.
    - **`post_index`** - pagination buttons top and bottom. List of divs with image on left, h3 title and p resume 50 characters at right. Each div is link to **`showPost`**
    - **`post_authors`** - list of links by author Firstname Lastname to posts from the author. Goes to **`FrontController index`**.
    - **`post_show`** - renders a post. h2 title at top, image after, content after, author Firstname Lastname after content at right. Author Firstname Lastname is link to posts by author. Next list of comments as div - h4 for user Firstname Lastname, p for comment. Form with textarea and button for adding comment from currently logged user for the given post.
- **`auth`**
    - **`login`** - form with fields email, password, button Login. Sends post request to **`AuthenticationController login`**. After form 2 links: one for "Don't have and account? Register", another for "Forgot my password"
    - **`register`** - form with fields firstname, lastname, email, password, password_confirm, button register. Sends post request to **`AuthenticationController register`**.
    - **`verify_message`** - page returned afer registration with message to user he should visit its email to verify account and login or password reset.
    - **`password_forgot`** - form with field for email address and button "Send Link". Submits to **`AuthenticationController sendPasswordResetLink`**.
    - **`password_reset`** - form with fields for password, password_confirm, button "Update". Form submits to **`AuthenticationController updatePassword`**
- **`admin`**
    - **`navigation`** - left sidebar with links "My posts", "My Comments", "Logout"
    - **`my_posts`** - button "Add Post" на горния ляв бутон. Пагинация горе и долу. Таблица с постове. Заглавия: PostID, Image, Title, Content, Date, Number of comments, Actions (View, Edit, Delete).
    - **`my_comments`** - Пагинация. Таблица с коментари. Заглавия: CommentId, PostTitle, Comment, Date, Actions (View, Edit, Delete).
    - **`new_edit_post`** - form with upload of image, field for Title, textarea with tinymc editor for content, button for "Save", button for "Discard".
    - **`new_edit_comment`** - form with textarea for comment.

---
## Repositories
- **`UserRepository`**
- **`PostRepository`**
    - **`getPostsByUserId(user_id)`**
- **`CommentRepository`**
    - **`getCommentsByPostId(post_id)`**
    - **`getCommentsByUserId(user_id)`**
- All have actions:
    - **`getAll()`** - returns all as array of models. Empty array if no rows.
    - **`getById(id)`** - returns single row by id, null if not found.
    - **`save(model data)`** - saves single row in db, returns row id on success, false on error. Saves error in log file.
    - **`update(model data)`** - updates single row in db, returns row id on success, false on error. Saves error in log file.
    - **`delete(id)`** - deletes single row by id. returns true on success, false on error. Saves error in log file
- **`SearchRepository`** (Meilisearch integration for indexing and full-text searching)

---
## External Drivers
- **`RedisClient`** - handles session storage and data caching.
- **`RabbitMQClient`** - handles publishing background jobs (emails, reports).

---
## Services
- **`AuthService`**
    - **`passwordHash`**(string plainPassword) - returns hashed password string.
    - **`passwordVerify`**(int userId, string plainPassword) - checks if hashed password is same as one in db for the given user id and returns true/false.
    - **`userRegister`**(array userData) - gets array of user data, validates it, creates new user via UserRepository, sends Verification email. returns void, writes error in log if such.
    - **`generatePasswordResetToken`** - generates token for password reset.
- **`GenerateCSVSummaryForNewPosts`** - gets all posts where **`created_at >= NOW() - INTERVAL 24 HOUR`** and generates csv file with table for title, author.
- **`GeneratePDFSummaryForNewPosts`** - gets all posts where **`created_at >= NOW() - INTERVAL 24 HOUR`** and generates pdf file with table for title, author.
- **`SendEmail`** - sends email to given recipient with subject, content, attachment.
- **`SearchService`** - coordinates syncing posts between MySQL and Meilisearch.
- **`QueueService`** - pushes jobs to RabbitMQ.

---
## Commands
- **`CleanUnverifiedUsers`** - deletes all users where **`created_at < NOW() - INTERVAL 24 HOUR`** and **`verified_at`** is null.
- **`GenerateSitemap`** - generates sitemap.xml with links to all posts.
- **`SendNotificationSummary`** - generates csv and pdf attachments via services and send them via email to all users.
- **`QueueWorker`** - Background daemon listening to **`RabbitMQ`** to process asynchronous emails and report generation tasks.