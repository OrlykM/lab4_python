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

    response = session.query(model).filter_by(**kwargs).one()
    session.close()
    return response


def get_entry_by_id(model, id, **kwargs):
    session = Session()
    if session.query(model).filter_by(id=id).all() == []:
        return 404
    response = session.query(model).filter_by(id=id).one()
    session.close()
    return response



def get_local_ad_by_location(model, locid, **kwargs):
    session=Session()
    response = session.query(model).filter_by(location_id=locid).all()
    session.close()
    return response

def get_entry_by_email(model, email, **kwargs):
    session = Session()
    if session.query(model).filter_by(email=email).all() == []:
        return 404
    resonse = session.query(model).filter_by(email=email).one()
    session.close()
    return resonse


def get_entry(model):
    session = Session()
    response = session.query(model).all()
    session.close()
    return response

def create_location(*, commit=True, **kwargs):
    session = Session()
    entry = Location(**kwargs)
    entry.country = "Ukraine"
    session.add(entry)
    if commit:
        session.commit()
        session.expunge_all()
    all = session.query(Location).filter_by(**kwargs).all()
    session.close()
    return all[len(all) - 1]

def update_entry(model, entry, id, *, commit=True, **kwargs):
    session = Session()
    if session.query(model).filter_by(id=id).all() == []:
        session.close()
        return 404
    session.execute(update(model).where(model.id == id).values(**kwargs))
    if commit:
        session.commit()
    response = get_entry_by_id(model, id, **kwargs)
    session.close()
    return response


def delete_entry_by_id(model, id, *, commit=True, **kwargs):
    session = Session()
    if session.query(model).filter_by(id=id).all() == []:
        session.close()
        return 404
    session.query(model).filter_by(id=id).delete()
    if commit:
        session.commit()
    session.close()

def create_usr(phn, eml, location, stats, *, commit=True, **kwargs):
    session = Session()
    if session.query(User).filter_by(phone=phn).all() != [] or session.query(User).filter_by(email=eml).all() != []:
        session.close()
        return 405
    if session.query(Location).filter_by(id=location).all() == [] or stats not in ['regular', 'premium']:
        session.close()
        return 406
    entry = User(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
        session.expunge_all()
    response = session.query(User).filter_by(**kwargs).one()
    session.close()
    return response


def update_usr(id, phn, eml, location, *, commit=True, **kwargs):
    session = Session()
    if session.query(User).filter_by(id=id).all() == []:
        session.close()
        return 404

    if phn == None and eml == None and location != None:
        if session.query(Location).filter_by(id=location).all() == []:
            session.close()
            return 405

    if phn == None and eml != None and location == None:
        if session.query(User).filter_by(email=eml).all() != []:
            session.close()
            return 406

    if phn == None and eml != None and location != None:
        if session.query(Location).filter_by(id=location).all() == []:
            session.close()
            return 405
        if session.query(User).filter_by(email=eml).all() != []:
            session.close()
            return 406

    if phn != None and eml == None and location == None:
        if session.query(User).filter_by(phone=phn).all() != []:
            session.close()
            return 406
    if phn != None and eml == None and location != None:
        if session.query(Location).filter_by(id=location).all() == []:
            session.close()
            return 405
        if session.query(User).filter_by(phone=phn).all() != []:
            session.close()
            return 406

    if phn != None and eml != None and location == None:
        if session.query(User).filter_by(phone=phn).all() != [] or session.query(User).filter_by(email=eml).all() != []:
            session.close()
            return 406

    if phn != None and eml != None and location != None:
        if session.query(Location).filter_by(id=location).all() == []:
            session.close()
            return 405
        if session.query(User).filter_by(phone=phn).all() != [] or session.query(User).filter_by(email=eml).all() != []:
            session.close()
            return 406

    session.execute(update(User).where(User.id == id).values(**kwargs))
    if commit:
        session.commit()

    response = get_entry_by_id(User, id, **kwargs)
    session.close()
    return response


def create_localad(category, user, location, *, commit=True, **kwargs):
    session = Session()
    if session.query(Category).filter_by(id=category).all() == [] or session.query(User).filter_by(
            id=user).all() == [] or session.query(Location).filter_by(id=location).all() == []:
        session.close()
        return 405
    entry = LocalAd(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
        session.expunge_all()
    qvries = session.query(LocalAd).filter_by(**kwargs).all()
    if len(qvries) > 1:
        session.close()
        return qvries[len(qvries) - 1]
    response = session.query(LocalAd).filter_by(**kwargs).one()
    session.close()
    return response


def update_localad(id, category, user, location, *, commit=True, **kwargs):
    session = Session()
    if session.query(LocalAd).filter_by(id=id).all() == []:
        session.close()
        return 404

    if category == None and user == None and location != None:
        if session.query(Location).filter_by(id=location).all() == []:
            session.close()
            return 405
    if category == None and user != None and location == None:
        if session.query(User).filter_by(id=user).all() == []:
            session.close()
            return 405
    if category == None and user != None and location != None:
        if session.query(User).filter_by(id=user).all() == [] \
                or session.query(Location).filter_by(id=location).all() == []:
            session.close()
            return 405
    if category != None and user == None and location == None:
        if session.query(Category).filter_by(id=category).all() == []:
            session.close()
            return 405
    if category != None and user == None and location != None:
        if session.query(Category).filter_by(id=category).all() == [] \
                or session.query(Location).filter_by(id=location).all() == []:
            session.close()
            return 405
    if category != None and user != None and location == None:
        if session.query(Category).filter_by(id=category).all() == [] \
                or session.query(User).filter_by(id=user).all() == []:
            session.close()
            return 405
    if category != None and user != None and location != None:
        if session.query(Category).filter_by(id=category).all() == [] \
                or session.query(User).filter_by(id=user).all() == [] \
                or session.query(Location).filter_by(id=location).all() == []:
            session.close()
            return 405
    session.execute(update(LocalAd).where(LocalAd.id == id).values(**kwargs))
    if commit:
        session.commit()
    response = get_entry_by_id(LocalAd, id, **kwargs)
    session.close()
    return response

def create_publicad(category, user, *, commit=True, **kwargs):
    session = Session()
    if session.query(Category).filter_by(id=category).all() == [] \
            or session.query(User).filter_by(id=user).all() == []:
        session.close()
        return 405
    entry = PublicAd(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
        session.expunge_all()
    qvries = session.query(PublicAd).filter_by(**kwargs).all()
    if len(qvries) > 1:
        session.close()
        return qvries[len(qvries) - 1]
    response = session.query(PublicAd).filter_by(**kwargs).one()
    session.close()
    return response


def update_publicad(id, category, user, *, commit=True, **kwargs):
    session = Session()
    if session.query(PublicAd).filter_by(id=id).all() == []:
        session.close()
        return 404

    if category == None and user != None:
        if session.query(User).filter_by(id=user).all() == []:
            session.close()
            return 405
    if category != None and user == None:
        if session.query(Category).filter_by(id=category).all() == []:
            session.close()
            return 405
    if category != None and user != None:
        if session.query(Category).filter_by(id=category).all() == [] \
                or session.query(User).filter_by(id=user).all() == []:
            session.close()
            return 405

    session.execute(update(PublicAd).where(PublicAd.id == id).values(**kwargs))
    if commit:
        session.commit()
    response = get_entry_by_id(PublicAd, id, **kwargs)
    return response