import os
import json
import uuid
import cloudinary
import cloudinary.uploader
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 1. إعدادات Cloudinary
cloudinary.config(
    cloud_name = "xb0obyk3",
    api_key = "315196189644478",
    api_secret = "rvS2Eur12DH8scXcge7YHCvnP0E",
    secure = True
)

# 2. حفظ قاعدة البيانات في مجلد /tmp الخاص ببيئة Vercel
DB_FILE = '/tmp/database.json'

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def save_db(data):
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Save Error:", e)

# 3. الـ Routes
@app.route('/', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        card_id = str(uuid.uuid4())[:8]

        # رفع الصورة إلى Cloudinary
        photo_file = request.files.get('photo_file')
        if photo_file and photo_file.filename != '':
            upload_result = cloudinary.uploader.upload(
                photo_file,
                folder="cards/photos"
            )
            photo_url = upload_result.get('secure_url')
        else:
            photo_url = ''

        # رفع الأغنية إلى Cloudinary
        song_file = request.files.get('song_file')
        if song_file and song_file.filename != '':
            upload_result = cloudinary.uploader.upload(
                song_file,
                resource_type="auto",
                folder="cards/audio"
            )
            song_url = upload_result.get('secure_url')
        else:
            song_url = ''

        # حفظ البيانات
        db = load_db()
        db[card_id] = {
            'recipient_name': request.form.get('recipient_name', 'Love'),
            'sender_name': request.form.get('sender_name', 'Me'),
            'email_message': request.form.get('email_message', ''),
            'main_message': request.form.get('main_message', ''),
            'photo_url': photo_url,
            'song_url': song_url,
            'bg_color': request.form.get('bg_color', '#d90429')
        }
        save_db(db)

        return redirect(url_for('show_card', card_id=card_id))

    return render_template('admin.html')

@app.route('/card/<card_id>')
def show_card(card_id):
    db = load_db()
    data = db.get(card_id, {
        'recipient_name': 'Love',
        'sender_name': 'Me',
        'email_message': 'You have a special message inside!',
        'main_message': 'Happy Birthday!',
        'photo_url': '',
        'song_url': '',
        'bg_color': '#d90429'
    })
    return render_template('card.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
