import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# تحديد فولدر حفظ الملفات المرفوعة
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cards_db = {}

@app.route('/', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        card_id = str(uuid.uuid4())[:8]

        # 1. معالجة رفع الصورة
        photo_file = request.files.get('photo_file')
        if photo_file and photo_file.filename != '':
            photo_filename = secure_filename(photo_file.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
            photo_file.save(photo_path)
            photo_url = f"/static/uploads/{photo_filename}"
        else:
            photo_url = '/static/child_cutout.png'

        # 2. معالجة رفع الأغنية
        song_file = request.files.get('song_file')
        if song_file and song_file.filename != '':
            song_filename = secure_filename(song_file.filename)
            song_path = os.path.join(app.config['UPLOAD_FOLDER'], song_filename)
            song_file.save(song_path)
            song_url = f"/static/uploads/{song_filename}"
        else:
            song_url = '/static/birthday_song.mp3'

        # حفظ البيانات في الداتابيز
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
        'email_message': 'You have a special birthday message inside!',
        'main_message': 'Happy Birthday, my love.',
        'photo_url': '/static/child_cutout.png',
        'song_url': '/static/birthday_song.mp3',
        'bg_color': '#d90429'
    })
    return render_template('card.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)