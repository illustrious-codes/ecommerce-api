python3.10 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python3.10 manage.py makemigrations
python3.10 manage.py migrate
python3.10 manage.py collectstatic --noinput