#!/usr/bin/env python3
"""
Karachuonyo Website Backend Server
Handles contact forms, newsletter subscriptions, and other server-side functionality
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from flask_mail import Mail, Message
from datetime import datetime
import sqlite3
import os
import re
import logging
from werkzeug.security import generate_password_hash

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'karachuonyo-dev-key-2024')

# CORS configuration
CORS(app, origins=['http://localhost:8000', 'http://127.0.0.1:8000', 'https://karachuonyofirst.com'])

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'contact@karachuonyofirst.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-app-password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'contact@karachuonyofirst.com')

mail = Mail(app)

# Database configuration
DATABASE = 'karachuonyo.db'

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Contact submissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            user_agent TEXT,
            status TEXT DEFAULT 'new'
        )
    ''')
    
    # Newsletter subscriptions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS newsletter_subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            status TEXT DEFAULT 'active',
            confirmation_token TEXT
        )
    ''')
    
    # Admin users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            role TEXT DEFAULT 'admin'
        )
    ''')
    
    # Donations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_name TEXT NOT NULL,
            donor_email TEXT,
            phone TEXT,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            transaction_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            ip_address TEXT,
            user_agent TEXT
        )
    ''')
    
    # News articles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            excerpt TEXT,
            content TEXT NOT NULL,
            featured_image TEXT,
            author TEXT DEFAULT 'Karachuonyo First Team',
            status TEXT DEFAULT 'draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            published_at TIMESTAMP,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            shares INTEGER DEFAULT 0,
            tags TEXT
        )
    ''')
    
    # Comments table for blog/news articles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            comment TEXT NOT NULL,
            approved INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            description TEXT,
            location TEXT,
            event_date TIMESTAMP NOT NULL,
            end_date TIMESTAMP,
            featured_image TEXT,
            status TEXT DEFAULT 'upcoming',
            max_attendees INTEGER,
            registration_required BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Event registrations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            status TEXT DEFAULT 'confirmed',
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (event_id) REFERENCES events (id)
        )
    ''')
    
    # Agenda items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agenda_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'planned',
            target_date TIMESTAMP,
            progress_percentage INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Volunteer registrations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS volunteer_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            location TEXT,
            skills TEXT,
            availability TEXT,
            experience TEXT,
            motivation TEXT,
            status TEXT DEFAULT 'pending',
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            user_agent TEXT
        )
    ''')
    
    # Add migration for likes and shares columns if they don't exist
    try:
        cursor.execute("ALTER TABLE news_articles ADD COLUMN likes INTEGER DEFAULT 0")
        logger.info("Added likes column to news_articles table")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute("ALTER TABLE news_articles ADD COLUMN shares INTEGER DEFAULT 0")
        logger.info("Added shares column to news_articles table")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate Kenyan phone number format"""
    if not phone:
        return True  # Phone is optional
    
    # Remove spaces and special characters
    clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check for valid Kenyan phone formats
    patterns = [
        r'^\+254[17]\d{8}$',  # +254 format
        r'^254[17]\d{8}$',   # 254 format
        r'^0[17]\d{8}$',     # 07/01 format
        r'^[17]\d{8}$'       # 7/1 format
    ]
    
    return any(re.match(pattern, clean_phone) for pattern in patterns)

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Karachuonyo Backend',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/contact', methods=['POST'])
def handle_contact_form():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field, '').strip():
                return jsonify({
                    'success': False,
                    'error': f'{field.title()} is required'
                }), 400
        
        # Validate email format
        if not validate_email(data['email']):
            return jsonify({
                'success': False,
                'error': 'Please enter a valid email address'
            }), 400
        
        # Validate phone if provided
        if data.get('phone') and not validate_phone(data['phone']):
            return jsonify({
                'success': False,
                'error': 'Please enter a valid Kenyan phone number'
            }), 400
        
        # Get client information
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        user_agent = request.headers.get('User-Agent', '')
        
        # Save to database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO contact_submissions 
            (name, email, phone, subject, message, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'].strip(),
            data['email'].strip().lower(),
            data.get('phone', '').strip(),
            data['subject'].strip(),
            data['message'].strip(),
            ip_address,
            user_agent
        ))
        
        submission_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Send email notification
        try:
            # Email to admin
            admin_msg = Message(
                subject=f"New Contact Form Submission: {data['subject']}",
                recipients=['contact@karachuonyofirst.com'],
                html=render_template_string('''
                <h2>New Contact Form Submission</h2>
                <p><strong>Submission ID:</strong> {{ submission_id }}</p>
                <p><strong>Name:</strong> {{ name }}</p>
                <p><strong>Email:</strong> {{ email }}</p>
                <p><strong>Phone:</strong> {{ phone or 'Not provided' }}</p>
                <p><strong>Subject:</strong> {{ subject }}</p>
                <p><strong>Message:</strong></p>
                <div style="background: #f5f5f5; padding: 15px; border-radius: 5px;">
                    {{ message | replace('\n', '<br>') | safe }}
                </div>
                <p><strong>Submitted:</strong> {{ timestamp }}</p>
                <p><strong>IP Address:</strong> {{ ip_address }}</p>
                ''', 
                submission_id=submission_id,
                name=data['name'],
                email=data['email'],
                phone=data.get('phone'),
                subject=data['subject'],
                message=data['message'],
                timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                ip_address=ip_address
                )
            )
            
            # Auto-reply to user
            user_msg = Message(
                subject="Thank you for contacting Karachuonyo First",
                recipients=[data['email']],
                html=render_template_string('''
                <h2>Thank you for your message!</h2>
                <p>Dear {{ name }},</p>
                <p>Thank you for reaching out to the Karachuonyo First campaign. We have received your message and will respond within 24-48 hours.</p>
                
                <h3>Your Message Details:</h3>
                <p><strong>Subject:</strong> {{ subject }}</p>
                <p><strong>Message:</strong></p>
                <div style="background: #f5f5f5; padding: 15px; border-radius: 5px;">
                    {{ message | replace('\n', '<br>') | safe }}
                </div>
                
                <p>Best regards,<br>
                <strong>Karachuonyo First Campaign Team</strong></p>
                
                <hr>
                <p style="font-size: 12px; color: #666;">
                This is an automated response. Please do not reply to this email.
                For urgent matters, call: +254 700 686 943
                </p>
                ''',
                name=data['name'],
                subject=data['subject'],
                message=data['message']
                )
            )
            
            mail.send(admin_msg)
            mail.send(user_msg)
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            # Don't fail the request if email fails
        
        logger.info(f"Contact form submitted successfully: ID {submission_id}")
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your message! We will get back to you soon.',
            'submission_id': submission_id
        })
        
    except Exception as e:
        logger.error(f"Contact form error: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your request. Please try again.'
        }), 500

