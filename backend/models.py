from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    experience_level = db.Column(db.String(20), default='student')  # student / professional
    semester = db.Column(db.Integer, nullable=True)
    branch = db.Column(db.String(100), nullable=True)
    interests = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_skills = db.relationship('UserSkill', backref='user', lazy=True, cascade='all, delete-orphan')
    bookmarks = db.relationship('Bookmark', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        import json
        interests_list = []
        if self.interests:
            try:
                interests_list = json.loads(self.interests)
            except:
                pass

        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'experience_level': self.experience_level,
            'semester': self.semester,
            'branch': self.branch,
            'interests': interests_list,
            'created_at': self.created_at.isoformat()
        }


class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(10), default='🔹')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'category': self.category, 'icon': self.icon}


class UserSkill(db.Model):
    __tablename__ = 'user_skills'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    skill = db.relationship('Skill')


class UserRoadmapSelection(db.Model):
    __tablename__ = 'user_roadmap_selections'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'), nullable=False)
    level = db.Column(db.String(20), default='student')
    selected_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    domain = db.relationship('Domain')
    user_rel = db.relationship('User', backref=db.backref('roadmap_selection', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'domain_id': self.domain_id,
            'domain_name': self.domain.name,
            'level': self.level,
            'selected_at': self.selected_at.isoformat()
        }


class UserCourseProgress(db.Model):
    __tablename__ = 'user_course_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    status = db.Column(db.String(20), default='not_started') # tried, in_progress, completed
    trial_started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    course = db.relationship('Course')

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'status': self.status,
            'trial_started_at': self.trial_started_at.isoformat() if self.trial_started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'course': self.course.to_dict()
        }


class Domain(db.Model):
    __tablename__ = 'domains'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(10), default='🎯')
    career_opportunities = db.Column(db.Text, nullable=False)  # JSON string
    required_skills = db.Column(db.Text, nullable=False)        # JSON string
    color = db.Column(db.String(20), default='#9B89C4')
    trending_score = db.Column(db.Integer, default=0)

    courses = db.relationship('Course', backref='domain', lazy=True)

    def to_dict(self):
        import json
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'career_opportunities': json.loads(self.career_opportunities),
            'required_skills': json.loads(self.required_skills),
            'color': self.color,
            'trending_score': self.trending_score
        }


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # Coursera, Udemy, etc.
    url = db.Column(db.String(500), nullable=False)
    coupon_code = db.Column(db.String(50), nullable=True)
    is_free = db.Column(db.Boolean, default=False)
    duration_weeks = db.Column(db.Integer, default=4)
    level = db.Column(db.String(20), default='student')  # student / professional / both
    rating = db.Column(db.Float, default=4.5)
    description = db.Column(db.Text, default='')
    has_trial = db.Column(db.Boolean, default=True)
    trial_days = db.Column(db.Integer, default=7)
    step_level = db.Column(db.Integer, default=1) # 1, 2, or 3

    def to_dict(self):
        return {
            'id': self.id,
            'domain_id': self.domain_id,
            'title': self.title,
            'platform': self.platform,
            'url': self.url,
            'coupon_code': self.coupon_code,
            'is_free': self.is_free,
            'duration_weeks': self.duration_weeks,
            'level': self.level,
            'rating': self.rating,
            'description': self.description,
            'has_trial': self.has_trial,
            'trial_days': self.trial_days,
            'step_level': self.step_level
        }


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    course = db.relationship('Course')

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'created_at': self.created_at.isoformat(),
            'course': self.course.to_dict()
        }

