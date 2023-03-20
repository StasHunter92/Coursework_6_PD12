import os
import time

from Coursework_6_PD12.settings import BASE_DIR

# ----------------------------------------------------------------------------------------------------------------------
# Create and run container
os.system(f"docker run --name coursework_6_postgres "
          f"-e POSTGRES_USER={os.environ.get('DB_USER')} "
          f"-e POSTGRES_PASSWORD={os.environ.get('DB_PASSWORD')} "
          f"-p {os.environ.get('DB_PORT')}:{os.environ.get('DB_PORT')} "
          f"-d postgres")

time.sleep(3)

# ----------------------------------------------------------------------------------------------------------------------
# Migrate database
os.system(f"cd {BASE_DIR} && python manage.py makemigrations users")
time.sleep(1)
os.system(f"cd {BASE_DIR} && python manage.py makemigrations advertisements")
time.sleep(1)
os.system(f"cd {BASE_DIR} && python manage.py migrate")
time.sleep(3)

# ----------------------------------------------------------------------------------------------------------------------
# Fill database
os.system(
    f"cd {BASE_DIR} "
    f"&& python manage.py loaddata fixtures/users.json "
    f"&& python manage.py loaddata fixtures/ad.json "
    f"&& python manage.py loaddata fixtures/comments.json")

print("Finished")
