"""Flask application configurations"""

import os

# Basic Flask configs
DEBUG = True
SECRET_KEY = 'dev'

# Website login credentials
USERNAME='admin'
PASSWORD='D6kbTfAgdpYUXHtwM'

# For RDS Postgres database instance
DATABASE = 'dbname=personalsitedb \
			user=personalsitedb \
			password=UDXWpPWuqTeH3rEqV \
			host=personalsitedb.cp0jtp5vvqiw.us-east-1.rds.amazonaws.com \
			port=5432'

# Flask-Dropzone settings
DROPZONE_UPLOAD_MULTIPLE = True
DROPZONE_INPUT_NAME = 'image'
DROPZONE_ALLOWED_FILE_CUSTOM = True
DROPZONE_ALLOWED_FILE_TYPE = 'image/*'
DROPZONE_REDIRECT_VIEW = 'show_posts'

# Flask-Uploads settings
# Will want to change this so that it points to an images folder in static directory 
UPLOADED_IMAGES_DEST = os.getcwd() + '/static/images'
