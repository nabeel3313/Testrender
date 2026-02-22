"""
MentorAI — Full Showcase (Frontend-only deployment)
No Firebase, no ML, no authentication.
All pages served with realistic dummy data.
"""
from flask import Flask, render_template, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'showcase-only'


# ──────────────────────────────────────────────
# Fake current_user (looks like a logged-in learner)
# ──────────────────────────────────────────────
class _FakeUser:
    is_authenticated = True
    id = 'demo-user'
    first_name = 'Alex'
    last_name = 'Johnson'
    email = 'alex.johnson@mentorai.com'
    user_type = 'learner'
    phone = '+91 98765 43210'
    bio = 'Passionate learner focused on AI and data science. Always looking to expand my skills with expert guidance.'
    specialization = None
    hourly_rate = None
    experience = None
    timezone = 'IST'
    created_at = datetime(2025, 6, 15)

    def email_split(self):
        return self.email.split('@')[0]


@app.context_processor
def inject_user():
    return dict(current_user=_FakeUser())


# ──────────────────────────────────────────────
# Dummy data helpers
# ──────────────────────────────────────────────
def _trainer(fn, ln, spec='Python & Data Science'):
    class T:
        first_name = fn
        last_name  = ln
        specialization = spec
    return T()


def _session(title, cat, diff, trainer_fn, trainer_ln, days_from_now, duration, price, desc=''):
    class S:
        id = title.lower().replace(' ', '-')[:12]
        category = cat
        difficulty = diff
        scheduled_time = datetime.now() + timedelta(days=days_from_now)
        rating = None
        trainer = _trainer(trainer_fn, trainer_ln)
    S.title = title
    S.duration = duration
    S.price = price
    S.description = desc or f'A comprehensive {cat} session with expert guidance and hands-on exercises.'
    return S()


UPCOMING = [
    _session('Python for Data Science', 'programming', 'beginner', 'Sarah', 'Chen', 2, 90, 49.99,
             'Master Python fundamentals with real-world data science projects and practical exercises.'),
    _session('Machine Learning Basics', 'programming', 'intermediate', 'Marcus', 'Kim', 5, 120, 79.99,
             'Deep dive into ML algorithms, model training, and evaluation using scikit-learn.'),
    _session('UI/UX Fundamentals', 'design', 'beginner', 'Priya', 'Sharma', 8, 60, 39.99,
             'Learn design thinking, wireframing, and user research from an industry professional.'),
]

COMPLETED = [
    _session('JavaScript ES6+', 'programming', 'intermediate', 'David', 'Lee', -5, 90, 49.99),
    _session('React Fundamentals', 'programming', 'intermediate', 'Emma', 'Wilson', -12, 120, 69.99),
    _session('SQL Mastery', 'academic', 'beginner', 'Raj', 'Patel', -20, 60, 29.99),
    _session('Public Speaking', 'business', 'beginner', 'Lisa', 'Moore', -28, 45, 35.99),
    _session('Digital Marketing', 'marketing', 'beginner', 'Tom', 'Garcia', -35, 75, 44.99),
]
for s in COMPLETED:
    s.rating = 5

ALL_SESSIONS = [
    _session('Python for Data Science', 'programming', 'beginner', 'Sarah', 'Chen', 3, 90, 49.99,
             'Master Python fundamentals with real-world data science projects and practical exercises.'),
    _session('Machine Learning Basics', 'programming', 'intermediate', 'Marcus', 'Kim', 5, 120, 79.99,
             'Deep dive into ML algorithms, model training, and evaluation using scikit-learn.'),
    _session('UI/UX Fundamentals', 'design', 'beginner', 'Priya', 'Sharma', 7, 60, 39.99,
             'Learn design thinking, wireframing, and user research from an industry professional.'),
    _session('Digital Marketing Strategy', 'marketing', 'intermediate', 'Tom', 'Garcia', 9, 90, 54.99,
             'Build and execute data-driven marketing campaigns across multiple channels.'),
    _session('Advanced SQL & Databases', 'academic', 'advanced', 'Raj', 'Patel', 11, 120, 74.99,
             'Deep dive into advanced SQL queries, indexing strategies, and database optimization.'),
    _session('React & Next.js Bootcamp', 'programming', 'intermediate', 'Emma', 'Wilson', 14, 180, 89.99,
             'Full-stack React development with Next.js, covering SSR, SSG, and API routes.'),
]

REPORTS = [
    {
        'title': 'JavaScript ES6+ Masterclass',
        'status': 'completed',
        'scheduled_time': datetime.now() - timedelta(days=5),
        'duration': 90,
        'category': 'Programming',
        'learner': {'first_name': 'Alex', 'last_name': 'Johnson'},
        'detection_count': 142,
    },
    {
        'title': 'React Fundamentals Workshop',
        'status': 'completed',
        'scheduled_time': datetime.now() - timedelta(days=12),
        'duration': 120,
        'category': 'Programming',
        'learner': {'first_name': 'Alex', 'last_name': 'Johnson'},
        'detection_count': 87,
    },
    {
        'title': 'SQL Mastery Bootcamp',
        'status': 'completed',
        'scheduled_time': datetime.now() - timedelta(days=20),
        'duration': 60,
        'category': 'Academic',
        'learner': {'first_name': 'Alex', 'last_name': 'Johnson'},
        'detection_count': 63,
    },
]


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('showcase_login.html')


@app.route('/register')
def register():
    return render_template('showcase_register.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',
                           upcoming_sessions=UPCOMING,
                           completed_sessions=COMPLETED,
                           total_hours=68,
                           trainers_count=12)


@app.route('/browse')
def browse_sessions():
    return render_template('browse_sessions.html', sessions=ALL_SESSIONS)


@app.route('/profile')
def profile():
    return render_template('showcase_profile.html')


@app.route('/change-password')
def change_password():
    return redirect(url_for('profile'))


@app.route('/create-session')
def create_session():
    return render_template('showcase_create_session.html')


@app.route('/session-reports')
def session_reports():
    class Stats:
        total_sessions = len(UPCOMING) + len(COMPLETED)
        upcoming_sessions = len(UPCOMING)
        total_earnings = '$1,247.50'
        average_rating = 4.8
    return render_template('session_reports.html', sessions=REPORTS)


@app.route('/trainer-dashboard')
def trainer_dashboard():
    class Stats:
        total_sessions = len(UPCOMING) + len(COMPLETED)
        upcoming_sessions = len(UPCOMING)
        total_earnings = '$1,247.50'
        average_rating = 4.8

    _review_date = datetime.now() - timedelta(days=3)

    class Review:
        rating = 5
        comment = 'Absolutely phenomenal session! Clear explanations and great patience.'
        created_at = datetime.now() - timedelta(days=3)
        class learner:
            first_name = 'Alex'

    return render_template('trainer_dashboard.html',
                           upcoming_sessions=UPCOMING,
                           session_requests=[],
                           recent_reviews=[Review()],
                           stats=Stats())


@app.route('/trainer-sessions')
def trainer_sessions():
    class Stats:
        total_sessions = len(UPCOMING) + len(COMPLETED)
        upcoming_sessions = len(UPCOMING)
        total_earnings = '$1,247.50'
        average_rating = 4.8
    return render_template('trainer_dashboard.html',
                           upcoming_sessions=UPCOMING,
                           session_requests=[],
                           recent_reviews=[],
                           stats=Stats())


# Named redirect endpoints so url_for() works in templates
@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.route('/session/<path:session_id>')
def session_room(session_id):
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False)
