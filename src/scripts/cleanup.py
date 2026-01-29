import os
import sys
import time
from datetime import datetime, timedelta

# Fix path to allow importing main and src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from main import app, db
from src.models import CyberAccount, SystemLog
from src.services.cyberpanel_service import CyberPanelService

cp_service = CyberPanelService()

def cleanup_suspended_accounts():
    with app.app_context():
        now = datetime.utcnow()
        
        # 1. Auto-suspend expired accounts (example logic)
        # In a real system, you'd check subscription expiry dates
        
        # 2. 15-day Cleanup
        cutoff_date = now - timedelta(days=15)
        # Find accounts suspended more than 15 days ago
        to_delete = CyberAccount.query.filter(
            CyberAccount.status == 'suspended',
            CyberAccount.suspension_date <= cutoff_date
        ).all()
        
        for account in to_delete:
            print(f"Cleaning up {account.domain}...")
            res = cp_service.delete_website(account.domain)
            if res.get('status') == 1:
                account.status = 'deleted'
                log = SystemLog(level="INFO", message=f"Auto-deleted {account.domain} after 15 days suspension")
                db.session.add(log)
            else:
                log = SystemLog(level="ERROR", message=f"Failed auto-delete for {account.domain}: {res.get('error')}")
                db.session.add(log)
        
        db.session.commit()

if __name__ == "__main__":
    while True:
        try:
            cleanup_suspended_accounts()
        except Exception as e:
            print(f"Cleanup error: {e}")
        time.sleep(86400) # Run daily
