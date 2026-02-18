# Email Verification Setup Guide

## Overview
The application requires email verification for user registration. This document explains how to set up email functionality.

## Option 1: Using Gmail (Recommended for Testing)

### Step 1: Set up Gmail App Password
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (if not already enabled)
3. Go to "App passwords" (appears after 2FA is enabled)
4. Select "Mail" and "Windows Computer" (or your device)
5. Google will generate a 16-character password - copy this

### Step 2: Update .env File
```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### Step 3: Restart Flask
```bash
pkill -9 -f "python.*app.py"
cd /workspaces/cognitive-career-recommender
python backend/app.py
```

### Step 4: Test Email Sending
1. Register a new account at `http://localhost:5000/register`
2. You should receive a verification email within seconds
3. Click the link to verify and log in

---

## Option 2: Using SendGrid (For Production)

### Step 1: Create SendGrid Account
1. Go to [SendGrid.com](https://sendgrid.com)
2. Create a free account
3. Verify your sender email
4. Generate an API key

### Step 2: Update .env File
```bash
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
MAIL_DEFAULT_SENDER=your-verified-email@domain.com
```

---

## Option 3: Using Other SMTP Services

You can use any SMTP service by updating the `.env` file:

| Service | MAIL_SERVER | MAIL_PORT | MAIL_USE_TLS |
|---------|------------|-----------|-------------|
| Gmail | smtp.gmail.com | 587 | True |
| Outlook | smtp.office365.com | 587 | True |
| SendGrid | smtp.sendgrid.net | 587 | True |
| Mailgun | smtp.mailgun.org | 587 | True |
| AWS SES | email-smtp.region.amazonaws.com | 587 | True |

---

## Testing Without Email Service

If you don't have email configured, the system will:
1. Still allow user registration
2. Create unverified user accounts
3. Log the verification token to the console

### Manual Email Verification for Testing
1. User registers at `/register`
2. Check Flask app.log for the verification token:
   ```
   WARNING: Email not configured. Skipping email send for user@example.com. Token: AbCdEf...
   ```
3. Go directly to verification URL:
   ```
   http://localhost:5000/verify-email/AbCdEf...
   ```
4. User is now verified and can log in

---

## Troubleshooting

### Email Not Sending?

**Check these steps:**
1. Verify MAIL_USERNAME and MAIL_PASSWORD are correct
2. Check Flask logs: `tail -100 app.log | grep -i email`
3. For Gmail: Ensure app-specific password (not regular password)
4. For Gmail: Ensure 2-Factor Authentication is enabled

**Common Errors:**
```
SMTPAuthenticationError: Check MAIL_USERNAME and MAIL_PASSWORD
SMTPException: Check MAIL_SERVER and MAIL_PORT are correct
```

### Email Received But Link Doesn't Work?

Make sure your `localhost:5000` is accessible:
- Running locally: Link should work as-is
- On remote server: Update verification link to use your domain

---

## Security Notes

- Never commit `.env` file with real credentials
- Use app-specific passwords, not main account passwords
- For production, use environment variables or secrets management
- MAIL_USERNAME and MAIL_PASSWORD are stored in server memory only

---

## Future Enhancements

- Email templates customization
- Password reset via email
- Account activity notifications
- Email preferences management
