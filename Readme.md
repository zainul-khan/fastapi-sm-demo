# Clone this repo

# Create and Activate the virtual enviroment (commands are for windows)
virtualenv .venv  <br />
.venv/Scripts/activate

# Install requirement.txt
cd ./app [go in app dir]  <br />
pip install -r requirements.txt

# Run database migrations
cd .. [run the below commad from root directory for migrations]  <br />
alembic upgrade head

# Use this command to run the project make sure that you are inside the root directory
uvicorn app.main:app --reload

# Check if localhost works fine on your browers
http://localhost:8000/

# NOTE: This project mainly focuses on setup and fast api project architecture. You can make it more modular such as subdividing the files into folders. For example, schemas.py can be a folder containing user_schemas.py, post_schemas.py, etc., as the project grows larger.


# Content
1) Folder structure (You can make it more moduler but follow this architecture only as its taken from fast api's documentation).
2) Authentication (Protecting your routes by Token based authentication).
3) Database connection and managing migration using alembic package.
4) File upload and form data.
5) Joins between two tables.
6) Subqueries.
7) Send responses using standard return methods, response models, and the `JsonResponse` function.