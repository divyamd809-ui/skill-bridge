from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Bookmark, Course

bookmarks_bp = Blueprint('bookmarks', __name__)

@bookmarks_bp.route('/', methods=['GET'])
@jwt_required()
def get_bookmarks():
    user_id = int(get_jwt_identity())
    user_bookmarks = Bookmark.query.filter_by(user_id=user_id).all()
    return jsonify([b.to_dict() for b in user_bookmarks]), 200

@bookmarks_bp.route('/', methods=['POST'])
@jwt_required()
def add_bookmark():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    course_id = data.get('course_id')
    
    if not course_id:
        return jsonify({'message': 'Course ID required'}), 400
        
    # Check if already bookmarked
    existing = Bookmark.query.filter_by(user_id=user_id, course_id=course_id).first()
    if existing:
        return jsonify({'message': 'Course already bookmarked'}), 200
        
    bookmark = Bookmark(user_id=user_id, course_id=course_id)
    db.session.add(bookmark)
    db.session.commit()
    
    return jsonify({'message': 'Bookmark added successfully'}), 201

@bookmarks_bp.route('/<int:course_id>', methods=['DELETE'])
@jwt_required()
def remove_bookmark(course_id):
    user_id = int(get_jwt_identity())
    bookmark = Bookmark.query.filter_by(user_id=user_id, course_id=course_id).first()
    
    if not bookmark:
        return jsonify({'message': 'Bookmark not found'}), 404
        
    db.session.delete(bookmark)
    db.session.commit()
    
    return jsonify({'message': 'Bookmark removed successfully'}), 200
