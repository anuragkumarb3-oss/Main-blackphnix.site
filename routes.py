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


@app.route('/pricing-shared')
def pricing_shared():
    # Direct server-side rendering for the pricing-shared route
    # instead of relying solely on the SPA to fetch data
    from models import HostingPlan
    plans = HostingPlan.query.filter_by(plan_type='shared', is_active=True).order_by(HostingPlan.display_order).all()
    
    # Simple HTML template for the pricing section
    plans_html = ""
    for plan in plans:
        featured_class = "border-blue-500 shadow-[0_0_30px_rgba(59,130,246,0.3)] bg-blue-500/5" if plan.is_featured else "border-white/10 bg-white/5"
        featured_tag = '<div class="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 text-xs font-bold text-white bg-blue-500 rounded-full uppercase tracking-wider">Most Popular</div>' if plan.is_featured else ""
        
        # Handle features as list or JSON string
        features = plan.features
        if isinstance(features, str):
            import json
            try:
                features = json.loads(features)
            except:
                features = [f.strip() for f in features.split(',')]
        
        features_list = ""
        for feature in features:
            features_list += f'''
            <li class="flex items-center text-gray-300">
                <svg class="w-5 h-5 text-blue-500 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                <span class="text-sm">{feature}</span>
            </li>'''

        plans_html += f'''
        <div class="relative group p-8 rounded-3xl border {featured_class} backdrop-blur-sm transition-all duration-500 hover:-translate-y-2 hover:border-blue-500/50">
            {featured_tag}
            <div class="mb-8">
                <h3 class="text-xl font-bold text-white mb-2">{plan.name}</h3>
                <p class="text-gray-400 text-sm">Perfect for growing projects</p>
            </div>
            
            <div class="flex items-baseline mb-8">
                <span class="text-5xl font-black text-white">${plan.price}</span>
                <span class="text-gray-400 ml-2 text-sm font-medium">/month</span>
            </div>
            
            <ul class="space-y-4 mb-10">
                {features_list}
            </ul>
            
            <button class="w-full py-4 rounded-2xl font-bold transition-all duration-300 {'bg-blue-600 text-white hover:bg-blue-500 shadow-lg shadow-blue-500/25' if plan.is_featured else 'bg-white/10 text-white hover:bg-white/20 border border-white/10'}">
                Select Plan
            </button>
        </div>
        '''

    html_content = f'''
    <!DOCTYPE html>
    <html lang="en" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Shared Hosting | BlackPhnix Hub</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            body {{ 
                font-family: 'Plus Jakarta Sans', sans-serif; 
                background-color: #030303;
                color: #ffffff;
                margin: 0;
            }}
            .mesh-gradient {{
                position: fixed;
                top: 0; left: 0; right: 0; bottom: 0;
                background: 
                    radial-gradient(circle at 0% 0%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 100% 100%, rgba(59, 130, 246, 0.1) 0%, transparent 50%);
                z-index: -1;
            }}
            .grid-bg {{
                position: fixed;
                top: 0; left: 0; right: 0; bottom: 0;
                background-image: linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
                                 linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
                background-size: 50px 50px;
                z-index: -1;
            }}
            @keyframes float {{
                0% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-10px); }}
                100% {{ transform: translateY(0px); }}
            }}
            .float {{ animation: float 6s ease-in-out infinite; }}
        </style>
    </head>
    <body class="antialiased selection:bg-blue-500/30">
        <div class="mesh-gradient"></div>
        <div class="grid-bg"></div>

        <nav class="max-w-7xl mx-auto p-8 flex justify-between items-center relative z-10">
            <div class="flex items-center space-x-2">
                <div class="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center font-black text-xl italic shadow-lg shadow-blue-500/20">B</div>
                <span class="text-xl font-extrabold tracking-tight">BLACKPHNIX</span>
            </div>
            <div class="hidden md:flex items-center space-x-10 text-sm font-semibold text-gray-400">
                <a href="/" class="hover:text-white transition-all duration-300">Overview</a>
                <a href="/pricing-shared" class="text-blue-500">Solutions</a>
                <a href="/support" class="hover:text-white transition-all duration-300">Resources</a>
                <a href="/login" class="px-6 py-2.5 bg-white/5 border border-white/10 rounded-full hover:bg-white/10 transition-all duration-300 text-white">Client Portal</a>
            </div>
        </nav>

        <main class="relative z-10 pt-20 pb-32">
            <div class="max-w-7xl mx-auto px-8">
                <div class="text-center mb-24">
                    <div class="inline-block px-4 py-1.5 mb-6 text-xs font-bold text-blue-400 bg-blue-500/10 border border-blue-500/20 rounded-full uppercase tracking-widest">
                        Hosting Solutions
                    </div>
                    <h1 class="text-6xl md:text-8xl font-extrabold mb-8 tracking-tighter leading-none">
                        Shared <span class="text-blue-500">Infrastructure.</span><br/>
                        Enterprise Power.
                    </h1>
                    <p class="text-xl text-gray-400 max-w-2xl mx-auto font-medium leading-relaxed">
                        Scale your digital footprint with ultra-low latency infrastructure and dedicated support engineered for high-performance projects.
                    </p>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 relative">
                    {plans_html}
                </div>
            </div>
        </main>

        <footer class="relative z-10 py-16 border-t border-white/5 bg-black/50 backdrop-blur-xl">
            <div class="max-w-7xl mx-auto px-8 flex flex-col md:row justify-between items-center text-gray-500 text-sm font-medium">
                <p>&copy; 2026 BlackPhnix Hub. High Performance Hosting.</p>
                <div class="mt-4 md:mt-0 space-x-8">
                    <a href="#" class="hover:text-white transition-colors">Privacy</a>
                    <a href="#" class="hover:text-white transition-colors">Terms</a>
                    <a href="#" class="hover:text-white transition-colors">Status</a>
                </div>
            </div>
        </footer>
    </body>
    </html>
    '''
    return html_content


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


