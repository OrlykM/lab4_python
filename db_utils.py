import json
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from models import *
from schemas import *


def create_entry(model, *, commit=True, **kwargs):
    session = Session()
    entry = model(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
        session.expunge_all()
    return session.query(model).filter_by(**kwargs).one()


def get_entry_by_id(model, id, **kwargs):
    session = Session()
    if session.query(model).filter_by(id=id).all() == []:
        return 404
    return session.query(model).filter_by(id=id).one()

def get_local_ad_by_location(model, locid, **kwargs):
    session=Session()
    # if session.query(model).filter_by(location_id=locid).all() = []:
    #     return 404
    return session.query(model).filter_by(location_id=locid).all()

def get_entry_by_email(model, email, **kwargs):
    session = Session()
    if session.query(model).filter_by(email=email).all() == []:
        return 404
    return session.query(model).filter_by(email=email).one()


def get_entry(model):
    session = Session()
    return session.query(model).all()


def update_entry(model, entry, id, *, commit=True, **kwargs):
    session = Session()
    if session.query(model).filter_by(id=id).all() == []:
        return 404

    session.execute(update(model).where(model.id == id).values(**kwargs))
    if commit:
        session.commit()
    return get_entry_by_id(model, id, **kwargs)


def delete_entry_by_id(model, id, *, commit=True, **kwargs):
    session = Session()
    if session.query(model).filter_by(id=id).all() == []:
        return 404
    session.query(model).filter_by(id=id).delete()
    if commit:
        session.commit()


def create_usr(phn, eml, location, stats, *, commit=True, **kwargs):
    session = Session()
    if session.query(User).filter_by(phone=phn).all() != [] or session.query(User).filter_by(email=eml).all() != []:
        return 405
    if session.query(Location).filter_by(id=location).all() == [] or stats not in ['regular', 'premium']:
        return 406
    entry = User(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
        session.expunge_all()
    return session.query(User).filter_by(**kwargs).one()


def update_usr(id, phn, eml, location, *, commit=True, **kwargs):
    session = Session()
    if session.query(User).filter_by(id=id).all() == []:
        return 404

    if phn == None and eml == None and location != None:
        if session.query(Location).filter_by(id=location).all() == []:
            return 405

    if phn == None and eml != None and location == None:
        if session.query(User).filter_by(email=eml).all() != []:
            return 406

    if phn == None and eml != None and location != None:
        if session.query(Location).filter_by(id=location).all() == []:
            return 405
        if session.query(User).filter_by(email=eml).all() != []:
            return 406

    if phn != None and eml == None and location == None:
        if session.query(User).filter_by(phone=phn).all() != []:
            return 406
    if phn != None and eml == None and location != None:
        if session.query(Location).filter_by(id=location).all() == []:
            return 405
        if session.query(User).filter_by(phone=phn).all() != []:
            return 406

    if phn != None and eml != None and location == None:
        if session.query(User).filter_by(phone=phn).all() != [] or session.query(User).filter_by(email=eml).all() != []:
            return 406

    if phn != None and eml != None and location != None:
        if session.query(Location).filter_by(id=location).all() == []:
            return 405
        if session.query(User).filter_by(phone=phn).all() != [] or session.query(User).filter_by(email=eml).all() != []:
            return 406

    session.execute(update(User).where(User.id == id).values(**kwargs))
    if commit:
        session.commit()
    return get_entry_by_id(User, id, **kwargs)


def create_localad(category, user, location, *, commit=True, **kwargs):
    session = Session()
    if session.query(Category).filter_by(id=category).all() == [] or session.query(User).filter_by(
            id=user).all() == [] or session.query(Location).filter_by(id=location).all() == []:
        return 405
    entry = LocalAd(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
        session.expunge_all()
    qvries = session.query(LocalAd).filter_by(**kwargs).all()
    if len(qvries) > 1:
        return qvries[len(qvries) - 1]
    return session.query(LocalAd).filter_by(**kwargs).one()


def update_localad(id, category, user, location, *, commit=True, **kwargs):
    session = Session()
    if session.query(LocalAd).filter_by(id=id).all() == []:
        return 404

    if category == None and user == None and location != None:
        if session.query(Location).filter_by(id=location).all() == []:
            return 405
    if category == None and user != None and location == None:
        if session.query(User).filter_by(id=user).all() == []:
            return 405
    if category == None and user != None and location != None:
        if session.query(User).filter_by(id=user).all() == [] \
                or session.query(Location).filter_by(id=location).all() == []:
            return 405
    if category != None and user == None and location == None:
        if session.query(Category).filter_by(id=category).all() == []:
            return 405
    if category != None and user == None and location != None:
        if session.query(Category).filter_by(id=category).all() == [] \
                or session.query(Location).filter_by(id=location).all() == []:
            return 405
    if category != None and user != None and location == None:
        if session.query(Category).filter_by(id=category).all() == [] \
                or session.query(User).filter_by(id=user).all() == []:
            return 405
    if category != None and user != None and location != None:
        if session.query(Category).filter_by(id=category).all() == [] \
                or session.query(User).filter_by(id=user).all() == [] \
                or session.query(Location).filter_by(id=location).all() == []:
            return 405
    session.execute(update(LocalAd).where(LocalAd.id == id).values(**kwargs))
    if commit:
        session.commit()
    return get_entry_by_id(LocalAd, id, **kwargs)


def create_publicad(category, user, *, commit=True, **kwargs):
    session = Session()
    if session.query(Category).filter_by(id=category).all() == [] \
            or session.query(User).filter_by(id=user).all() == []:
        return 405
    entry = PublicAd(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
        session.expunge_all()
    qvries = session.query(PublicAd).filter_by(**kwargs).all()
    if len(qvries) > 1:
        return qvries[len(qvries) - 1]
    return session.query(PublicAd).filter_by(**kwargs).one()


def update_publicad(id, category, user, *, commit=True, **kwargs):
    session = Session()
    if session.query(PublicAd).filter_by(id=id).all() == []:
        return 404

    if category == None and user != None:
        if session.query(User).filter_by(id=user).all() == []:
            return 405
    if category != None and user == None:
        if session.query(Category).filter_by(id=category).all() == []:
            return 405
    if category != None and user != None:
        if session.query(Category).filter_by(id=category).all() == [] \
                or session.query(User).filter_by(id=user).all() == []:
            return 405

    session.execute(update(PublicAd).where(PublicAd.id == id).values(**kwargs))
    if commit:
        session.commit()

    return get_entry_by_id(PublicAd, id, **kwargs)