@app.route('/api/newsletter/subscribe', methods=['POST'])
def handle_newsletter_subscription():
    """Handle newsletter subscription"""
    try:
        data = request.get_json()
        
        # Validate email
        email = data.get('email', '').strip().lower()
        if not email or not validate_email(email):
            return jsonify({
                'success': False,
                'error': 'Please enter a valid email address'
            }), 400
        
        name = data.get('name', '').strip()
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        
        # Check if already subscribed
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, status FROM newsletter_subscriptions WHERE email = ?', (email,))
        existing = cursor.fetchone()
        
        if existing:
            if existing[1] == 'active':
                return jsonify({
                    'success': False,
                    'error': 'This email is already subscribed to our newsletter'
                }), 400
            else:
                # Reactivate subscription
                cursor.execute(
                    'UPDATE newsletter_subscriptions SET status = ?, subscribed_at = ? WHERE email = ?',
                    ('active', datetime.now(), email)
                )
        else:
            # New subscription
            cursor.execute('''
                INSERT INTO newsletter_subscriptions (email, name, ip_address)
                VALUES (?, ?, ?)
            ''', (email, name, ip_address))
        
        conn.commit()
        conn.close()
        
        # Send welcome email
        try:
            welcome_msg = Message(
                subject="Welcome to Karachuonyo First Newsletter!",
                recipients=[email],
                html=render_template_string('''
                <h2>Welcome to Karachuonyo First!</h2>
                <p>Dear {{ name or 'Supporter' }},</p>
                <p>Thank you for subscribing to our newsletter! You'll now receive updates about:</p>
                <ul>
                    <li>Campaign events and rallies</li>
                    <li>Policy announcements</li>
                    <li>Community development projects</li>
                    <li>Important political updates</li>
                </ul>
                
                <p>Together, we're building a better future for Karachuonyo!</p>
                
                <p>Best regards,<br>
                <strong>Karachuonyo First Campaign Team</strong></p>
                
                <hr>
                <p style="font-size: 12px; color: #666;">
                You can unsubscribe at any time by replying to this email with "UNSUBSCRIBE".
                </p>
                ''',
                name=name
                )
            )
            
            mail.send(welcome_msg)
            
        except Exception as e:
            logger.error(f"Failed to send welcome email: {e}")
        
        logger.info(f"Newsletter subscription: {email}")
        
        return jsonify({
            'success': True,
            'message': 'Successfully subscribed to our newsletter!'
        })
        
    except Exception as e:
        logger.error(f"Newsletter subscription error: {e}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your subscription. Please try again.'
        }), 500

