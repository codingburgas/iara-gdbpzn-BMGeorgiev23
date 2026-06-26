# create_user.py
from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    
    # Check if user already exists
    existing_user = User.query.filter_by(email='admin@example.com').first()
    
    if existing_user:
        print('User already exists!')
    else:
        # Create test user
        user = User(
            email='admin@example.com',
            name='Admin',
            password='admin123'  # In production, hash this!
        )
        db.session.add(user)
        db.session.commit()
        print('✅ Test user created successfully!')
        print('Email: admin@example.com')
        print('Password: admin123')