# scripts/setup_db.py
from backend.services.database_service import DatabaseService


def seed():
    db = DatabaseService()
    # create test users
    try:
        u1 = db.create_user("alice")
        u2 = db.create_user("bob")
        print("Created users:", u1, u2)
    except Exception as e:
        print("Users probably already exist:", e)

    # add a sample game
    import uuid, chess
    gid = str(uuid.uuid4())
    board = chess.Board()
    db.create_game(gid, board.fen(), "local", "alice", "bob")
    print("Created sample game:", gid)


if __name__ == "__main__":
    seed()
