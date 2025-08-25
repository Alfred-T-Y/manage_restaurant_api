import os
from dotenv import load_dotenv

load_dotenv()
from authentication.models import User

username = os.getenv("SUPERUSER_NAME")
password = os.getenv("SUPERUSER_PASSWORD")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password)
    print(f"Superuser {username} created.")
else:
    print(f"Superuser {username} already exists.")
