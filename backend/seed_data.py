import json
from models import db, Skill, Domain, Course

SKILLS_DATA = [
    {'name': 'Coding', 'category': 'Technical', 'icon': '💻'},
    {'name': 'Python', 'category': 'Technical', 'icon': '🐍'},
    {'name': 'JavaScript', 'category': 'Technical', 'icon': '⚡'},
    {'name': 'Data Analysis', 'category': 'Technical', 'icon': '📊'},
    {'name': 'Machine Learning', 'category': 'Technical', 'icon': '🤖'},
    {'name': 'Designing', 'category': 'Creative', 'icon': '🎨'},
    {'name': 'UI/UX', 'category': 'Creative', 'icon': '✏️'},
    {'name': 'Communication', 'category': 'Soft Skills', 'icon': '🗣️'},
    {'name': 'Problem Solving', 'category': 'Soft Skills', 'icon': '🧩'},
    {'name': 'Analytical Thinking', 'category': 'Soft Skills', 'icon': '🔍'},
    {'name': 'Management', 'category': 'Business', 'icon': '📋'},
    {'name': 'Marketing', 'category': 'Business', 'icon': '📣'},
    {'name': 'Mathematics', 'category': 'Technical', 'icon': '🔢'},
    {'name': 'Statistics', 'category': 'Technical', 'icon': '📈'},
    {'name': 'Networking', 'category': 'Technical', 'icon': '🌐'},
    {'name': 'Cybersecurity', 'category': 'Technical', 'icon': '🔒'},
    {'name': 'Cloud Computing', 'category': 'Technical', 'icon': '☁️'},
    {'name': 'Project Management', 'category': 'Business', 'icon': '🗂️'},
    {'name': 'Public Speaking', 'category': 'Soft Skills', 'icon': '🎤'},
    {'name': 'Creativity', 'category': 'Creative', 'icon': '💡'},
]

