import os
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

# ذاكرة مؤقتة بسيطة
cards_db = {}

@app.route('/', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        card_id = str(uuid.uuid4())[:8]

        # رفع الصورة
        photo_file = request.files.get('photo_file')
        photo_url = ''
        if photo_file and photo_file.filename != '':
            try:
                res = cloudinary.uploader.upload(photo_file, folder="cards/photos")
                photo_url = res.get('secure_url', '')
            except Exception as e:
                print("Photo Upload Error:", e)

        # رفع الصوت
        song_file = request.files.get('song_file')
        song_url = ''
        if song_file and song_file.filename != '':
            try:
                res = cloudinary.uploader.upload(song_file, resource_type="auto", folder="cards/audio")
                song_url = res.get('secure_url', '')
            except Exception as e:
                print("Song Upload Error:", e)

        # حفظ الكارت
        cards_db[card_id] = {
            'recipient_name': request.form.get('recipient_name', 'Love'),
            'sender_name': request.form.get('sender_name', 'Me'),
            'email_message': request.form.get('email_message', ''),
            'main_message': request.form.get('main_message', ''),
            'photo_url': photo_url,
            'song_url': song_url,
            'bg_color': request.form.get('bg_color', '#d90429')
        }

        return redirect(url_for('show_card', card_id=card_id))

    return render_template('admin.html')

@app.route('/card/<card_id>')
def show_card(card_id):
    data = cards_db.get(card_id, {
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
