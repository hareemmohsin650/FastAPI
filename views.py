from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Dict
from datetime import datetime, timedelta
from cachetools import TTLCache
import jwt  # Import the JWT library


app = FastAPI()

# Fake database to store user information and posts
db_users = {}
db_posts = {}

# Fake secret key for JWT (in production, use a proper secret key)
SECRET_KEY = "fake-secret-key"

# Fake cache to store cached responses for getPosts endpoint
cache = TTLCache(maxsize=1000, ttl=300)  # Cache for 5 minutes

class Token(BaseModel):
    access_token: str

class User(BaseModel):
    email: EmailStr
    password: str

class Post(BaseModel):
    text: str

def generate_token(user_email: str) -> str:
    expiration = datetime.utcnow() + timedelta(minutes=30)
    payload = {
        "sub": user_email,
        "exp": expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token: str) -> Dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Depends(verify_token)):
    print(f'token {token}')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(f'payload {payload}')
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/signup", response_model=Token)
async def signup(user: User):
    db_users[user.email] = user
    token = generate_token(user.email)
    return Token(access_token=token)


@app.post("/login", response_model=Token)
async def login(user: User):
    if user.email in db_users and db_users[user.email].password == user.password:
        token = generate_token(user.email)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/addPost")
async def add_post(post: Post, current_user: Dict = Depends(get_current_user)):
    if len(post.text.encode()) > 1024 * 1024:
        raise HTTPException(status_code=400, detail="Payload size too large")
    post_id = len(db_posts) + 1
    db_posts[post_id] = {"text": post.text, "author": current_user['email']}
    return {"postID": post_id}

@app.get("/getPosts")
async def get_posts(current_user: Dict = Depends(get_current_user)):
    cached_response = cache.get(current_user["email"])
    if cached_response:
        return cached_response
    posts = [{"postID": post_id, **post} for post_id, post in db_posts.items() if post["author"] == current_user['email']]
    cache[current_user['email']] = posts
    return posts

@app.delete("/deletePost")
async def delete_post(post_id: int, current_user: Dict = Depends(get_current_user)):
    if post_id in db_posts and db_posts[post_id]["author"] == current_user['email']:
        del db_posts[post_id]
        return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found or unauthorized")