DOMAINS_DATA = [
    {
        'name': 'Web Development',
        'icon': '🌐',
        'color': '#9B89C4',
        'trending_score': 95,
        'description': 'Build modern, interactive web applications using cutting-edge technologies. Covers frontend, backend, and full-stack development across a wide range of industries.',
        'career_opportunities': json.dumps(['Frontend Developer', 'Backend Developer', 'Full Stack Developer', 'React Developer', 'Node.js Developer', 'DevOps Engineer']),
        'required_skills': json.dumps(['Coding', 'JavaScript', 'Problem Solving', 'UI/UX']),
        'weight_map': {'Coding': 10, 'JavaScript': 10, 'Problem Solving': 8, 'UI/UX': 6, 'Designing': 5, 'Python': 5, 'Communication': 3, 'Creativity': 4},
    },
    {
        'name': 'Data Science & AI',
        'icon': '🤖',
        'color': '#B8A9D9',
        'trending_score': 98,
        'description': 'Leverage data and artificial intelligence to extract insights, build predictive models, and drive intelligent decision-making across industries.',
        'career_opportunities': json.dumps(['Data Scientist', 'ML Engineer', 'AI Researcher', 'Data Analyst', 'Business Intelligence Analyst', 'NLP Engineer']),
        'required_skills': json.dumps(['Python', 'Mathematics', 'Statistics', 'Machine Learning', 'Analytical Thinking']),
        'weight_map': {'Python': 10, 'Mathematics': 10, 'Statistics': 10, 'Machine Learning': 10, 'Analytical Thinking': 9, 'Data Analysis': 9, 'Coding': 6, 'Problem Solving': 7},
    },
    {
        'name': 'UX/UI Design',
        'icon': '🎨',
        'color': '#C9B8E8',
        'trending_score': 88,
        'description': 'Create beautiful and intuitive user experiences. Combine design principles with user research to craft digital products people love using.',
        'career_opportunities': json.dumps(['UX Designer', 'UI Designer', 'Product Designer', 'Interaction Designer', 'Visual Designer', 'Design Lead']),
        'required_skills': json.dumps(['Designing', 'UI/UX', 'Creativity', 'Communication']),
        'weight_map': {'Designing': 10, 'UI/UX': 10, 'Creativity': 9, 'Communication': 7, 'Problem Solving': 6, 'Analytical Thinking': 5},
    },
    {
        'name': 'Business & Management',
        'icon': '📊',
        'color': '#A896CB',
        'trending_score': 82,
        'description': 'Drive organizational growth through strategic thinking, leadership, and business acumen. Manage teams, projects, and business operations effectively.',
        'career_opportunities': json.dumps(['Business Analyst', 'Project Manager', 'Operations Manager', 'Product Manager', 'Management Consultant', 'Entrepreneur']),
        'required_skills': json.dumps(['Communication', 'Management', 'Analytical Thinking', 'Project Management']),
        'weight_map': {'Communication': 10, 'Management': 10, 'Analytical Thinking': 8, 'Project Management': 9, 'Problem Solving': 7, 'Public Speaking': 8, 'Marketing': 6},
    },
    {
        'name': 'Digital Marketing',
        'icon': '📣',
        'color': '#B5A3D6',
        'trending_score': 75,
        'description': 'Grow brands and reach audiences through data-driven digital strategies. Master SEO, social media, content marketing, and paid advertising.',
        'career_opportunities': json.dumps(['Digital Marketer', 'SEO Specialist', 'Content Strategist', 'Social Media Manager', 'Growth Hacker', 'Brand Manager']),
        'required_skills': json.dumps(['Marketing', 'Communication', 'Creativity', 'Analytical Thinking']),
        'weight_map': {'Marketing': 10, 'Communication': 9, 'Creativity': 8, 'Analytical Thinking': 7, 'Public Speaking': 6, 'Problem Solving': 5},
    },
    {
        'name': 'Cybersecurity',
        'icon': '🔒',
        'color': '#8A78B5',
        'trending_score': 92,
        'description': 'Protect digital assets and infrastructure from threats. Master ethical hacking, network security, and security architecture to defend organizations.',
        'career_opportunities': json.dumps(['Security Analyst', 'Ethical Hacker', 'Penetration Tester', 'Security Engineer', 'SOC Analyst', 'CISO']),
        'required_skills': json.dumps(['Cybersecurity', 'Networking', 'Coding', 'Analytical Thinking']),
        'weight_map': {'Cybersecurity': 10, 'Networking': 10, 'Coding': 8, 'Analytical Thinking': 8, 'Problem Solving': 7, 'Python': 6, 'Mathematics': 4},
    },
    {
        'name': 'Cloud & DevOps',
        'icon': '☁️',
        'color': '#9E8EC7',
        'trending_score': 94,
        'description': 'Build and manage scalable cloud infrastructure. Automate deployments, ensure reliability, and bridge the gap between development and operations.',
        'career_opportunities': json.dumps(['Cloud Architect', 'DevOps Engineer', 'Site Reliability Engineer', 'Platform Engineer', 'Cloud Consultant', 'Kubernetes Engineer']),
        'required_skills': json.dumps(['Cloud Computing', 'Coding', 'Networking', 'Problem Solving']),
        'weight_map': {'Cloud Computing': 10, 'Coding': 8, 'Networking': 8, 'Problem Solving': 7, 'Python': 6, 'Cybersecurity': 5, 'JavaScript': 4},
    },
    {
        'name': 'Product Management',
        'icon': '🚀',
        'color': '#ADA0D2',
        'trending_score': 85,
        'description': 'Own the vision and strategy of digital products. Balance user needs, business goals, and technical constraints to build products that matter.',
        'career_opportunities': json.dumps(['Product Manager', 'Product Owner', 'Growth Product Manager', 'Technical PM', 'Chief Product Officer', 'Startup Founder']),
        'required_skills': json.dumps(['Communication', 'Analytical Thinking', 'Management', 'Problem Solving']),
        'weight_map': {'Communication': 9, 'Analytical Thinking': 9, 'Management': 8, 'Problem Solving': 8, 'Marketing': 6, 'Coding': 5, 'UI/UX': 5, 'Project Management': 7},
    },
]

