# Invite-Only Indian Dating App

This is a Django-based invitation-only dating platform for Indians and the Indian diaspora.

## Features
- Referral-based candidate registration via QR code or code
- Admin and consultant dashboards
- Profile creation and preview
- Email confirmation using SendGrid

## Setup

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd invite_dating
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
Deployment
Supports SQLite for dev

Can be deployed to Heroku, AWS, or DigitalOcean

License
MIT

---

### ✅ Step 3: Commit and Push

```bash
git add .gitignore README.md
git commit -m "Add .gitignore and project README"
git push origin main
