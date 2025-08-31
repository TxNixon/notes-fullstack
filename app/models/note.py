import uuid
from app import db, bcrypt
from datetime import datetime

class Note(db.Model):
    #nama tabel
    __tablename__ = 'notes'
    #nama field table
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum("public", "protected", "private"), default="public", nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    password_hint = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    
    #relasi ke model user
    user = db.relationship('User', back_populates='notes')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_json(self, include_user=True):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'status': self.status,
            'password_hint': self.password_hint,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None
        }
        if include_user:
            data['user'] = self.user.to_json(include_note=False)

        return data