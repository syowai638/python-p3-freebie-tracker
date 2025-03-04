from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Company, Dev, Freebie

# Create a database engine
engine = create_engine('sqlite:///freebies.db')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data
session.query(Company).delete()
session.query(Dev).delete()
session.query(Freebie).delete()
session.commit()

# Create companies
safaricom = Company(name="Safaricom", founding_year=1997)
eabl = Company(name="East Africa Breweries", founding_year=1922)
deloitte = Company(name="Deloitte", founding_year=1845)
nmg = Company(name="Nation Media Group", founding_year=1959)

# Create developers
linda = Dev(name="Linda")
alvin = Dev(name="Alvin")
lorna = Dev(name="Lorna")
judy = Dev(name="Judy")

# Add companies and devs to session
session.add_all([safaricom, eabl, deloitte, nmg, linda, alvin, lorna, judy])
session.commit()

# Create freebies
tshirt = Freebie(item_name="T-Shirt", value=10, dev=linda, company=safaricom)
mug = Freebie(item_name="Mug", value=5, dev=alvin, company=eabl)
sticker = Freebie(item_name="Sticker", value=2, dev=lorna, company=deloitte)
notebook = Freebie(item_name="Notebook", value=15, dev=judy, company=nmg)

# Add freebies to session
session.add_all([tshirt, mug, sticker, notebook])
session.commit()

# Print test data
print("Seed data added successfully!")

# Verify relationships
print(f"{linda.name} has freebies from: {[company.name for company in linda.companies]}")
print(f"Oldest company: {Company.oldest_company(session).name}")
print(f"{tshirt.print_details()}")

# Close the session
session.close()
