import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os

def send_daily_leads(email_to, smtp_password):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"permits_{today}.csv"

    if not os.path.exists(filename):
        print("⚠️ Running scraper first...")
        os.system("python real_scraper.py")

    if not os.path.exists(filename):
        print("❌ No permits file found!")
        return

    df = pd.read_csv(filename)
    top_leads = df.head(12)

    html = f"""
    <h2>🏗️ Arizona Permit Pulse - Daily Leads ({today})</h2>
    <p><strong>{len(df)} new high-value permits across Tucson + Phoenix today.</strong></p>
    
    <h3>🔥 Top 12 Opportunities</h3>
    <table border="1" cellpadding="8" style="border-collapse: collapse; width:100%;">
        <tr>
            <th>City</th>
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
            <td>{row.get('City', 'AZ')}</td>
            <td>{row['Type']}</td>
            <td>{row['Address']}</td>
            <td>${row['Value']:,.0f}</td>
            <td><b>{row['Priority']}</b></td>
            <td>{row['Details']}</td>
        </tr>
        """

    html += "</table>"
    html += f"<p><strong>Total Value Today: ${df['Value'].sum():,}</strong></p>"
    html += "<p>Full CSV attached • Dashboard: https://arizonapermitpulse-ywqioednez3qgkevrfxjeu.streamlit.app/</p>"

    # Email setup
    msg = MIMEMultipart()
    msg['From'] = email_to
    msg['To'] = email_to
    msg['Subject'] = f"Arizona Permit Pulse - {len(df)} New Leads Today ({today})"
    msg.attach(MIMEText(html, 'html'))

    # Attach CSV
    with open(filename, "rb") as f:
        attach = MIMEBase('application', 'octet-stream')
        attach.set_payload(f.read())
        encoders.encode_base64(attach)
        attach.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(attach)

    # Send via iCloud
    try:
        server = smtplib.SMTP('smtp.mail.me.com', 587)
        server.starttls()
        server.login(email_to, smtp_password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent successfully to {email_to} with {len(df)} leads!")
    except Exception as e:
        print(f"❌ Email error: {e}")

if __name__ == "__main__":
    YOUR_EMAIL = "domleon95@icloud.com"
    APP_PASSWORD = "atqz-lviz-gjlq-tiyj"   # ← Your iCloud app password
    send_daily_leads(YOUR_EMAIL, APP_PASSWORD)