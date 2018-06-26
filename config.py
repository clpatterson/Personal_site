# instance/config.py
from personal_site_copy import application
import os

# Below is one option for connecting to the db in Elastic Beanstalk. 
#   I'd have to provision the RDS instance inside my elb environment
#   to be able to use this option. Elb would then create these environ-
#   variables for me to access in my app via os.
# DATABASE_URI = postgresql+psycopg2:// \
# 				+ os.environ['RDS_USERNAME'] 
# 				+ ':' + os.environ['RDS_PASSWORD'] \
# 				+ '@' + os.environ['RDS_HOSTNAME'] 
# 				+ ':' + os.environ['RDS_PORT'] \
# 				+ '/' + os.environ['RDS_DB_NAME']
# To format connection parameters for psycopg2 see:
# http://initd.org/psycopg/docs/module.html
DATABASE = 'your db connection parameters here'
SECRET_KEY='your key here'
USERNAME='admin'
PASSWORD='your password here'
DEBUG=True