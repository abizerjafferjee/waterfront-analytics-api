Django Rest API for waterfrontanalytics.com

Production Set Up

# TODO: Set to URL of git repo.
PROJECT_GIT_URL=''

PROJECT_BASE_PATH='/home/deploy/waterfront-analytics-api'
VIRTUALENV_BASE_PATH='/home/deploy/waterfront-analytics-api/wfa'

# Install Python, SQLite and pip
apt-get update
apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git

mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

mkdir -p $VIRTUALENV_BASE_PATH
python3 -m venv $VIRTUALENV_BASE_PATH

$VIRTUALENV_BASE_PATH/bin/pip install -r $PROJECT_BASE_PATH/requirements.txt

# Run migrations

# Setup Supervisor to run our uwsgi process.
cp $PROJECT_BASE_PATH/waterfront-api/deploy/supervisor_waterfront_api.conf /etc/supervisor/conf.d/waterfront_api.conf
supervisorctl reread
supervisorctl update
supervisorctl restart waterfront_api

# Setup nginx to make our application accessible.
cp $PROJECT_BASE_PATH/waterfront-api/deploy/nginx_waterfront_api.conf /etc/nginx/sites-available/waterfront_api.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/waterfront_api.conf /etc/nginx/sites-enabled/waterfront_api.conf
systemctl restart nginx.service

Hint
- allow port 80 on firewall

Resource links
- https://www.youtube.com/watch?v=NJDNe7mcZeU&list=PL8GFhcuc_fW4cxdkRtWIlln1DQ3CZwQen&index=71 (starting video 64)
- https://medium.com/@biswashirok/deploying-django-python-3-6-to-digital-ocean-with-uwsgi-nginx-ubuntu-18-04-3f8c2731ade1
- https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-uwsgi-and-nginx-on-ubuntu-16-04#setting-up-the-uwsgi-application-server
- https://stackoverflow.com/questions/46644774/deploying-django-to-a-server

Letsencrypt - SSL
- https://medium.com/@kwekuq/secure-django-nginx-with-lets-encrypt-on-ubuntu-18-04-ba096abdc892