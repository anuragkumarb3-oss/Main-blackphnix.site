from datetime import datetime
from main import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CyberAccount(db.Model):
    __tablename__ = 'cyber_accounts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    domain = db.Column(db.String(255), unique=True)
    cp_username = db.Column(db.String(80))
    status = db.Column(db.String(20), default='active') # active, suspended, deleted
    suspension_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemLog(db.Model):
    __tablename__ = 'system_logs'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(20))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class HostingPlan(db.Model):
    __tablename__ = 'hosting_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    plan_type = db.Column(db.String(50), nullable=False, default='shared')  # shared, vps, dedicated
    price = db.Column(db.Float, nullable=False)
    billing_cycle = db.Column(db.String(20), default='monthly')  # monthly, yearly
    storage = db.Column(db.String(50))
    bandwidth = db.Column(db.String(50))
    domains = db.Column(db.Integer, default=1)
    email_accounts = db.Column(db.Integer, default=1)
    ssl = db.Column(db.Boolean, default=True)
    cpu = db.Column(db.String(50))
    ram = db.Column(db.String(50))
    features = db.Column(db.Text)  # JSON string of features
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        import json
        return {
            'id': self.id,
            'name': self.name,
            'planType': self.plan_type,
            'price': self.price,
            'billingCycle': self.billing_cycle,
            'storage': self.storage,
            'bandwidth': self.bandwidth,
            'domains': self.domains,
            'emailAccounts': self.email_accounts,
            'ssl': self.ssl,
            'cpu': self.cpu,
            'ram': self.ram,
            'features': json.loads(self.features) if self.features else [],
            'isActive': self.is_active,
            'isFeatured': self.is_featured,
            'displayOrder': self.display_order,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(255))
    plan_id = db.Column(db.Integer, db.ForeignKey('hosting_plans.id'))
    plan_name = db.Column(db.String(100))
    status = db.Column(db.String(50), default='pending')  # pending, active, cancelled, expired
    amount = db.Column(db.Float)
    payment_status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    plan = db.relationship('HostingPlan', backref='orders')

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'userEmail': self.user_email,
            'planId': self.plan_id,
            'planName': self.plan_name,
            'status': self.status,
            'amount': self.amount,
            'paymentStatus': self.payment_status,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'expiresAt': self.expires_at.isoformat() if self.expires_at else None
        }


class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(255))
    subject = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='open')  # open, in_progress, resolved, closed
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'userEmail': self.user_email,
            'subject': self.subject,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
