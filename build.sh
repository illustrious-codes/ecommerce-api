python3.10 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
Python3.10 manage.py makemigrations
Python3.10 manage.py migrate
Python3.10 manage.py collectstatic