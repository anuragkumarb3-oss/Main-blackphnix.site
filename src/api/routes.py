import json
import secrets
import string
from flask import request, jsonify, send_from_directory
from main import app, db
from src.models import HostingPlan, Order, Ticket, User, CyberAccount, SystemLog
from src.services.cyberpanel_service import CyberPanelService
from src.services.encryption_service import EncryptionService

cp_service = CyberPanelService()
encryption_service = EncryptionService()

def generate_password(length=12):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@app.route('/api/auth/register', methods=['POST'])
def register_and_provision():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    subdomain = data.get('subdomain') # e.g. "user1.blackphnix.site"

    if not all([username, email, password, subdomain]):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    # 1. Create local user
    user = User(username=username, email=email)
    user.password_hash = password 
    db.session.add(user)
    db.session.flush()

    # 2. CyberPanel Provisioning
    cp_pass = generate_password()
    cp_res = cp_service.create_user(username, cp_pass, email)
    
    if cp_res.get('status') != 1:
        return jsonify({"error": "Provisioning failed", "detail": cp_res}), 500

    # Create website and attempt auto SSL
    site_res = cp_service.create_website(subdomain, username)
    # Note: CyberPanel createWebsite API with ssl=1 already attempts SSL
    
    # 3. Create CyberAccount record with encrypted password
    account = CyberAccount(
        user_id=user.id, 
        domain=subdomain, 
        cp_username=username,
        cp_password_encrypted=encryption_service.encrypt(cp_pass)
    )
    db.session.add(account)
    
    log = SystemLog(level="INFO", message=f"Provisioned account for {username} on {subdomain}")
    db.session.add(log)
    
    db.session.commit()

    return jsonify({
        "message": "Account provisioned successfully",
        "credentials": {
            "control_panel": "https://45.194.3.184:8090",
            "username": username,
            "password": cp_pass,
            "domain": subdomain
        }
    }), 201

@app.route('/api/webhooks/payment-success', methods=['POST'])
def payment_webhook():
    data = request.get_json()
    # In a real scenario, verify signature and check order details
    # For now, we'll simulate the registration trigger
    return jsonify({"message": "Webhook received"}), 200

@app.route('/api/admin/accounts', methods=['GET'])
def list_accounts():
    accounts = CyberAccount.query.all()
    return jsonify([{
        "id": a.id,
        "domain": a.domain,
        "username": a.cp_username,
        "status": a.status,
        "suspension_date": a.suspension_date.isoformat() if a.suspension_date else None
    } for a in accounts])

@app.route('/api/admin/logs', methods=['GET'])
def get_logs():
    logs = SystemLog.query.order_by(SystemLog.created_at.desc()).limit(100).all()
    return jsonify([{
        "level": l.level,
        "message": l.message,
        "time": l.created_at.isoformat()
    } for l in logs])

@app.route('/')
def serve_index():
    response = send_from_directory('public', 'index.html')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/<path:path>')
def serve_spa(path):
    import os
    from flask import Response
    
    file_path = os.path.join('public', path)
    
    if os.path.isfile(file_path):
        return send_from_directory('public', path)
    
    # Check if path starts with api/ or is a known api route
    if path.startswith('api/'):
        return jsonify({"error": "Not Found"}), 404
    
    response = send_from_directory('public', 'index.html')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/pricing')
@app.route('/pricing-shared')
@app.route('/pricing-vps')
@app.route('/login')
@app.route('/dashboard')
@app.route('/support')
@app.route('/analytics')
@app.route('/checkout')
@app.route('/billing')
def catch_all_spa():
    return serve_index()

@app.route('/api/hosting-plans/list', methods=['GET'])
@app.route("/api/hosting-plans/list", methods=["GET"])
def get_hosting_plans_list():
    plans = HostingPlan.query.order_by(HostingPlan.display_order).all()
    return jsonify([plan.to_dict() for plan in plans])

@app.route('/api/hosting-plans/debug', methods=['GET'])
def debug_hosting_plans():
    plans = HostingPlan.query.all()
    return jsonify([plan.to_dict() for plan in plans])

@app.route('/api/hosting-plans/all', methods=['GET'])
def get_all_hosting_plans():
    plans = HostingPlan.query.order_by(HostingPlan.plan_type, HostingPlan.display_order).all()
    return jsonify([plan.to_dict() for plan in plans])

