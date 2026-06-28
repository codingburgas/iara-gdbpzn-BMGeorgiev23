from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    
    existing_user = User.query.filter_by(email='admin@example.com').first()
    
    if existing_user:
        print('User already exists.')
    else:
        hashed_password = generate_password_hash('admin123')
        user = User(
            email='admin@example.com',
            name='Admin',
            password=hashed_password,
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        print('Test user created successfully.')
        print('Email: admin@example.com')
        print('Password: admin123')