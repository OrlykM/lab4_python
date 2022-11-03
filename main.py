


from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql://root:root@localhost:3306/lab6orm")
Session = sessionmaker(bind=engine)

session = Session()


Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    firstName = Column(String(45))
    lastName = Column(String(45))
    email = Column(String(45))
    password = Column(String(45))
    phone = Column(String(45))
    userStatus = Column(Enum('regular', 'premium'))
    idlocation = Column(Integer, ForeignKey("location.id"))

    location = relationship("Location", backref=backref("user", uselist=False))


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    country = Column(String(45))
    city = Column(String(45))


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key = True)
    name = Column(String(45))


class LocalAd(Base):
    __tablename__ = "localAd"
    id = Column(Integer, primary_key = True)
    title = Column(String(45))
    id_category = Column(Integer, ForeignKey("category.id"))
    status = Column(Enum("active", "closed", "confirmed"))
    publishingDate =Column(DateTime)
    about = Column(String(45))
    photoUrl = Column(String(45))
    user_id = Column(Integer, ForeignKey("user.id"))
    location_id = Column(Integer, ForeignKey("location.id"))

    location = relationship("Location", backref=backref("localAd", uselist=False))
    user = relationship("User", backref = backref("localAd", uselist = False))
    category = relationship("Category", backref = backref("localAd", uselist = False))


class PublicAd(Base):
    __tablename__ = "publicAd"
    id = Column(Integer, primary_key = True)
    title = Column(String(45))
    id_category = Column(Integer, ForeignKey("category.id"))
    status = Column(Enum("active", "closed", "confirmed"))
    publishingDate =Column(DateTime)
    about = Column(String(45))
    photoUrl = Column(String(45))
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", backref=backref("publicAd", uselist=False))
    category = relationship("Category", backref=backref("publicAd", uselist=False))

Base.metadata.create_all(engine)

location1 = Location(country = "Ukraine", city = "Vinnytsia")
location2 = Location(country = "Ukraine", city = "Lviv")
location3 = Location(country = "England", city = "London")

session.add_all([location1, location2, location3])

category1 = Category(name = "commercial")
category2 = Category(name = "charity")
category3 = Category(name = "social")

session.add_all([category1, category2, category3])
user1 = User(firstName = "Stas", lastName  = "Semenenko", email="fpkljajpa", password = "ogfjoja", phone = "58926865", userStatus = "premium", idlocation = location1.id)
user2 = User(firstName = "Max", lastName  = "Orlianskiy", email="b;lhd;'", password = "fgojfpgfog", phone = "8969380897", userStatus = "premium", idlocation = location2.id)
user3 = User(firstName = "Dmytro", lastName  = "Rabotihov", email="kl;f;lkjhf", password = "yuyqpqq", phone = "66478333", userStatus = "premium", idlocation = location3.id)

session.add_all([user1, user2, user3])

session.commit()

localAd1 = LocalAd(title = "faljfalkfalkj", id_category = category3.id, status = "closed", publishingDate = "2022-07-12 05:55:33", about = "apngal", photoUrl = "pfapaj", user_id = user3.id, location_id = location1.id)

session.add(localAd1)

PublicAd1 = PublicAd(title = ";ksj;klgs", id_category = category1.id, status = "closed", publishingDate = "2022-07-22 20:55:33", about = "dhgdg", photoUrl = "eerere", user_id = user2.id)

session.add(PublicAd1)

session.commit()
