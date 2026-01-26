import os
import requests
import json

def send_order_email(to_email, name, order_id, plan, price, date):
    """
    Sends a branded HTML order confirmation email using Brevo API.
    """
    api_key = os.environ.get("BREVO_API_KEY")
    sender_email = "anurag@blackphnix.site"
    sender_name = "Blackphnix Hosting"

    if not api_key:
        print("Error: BREVO_API_KEY not found in environment.")
        return False

    # Read the HTML template
    try:
        with open("email_template.html", "r") as f:
            html_content = f.read()
    except FileNotFoundError:
        print("Error: email_template.html not found.")
        return False

    # Replace placeholders
    html_content = html_content.replace("{{name}}", name)
    html_content = html_content.replace("{{orderId}}", order_id)
    html_content = html_content.replace("{{plan}}", plan)
    html_content = html_content.replace("{{price}}", price)
    html_content = html_content.replace("{{date}}", date)

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }
    
    payload = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [{"email": to_email, "name": name}],
        "subject": f"Order Confirmed: {order_id}",
        "htmlContent": html_content
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [201, 200, 202]:
            print(f"Order confirmation email sent to {to_email}")
            return True
        else:
            print(f"Failed to send email via Brevo: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == "__main__":
    # Test sending (if key is set)
    # send_order_email("test@example.com", "User", "BPX-12345", "Starter Plan", "₹299/mo", "2026-01-25")
    pass
