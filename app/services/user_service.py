from app.models.user import User
from werkzeug.utils import secure_filename
from app import db
import os, uuid

def is_valid_image(filename):
    valid_text = {'.jpg', '.jpeg', '.png'}
    
    #untuk split nama file dan ext
    _, ext = os.path.splitext(filename.lower())
    return ext in valid_text

def random_name(filename):
    ext = os.path.splitext(filename)[1].lower()
    #random filename
    name = f"{uuid.uuid4().hex}{ext}"
    return name

def get_user_by_id(user_id):
    user = User.query.get(user_id)

    if not user :
        return None, "User not found"

    return user.to_json(), "get user success"

def update_user(user_id, data, profile_image_file=None, thumbnail_img_file=None):
    user = User.query.get(user_id)

    if not user :
        return None, "User not found"
    
    try:
        #update password (optional)
        if 'password' in data and data ['password']:
            user.set_password(data['password'])
        #update username dan email
        for field in ['username', 'email']:
            if field in data and data[field]:
                setattr(user, field, data[field])
        #buat direktori uploads
        os.makedirs('uploads', exist_ok=True)

        if profile_image_file and is_valid_image(profile_image_file.filename):
            name = random_name(profile_image_file.filename)
            filename = secure_filename(name)
            path = os.path.join('uploads', filename)
            #jika ada file sebelum nya
            profile_image_file.save(path)
            if user.profile_image:
                filename_old = user.profile_image.replace('/uploads/', '')
                path_old = os.path.join('uploads', filename_old)
                #untuk hapus file profile yang sebelumnya
                if os.path.exists(path_old):
                    os.remove(path_old)
            
            setattr(user, 'profile_image', f'/uploads/{filename}')
        #ganti thumbnail image
        if thumbnail_img_file and is_valid_image(thumbnail_img_file.filename):
            name = random_name(thumbnail_img_file.filename)
            filename = secure_filename(name)
            path = os.path.join('uploads', filename)
            #jika ada file sebelum nya
            thumbnail_img_file.save(path)
            if user.thumbnail_img:
                filename_old = user.thumbnail_img.replace('/uploads/', '')
                path_old = os.path.join('uploads', filename_old)
                #untuk hapus file thumbnail yang sebelumnya
                if os.path.exists(path_old):
                    os.remove(path_old)

            setattr(user, 'thumbnail_img', f'/uploads/{filename}')
        
        db.session.add(user)
        db.session.commit()

        return user.to_json(), f"update user {user.username} success"
    except Exception as e:
        db.session.rollback()
        return None, f"update user failed: {str(e)}"
