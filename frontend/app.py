import streamlit as st
import requests
import pandas as pd

# Base URL of FastAPI backend
API_BASE = "http://backend:8000"

st.title("🎮 Mobile Gaming Platform - Frontend")

menu = ["Users", "Games"]
choice = st.sidebar.selectbox("Choose Option", menu)

# ================= USERS SECTION =================
if choice == "Users":
    st.subheader("➕ Create New User")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    subscription = st.selectbox("Subscription Type", ["Free", "Pro"])

    if st.button("Add User"):
        data = {
            "username": username,
            "email": email,
            "password": password,
            "subscription_type": subscription
        }
        res = requests.post(f"{API_BASE}/users", json=data)
        if res.status_code == 200:
            st.success(res.json().get("message", "User added!"))
        else:
            st.error("Failed to add user. Please try again.")

    st.subheader("📋 All Users")
    try:
        users = requests.get(f"{API_BASE}/users").json()
        if users:
            df = pd.DataFrame(users, columns=["User ID", "Username", "Email", "Subscription"])
            st.table(df)
        else:
            st.info("No users found.")
    except Exception as e:
        st.error(f"Error fetching users: {e}")

    st.subheader("❌ Delete User")
    del_user_id = st.text_input("Enter User ID to delete")
    if st.button("Delete User"):
        try:
            res = requests.delete(f"{API_BASE}/users/{del_user_id}")
            st.success(res.json().get("message", "User deleted!"))
        except Exception as e:
            st.error(f"Error deleting user: {e}")

    st.subheader("✏️ Update User")
    upd_user_id = st.text_input("Enter User ID to update")
    new_username = st.text_input("New Username")
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    new_subscription = st.selectbox("New Subscription Type", ["Free", "Pro"])

    if st.button("Update User"):
        try:
            updated_data = {
                "username": new_username,
                "email": new_email,
                "password": new_password,
                "subscription_type": new_subscription
            }
            res = requests.put(f"{API_BASE}/users/{upd_user_id}", json=updated_data)
            st.success(res.json().get("message", "User updated!"))
        except Exception as e:
            st.error(f"Error updating user: {e}")

# ================= GAMES SECTION =================
if choice == "Games":
    st.subheader("➕ Add New Game")

    game_name = st.text_input("Game Name")
    developer = st.text_input("Developer")
    genre = st.text_input("Genre")
    platform = st.selectbox("Platform", ["Steam Deck", "Stadia", "Both"])

    if st.button("Add Game"):
        data = {
            "game_name": game_name,
            "developer": developer,
            "genre": genre,
            "platform": platform
        }
        res = requests.post(f"{API_BASE}/games", json=data)
        if res.status_code == 200:
            st.success(res.json().get("message", "Game added!"))
        else:
            st.error("Failed to add game. Please try again.")

    st.subheader("📋 All Games")
    try:
        games = requests.get(f"{API_BASE}/games").json()
        if games:
            df = pd.DataFrame(games, columns=["Game ID", "Game Name", "Developer", "Genre", "Platform"])
            st.table(df)
        else:
            st.info("No games found.")
    except Exception as e:
        st.error(f"Error fetching games: {e}")

    st.subheader("❌ Delete Game")
    del_game_id = st.text_input("Enter Game ID to delete")
    if st.button("Delete Game"):
        try:
            res = requests.delete(f"{API_BASE}/games/{del_game_id}")
            st.success(res.json().get("message", "Game deleted!"))
        except Exception as e:
            st.error(f"Error deleting game: {e}")

    st.subheader("✏️ Update Game")
    upd_game_id = st.text_input("Enter Game ID to update")
    upd_game_name = st.text_input("New Game Name")
    upd_developer = st.text_input("New Developer")
    upd_genre = st.text_input("New Genre")
    upd_platform = st.selectbox("New Platform", ["Steam Deck", "Stadia", "Both"])

    if st.button("Update Game"):
        try:
            updated_game = {
                "game_name": upd_game_name,
                "developer": upd_developer,
                "genre": upd_genre,
                "platform": upd_platform
            }
            res = requests.put(f"{API_BASE}/games/{upd_game_id}", json=updated_game)
            st.success(res.json().get("message", "Game updated!"))
        except Exception as e:
            st.error(f"Error updating game: {e}")
