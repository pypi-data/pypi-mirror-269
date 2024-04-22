

from sqlalchemy import Column
from tests.test_models import Base
from sqlalchemy.dialects.sqlite import INTEGER
from sqlalchemy.dialects.sqlite import TEXT
from sqlalchemy.dialects.sqlite import REAL
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import relationship


class Parent(Base):
    __tablename__ = 'parent'


    id = Column(INTEGER, primary_key=True)
    name = Column(TEXT, nullable=True, default=None)
    age = Column(INTEGER, nullable=True, default=None)
    height = Column(REAL, nullable=True, default=None)
    is_active = Column(BLOB, nullable=True, default=None)


    children_Child = relationship("Child", back_populates="parent_Parent", lazy="joined")
    
    def __str__(self):

        return (f'User(id={self.id},'
			f'name={self.name},'
			f'age={self.age},'
			f'height={self.height},'
			f'is_active={self.is_active})')

