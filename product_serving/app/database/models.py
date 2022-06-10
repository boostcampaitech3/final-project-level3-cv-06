from codecs import backslashreplace_errors
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    Enum, Boolean,
)
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql.expression import intersect
from sqlalchemy.sql.schema import ForeignKey
from app.database.conn import Base, db


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    def all_columns(self):
        return [c for c in self.__table__.columns if c.primary_key is False and c.name != "created_at"]

    @classmethod
    def create(cls, session: Session, auto_commit=False, **kwargs):
        obj = cls()
        for col in obj.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(obj, col_name, kwargs.get(col_name))
        session.add(obj)
        session.flush()
        if auto_commit:
            session.commit()
        return obj

    @classmethod
    def get(cls, **kwargs):
        session = next(db.session())
        query = session.query(cls)
        for key, val in kwargs.items():
            col = getattr(cls, key)
            query = query.filter(col == val)

        if query.count() > 1:
            raise Exception("Only one row is supposed to be returned, but got more than one.")
        return query.first()

    def update(self, auto_commit: bool = False, **kwargs):
        qs = self._q.update(kwargs)
        get_id = self.id
        ret = None

        self._session.flush()
        if qs > 0 :
            ret = self._q.first()
        if auto_commit:
            self._session.commit()
        return ret

    # @classmethod
    # def filter(cls, session: Session = None, **kwargs):
    #     """
    #     Simply get a Row
    #     :param session:
    #     :param kwargs:
    #     :return:
    #     """
    #     cond = []
    #     for key, val in kwargs.items():
    #         key = key.split("__")
    #         if len(key) > 2:
    #             raise Exception("No 2 more dunders")
    #         col = getattr(cls, key[0])
    #         if len(key) == 1: cond.append((col == val))
    #         elif len(key) == 2 and key[1] == 'gt': cond.append((col > val))
    #         elif len(key) == 2 and key[1] == 'gte': cond.append((col >= val))
    #         elif len(key) == 2 and key[1] == 'lt': cond.append((col < val))
    #         elif len(key) == 2 and key[1] == 'lte': cond.append((col <= val))
    #         elif len(key) == 2 and key[1] == 'in': cond.append((col.in_(val)))
    #     obj = cls()
    #     if session:
    #         obj._session = session
    #         obj.served = True
    #     else:
    #         obj._session = next(db.session())
    #         obj.served = False
    #     query = obj._session.query(cls)
    #     query = query.filter(*cond)
    #     obj._q = query
    #     return obj


class User(Base, BaseMixin):
    __tablename__ = 'user'
    
    user_id = Column(String(length=255), nullable=False)
    password = Column(String(length=2000), nullable=False)
    
    image = relationship("Image", back_populates="user")




class Image(Base, BaseMixin):
    __tablename__ = 'image'
    
    image_path = Column(String(length=400), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id))

    user = relationship("User", back_populates="image")
    inference = relationship("Inference", back_populates="image")
    

class Inference(Base, BaseMixin):
    __tablename__ = 'inference'
    
    xmin = Column(Integer, nullable=False)
    ymin = Column(Integer, nullable=False)
    xmax = Column(Integer, nullable=False)
    ymax = Column(Integer, nullable=False)
    trouble_type = Column(Integer, nullable=False)
    image_id = Column(Integer, ForeignKey(Image.id))
    
    image = relationship("Image", back_populates="inference")


# class Tire(Base, BaseMixin):
#     __tablename__ = 'Tire'
    
#     rim_inch = Column(Integer)
#     structure = Column(String(length=5))
#     aspect_ratio = Column(Integer)
#     wheel_size = Column(Integer)
#     user_id = Column(Integer, ForeignKey(User.id))
#     position_id = Column(Integer, ForeignKey(Position.id))
    
#     position = relationship("Position", back_populates="tire")
#     user = relationship("User", back_populates="tire")