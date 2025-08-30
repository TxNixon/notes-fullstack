import uuid
from app.models.note import Note
from app import db


VALID_STATUS = {"public", "protected", "private"}

def random_slug() -> str:
    return str(uuid.uuid4())

def create_note(user_id, title, content, status, password_hash=None, password_hint=None):
    

    if status not in VALID_STATUS:
        return None, "Invalid status, Must be public, private or protected"
    
    if status == "protected" and not password_hash:
        return None, "Password is required for protected notes"
    
    new_note = Note(
        user_id=user_id,
        title=title,
        slug=random_slug(),
        content=content,
        status=status,
        password_hint=password_hint
    )

    if status == "protected":
        new_note.set_password(password_hash)
    
    try:
        db.session.add(new_note)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return None, str(e)

    return new_note, "create note success"
