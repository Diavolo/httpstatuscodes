from app import create_app

# For production, run: gunicorn --workers 4 --bind 0.0.0.0:8000 main:app
app = create_app()

# For development, run: flask --app main run --debug
if __name__ == "__main__":
    app.run()
