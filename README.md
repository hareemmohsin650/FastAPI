# FastAPI User Posts API

This project implements a simple FastAPI-based API for user authentication and post management.

## Requirements

- Python 3.8 or higher
- pip package manager

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/fastapi-user-posts.git
   cd fastapi-user-posts

2. Create and activate a virtual environment (optional but recommended):
    python3 -m venv venv
    source venv/bin/activate
3. Install the project dependencies:
    pip install -r requirements.txt

## Usage
Start the FastAPI server:
```uvicorn main:app --reload```
The server will be accessible at http://127.0.0.1:8000.

## Endpoints

### Signup Endpoint
URL: /signup

Method: POST

Request Body:
{
  "email": "user@example.com",
  "password": "your_password"
}
#### Response:

{
  "access_token": "your_jwt_token"
}


### Login Endpoint
URL: /login

Method: POST

Request Body:
{
  "email": "user@example.com",
  "password": "your_password"
}
#### Response:
{
  "access_token": "your_jwt_token"
}

### AddPost Endpoint
URL: /addPost

Method: POST

### Request Headers:

Authorization: Bearer your_jwt_token
Request Body:


{
  "text": "Your post text here"
}
#### Response:


{
  "postID": 1
}

### GetPosts Endpoint
URL: /getPosts

Method: GET

#### Request Headers:



Authorization: Bearer your_jwt_token
#### Response:


[
  {
    "postID": 1,
    "text": "Your post text here",
    "author": "user@example.com"
  }
]
DeletePost Endpoint
URL: /deletePost

Method: DELETE

#### Request Headers:



Authorization: Bearer your_jwt_token
Request Query Parameters:

post_id: The ID of the post to be deleted
#### Response:


{
  "message": "Post deleted successfully"
}