from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Skill, UserSkill, User

skills_bp = Blueprint('skills', __name__)

@skills_bp.route('/skills', methods=['GET'])
def get_all_skills():
    skills = Skill.query.all()
    return jsonify([s.to_dict() for s in skills]), 200

@skills_bp.route('/user/skills', methods=['GET'])
@jwt_required()
def get_user_skills():
    user_id = int(get_jwt_identity())
    user_skills = UserSkill.query.filter_by(user_id=user_id).all()
    skills = [us.skill.to_dict() for us in user_skills]
    return jsonify(skills), 200

@skills_bp.route('/user/skills', methods=['POST'])
@jwt_required()
def save_user_skills():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    skill_ids = data.get('skill_ids', [])
    experience_level = data.get('experience_level', 'student')
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
        
    user.experience_level = experience_level
    
    # Simple strategy: clear existing and add new
    UserSkill.query.filter_by(user_id=user_id).delete()
    
    for sid in skill_ids:
        user_skill = UserSkill(user_id=user_id, skill_id=sid)
        db.session.add(user_skill)
    
    db.session.commit()
    
    return jsonify({'message': 'Skills saved successfully'}), 200
