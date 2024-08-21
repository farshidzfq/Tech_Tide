from app import app, db
from models import Product, User

def create_sample_data():
    # Create the database and tables
    with app.app_context():
        db.create_all()

        # Clear existing data
        Product.query.delete()
        User.query.delete()

        # Create sample products
        products = [
            {'name': 'Laptop', 'price': 999.99},
            {'name': 'Smartphone', 'price': 499.99},
            {'name': 'Headphones', 'price': 149.99},
            {'name': 'Smartwatch', 'price': 199.99},
            {'name': 'Keyboard', 'price': 49.99},
            {'name': 'Mouse', 'price': 29.99},
            {'name': 'Monitor', 'price': 249.99},
            {'name': 'Printer', 'price': 89.99}
        ]

        # Add products to the database
        for item in products:
            product = Product(name=item['name'], price=item['price'])
            db.session.add(product)

        # Create a sample user (optional for testing)
        user = User(username='testuser', email='testuser@example.com', password='password')
        db.session.add(user)

        # Commit changes
        db.session.commit()

        print("Sample data added successfully.")

if __name__ == '__main__':
    create_sample_data()
