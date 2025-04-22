from fastapi import APIRouter
from app.models.user_model import User
from app.database.db import get_db

router = APIRouter()

@router.post("/users")
def create_user(user: User):
    conn = get_db()
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            subscription_type TEXT CHECK(subscription_type IN ('Free', 'Pro')) DEFAULT 'Free'
        )
    """)

    # Insert user
    cursor.execute("""
        INSERT INTO users (username, email, password, subscription_type)
        VALUES (?, ?, ?, ?)
    """, (user.username, user.email, user.password, user.subscription_type))

    conn.commit()
    conn.close()
    return {"message": "User created successfully"}

@router.get("/users")
def get_users():
    conn = get_db()
    cursor = conn.cursor()

    # Make sure the table exists before querying
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            subscription_type TEXT CHECK(subscription_type IN ('Free', 'Pro')) DEFAULT 'Free'
        )
    """)

    # Select all users
    cursor.execute("SELECT user_id, username, email, subscription_type FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

@router.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    if not cursor.fetchone():
        return {"error": "User not found"}

    cursor.execute("""
        UPDATE users
        SET username=?, email=?, password=?, subscription_type=?
        WHERE user_id=?
    """, (user.username, user.email, user.password, user.subscription_type, user_id))

    conn.commit()
    conn.close()
    return {"message": "User updated successfully"}

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
    return {"message": "User deleted successfully"}
