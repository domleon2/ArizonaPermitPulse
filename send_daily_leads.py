import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

def send_daily_leads(email_to, smtp_password):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"permits_{today}.csv"

    if not os.path.exists(filename):
        print("Running scraper first...")
        os.system("python real_scraper.py")

    df = pd.read_csv(filename)
    top_leads = df.head(10)

    html = f"""
    <h2>🏗️ Arizona Permit Pulse - Daily Leads ({today})</h2>
    <p><strong>{len(df)} new high-value permits in Pima County today.</strong></p>
    
    <h3>🔥 Top Opportunities</h3>
    <table border="1" cellpadding="8" style="border-collapse: collapse; width:100%;">
        <tr>
            <th>Type</th>
            <th>Address</th>
            <th>Value</th>
            <th>Priority</th>
            <th>Details</th>
        </tr>
    """

    for _, row in top_leads.iterrows():
        html += f"""
        <tr>
            <td>{row['Type']}</td>
            <td>{row['Address']}</td>
            <td>${row['Value']:,}</td>
            <td><b>{row['Priority']}</b></td>
            <td>{row['Details']}</td>
        </tr>
        """

    html += "</table><p>Full CSV attached • Dashboard: http://localhost:8501</p>"

    # Email
    msg = MIMEMultipart()
    msg['From'] = email_to
    msg['To'] = email_to
    msg['Subject'] = f"Arizona Permit Pulse - {len(df)} New Leads Today"
    msg.attach(MIMEText(html, 'html'))

    # Attach CSV
    with open(filename, "rb") as f:
        attach = MIMEText(f.read().decode(), 'csv')
        attach.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attach)

    # Send via iCloud
    try:
        server = smtplib.SMTP('smtp.mail.me.com', 587)
        server.starttls()
        server.login(email_to, smtp_password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent successfully to {email_to}!")
    except Exception as e:
        print(f"❌ Email error: {e}")

if __name__ == "__main__":
    YOUR_EMAIL = "domleon95@icloud.com"
    APP_PASSWORD = "atqz-lviz-gjlq-tiyj"
    send_daily_leads(YOUR_EMAIL, APP_PASSWORD)