@app.route('/api/admin/contacts', methods=['GET'])
def get_contact_submissions():
    """Get all contact submissions (admin endpoint)"""
    # TODO: Add authentication
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, email, phone, subject, message, submitted_at, status
            FROM contact_submissions
            ORDER BY submitted_at DESC
        ''')
        
        submissions = []
        for row in cursor.fetchall():
            submissions.append({
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'phone': row[3],
                'subject': row[4],
                'message': row[5],
                'submitted_at': row[6],
                'status': row[7]
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'submissions': submissions
        })
        
    except Exception as e:
        logger.error(f"Error fetching submissions: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch submissions'
        }), 500

@app.route('/api/admin/donations', methods=['GET'])
def admin_donations():
    try:
        conn = sqlite3.connect('karachuonyo.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, donor_name, donor_email, phone, amount, payment_method, 
                   status, transaction_id, created_at, completed_at
            FROM donations 
            ORDER BY created_at DESC
        ''')
        
        donations = []
        for row in cursor.fetchall():
            donations.append({
                'id': row[0],
                'donor_name': row[1],
                'donor_email': row[2],
                'phone': row[3],
                'amount': row[4],
                'payment_method': row[5],
                'status': row[6],
                'transaction_id': row[7],
                'created_at': row[8],
                'completed_at': row[9]
            })
        
        conn.close()
        return jsonify({'donations': donations})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin authentication (simple token-based)
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    import time
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Simple hardcoded admin credentials (in production, use proper authentication)
    if username == 'admin' and password == 'karachuonyo2024':
        # Generate a simple token (in production, use JWT)
        token = 'admin_token_' + str(int(time.time()))
        return jsonify({'token': token, 'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# News Articles Management
@app.route('/api/admin/news', methods=['GET', 'POST'])
def admin_news():
    if request.method == 'GET':
        try:
            conn = sqlite3.connect('karachuonyo.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, slug, excerpt, author, status, created_at, published_at, views
                FROM news_articles 
                ORDER BY created_at DESC
            ''')
            
            articles = []
            for row in cursor.fetchall():
                articles.append({
                    'id': row[0],
                    'title': row[1],
                    'slug': row[2],
                    'excerpt': row[3],
                    'author': row[4],
                    'status': row[5],
                    'created_at': row[6],
                    'published_at': row[7],
                    'views': row[8]
                })
            
            conn.close()
            return jsonify({'articles': articles})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            title = data.get('title')
            content = data.get('content')
            excerpt = data.get('excerpt', '')
            slug = data.get('slug', title.lower().replace(' ', '-').replace(',', '').replace('.', ''))
            author = data.get('author', 'Karachuonyo First Team')
            status = data.get('status', 'draft')
            tags = data.get('tags', '')
            
            conn = sqlite3.connect('karachuonyo.db')
            cursor = conn.cursor()
            
            published_at = datetime.now().isoformat() if status == 'published' else None
            
            cursor.execute('''
                INSERT INTO news_articles (title, slug, excerpt, content, author, status, published_at, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, slug, excerpt, content, author, status, published_at, tags))
            
            conn.commit()
            article_id = cursor.lastrowid
            conn.close()
            
            return jsonify({'message': 'Article created successfully', 'id': article_id})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/admin/news/<int:article_id>', methods=['GET', 'PUT', 'DELETE'])
def admin_news_item(article_id):
    if request.method == 'GET':
        try:
            conn = sqlite3.connect('karachuonyo.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, slug, excerpt, content, featured_image, author, status, 
                       created_at, updated_at, published_at, views, tags
                FROM news_articles WHERE id = ?
            ''', (article_id,))
            
            row = cursor.fetchone()
            if row:
                article = {
                    'id': row[0],
                    'title': row[1],
                    'slug': row[2],
                    'excerpt': row[3],
                    'content': row[4],
                    'featured_image': row[5],
                    'author': row[6],
                    'status': row[7],
                    'created_at': row[8],
                    'updated_at': row[9],
                    'published_at': row[10],
                    'views': row[11],
                    'tags': row[12]
                }
                conn.close()
                return jsonify(article)
            else:
                conn.close()
                return jsonify({'error': 'Article not found'}), 404
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            conn = sqlite3.connect('karachuonyo.db')
            cursor = conn.cursor()
            
            # Check if status changed to published
            published_at = None
            if data.get('status') == 'published':
                cursor.execute('SELECT published_at FROM news_articles WHERE id = ?', (article_id,))
                current_published = cursor.fetchone()[0]
                if not current_published:
                    published_at = datetime.now().isoformat()
            
            cursor.execute('''
                UPDATE news_articles 
                SET title = ?, slug = ?, excerpt = ?, content = ?, author = ?, 
                    status = ?, tags = ?, updated_at = CURRENT_TIMESTAMP
                    {} 
                WHERE id = ?
            '''.format(', published_at = ?' if published_at else ''), 
            (data.get('title'), data.get('slug'), data.get('excerpt'), 
             data.get('content'), data.get('author'), data.get('status'), 
             data.get('tags')) + ((published_at, article_id) if published_at else (article_id,)))
            
            conn.commit()
            conn.close()
            
            return jsonify({'message': 'Article updated successfully'})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            conn = sqlite3.connect('karachuonyo.db')
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM news_articles WHERE id = ?', (article_id,))
            conn.commit()
            conn.close()
            
            return jsonify({'message': 'Article deleted successfully'})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Events Management
@app.route('/api/admin/events', methods=['GET', 'POST'])
def admin_events():
    if request.method == 'GET':
        try:
            conn = sqlite3.connect('karachuonyo.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, slug, description, location, event_date, end_date, 
                       status, max_attendees, registration_required, created_at
                FROM events 
                ORDER BY event_date DESC
            ''')
            
            events = []
            for row in cursor.fetchall():
                events.append({
                    'id': row[0],
                    'title': row[1],
                    'slug': row[2],
                    'description': row[3],
                    'location': row[4],
                    'event_date': row[5],
                    'end_date': row[6],
                    'status': row[7],
                    'max_attendees': row[8],
                    'registration_required': bool(row[9]),
                    'created_at': row[10]
                })
            
            conn.close()
            return jsonify({'events': events})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            title = data.get('title')
            description = data.get('description', '')
            location = data.get('location', '')
            event_date = data.get('event_date')
            end_date = data.get('end_date')
            slug = data.get('slug', title.lower().replace(' ', '-').replace(',', '').replace('.', ''))
            status = data.get('status', 'upcoming')
            max_attendees = data.get('max_attendees')
            registration_required = data.get('registration_required', False)
            
            conn = sqlite3.connect('karachuonyo.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO events (title, slug, description, location, event_date, end_date, 
                                  status, max_attendees, registration_required)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, slug, description, location, event_date, end_date, 
                  status, max_attendees, registration_required))
            
            conn.commit()
            event_id = cursor.lastrowid
            conn.close()
            
            return jsonify({'message': 'Event created successfully', 'id': event_id})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/admin/events/<int:event_id>', methods=['GET', 'PUT', 'DELETE'])
