from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Domain, Skill, UserSkill
from seed_data import SKILL_DOMAIN_WEIGHTS
import json

domains_bp = Blueprint('domains', __name__)

@domains_bp.route('/', methods=['GET'])
def get_all_domains():
    domains = Domain.query.all()
    return jsonify([d.to_dict() for d in domains]), 200

@domains_bp.route('/trending', methods=['GET'])
def get_trending_domains():
    # Return top 4 domains by trending_score
    trending = Domain.query.order_by(Domain.trending_score.desc()).limit(4).all()
    return jsonify([d.to_dict() for d in trending]), 200


@domains_bp.route('/match', methods=['POST'])
@jwt_required()
def match_domains():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    # Get user skills from database or request
    skill_ids = data.get('skill_ids')
    if not skill_ids:
        user_skills = UserSkill.query.filter_by(user_id=user_id).all()
        skill_names = [us.skill.name for us in user_skills]
    else:
        skills = Skill.query.filter(Skill.id.in_(skill_ids)).all()
        skill_names = [s.name for s in skills]

    if not skill_names:
        return jsonify({'message': 'No skills provided for matching'}), 400

    # Scoring algorithm
    domain_scores = []
    all_domains = Domain.query.all()
    
    for domain in all_domains:
        score = 0
        max_possible_score = 0
        
        # Get weights for this domain
        weights = SKILL_DOMAIN_WEIGHTS.get(domain.name, {})
        
        # Calculate score based on user skills matching domain weights
        for skill_name, weight in weights.items():
            max_possible_score += weight
            if skill_name in skill_names:
                score += weight
        
        # Normalize score to percentage
        match_percentage = round((score / max_possible_score) * 100) if max_possible_score > 0 else 0
        
        domain_scores.append({
            'domain': domain.to_dict(),
            'match_score': match_percentage
        })
    
    # Sort by match score descending
    domain_scores.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Return top 3 matches
    return jsonify(domain_scores[:3]), 200
