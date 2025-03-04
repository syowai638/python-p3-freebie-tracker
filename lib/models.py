from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    founding_year = Column(Integer)

    freebies = relationship('Freebie', back_populates='company', overlaps="devs,companies")
    devs = relationship('Dev', secondary='freebies', back_populates='companies', overlaps="freebies,company")

    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()

    def give_freebie(self, dev, item_name, value, session):
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        session.add(freebie)
        session.commit()

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    freebies = relationship('Freebie', back_populates='dev', overlaps="companies,company")
    companies = relationship('Company', secondary='freebies', back_populates='devs', overlaps="freebies,devs")

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie, session):
        if freebie in self.freebies:
            freebie.dev = dev
            session.commit()

    def __repr__(self):
        return f'<Dev {self.name}>'

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer)
    
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    dev = relationship('Dev', back_populates='freebies', overlaps="companies,company,devs")
    company = relationship('Company', back_populates='freebies', overlaps="devs,companies")

    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company.name}'

    def __repr__(self):
        return f'<Freebie {self.item_name}, Value: {self.value}>'