def admin_event_item(event_id):
    if request.method == 'GET':
        try:
            conn = sqlite3.connect('karachuonyo.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, slug, description, location, event_date, end_date, 
                       featured_image, status, max_attendees, registration_required, 
                       created_at, updated_at
                FROM events WHERE id = ?
            ''', (event_id,))
            
            row = cursor.fetchone()
            if row:
                event = {
                    'id': row[0],
                    'title': row[1],
                    'slug': row[2],
                    'description': row[3],
                    'location': row[4],
                    'event_date': row[5],
                    'end_date': row[6],
                    'featured_image': row[7],
                    'status': row[8],
                    'max_attendees': row[9],
                    'registration_required': bool(row[10]),
                    'created_at': row[11],
                    'updated_at': row[12]
                }
                conn.close()
                return jsonify(event)
            else:
                conn.close()
                return jsonify({'error': 'Event not found'}), 404
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            conn = sqlite3.connect('karachuonyo.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE events 
                SET title = ?, slug = ?, description = ?, location = ?, event_date = ?, 
                    end_date = ?, status = ?, max_attendees = ?, registration_required = ?, 
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (data.get('title'), data.get('slug'), data.get('description'), 
                  data.get('location'), data.get('event_date'), data.get('end_date'), 
                  data.get('status'), data.get('max_attendees'), 
                  data.get('registration_required', False), event_id))
            
            conn.commit()
            conn.close()
            
            return jsonify({'message': 'Event updated successfully'})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            conn = sqlite3.connect('karachuonyo.db')
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
            conn.commit()
            conn.close()
            
            return jsonify({'message': 'Event deleted successfully'})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Agenda Items Management
@app.route('/api/admin/agenda', methods=['GET', 'POST'])
def admin_agenda():
    if request.method == 'GET':
        try:
            conn = sqlite3.connect('karachuonyo.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, description, category, priority, status, 
                       target_date, progress_percentage, created_at, updated_at
                FROM agenda_items 
                ORDER BY priority DESC, created_at DESC
            ''')
            
            items = []
            for row in cursor.fetchall():
                items.append({
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'category': row[3],
                    'priority': row[4],
                    'status': row[5],
                    'target_date': row[6],
                    'progress_percentage': row[7],
                    'created_at': row[8],
                    'updated_at': row[9]
                })
            
            conn.close()
            return jsonify({'agenda_items': items})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            title = data.get('title')
            description = data.get('description', '')
            category = data.get('category', '')
            priority = data.get('priority', 'medium')
            status = data.get('status', 'planned')
            target_date = data.get('target_date')
            progress_percentage = data.get('progress_percentage', 0)
            
            conn = sqlite3.connect('karachuonyo.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO agenda_items (title, description, category, priority, status, 
                                        target_date, progress_percentage)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (title, description, category, priority, status, target_date, progress_percentage))
            
            conn.commit()
            item_id = cursor.lastrowid
            conn.close()
            
            return jsonify({'message': 'Agenda item created successfully', 'id': item_id})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/admin/agenda/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def admin_agenda_item(item_id):
    if request.method == 'PUT':
        try:
            data = request.get_json()
            conn = sqlite3.connect('karachuonyo.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE agenda_items 
                SET title = ?, description = ?, category = ?, priority = ?, status = ?, 
                    target_date = ?, progress_percentage = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (data.get('title'), data.get('description'), data.get('category'), 
                  data.get('priority'), data.get('status'), data.get('target_date'), 
                  data.get('progress_percentage'), item_id))
            
            conn.commit()
            conn.close()
            
            return jsonify({'message': 'Agenda item updated successfully'})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            conn = sqlite3.connect('karachuonyo.db')
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM agenda_items WHERE id = ?', (item_id,))
            conn.commit()
            conn.close()
            
            return jsonify({'message': 'Agenda item deleted successfully'})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Blog/News articles data
