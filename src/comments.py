"""Optional ticket comments stored in MongoDB (flexible fields and tags)."""
import os

from dotenv import load_dotenv

from db import ROOT

load_dotenv(ROOT / ".env")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DATABASE", "supportdesk")


def get_collection():
    """Return the 'comments' collection. Set MONGO_MOCK=1 to use an in-memory fake (no server needed)."""
    if os.getenv("MONGO_MOCK") == "1":
        return _mock_client().get_database(MONGO_DB)["comments"]
    from pymongo import MongoClient
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    client.admin.command("ping")  # fail fast if MongoDB is not running
    return client[MONGO_DB]["comments"]


_MOCK = None


def _mock_client():
    global _MOCK
    if _MOCK is None:
        import mongomock
        _MOCK = mongomock.MongoClient()
    return _MOCK


def add_comment(ticket_id, comment, tags=None, **extra_fields):
    """Store a comment. Extra fields are allowed because documents are schema-flexible."""
    doc = {"ticket_id": ticket_id, "comment": comment, "tags": tags or [], **extra_fields}
    get_collection().insert_one(doc)
    return doc


def get_comments(ticket_id):
    """Return all comments for a ticket."""
    return list(get_collection().find({"ticket_id": ticket_id}, {"_id": 0}))


def seed_comments():
    """Insert a few sample comments (replaces existing ones)."""
    col = get_collection()
    col.delete_many({})
    col.insert_many([
        {"ticket_id": 1, "comment": "Reset password and confirmed login.", "tags": ["login", "resolved"]},
        {"ticket_id": 2, "comment": "Refunded the duplicate charge.", "tags": ["billing", "refund"], "refund_amount": 499},
        {"ticket_id": 8, "comment": "Escalated to engineering.", "tags": ["export", "escalated"]},
    ])
