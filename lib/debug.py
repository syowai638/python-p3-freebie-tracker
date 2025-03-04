from db import session
from models import Dev, Company, Freebie

def fetch_all_data():
    """Fetch all data from the database and display it."""
    try:
        devs = session.query(Dev).all()
        companies = session.query(Company).all()
        freebies = session.query(Freebie).all()

        print("\n=== All Developers ===")
        for dev in devs:
            print(dev)

        print("\n=== All Companies ===")
        for company in companies:
            print(company)

        print("\n=== All Freebies ===")
        for freebie in freebies:
            print(freebie)

    except Exception as e:
        print(f"Error fetching data: {e}")

def test_freebie_details():
    """Test Freebie.print_details()"""
    try:
        tshirt = session.query(Freebie).filter_by(item_name="T-Shirt").first()
        if tshirt:
            print("\n=== Freebie Details ===")
            print(tshirt.print_details())
        else:
            print("\nNo T-Shirt freebie found.")
    except Exception as e:
        print(f"Error testing Freebie.print_details: {e}")

def test_oldest_company():
    """Test Company.oldest_company()"""
    try:
        oldest_company = Company.oldest_company(session)
        if oldest_company:
            print("\n=== Oldest Company ===")
            print(f"Oldest company: {oldest_company.name} (Founded in {oldest_company.founding_year})")
        else:
            print("\nNo companies found.")
    except Exception as e:
        print(f"Error finding oldest company: {e}")

def test_dev_received_one():
    """Test Dev.received_one()"""
    try:
        linda = session.query(Dev).filter_by(name="Linda").first()
        if linda:
            print("\n=== Checking Linda's Freebies ===")
            print(f"Linda received a T-Shirt: {linda.received_one('T-Shirt')}")
            print(f"Linda received a Mug: {linda.received_one('Mug')}")
        else:
            print("\nLinda not found in database.")
    except Exception as e:
        print(f"Error checking Linda's freebies: {e}")

def test_give_freebie():
    """Test Company.give_freebie()"""
    try:
        safaricom = session.query(Company).filter_by(name="Safaricom").first()
        linda = session.query(Dev).filter_by(name="Linda").first()

        if safaricom and linda:
            print("\n=== Giving Freebie ===")
            safaricom.give_freebie(linda, "Water Bottle", 12, session)
            session.commit()
            print(f"Linda received a Water Bottle: {linda.received_one('Water Bottle')}")
        else:
            print("\nEither Safaricom or Linda was not found.")
    except Exception as e:
        session.rollback()
        print(f"Error giving freebie: {e}")

def test_give_away():
    """Test Dev.give_away()"""
    try:
        linda = session.query(Dev).filter_by(name="Linda").first()
        alvin = session.query(Dev).filter_by(name="Alvin").first()
        tshirt = session.query(Freebie).filter_by(item_name="T-Shirt").first()

        if linda and alvin and tshirt:
            print("\n=== Transferring Freebie ===")
            linda.give_away(alvin, tshirt, session)
            session.commit()
            print(f"T-Shirt now belongs to: {tshirt.dev.name}")
        else:
            print("\nEither Linda, Alvin, or the T-Shirt was not found.")
    except Exception as e:
        session.rollback()
        print(f"Error transferring freebie: {e}")

# Run all tests
if __name__ == "__main__":
    fetch_all_data()
    test_freebie_details()
    test_oldest_company()
    test_dev_received_one()
    test_give_freebie()
    test_give_away()