ARTICLES = {
    'ward-cleanup-drive': {
        'id': 'ward-cleanup-drive',
        'title': 'Ward Clean-Up Drive Launched',
        'date': 'August 24, 2025',
        'category': 'Community',
        'author': 'Karachuonyo First Team',
        'excerpt': 'We flagged off a community clean-up across trading centers with youth groups and churches.',
        'content': '''<p>In a remarkable display of community spirit, the Karachuonyo First campaign launched a comprehensive ward clean-up drive across all major trading centers in our constituency. This initiative, which began early Saturday morning, brought together youth groups, church organizations, and community volunteers in an unprecedented show of unity.</p>
        
        <h2>Community Mobilization</h2>
        <p>The clean-up drive saw participation from over 200 volunteers, including members from various youth groups such as the Karachuonyo Youth Network, local church congregations, and community-based organizations. The enthusiasm and dedication shown by our young people was particularly inspiring.</p>
        
        <blockquote>"This is what true leadership looks like - bringing people together for the common good of our community," said Mary Otieno, a local church leader who participated in the drive.</blockquote>
        
        <h2>Areas Covered</h2>
        <p>The clean-up exercise covered major trading centers including:</p>
        <ul>
            <li>Kendu Bay Market and surrounding areas</li>
            <li>Homa Hills Trading Center</li>
            <li>Kadel Market Square</li>
            <li>Nyadhi Shopping Center</li>
        </ul>
        
        <h2>Environmental Impact</h2>
        <p>The initiative resulted in the collection of over 50 bags of waste, clearing of drainage systems, and general beautification of our trading centers. This effort not only improved the aesthetic appeal of our markets but also contributed to better health and sanitation conditions for traders and customers alike.</p>
        
        <h2>Moving Forward</h2>
        <p>This clean-up drive is just the beginning of our comprehensive environmental conservation program. We plan to make this a monthly initiative, with each session focusing on different areas within our ward. Additionally, we are working on establishing permanent waste management systems in all major trading centers.</p>
        
        <p>The success of this initiative demonstrates what we can achieve when we work together as a community. It reflects our commitment to not just talking about change, but actively implementing solutions that improve the lives of our people.</p>''',
        'read_time': '5 min read',
        'tags': ['community', 'environment', 'youth'],
        'featured_image': '/images/cleanup-drive.jpg',
        'published': True,
        'created_at': '2025-08-24T08:00:00Z',
        'updated_at': '2025-08-24T08:00:00Z'
    },
    'bursary-vetting-guidelines': {
        'id': 'bursary-vetting-guidelines',
        'title': 'Bursary Vetting Guidelines',
        'date': 'August 18, 2025',
        'category': 'Education',
        'author': 'Karachuonyo First Team',
        'excerpt': 'Transparent criteria and timelines to ensure fairness and inclusion.',
        'content': '''<p>Education remains the cornerstone of our development agenda, and we are committed to ensuring that every child in Karachuonyo has access to quality education regardless of their family's financial situation. Today, we are proud to announce the comprehensive bursary vetting guidelines that will govern the distribution of educational support in our constituency.</p>
        
        <h2>Transparency First</h2>
        <p>Our bursary program is built on the principles of transparency, fairness, and inclusivity. We believe that every family deserves to know exactly how bursaries are allocated and what criteria are used in the selection process.</p>
        
        <h2>Eligibility Criteria</h2>
        <p>The following criteria will be used to assess bursary applications:</p>
        <ul>
            <li><strong>Financial Need:</strong> Family income assessment and economic circumstances</li>
            <li><strong>Academic Performance:</strong> Student's academic record and potential</li>
            <li><strong>Community Involvement:</strong> Family's participation in community activities</li>
            <li><strong>Special Circumstances:</strong> Orphaned students, students with disabilities, and other vulnerable cases</li>
        </ul>
        
        <h2>Application Process</h2>
        <p>The application process has been streamlined to make it accessible to all families:</p>
        <ol>
            <li>Application forms available at all chief's offices and online</li>
            <li>Required documents clearly listed and easily obtainable</li>
            <li>Community-based vetting committees in each location</li>
            <li>Appeals process for disputed decisions</li>
        </ol>
        
        <blockquote>"Education is not a privilege for the few, but a right for all. These guidelines ensure that deserving students get the support they need to achieve their dreams," emphasized our Education Coordinator.</blockquote>
        
        <h2>Timeline and Deadlines</h2>
        <p>Applications will be accepted twice a year:</p>
        <ul>
            <li><strong>First Term:</strong> Applications due by December 15th</li>
            <li><strong>Second Term:</strong> Applications due by April 15th</li>
        </ul>
        
        <h2>Accountability Measures</h2>
        <p>To ensure accountability and proper use of funds:</p>
        <ul>
            <li>Regular monitoring of beneficiaries' academic progress</li>
            <li>Direct payment to educational institutions</li>
            <li>Annual public reporting on bursary distribution</li>
            <li>Community feedback mechanisms</li>
        </ul>
        
        <p>We encourage all families with school-going children to familiarize themselves with these guidelines and to apply when the application windows open. Together, we can ensure that no child in Karachuonyo is denied education due to financial constraints.</p>''',
        'read_time': '4 min read',
        'tags': ['education', 'bursary', 'transparency'],
        'featured_image': '/images/education-bursary.jpg',
        'published': True,
        'created_at': '2025-08-18T10:00:00Z',
        'updated_at': '2025-08-18T10:00:00Z'
    },
    'water-nyadhi-project': {
        'id': 'water-nyadhi-project',
        'title': 'Water for Nyadhi – Project Update',
        'date': 'August 2, 2025',
        'category': 'Development',
        'author': 'Karachuonyo First Team',
        'excerpt': 'Borehole survey completed; rig mobilization scheduled pending NEMA greenlight.',
        'content': '''<p>Access to clean, safe water is a fundamental human right, and we are making significant progress in ensuring that the people of Nyadhi have reliable access to this precious resource. Today, we provide a comprehensive update on the Water for Nyadhi project, which represents a major milestone in our infrastructure development agenda.</p>
        
        <h2>Project Background</h2>
        <p>The Nyadhi community has faced water scarcity challenges for decades, with residents often walking long distances to access clean water. This project aims to drill a high-capacity borehole that will serve over 500 households and several institutions including schools and health facilities.</p>
        
        <h2>Survey Completion</h2>
        <p>We are pleased to report that the comprehensive borehole survey has been successfully completed by certified hydrogeologists. The survey results are highly encouraging:</p>
        <ul>
            <li><strong>Water Table Depth:</strong> 45 meters - well within drilling capacity</li>
            <li><strong>Estimated Yield:</strong> 15,000 liters per hour - sufficient for community needs</li>
            <li><strong>Water Quality:</strong> Preliminary tests indicate excellent quality</li>
            <li><strong>Sustainability:</strong> Aquifer shows signs of good recharge potential</li>
        </ul>
        
        <h2>Environmental Compliance</h2>
        <p>As responsible stewards of our environment, we have submitted all required documentation to the National Environment Management Authority (NEMA) for environmental impact assessment. This includes:</p>
        <ul>
            <li>Environmental Impact Assessment (EIA) report</li>
            <li>Community consultation reports</li>
            <li>Hydrogeological survey findings</li>
            <li>Waste management and site restoration plans</li>
        </ul>
        
        <blockquote>"We are committed to ensuring that this project not only provides water but also protects our environment for future generations," stated our Project Coordinator.</blockquote>
        
        <h2>Next Steps</h2>
        <p>Upon receiving NEMA clearance, which we expect within the next two weeks, we will immediately proceed with:</p>
        <ol>
            <li>Drilling rig mobilization to site</li>
            <li>Commencement of drilling operations</li>
            <li>Installation of pumping equipment</li>
            <li>Construction of distribution network</li>
            <li>Community training on maintenance</li>
        </ol>
        
        <h2>Community Involvement</h2>
        <p>This project has been a true community effort from the beginning. Local residents have contributed through:</p>
        <ul>
            <li>Site identification and access provision</li>
            <li>Local labor and materials where possible</li>
            <li>Formation of a water management committee</li>
            <li>Commitment to ongoing maintenance and sustainability</li>
        </ul>
        
        <h2>Expected Timeline</h2>
        <p>Based on current progress and pending approvals:</p>
        <ul>
            <li><strong>NEMA Approval:</strong> Expected by August 15, 2025</li>
            <li><strong>Drilling Commencement:</strong> August 20, 2025</li>
            <li><strong>Project Completion:</strong> September 30, 2025</li>
            <li><strong>Community Handover:</strong> October 5, 2025</li>
        </ul>
        
        <p>The Water for Nyadhi project exemplifies our commitment to addressing the real, everyday challenges facing our people. Clean water access will not only improve health outcomes but also free up time for productive activities, particularly for women and children who currently bear the burden of water collection.</p>
        
        <p>We will continue to provide regular updates on this project and welcome community feedback and involvement at every stage.</p>''',
        'read_time': '6 min read',
        'tags': ['development', 'water', 'infrastructure'],
        'featured_image': '/images/water-project.jpg',
        'published': True,
        'created_at': '2025-08-02T09:00:00Z',
        'updated_at': '2025-08-02T09:00:00Z'
    }
}

