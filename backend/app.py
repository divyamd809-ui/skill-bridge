import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from seed_data import seed_database

# Resolve the frontend folder (one level up, then frontend/)
BASE_DIR  = os.path.abspath(os.path.dirname(__file__))
FRONTEND  = os.path.join(BASE_DIR, '..', 'frontend')

def create_app():
    app = Flask(__name__, static_folder=FRONTEND, static_url_path='')
    app.config.from_object(Config)

    # Enable CORS for all origins (needed for fetch() calls from the same server)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    JWTManager(app)

    # ── API blueprints ─────────────────────────────────────────────────────
    from routes.auth      import auth_bp
    from routes.skills    import skills_bp
    from routes.domains   import domains_bp
    from routes.roadmaps  import roadmaps_bp
    from routes.bookmarks import bookmarks_bp
    from routes.progress  import progress_bp

    app.register_blueprint(auth_bp,      url_prefix='/api/auth')
    app.register_blueprint(skills_bp,    url_prefix='/api')
    app.register_blueprint(domains_bp,   url_prefix='/api/domains')
    app.register_blueprint(roadmaps_bp,  url_prefix='/api/roadmaps')
    app.register_blueprint(bookmarks_bp, url_prefix='/api/bookmarks')
    app.register_blueprint(progress_bp,  url_prefix='/api/progress')


    # ── Health check ───────────────────────────────────────────────────────
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'SkillBridge API'})

    # ── Serve frontend HTML pages ──────────────────────────────────────────
    @app.route('/', defaults={'path': 'index.html'})
    @app.route('/<path:path>')
    def serve_frontend(path):
        """Serve any file from the frontend folder (HTML, CSS, JS, assets)."""
        if path and os.path.exists(os.path.join(FRONTEND, path)):
            return send_from_directory(FRONTEND, path)
        return send_from_directory(FRONTEND, 'index.html')

    # ── DB init & seed ─────────────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        seed_database(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)

