from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, UserCourseProgress, UserRoadmapSelection, Course, Domain
from datetime import datetime

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/try', methods=['POST'])
@jwt_required()
def try_course():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    course_id = data.get('course_id')
    
    if not course_id:
        return jsonify({'message': 'Missing course_id'}), 400
        
    progress = UserCourseProgress.query.filter_by(user_id=user_id, course_id=course_id).first()
    
    if not progress:
        progress = UserCourseProgress(
            user_id=user_id,
            course_id=course_id,
            status='tried',
            trial_started_at=datetime.utcnow()
        )
        db.session.add(progress)
    else:
        # If already completed, don't revert to tried
        if progress.status != 'completed':
            progress.status = 'tried'
            progress.trial_started_at = datetime.utcnow()
            
    db.session.commit()
    return jsonify(progress.to_dict()), 200

@progress_bp.route('/complete', methods=['POST'])
@jwt_required()
def complete_course():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    course_id = data.get('course_id')
    
    if not course_id:
        return jsonify({'message': 'Missing course_id'}), 400
        
    progress = UserCourseProgress.query.filter_by(user_id=user_id, course_id=course_id).first()
    
    if not progress:
        progress = UserCourseProgress(
            user_id=user_id,
            course_id=course_id,
            status='completed',
            completed_at=datetime.utcnow()
        )
        db.session.add(progress)
    else:
        progress.status = 'completed'
        progress.completed_at = datetime.utcnow()
        
    db.session.commit()
    return jsonify(progress.to_dict()), 200

@progress_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_progress():
    user_id = int(get_jwt_identity())
    progress = UserCourseProgress.query.filter_by(user_id=user_id).all()
    return jsonify([p.to_dict() for p in progress]), 200

@progress_bp.route('/select-roadmap', methods=['POST'])
@jwt_required()
def select_roadmap():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    domain_id = data.get('domain_id')
    level = data.get('level', 'student')
    
    if not domain_id:
        return jsonify({'message': 'Missing domain_id'}), 400
        
    selection = UserRoadmapSelection.query.filter_by(user_id=user_id).first()
    
    if not selection:
        selection = UserRoadmapSelection(
            user_id=user_id,
            domain_id=domain_id,
            level=level
        )
        db.session.add(selection)
    else:
        selection.domain_id = domain_id
        selection.level = level
        selection.selected_at = datetime.utcnow()
        
    db.session.commit()
    return jsonify(selection.to_dict()), 200

@progress_bp.route('/selected-roadmap', methods=['GET'])
@jwt_required()
def get_selected_roadmap():
    user_id = int(get_jwt_identity())
    selection = UserRoadmapSelection.query.filter_by(user_id=user_id).first()
    if not selection:
        return jsonify(None), 200
    return jsonify(selection.to_dict()), 200
