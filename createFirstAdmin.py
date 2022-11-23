from laba8.models import *
from flask_bcrypt import generate_password_hash

session = Session()

user1 = User(firstName="admin", lastName="admin", email="admin@gmail.com",
             password=generate_password_hash("admin123admin"), phone="+380963651527",
            userStatus='premium', isAdmin=1)

session.add(user1)
session.commit()