# Public API endpoints for blog/news
@app.route('/api/news', methods=['GET'])
def get_news_articles():
    """Get published news articles"""
    try:
        # Get query parameters
        category = request.args.get('category')
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
        
        # Filter published articles
        published_articles = [article for article in ARTICLES.values() if article.get('published', False)]
        
        # Filter by category if specified
        if category:
            published_articles = [article for article in published_articles if article.get('category', '').lower() == category.lower()]
        
        # Sort by date (newest first)
        published_articles.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        # Apply pagination
        total = len(published_articles)
        articles = published_articles[offset:offset + limit]
        
        # Remove full content from list view
        article_summaries = []
        for article in articles:
            summary = article.copy()
            summary.pop('content', None)  # Remove full content for list view
            article_summaries.append(summary)
        
        return jsonify({
            'success': True,
            'articles': article_summaries,
            'total': total,
            'limit': limit,
            'offset': offset
        })
        
    except Exception as e:
        logger.error(f"Error fetching news articles: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch articles'
        }), 500

@app.route('/api/news/<article_id>', methods=['GET'])
def get_news_article(article_id):
    """Get a specific news article by ID and increment view count"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # First try to get from database
        cursor.execute('''
            SELECT id, title, slug, excerpt, content, featured_image, author, 
                   created_at, updated_at, published_at, views, likes, shares, tags
            FROM news_articles 
            WHERE (slug = ? OR id = ?) AND status = 'published'
        ''', (article_id, article_id))
        
        row = cursor.fetchone()
        
        if row:
            # Increment view count
            cursor.execute('UPDATE news_articles SET views = views + 1 WHERE slug = ? OR id = ?', 
                         (article_id, article_id))
            conn.commit()
            
            article = {
                'id': row[0],
                'title': row[1],
                'slug': row[2],
                'excerpt': row[3],
                'content': row[4],
                'featured_image': row[5],
                'author': row[6],
                'created_at': row[7],
                'updated_at': row[8],
                'published_at': row[9],
                'views': row[10] + 1,  # Return incremented count
                'likes': row[11],
                'shares': row[12],
                'tags': row[13].split(',') if row[13] else []
            }
        else:
            # Fallback to hardcoded articles
            article = ARTICLES.get(article_id)
            if not article or not article.get('published', False):
                conn.close()
                return jsonify({
                    'success': False,
                    'error': 'Article not found'
                }), 404
        
        conn.close()
        
        return jsonify({
            'success': True,
            'article': article
        })
        
    except Exception as e:
        logger.error(f"Error fetching article {article_id}: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch article'
        }), 500

@app.route('/api/news/categories', methods=['GET'])
def get_news_categories():
    """Get all available news categories"""
    try:
        categories = set()
        for article in ARTICLES.values():
            if article.get('published', False) and article.get('category'):
                categories.add(article['category'])
        
        return jsonify({
            'success': True,
            'categories': sorted(list(categories))
        })
        
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch categories'
        }), 500

@app.route('/api/news/<article_id>/like', methods=['POST'])
def like_article(article_id):
    """Like a news article"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Check if article exists
        cursor.execute('SELECT id FROM news_articles WHERE (slug = ? OR id = ?) AND status = "published"', 
                      (article_id, article_id))
        
        if not cursor.fetchone():
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Article not found'
            }), 404
        
        # Increment like count
        cursor.execute('UPDATE news_articles SET likes = likes + 1 WHERE slug = ? OR id = ?', 
                      (article_id, article_id))
        
        # Get updated like count
        cursor.execute('SELECT likes FROM news_articles WHERE slug = ? OR id = ?', 
                      (article_id, article_id))
        
        new_likes = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'likes': new_likes,
            'message': 'Article liked successfully'
        })
        
    except Exception as e:
        logger.error(f"Error liking article {article_id}: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to like article'
        }), 500

