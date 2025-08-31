import uuid
from app.models.note import Note
from app import db
from sqlalchemy import asc, desc


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


def get_public_notes(q=None, page=1, per_page=10, sort="created_at", order="desc"):
    query = Note.query.filter(Note.status == "public", Note.deleted_at == None)

    if q:
        query = query.filter(Note.title.contains(q) | Note.content.contains(q) | Note.title.ilike(f"%{q}%") | Note.content.ilike(f"%{q}%"))

    sort_map = {
        "title" : Note.title,
        "created_at" : Note.created_at,
        "updated_at" : Note.updated_at
    }
    
    sort_column = sort_map.get(sort, Note.created_at)

    #order by
    if order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    notes_data = [note.to_json(include_user=True) for note in pagination.items]

    meta = {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
        "sort" : sort,
        "order": order,
        "q" : q or ""
    }

    return notes_data, meta, "Get public notes"