# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.11** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Run Test File

```bash
python test_flaskr.py
```

# API Documentation

## 1. **Get All Categories**

### **Endpoint**: `/categories`

- **Method**: `GET`
- **Description**: Retrieves all categories.
- **Response**:
  - **Status**: 200 OK
  - **Body**:
    ```json
    {
      "status": 200,
      "categories": {
        "<category_id>": "<category_type>"
      }
    }
    ```

#### Example:

```json
{
  "status": 200,
  "categories": {
    "1": "Science",
    "2": "Art"
  }
}
```

---

## 2. **Get Paginated Questions**

### **Endpoint**: `/questions`

- **Method**: `GET`
- **Description**: Retrieves a paginated list of questions.
- **Query Parameters**:
  - `page` (optional): Page number for pagination (defaults to 1).
- **Response**:
  - **Status**: 200 OK
  - **Body**:
    ```json
    {
      "status": 200,
      "questions": [<question_object>, ...],
      "total_questions": <total_count>,
      "categories": {
        "<category_id>": "<category_type>"
      },
      "current_category": "All"
    }
    ```

#### Example:

```json
{
  "status": 200,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "difficulty": 1,
      "category": "Geography"
    }
  ],
  "total_questions": 50,
  "categories": {
    "1": "Science",
    "2": "Art"
  },
  "current_category": "All"
}
```

---

## 3. **Update Question by ID**

### **Endpoint**: `/questions/<int:id>`

- **Method**: `PUT`
- **Description**: Updates a question's details by its ID.
- **Request Body**:
  ```json
  {
    "question": "<new_question_text>",
    "answer": "<new_answer_text>",
    "difficulty": <new_difficulty_level>,
    "category": "<new_category_id>"
  }
  ```
- **Response**:
  - **Status**: 200 OK or 400 Bad Request or 404 Not Found
  - **Body** (on success):
    ```json
    {
      "status": 200,
      "message": "Success"
    }
    ```
  - **Body** (on failure):
    ```json
    {
      "status": 400,
      "message": "Missing required params."
    }
    ```
    or
    ```json
    {
      "status": 404,
      "message": "Question not found."
    }
    ```

#### Example (Success):

```json
{
  "status": 200,
  "message": "Success"
}
```

---

## 4. **Delete Question by ID**

### **Endpoint**: `/questions/<int:id>`

- **Method**: `DELETE`
- **Description**: Deletes a question by its ID.
- **Response**:
  - **Status**: 200 OK or 404 Not Found
  - **Body** (on success):
    ```json
    {
      "status": 200,
      "message": "Success"
    }
    ```
  - **Body** (on failure):
    ```json
    {
      "status": 404,
      "message": "Question not found"
    }
    ```

#### Example (Success):

```json
{
  "status": 200,
  "message": "Success"
}
```

---

## 5. **Add a New Question**

### **Endpoint**: `/questions`

- **Method**: `POST`
- **Description**: Adds a new question to the system.
- **Request Body**:
  ```json
  {
    "question": "<question_text>",
    "answer": "<answer_text>",
    "difficulty": <difficulty_level>,
    "category": "<category_id>"
  }
  ```
- **Response**:
  - **Status**: 200 OK or 400 Bad Request
  - **Body** (on success):
    ```json
    {
      "status": 200,
      "message": "Success"
    }
    ```
  - **Body** (on failure):
    ```json
    {
      "status": 400,
      "message": "Add Question Failed"
    }
    ```

#### Example (Success):

```json
{
  "status": 200,
  "message": "Success"
}
```

---

## 6. **Search Questions by Term**

### **Endpoint**: `/questions/search`

- **Method**: `POST`
- **Description**: Searches for questions based on a search term.
- **Request Body**:
  ```json
  {
    "searchTerm": "<term>"
  }
  ```
- **Response**:
  - **Status**: 200 OK or 400 Bad Request
  - **Body**:
    ```json
    {
      "status": 200,
      "questions": [<question_object>, ...],
      "total_questions": <total_count>,
      "current_category": "All"
    }
    ```

#### Example:

```json
{
  "status": 200,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "difficulty": 1,
      "category": "Geography"
    }
  ],
  "total_questions": 1,
  "current_category": "All"
}
```

---

## 7. **Get Questions by Category**

### **Endpoint**: `/categories/<int:id>/questions`

- **Method**: `GET`
- **Description**: Retrieves all questions for a given category by category ID.
- **Response**:
  - **Status**: 200 OK or 404 Not Found
  - **Body**:
    ```json
    {
      "status": 200,
      "questions": [<question_object>, ...],
      "total_questions": <total_count>,
      "current_category": "<category_type>"
    }
    ```

#### Example:

```json
{
  "status": 200,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "difficulty": 1,
      "category": "Geography"
    }
  ],
  "total_questions": 10,
  "current_category": "Geography"
}
```

---

## 8. **Start Quiz**

### **Endpoint**: `/quizzes`

- **Method**: `POST`
- **Description**: Starts a quiz by retrieving a random question from the selected category, excluding any previously answered questions.
- **Request Body**:
  ```json
  {
    "previous_questions": [<question_id>, ...],
    "quiz_category": {
      "id": <category_id>,
      "type": "<category_type>"
    }
  }
  ```
- **Response**:
  - **Status**: 200 OK or 400 Bad Request
  - **Body**:
    ```json
    {
      "status": 200,
      "question": <random_question_object>
    }
    ```

#### Example:

```json
{
  "status": 200,
  "question": {
    "id": 1,
    "question": "What is the capital of France?",
    "answer": "Paris",
    "difficulty": 1,
    "category": "Geography"
  }
}
```
