from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import anthropic
import os
import json
from database import db, History, Cache, Bookmark, SampleData, init_db

app = Flask(__name__, static_folder='static')
CORS(app)
db_url = os.environ.get('DATABASE_URL', 'sqlite:///secureagent.db')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# ── 정적 파일 서빙 ──
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# ── Claude API 중계 ──
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    api_key = request.headers.get('X-API-Key', '')
    if not api_key or not api_key.startswith('sk-ant-'):
        return jsonify({'error': 'API 키가 올바르지 않습니다'}), 401
    try:
        import httpx
        client = anthropic.Anthropic(
            api_key=api_key,
            http_client=httpx.Client()
        )
        msg = client.messages.create(
            model=data.get('model', 'claude-haiku-4-5-20251001'),
            max_tokens=data.get('max_tokens', 2500),
            system=data.get('system', ''),
            messages=data.get('messages', [])
        )
        return jsonify({'content': [{'type': 'text', 'text': msg.content[0].text}]})
    except anthropic.AuthenticationError:
        return jsonify({'error': 'API 키가 올바르지 않습니다'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── 히스토리 API ──
@app.route('/api/history', methods=['GET'])
def get_history():
    items = History.query.order_by(History.created_at.desc()).limit(50).all()
    return jsonify([{'question': h.question, 'created_at': str(h.created_at)} for h in items])

@app.route('/api/history', methods=['POST'])
def save_history():
    q = request.json.get('question', '').strip()
    if not q:
        return jsonify({'ok': False}), 400
    try:
        existing = History.query.filter_by(question=q).first()
        if existing:
            db.session.delete(existing)
            db.session.flush()
        h = History(question=q)
        db.session.add(h)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return jsonify({'ok': True})

@app.route('/api/history/<path:question>', methods=['DELETE'])
def delete_history(question):
    h = History.query.filter_by(question=question).first()
    if h:
        db.session.delete(h)
        db.session.commit()
    c = Cache.query.filter_by(question=question).first()
    if c:
        db.session.delete(c)
        db.session.commit()
    return jsonify({'ok': True})

@app.route('/api/history', methods=['DELETE'])
def clear_history():
    History.query.delete()
    Cache.query.delete()
    Bookmark.query.delete()
    db.session.commit()
    return jsonify({'ok': True})

# ── 캐시 API ──
@app.route('/api/cache/<path:question>', methods=['GET'])
def get_cache(question):
    c = Cache.query.filter_by(question=question).first()
    if not c:
        return jsonify(None)
    return jsonify({'chatHTML': c.chat_html, 'sess': json.loads(c.session_data)})

@app.route('/api/cache', methods=['POST'])
def save_cache():
    data = request.json
    q = data.get('question', '').strip()
    if not q:
        return jsonify({'ok': False}), 400
    c = Cache.query.filter_by(question=q).first()
    if c:
        c.chat_html = data.get('chatHTML', '')
        c.session_data = json.dumps(data.get('sess', {}))
    else:
        c = Cache(question=q, chat_html=data.get('chatHTML', ''),
                  session_data=json.dumps(data.get('sess', {})))
        db.session.add(c)
    db.session.commit()
    return jsonify({'ok': True})

# ── 북마크 API ──
@app.route('/api/bookmark', methods=['GET'])
def get_bookmarks():
    items = Bookmark.query.order_by(Bookmark.created_at.desc()).all()
    result = {}
    for b in items:
        result[b.question] = {'ts': b.created_at.timestamp() * 1000, 'memo': b.memo or ''}
    return jsonify(result)

@app.route('/api/bookmark', methods=['POST'])
def save_bookmark():
    data = request.json
    q = data.get('question', '').strip()
    if not q:
        return jsonify({'ok': False}), 400
    b = Bookmark.query.filter_by(question=q).first()
    if b:
        db.session.delete(b)
        db.session.commit()
        return jsonify({'ok': True, 'action': 'removed'})
    b = Bookmark(question=q, memo=data.get('memo', ''))
    db.session.add(b)
    db.session.commit()
    return jsonify({'ok': True, 'action': 'added'})

@app.route('/api/bookmark/memo', methods=['POST'])
def save_memo():
    data = request.json
    q = data.get('question', '').strip()
    b = Bookmark.query.filter_by(question=q).first()
    if not b:
        b = Bookmark(question=q, memo=data.get('memo', ''))
        db.session.add(b)
    else:
        b.memo = data.get('memo', '')
    db.session.commit()
    return jsonify({'ok': True})

# ── 샘플 데이터 API ──
@app.route('/api/sample', methods=['GET'])
def get_samples():
    items = SampleData.query.all()
    return jsonify({s.label: s.raw_data for s in items})

# Render/gunicorn 환경에서도 DB 초기화 실행
with app.app_context():
    init_db(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