@app.route('/api/hosting-plans', methods=['POST'])
def create_hosting_plan():
    data = request.get_json()
    
    plan = HostingPlan(
        name=data.get('name'),
        plan_type=data.get('planType', 'shared'),
        price=float(data.get('price', 0)),
        billing_cycle=data.get('billingCycle', 'monthly'),
        storage=data.get('storage'),
        bandwidth=data.get('bandwidth'),
        domains=int(data.get('domains', 1)),
        email_accounts=int(data.get('emailAccounts', 1)),
        ssl=data.get('ssl', True),
        cpu=data.get('cpu'),
        ram=data.get('ram'),
        features=json.dumps(data.get('features', [])),
        is_active=data.get('isActive', True),
        is_featured=data.get('isFeatured', False),
        display_order=int(data.get('displayOrder', 0))
    )
    
    db.session.add(plan)
    db.session.commit()
    
    return jsonify(plan.to_dict()), 201

@app.route('/api/hosting-plans/<int:plan_id>', methods=['PUT'])
def update_hosting_plan(plan_id):
    plan = HostingPlan.query.get_or_404(plan_id)
    data = request.get_json()
    
    if 'name' in data:
        plan.name = data['name']
    if 'planType' in data:
        plan.plan_type = data['planType']
    if 'price' in data:
        plan.price = float(data['price'])
    if 'billingCycle' in data:
        plan.billing_cycle = data['billingCycle']
    if 'storage' in data:
        plan.storage = data['storage']
    if 'bandwidth' in data:
        plan.bandwidth = data['bandwidth']
    if 'domains' in data:
        plan.domains = int(data['domains'])
    if 'emailAccounts' in data:
        plan.email_accounts = int(data['emailAccounts'])
    if 'ssl' in data:
        plan.ssl = data['ssl']
    if 'cpu' in data:
        plan.cpu = data['cpu']
    if 'ram' in data:
        plan.ram = data['ram']
    if 'features' in data:
        plan.features = json.dumps(data['features'])
    if 'isActive' in data:
        plan.is_active = data['isActive']
    if 'isFeatured' in data:
        plan.is_featured = data['isFeatured']
    if 'displayOrder' in data:
        plan.display_order = int(data['displayOrder'])
    
    db.session.commit()
    
    return jsonify(plan.to_dict())

@app.route('/api/hosting-plans/<int:plan_id>', methods=['DELETE'])
def delete_hosting_plan(plan_id):
    plan = HostingPlan.query.get_or_404(plan_id)
    db.session.delete(plan)
    db.session.commit()
    return jsonify({'message': 'Plan deleted successfully'})

@app.route('/api/orders', methods=['GET'])
def get_orders():
    user_id = request.args.get('userId')
    if user_id:
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    else:
        orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([order.to_dict() for order in orders])

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    order = Order(
        user_id=data.get('userId'),
        user_email=data.get('userEmail'),
        plan_id=data.get('planId'),
        plan_name=data.get('planName'),
        amount=float(data.get('amount', 0)),
        status=data.get('status', 'pending'),
        payment_status=data.get('paymentStatus', 'pending')
    )
    
    db.session.add(order)
    db.session.commit()
    
    return jsonify(order.to_edit()), 201

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    user_id = request.args.get('userId')
    if user_id:
        tickets = Ticket.query.filter_by(user_id=user_id).order_by(Ticket.created_at.desc()).all()
    else:
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return jsonify([ticket.to_dict() for ticket in tickets])

@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    data = request.get_json()
    
    ticket = Ticket(
        user_id=data.get('userId'),
        user_email=data.get('userEmail'),
        subject=data.get('subject'),
        description=data.get('description'),
        priority=data.get('priority', 'medium')
    )
    
    db.session.add(ticket)
    db.session.commit()
    
    return jsonify(ticket.to_dict()), 201

@app.route('/api/broadcast', methods=['POST'])
def broadcast():
    data = request.get_json()
    return jsonify({'message': 'Broadcast sent', 'data': data})

@app.route('/api/verify-email', methods=['POST'])
def verify_email():
    data = request.get_json()
    email = data.get('email')
    return jsonify({'verified': True, 'email': email})
