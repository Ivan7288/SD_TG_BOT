from flask import Flask, render_template, request, jsonify, send_file
from services.sd_service import StableDiffusionService
from models import Session, GeneratedImage
import os
import uuid

app = Flask(__name__)
sd_service = StableDiffusionService()

# Ensure uploads directory exists
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({'success': False, 'error': 'No prompt provided'})

        # Generate unique filename
        filename = f"{uuid.uuid4()}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # Generate image
        sd_service.generate_image(prompt, filepath)

        # Save to database
        session = Session()
        image = GeneratedImage(
            prompt=prompt,
            image_path=filename,
            user_id=request.headers.get('X-Telegram-User-Id', 0)
        )
        session.add(image)
        session.commit()
        session.close()

        return jsonify({
            'success': True,
            'image_url': f'/static/uploads/{filename}'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/history')
def history():
    session = Session()
    images = session.query(GeneratedImage).order_by(GeneratedImage.created_at.desc()).limit(10).all()
    session.close()

    return jsonify({
        'images': [{
            'url': f'/static/uploads/{img.image_path}',
            'prompt': img.prompt,
            'created_at': img.created_at.isoformat()
        } for img in images]
    })


@app.route('/static/uploads/<filename>')
def serve_image(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
