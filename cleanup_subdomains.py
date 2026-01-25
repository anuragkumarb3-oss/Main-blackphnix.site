import os
import psycopg2
from datetime import datetime, timedelta

def delete_suspended_subdomains():
    try:
        # Use Replit's DATABASE_URL
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
        cur = conn.cursor()
        
        # SQL to find and delete subdomains suspended for more than 30 days
        # Assuming a 'subdomains' table with 'status' and 'suspended_at' columns
        delete_query = """
        DELETE FROM subdomains 
        WHERE status = 'suspended' 
        AND suspended_at < %s
        """
        threshold_date = datetime.now() - timedelta(days=2)
        
        cur.execute(delete_query, (threshold_date,))
        deleted_count = cur.rowcount
        conn.commit()
        
        print(f"[{datetime.now()}] Deleted {deleted_count} suspended subdomains.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error deleting subdomains: {e}")

if __name__ == "__main__":
    delete_suspended_subdomains()
