import json
from flask import request, jsonify, send_from_directory
from main import app, db
from models import HostingPlan, Order, Ticket


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
    
    response = send_from_directory('public', 'index.html')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/api/hosting-plans', methods=['GET'])
def get_hosting_plans():
    plan_type = request.args.get('type', 'shared')
    plans = HostingPlan.query.filter_by(plan_type=plan_type, is_active=True).order_by(HostingPlan.display_order).all()
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
    
    return jsonify(order.to_dict()), 201


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
