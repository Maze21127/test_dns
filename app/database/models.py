from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)


class Edge(Base):
    __tablename__ = "edge"

    id = Column(Integer, primary_key=True, index=True)
    from_city_id = Column(Integer, ForeignKey("city.id"))
    to_city_id = Column(Integer, ForeignKey("city.id"))
    distance = Column(Integer)
    from_city = relationship("City", primaryjoin='Edge.from_city_id == City.id')
    to_city = relationship("City", primaryjoin='Edge.to_city_id == City.id')

    __table_args__ = (
        UniqueConstraint('from_city_id', 'to_city_id', name='_from_to_uc'),
    )

    def __repr__(self):
        return f"from {self.from_city.name} to {self.to_city.name} = {self.distance}"
