# imcapsule

Project Setup
1. Create and activate virtual environment
2. Install requirements.txt : pip install -r requirements.txt
3. Migrate database: 
   python manage.py makemigrations
   python manage.py migrate
4. Create superuser: python manage.py createsuperuser
5. Run application: python manage.py runserver


Api details
User apis:
1. POST /user - for creating a user
2. POST /login - for user login. The api generates access token and refresh token

Recipe Apis:
1. POST /recipe - to create a recipe
2. GET /recipes - to return all the recipies
3. GET /recipes/current_user - returns all the recipies created by the loggedin user
4. GET /recipe/{recipe_id} - returns the details of a particular recipe
5. DELETE /recipe/{recipe_id} - delete a particular recipe
6. PUT /recipe/{recipe_id} - update a particular recipe
7. GET /search?keyword={search_key}

Wishlist Apis
1. POST /wishlist - to wishlist a recipe
2. GET /wishlist - returns all the wishlisted items by the loggedin user
3. DELETE /wishlist/{wishlist_id} - to remove a wishlisted item

Comment Apis
1. POST /comment - to add a comment
2. GET /get_comment/{recipe_id} - retuns all the comments of a particular recipe
3. PUT /comment/{comment_id} - edit a particular comment
4. DELETE /comment/{comment_id} - delete a particular comment
