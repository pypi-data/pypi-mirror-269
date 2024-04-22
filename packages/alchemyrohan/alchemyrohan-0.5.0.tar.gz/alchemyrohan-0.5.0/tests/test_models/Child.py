

from sqlalchemy import Column
from tests.test_models import Base
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.sqlite import INTEGER
from sqlalchemy.dialects.sqlite import TEXT
from sqlalchemy.dialects.sqlite import REAL
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import relationship


class Child(Base):
    __tablename__ = 'child'


    id = Column(INTEGER, primary_key=True)
    parent_id = Column(INTEGER, ForeignKey('parent.id'), nullable=True, default=None)
    name = Column(TEXT, nullable=True, default=None)
    grade = Column(INTEGER, nullable=True, default=None)


    parent_Parent = relationship("Parent", back_populates="children_Child", lazy="joined")
    
    def __str__(self):

        return (f'User(id={self.id},'
			f'parent_id={self.parent_id},'
			f'name={self.name},'
			f'grade={self.grade})')

