import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_order_email(to_email, name, order_id, plan, price, date):
    """
    Sends a branded HTML order confirmation email using SendGrid SMTP.
    """
    # Load configuration from environment variables
    smtp_server = "smtp.sendgrid.net"
    smtp_port = 587
    # Note: Use the SendGrid integration to manage these secrets
    sender_email = "anurag@blackphnix.site"
    # SendGrid username is always 'apikey'
    username = "apikey"
    password = os.environ.get("SENDGRID_API_KEY")

    if not password:
        print("Error: SENDGRID_API_KEY not found in environment.")
        return False

    # Create the email message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Order Confirmed: {order_id}"
    msg["From"] = f"Blackphnix Hosting <{sender_email}>"
    msg["To"] = to_email

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

    # Attach HTML content
    msg.attach(MIMEText(html_content, "html"))

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
        print(f"Order confirmation email sent to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

if __name__ == "__main__":
    # Test sending (if key is set)
    # send_order_email("test@example.com", "User", "BPX-12345", "Starter Plan", "₹299/mo", "2026-01-25")
    pass