COURSES_DATA = [
    # Web Development
    {'domain': 'Web Development', 'title': 'Responsive Web Design', 'platform': 'freeCodeCamp', 'url': 'https://www.freecodecamp.org/learn/2022/responsive-web-design/', 'coupon_code': None, 'is_free': True, 'duration_weeks': 8, 'level': 'student', 'rating': 4.8, 'description': 'Learn HTML5, CSS3, Flexbox, Grid, and responsive design principles.', 'has_trial': False, 'trial_days': 0, 'step_level': 1},
    {'domain': 'Web Development', 'title': 'The Complete Web Developer Bootcamp', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/the-complete-web-development-bootcamp/', 'coupon_code': 'WEBDEV2024', 'is_free': False, 'duration_weeks': 16, 'level': 'student', 'rating': 4.7, 'description': 'Master JavaScript, Node, React, and MongoDB.', 'has_trial': True, 'trial_days': 7, 'step_level': 2},
    {'domain': 'Web Development', 'title': 'Advanced JavaScript Concepts', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/advanced-javascript-concepts/', 'coupon_code': 'JSADV30', 'is_free': False, 'duration_weeks': 10, 'level': 'professional', 'rating': 4.7, 'description': 'Deep dive into engine internals, patterns, and performance.', 'has_trial': True, 'trial_days': 30, 'step_level': 3},
    
    # Data Science & AI
    {'domain': 'Data Science & AI', 'title': 'Data Analysis with Python', 'platform': 'freeCodeCamp', 'url': 'https://www.freecodecamp.org/learn/data-analysis-with-python/', 'coupon_code': None, 'is_free': True, 'duration_weeks': 6, 'level': 'student', 'rating': 4.7, 'description': 'NumPy, Pandas, Matplotlib, and data visualization.', 'has_trial': False, 'trial_days': 0, 'step_level': 1},
    {'domain': 'Data Science & AI', 'title': 'IBM Data Science Certificate', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/ibm-data-science', 'coupon_code': 'COURSERA7', 'is_free': False, 'duration_weeks': 40, 'level': 'student', 'rating': 4.6, 'description': 'Comprehensive path to becoming a Data Scientist.', 'has_trial': True, 'trial_days': 7, 'step_level': 2},
    {'domain': 'Data Science & AI', 'title': 'Deep Learning Specialization', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/deep-learning', 'coupon_code': 'DEEPLEARN24', 'is_free': False, 'duration_weeks': 20, 'level': 'professional', 'rating': 4.9, 'description': 'Neural networks, CNNs, RNNs with Andrew Ng.', 'has_trial': True, 'trial_days': 7, 'step_level': 3},

    # UX/UI Design
    {'domain': 'UX/UI Design', 'title': 'Introduction to User Experience Design', 'platform': 'Coursera', 'url': 'https://www.coursera.org/learn/user-experience-design', 'coupon_code': None, 'is_free': True, 'duration_weeks': 4, 'level': 'student', 'rating': 4.5, 'description': 'Core principles of UX design and user research.', 'has_trial': False, 'trial_days': 0, 'step_level': 1},
    {'domain': 'UX/UI Design', 'title': 'Google UX Design Certificate', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/google-ux-design', 'coupon_code': 'COURSERA7', 'is_free': False, 'duration_weeks': 26, 'level': 'student', 'rating': 4.8, 'description': 'Professional certification from Google.', 'has_trial': True, 'trial_days': 7, 'step_level': 2},
    {'domain': 'UX/UI Design', 'title': 'Advanced Figma for Professionals', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/figma-ux-ui-design-user-experience-tutorial-course/', 'coupon_code': 'FIGMA30', 'is_free': False, 'duration_weeks': 8, 'level': 'professional', 'rating': 4.6, 'description': 'Design systems and collaboration at scale.', 'has_trial': True, 'trial_days': 30, 'step_level': 3},

    # Business & Management
    {'domain': 'Business & Management', 'title': 'Introduction to Management', 'platform': 'edX', 'url': 'https://www.edx.org/course/introduction-to-management', 'coupon_code': None, 'is_free': True, 'duration_weeks': 6, 'level': 'student', 'rating': 4.5, 'description': 'Core management principles and leadership.', 'has_trial': False, 'trial_days': 0, 'step_level': 1},
    {'domain': 'Business & Management', 'title': 'Business Analytics Specialization', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/business-analytics', 'coupon_code': 'COURSERA7', 'is_free': False, 'duration_weeks': 20, 'level': 'student', 'rating': 4.6, 'description': 'Data-driven decision making at Wharton.', 'has_trial': True, 'trial_days': 7, 'step_level': 2},
    {'domain': 'Business & Management', 'title': 'PMP Certification Exam Prep', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/pmp-certification-exam-prep-course-pmbok-6th-edition/', 'coupon_code': 'PMP2024', 'is_free': False, 'duration_weeks': 8, 'level': 'professional', 'rating': 4.7, 'description': 'Prepare for the PMP certification.', 'has_trial': True, 'trial_days': 30, 'step_level': 3},

    # Digital Marketing
    {'domain': 'Digital Marketing', 'title': 'Digital Marketing Fundamentals', 'platform': 'Google Digital Garage', 'url': 'https://learndigital.withgoogle.com/digitalgarage/course/digital-marketing', 'coupon_code': None, 'is_free': True, 'duration_weeks': 40, 'level': 'student', 'rating': 4.8, 'description': 'Master the basics of digital marketing.', 'has_trial': False, 'trial_days': 0, 'step_level': 1},
    {'domain': 'Digital Marketing', 'title': 'Facebook Social Media Marketing', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/facebook-social-media-marketing', 'coupon_code': 'COURSERA7', 'is_free': False, 'duration_weeks': 20, 'level': 'student', 'rating': 4.8, 'description': 'Official Meta social media certification.', 'has_trial': True, 'trial_days': 7, 'step_level': 2},
    {'domain': 'Digital Marketing', 'title': 'Digital Marketing Analytics', 'platform': 'Coursera', 'url': 'https://www.coursera.org/learn/marketing-analytics', 'coupon_code': 'COURSERA7', 'is_free': False, 'duration_weeks': 12, 'level': 'professional', 'rating': 4.7, 'description': 'Advanced analytics and measurement.', 'has_trial': True, 'trial_days': 7, 'step_level': 3},

    # Cybersecurity
    {'domain': 'Cybersecurity', 'title': 'Cybersecurity Essentials', 'platform': 'Cisco', 'url': 'https://www.netacad.com/courses/cybersecurity/cybersecurity-essentials', 'coupon_code': None, 'is_free': True, 'duration_weeks': 10, 'level': 'student', 'rating': 4.6, 'description': 'Fundamentals of network security.', 'has_trial': False, 'trial_days': 0, 'step_level': 1},
    {'domain': 'Cybersecurity', 'title': 'Google Cybersecurity Certificate', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/google-cybersecurity', 'coupon_code': 'COURSERA7', 'is_free': False, 'duration_weeks': 26, 'level': 'student', 'rating': 4.8, 'description': 'Entry-level professional certification.', 'has_trial': True, 'trial_days': 7, 'step_level': 2},
    {'domain': 'Cybersecurity', 'title': 'Ethical Hacking Bootcamp', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/learn-ethical-hacking-from-scratch/', 'coupon_code': 'HACK24', 'is_free': False, 'duration_weeks': 12, 'level': 'professional', 'rating': 4.6, 'description': 'Hands-on penetration testing skills.', 'has_trial': True, 'trial_days': 30, 'step_level': 3},

    # Cloud & DevOps
    {'domain': 'Cloud & DevOps', 'title': 'AWS Cloud Practitioner Essentials', 'platform': 'AWS', 'url': 'https://aws.amazon.com/training/learn-about/cloud-practitioner/', 'coupon_code': None, 'is_free': True, 'duration_weeks': 4, 'level': 'student', 'rating': 4.7, 'description': 'Official AWS beginner training.', 'has_trial': False, 'trial_days': 0, 'step_level': 1},
    {'domain': 'Cloud & DevOps', 'title': 'DevOps and Software Engineering', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/devops-and-software-engineering', 'coupon_code': 'COURSERA7', 'is_free': False, 'duration_weeks': 30, 'level': 'professional', 'rating': 4.6, 'description': 'IBM\'s comprehensive DevOps path.', 'has_trial': True, 'trial_days': 7, 'step_level': 2},
    {'domain': 'Cloud & DevOps', 'title': 'Docker and Kubernetes Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/', 'coupon_code': 'KUBE24', 'is_free': False, 'duration_weeks': 8, 'level': 'professional', 'rating': 4.7, 'description': 'Master container orchestration.', 'has_trial': True, 'trial_days': 30, 'step_level': 3},

    # Product Management
    {'domain': 'Product Management', 'title': 'Product Management Fundamentals', 'platform': 'Coursera', 'url': 'https://www.coursera.org/learn/uva-darden-digital-product-management', 'coupon_code': 'COURSERA7', 'is_free': False, 'duration_weeks': 8, 'level': 'student', 'rating': 4.6, 'description': 'Core skills for aspiring PMs.', 'has_trial': True, 'trial_days': 7, 'step_level': 1},
    {'domain': 'Product Management', 'title': 'Become a Product Manager', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/become-a-product-manager-learn-the-skills-get-a-job/', 'coupon_code': 'PM24', 'is_free': False, 'duration_weeks': 6, 'level': 'student', 'rating': 4.6, 'description': 'A to Z of product management.', 'has_trial': True, 'trial_days': 30, 'step_level': 2},
    {'domain': 'Product Management', 'title': 'Digital Product Management (BCG)', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/digital-product-management', 'coupon_code': 'COURSERA7', 'is_free': False, 'duration_weeks': 16, 'level': 'professional', 'rating': 4.7, 'description': 'Advanced growth strategy and leadership.', 'has_trial': True, 'trial_days': 7, 'step_level': 3},
]

# Skill → Domain scoring weights (remains same)
SKILL_DOMAIN_WEIGHTS = {
    'Web Development': {'Coding': 10, 'JavaScript': 10, 'Problem Solving': 8, 'UI/UX': 6, 'Designing': 5, 'Python': 5, 'Communication': 3, 'Creativity': 4},
    'Data Science & AI': {'Python': 10, 'Mathematics': 10, 'Statistics': 10, 'Machine Learning': 10, 'Analytical Thinking': 9, 'Data Analysis': 9, 'Coding': 6, 'Problem Solving': 7},
    'UX/UI Design': {'Designing': 10, 'UI/UX': 10, 'Creativity': 9, 'Communication': 7, 'Problem Solving': 6, 'Analytical Thinking': 5},
    'Business & Management': {'Communication': 10, 'Management': 10, 'Analytical Thinking': 8, 'Project Management': 9, 'Problem Solving': 7, 'Public Speaking': 8, 'Marketing': 6},
    'Digital Marketing': {'Marketing': 10, 'Communication': 9, 'Creativity': 8, 'Analytical Thinking': 7, 'Public Speaking': 6, 'Problem Solving': 5},
    'Cybersecurity': {'Cybersecurity': 10, 'Networking': 10, 'Coding': 8, 'Analytical Thinking': 8, 'Problem Solving': 7, 'Python': 6, 'Mathematics': 4},
    'Cloud & DevOps': {'Cloud Computing': 10, 'Coding': 8, 'Networking': 8, 'Problem Solving': 7, 'Python': 6, 'Cybersecurity': 5, 'JavaScript': 4},
    'Product Management': {'Communication': 9, 'Analytical Thinking': 9, 'Management': 8, 'Problem Solving': 8, 'Marketing': 6, 'Coding': 5, 'UI/UX': 5, 'Project Management': 7},
}


def seed_database(app):
    with app.app_context():
        # Clean current data to allow fresh seed with new schema
        db.drop_all()
        db.create_all()

        print("Seeding database (v2)...")

        # Seed skills
        skill_map = {}
        for s in SKILLS_DATA:
            skill = Skill(name=s['name'], category=s['category'], icon=s['icon'])
            db.session.add(skill)
            db.session.flush()
            skill_map[s['name']] = skill.id

        # Seed domains
        domain_map = {}
        for d in DOMAINS_DATA:
            domain = Domain(
                name=d['name'],
                icon=d['icon'],
                color=d['color'],
                trending_score=d['trending_score'],
                description=d['description'],
                career_opportunities=d['career_opportunities'],
                required_skills=d['required_skills'],
            )
            db.session.add(domain)
            db.session.flush()
            domain_map[d['name']] = domain.id

        # Seed courses
        for c in COURSES_DATA:
            domain_id = domain_map.get(c['domain'])
            if domain_id:
                course = Course(
                    domain_id=domain_id,
                    title=c['title'],
                    platform=c['platform'],
                    url=c['url'],
                    coupon_code=c['coupon_code'],
                    is_free=c['is_free'],
                    duration_weeks=c['duration_weeks'],
                    level=c['level'],
                    rating=c['rating'],
                    description=c['description'],
                    has_trial=c['has_trial'],
                    trial_days=c['trial_days'],
                    step_level=c['step_level']
                )
                db.session.add(course)

        db.session.commit()
        print(f"Seeded {len(SKILLS_DATA)} skills, {len(DOMAINS_DATA)} domains, {len(COURSES_DATA)} courses.")

