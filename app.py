import os
import uuid
import qrcode
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['QR_FOLDER'] = 'static/qrcodes'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['QR_FOLDER'], exist_ok=True)

# قاعدة بيانات مؤقتة في الذاكرة
db = {}

@app.route('/', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        page_id = str(uuid.uuid4())[:8]
        
        # استلام البيانات من الفورم
        sender_name = request.form.get('sender_name', 'Babe')
        recipient_name = request.form.get('recipient_name', 'My Love')
        email_message = request.form.get('email_message', 'Check out this awesome surprises for YOU!')
        main_message = request.form.get('main_message', '')
        
        # رفع الصورة الشخصية
        photo = request.files.get('photo')
        photo_url = None
        if photo and photo.filename != '':
            filename = f"{page_id}_{secure_filename(photo.filename)}"
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_url = url_for('static', filename=f'uploads/{filename}')

        # رفع الملف الصوتى
        song = request.files.get('song')
        song_url = None
        if song and song.filename != '':
            song_name = f"{page_id}_{secure_filename(song.filename)}"
            song.save(os.path.join(app.config['UPLOAD_FOLDER'], song_name))
            song_url = url_for('static', filename=f'uploads/{song_name}')

        # حفظ البيانات
        db[page_id] = {
            'sender_name': sender_name,
            'recipient_name': recipient_name,
            'email_message': email_message,
            'main_message': main_message,
            'photo_url': photo_url,
            'song_url': song_url
        }

        # إنشاء QR Code
        domain = request.host_url.rstrip('/')
        target_url = f"{domain}/card/{page_id}"
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(target_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_filename = f"{page_id}.png"
        qr_img.save(os.path.join(app.config['QR_FOLDER'], qr_filename))

        return render_template('admin.html', 
                               card_url=target_url, 
                               qr_url=url_for('static', filename=f'qrcodes/{qr_filename}'))

    return render_template('admin.html')

@app.route('/card/<page_id>')
def show_card(page_id):
    data = db.get(page_id)
    if not data:
        return "الصفحة غير موجودة 404", 404
    return render_template('card.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)