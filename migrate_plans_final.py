
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
    plans = list(plans_ref.stream())

    for plan in plans:
        plan_data = plan.to_dict()
        plan_id = plan.id
        plan_name = plan_data.get('name')

        if not plan_name:
            continue

        new_id = slugify(plan_name)
        if plan_id == new_id:
            continue

        new_plan_ref = plans_ref.document(new_id)
        if new_plan_ref.get().exists:
            continue

        new_plan_ref.set(plan_data)
        plans_ref.document(plan_id).delete()
        print(f"Migrated {plan_id} -> {new_id}")

if __name__ == "__main__":
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app()
    migrate_plans()