@app.route('/api/news/<article_id>/share', methods=['POST'])
def share_article(article_id):
    """Increment share count for a news article"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Check if article exists
        cursor.execute('SELECT id FROM news_articles WHERE (slug = ? OR id = ?) AND status = "published"', 
                      (article_id, article_id))
        
        if not cursor.fetchone():
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Article not found'
            }), 404
        
        # Increment share count
        cursor.execute('UPDATE news_articles SET shares = shares + 1 WHERE slug = ? OR id = ?', 
                      (article_id, article_id))
        
        # Get updated share count
        cursor.execute('SELECT shares FROM news_articles WHERE slug = ? OR id = ?', 
                      (article_id, article_id))
        
        new_shares = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'shares': new_shares,
            'message': 'Share count updated successfully'
        })
        
    except Exception as e:
        logger.error(f"Error updating share count for article {article_id}: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to update share count'
        }), 500

@app.route('/api/news/<article_id>/metrics', methods=['GET'])
def get_article_metrics(article_id):
    """Get current metrics (views, likes, shares) for an article"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('SELECT views, likes, shares FROM news_articles WHERE (slug = ? OR id = ?) AND status = "published"', 
                      (article_id, article_id))
        
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return jsonify({
                'success': False,
                'error': 'Article not found'
            }), 404
        
        conn.close()
        
        return jsonify({
            'success': True,
            'metrics': {
                'views': row[0],
                'likes': row[1],
                'shares': row[2]
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching metrics for article {article_id}: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch article metrics'
        }), 500

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"Starting Karachuonyo Backend Server on port {port}")
    print(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)