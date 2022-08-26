from sqlalchemy.orm import Session

import models


def create_fixed(db: Session,
                 owner,
                 where,
                 value,
                 category
                 ):
    if where == 'first':
        value_second = 0
        value_first = value
    else:
        value_first = 0
        value_second = value

    db_fixed = models.Fixed(owner=owner, value_first=value_first,
                            value_second=value_second, category=category)
    db.add(db_fixed)
    db.commit()
    db.refresh(db_fixed)
    return db_fixed


def create_var(db: Session,
               owner,
               date,
               value,
               category):

    db_var = models.VarDetailed(owner=owner, date=date,
                                val=value, category=category)
    db.add(db_var)
    db.commit()
    db.refresh(db_var)
    return db_var
