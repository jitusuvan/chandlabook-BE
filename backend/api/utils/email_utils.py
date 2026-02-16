from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_password_reset_email(user_email, reset_link, user_name=None):
    """
    Send password reset email with professional HTML formatting
    """
    subject = "🔐 Chandla Book - Password Reset Request"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Reset</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            .container {{
                background-color: #ffffff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #e74c3c;
            }}
            .logo {{
                font-size: 28px;
                font-weight: bold;
                color: #e74c3c;
                margin-bottom: 10px;
            }}
            .reset-button {{
                display: inline-block;
                padding: 15px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                margin: 20px 0;
            }}
            .warning {{
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                color: #856404;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                color: #666;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🎁 Chandla Book</div>
                <p>Password Reset Request</p>
            </div>
            
            <div class="content">
                <h2>Hello{' ' + user_name if user_name else ''}!</h2>
                
                <p>We received a request to reset your password for your Chandla Book account. Click the button below to reset your password:</p>
                
                <div style="text-align: center;">
                    <a href="{reset_link}" class="reset-button">Reset Password</a>
                </div>
                
                <p>Or copy and paste this link in your browser:</p>
                <p style="word-break: break-all; background-color: #f8f9fa; padding: 10px; border-radius: 5px;">{reset_link}</p>
                
                <div class="warning">
                    <strong>⚠️ Security Notice:</strong>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        <li>This link is valid for <strong>1 hour only</strong></li>
                        <li>If you didn't request this, please ignore this email</li>
                        <li>Your account remains secure</li>
                    </ul>
                </div>
            </div>
            
            <div class="footer">
                <p><strong>Chandla Book Team</strong></p>
                <p>This is an automated message. Please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Chandla Book - Password Reset Request
    
    Hello{' ' + user_name if user_name else ''}!
    
    We received a request to reset your password for your Chandla Book account.
    
    Reset Link: {reset_link}
    
    This link is valid for 1 hour only.
    
    Security Notice:
    - If you didn't request this, please ignore this email
    - Your account remains secure
    
    Best regards,
    Chandla Book Team
    """
    
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email]
    )
    
    msg.attach_alternative(html_content, "text/html")
    
    return msg.send()

def send_welcome_email(user_email, user_name):
    """
    Send welcome email to new users
    """
    subject = "🎉 Welcome to Chandla Book!"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to Chandla Book</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            .container {{
                background-color: #ffffff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #27ae60;
            }}
            .logo {{
                font-size: 28px;
                font-weight: bold;
                color: #27ae60;
                margin-bottom: 10px;
            }}
            .feature-box {{
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                border-left: 4px solid #27ae60;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                color: #666;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🎁 Chandla Book</div>
                <p>Welcome to Your Gift Management Platform</p>
            </div>
            
            <div class="content">
                <h2>Welcome, {user_name}! 🎉</h2>
                
                <p>Thank you for joining Chandla Book! Your account has been successfully created and you're ready to start managing your gift records.</p>
                
                <div class="feature-box">
                    <h3>🚀 What you can do now:</h3>
                    <ul>
                        <li><strong>Add Guests:</strong> Create profiles for friends and family</li>
                        <li><strong>Track Records:</strong> Record Aavel (given) and Mukel (received) gifts</li>
                        <li><strong>View Analytics:</strong> See yearly summaries and guest totals</li>
                        <li><strong>Dashboard:</strong> Monitor today's and upcoming events</li>
                    </ul>
                </div>
                
                <p>Start by adding your first guest and recording your chandla transactions.</p>
            </div>
            
            <div class="footer">
                <p><strong>Happy Gift Tracking!</strong></p>
                <p><strong>Chandla Book Team</strong></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Welcome to Chandla Book!
    
    Hello {user_name}!
    
    Thank you for joining Chandla Book! Your account has been successfully created.
    
    What you can do now:
    - Add Guests: Create profiles for friends and family
    - Track Records: Record Aavel (given) and Mukel (received) gifts
    - View Analytics: See yearly summaries and guest totals
    - Dashboard: Monitor today's and upcoming events
    
    Happy Gift Tracking!
    Chandla Book Team
    """
    
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email]
    )
    
    msg.attach_alternative(html_content, "text/html")
    
    return msg.send()