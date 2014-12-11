from flask import Flask
from app.admin import admin
from flask.ext.mail import Mail
import pymongo


# needed for global settings
c = pymongo.Connection()

app = Flask(__name__,
        static_folder="static", # match with your static folder
        static_url_path="/static" # you can change this to anything other than static, its your URL
      )

# mail config start

mail = Mail(app)

app.config.update(
                    MAIL_SERVER='smtp.gmail.com',
                    MAIL_PORT=465,
                    MAIL_USE_SSL=True,
                    MAIL_USERNAME = 'email@gmail.com',
                    MAIL_PASSWORD = 'yourcurrentpasswordis'
                  )
# mail config end

from app import views


# global domain name config
# calling from jinja => {{ config["domain_name"] }}
# ambil informasi ini dari databse admindb.settings
admindb = c["admindb"]
data = admindb.settings.find_one()

if not data:  # jika data lom ada (baru deploy/localhost)
    data = {}
    data["name"] = "example"
    data["url"] = "http://127.0.0.1:5000"

app.config["SITE_NAME"] = data["name"]
app.config["SITE_URL"] = data["url"]
app.config["VERSION"] = "1.0"
app.config["APP_TITLE"] = data["name"]

# important! needed for login things >> joss
app.secret_key = "vertigo"

# adding admin blueprint
from app.admin.views import admin
app.register_blueprint(admin)

# logging tools
# author: https://gist.github.com/mitsuhiko/5659670
# monitor uwsgi access / error :: output di nohup.out

import sys
from logging import Formatter, StreamHandler
handler = StreamHandler(sys.stderr)
handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(handler)
