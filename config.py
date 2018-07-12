"""Flask application configurations"""

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
