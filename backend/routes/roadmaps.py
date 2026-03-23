from flask import Blueprint, request, jsonify
from models import Course, Domain

roadmaps_bp = Blueprint('roadmaps', __name__)

@roadmaps_bp.route('/<int:domain_id>', methods=['GET'])
def get_roadmap(domain_id):
    level = request.args.get('level', 'student')
    
    domain = Domain.query.get(domain_id)
    if not domain:
        return jsonify({'message': 'Domain not found'}), 404
        
    # Get courses for this domain and level
    # "both" level courses are included for everyone
    courses = Course.query.filter(
        Course.domain_id == domain_id,
        (Course.level == level) | (Course.level == 'both')
    ).all()
    
    return jsonify({
        'domain': domain.to_dict(),
        'courses': [c.to_dict() for c in courses]
    }), 200

@roadmaps_bp.route('/all', methods=['GET'])
def get_all_roadmaps():
    domains = Domain.query.all()
    result = []
    for d in domains:
        courses = Course.query.filter_by(domain_id=d.id).all()
        result.append({
            'domain': d.to_dict(),
            'courses': [c.to_dict() for c in courses]
        })
    return jsonify(result), 200
