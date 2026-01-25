
import os
import firebase_admin
from firebase_admin import credentials, firestore
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def migrate_plans():
    db = firestore.client()
    plans_ref = db.collection('plans')
    plans = plans_ref.stream()

    for plan in plans:
        plan_data = plan.to_dict()
        plan_id = plan.id
        plan_name = plan_data.get('name')

        if not plan_name:
            print(f"Skipping plan {plan_id} (no name)")
            continue

        new_id = slugify(plan_name)

        if plan_id == new_id:
            print(f"Plan {plan_id} already has correct ID")
            continue

        print(f"Migrating {plan_id} -> {new_id}")
        
        # Check if new ID already exists
        new_plan_ref = plans_ref.document(new_id)
        if new_plan_ref.get().exists:
            print(f"Warning: Destination ID {new_id} already exists. Skipping.")
            continue

        # Create new document and delete old one
        new_plan_ref.set(plan_data)
        plans_ref.document(plan_id).delete()
        print(f"Successfully migrated {plan_name}")

if __name__ == "__main__":
    # Firebase is already initialized via the integration in main.py or server.py
    # We'll just use the default app if initialized, otherwise init here.
    try:
        firebase_admin.get_app()
    except ValueError:
        # If not initialized, we assume secrets are available in env
        # In Replit, this is handled by the integration
        firebase_admin.initialize_app()
    
    migrate_plans()
