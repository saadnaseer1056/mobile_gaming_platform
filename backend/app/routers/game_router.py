from fastapi import APIRouter
from app.models.game_model import Game
from app.database.db import get_db

router = APIRouter()

@router.post("/games")
def create_game(game: Game):
    conn = get_db()
    cursor = conn.cursor()

    # Ensure the table exists before inserting
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_library (
            game_id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_name TEXT NOT NULL UNIQUE,
            developer TEXT NOT NULL,
            genre TEXT,
            platform TEXT CHECK(platform IN ('Steam Deck', 'Stadia', 'Both')) NOT NULL
        )
    """)

    # Insert the game
    cursor.execute("""
        INSERT INTO game_library (game_name, developer, genre, platform)
        VALUES (?, ?, ?, ?)
    """, (game.game_name, game.developer, game.genre, game.platform))

    conn.commit()
    conn.close()
    return {"message": "Game added successfully"}

@router.get("/games")
def get_games():
    conn = get_db()
    cursor = conn.cursor()

    # Ensure the table exists before selecting
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_library (
            game_id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_name TEXT NOT NULL UNIQUE,
            developer TEXT NOT NULL,
            genre TEXT,
            platform TEXT CHECK(platform IN ('Steam Deck', 'Stadia', 'Both')) NOT NULL
        )
    """)

    # Fetch all games
    cursor.execute("SELECT * FROM game_library")
    games = cursor.fetchall()
    conn.close()
    return games

@router.put("/games/{game_id}")
def update_game(game_id: int, game: Game):
    conn = get_db()
    cursor = conn.cursor()

    # Check if game exists
    cursor.execute("SELECT * FROM game_library WHERE game_id=?", (game_id,))
    if not cursor.fetchone():
        return {"error": "Game not found"}

    # Update the game
    cursor.execute("""
        UPDATE game_library
        SET game_name=?, developer=?, genre=?, platform=?
        WHERE game_id=?
    """, (game.game_name, game.developer, game.genre, game.platform, game_id))

    conn.commit()
    conn.close()
    return {"message": "Game updated successfully"}

@router.delete("/games/{game_id}")
def delete_game(game_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM game_library WHERE game_id=?", (game_id,))
    conn.commit()
    conn.close()
    return {"message": "Game deleted successfully"}
