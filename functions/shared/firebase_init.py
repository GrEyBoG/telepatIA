from firebase_admin import initialize_app, get_app

try:
    firebase_app = get_app()
except ValueError:
    firebase_app = initialize_app()
