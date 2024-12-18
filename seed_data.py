from app import create_app, db
from app.models import Product
from datetime import datetime

app = create_app()

with app.app_context():
    # Очистим старые товары (опционально, если хотите начать с чистого листа)
    Product.query.delete()
    db.session.commit()

    products = [
        Product(name="Aurora Linen Lounge Chair", category="chair", color="beige", material="fabric", price=179.00, image_url="https://source.unsplash.com/featured/?chair", created_at=datetime.utcnow()),
        Product(name="Granite Frame Wooden Armchair", category="chair", color="dark brown", material="wood", price=249.00, image_url="https://source.unsplash.com/featured/?armchair", created_at=datetime.utcnow()),
        Product(name="Skyfall Velvet Accent Chair", category="chair", color="teal", material="fabric", price=199.00, image_url="https://source.unsplash.com/featured/?velvetchair", created_at=datetime.utcnow()),
        Product(name="Cinder Modern Metal Stool", category="chair", color="black", material="metal", price=89.99, image_url="https://source.unsplash.com/featured/?metalstool", created_at=datetime.utcnow()),
        Product(name="Meadow Wicker Dining Chair", category="chair", color="light brown", material="wicker", price=129.00, image_url="https://source.unsplash.com/featured/?diningchair", created_at=datetime.utcnow()),
        Product(name="Serenity White Plastic Chair", category="chair", color="white", material="plastic", price=49.99, image_url="https://source.unsplash.com/featured/?plasticchair", created_at=datetime.utcnow()),

        Product(name="Verona Oak Dining Table", category="table", color="oak", material="wood", price=499.00, image_url="https://source.unsplash.com/featured/?diningtable", created_at=datetime.utcnow()),
        Product(name="Crystal Glass Coffee Table", category="table", color="clear", material="glass", price=299.00, image_url="https://source.unsplash.com/featured/?coffeetable", created_at=datetime.utcnow()),
        Product(name="Lunar White Work Desk", category="table", color="white", material="wood", price=199.00, image_url="https://source.unsplash.com/featured/?desk", created_at=datetime.utcnow()),
        Product(name="Cast Iron Bistro Table", category="table", color="black", material="metal", price=220.00, image_url="https://source.unsplash.com/featured/?bistrotable", created_at=datetime.utcnow()),
        Product(name="Marina Blue Side Table", category="table", color="blue", material="wood", price=150.00, image_url="https://source.unsplash.com/featured/?sidetable", created_at=datetime.utcnow()),
        Product(name="Sienna Rustic Kitchen Table", category="table", color="brown", material="wood", price=399.00, image_url="https://source.unsplash.com/featured/?kitchentable", created_at=datetime.utcnow()),

        Product(name="Milano Grey Velvet Sofa", category="sofa", color="grey", material="fabric", price=999.00, image_url="https://source.unsplash.com/featured/?sofa", created_at=datetime.utcnow()),
        Product(name="Opal Leather Chesterfield Sofa", category="sofa", color="brown", material="leather", price=1299.00, image_url="https://source.unsplash.com/featured/?leathersofa", created_at=datetime.utcnow()),
        Product(name="Emerald Green Sectional Sofa", category="sofa", color="green", material="fabric", price=1199.00, image_url="https://source.unsplash.com/featured/?sectionalsofa", created_at=datetime.utcnow()),
        Product(name="Blossom Blue Loveseat", category="sofa", color="blue", material="fabric", price=850.00, image_url="https://source.unsplash.com/featured/?loveseat", created_at=datetime.utcnow()),
        Product(name="Snowflake White Modular Sofa", category="sofa", color="white", material="fabric", price=1100.00, image_url="https://source.unsplash.com/featured/?modularsofa", created_at=datetime.utcnow()),
        Product(name="Onyx Black Leather Recliner Sofa", category="sofa", color="black", material="leather", price=2000.00, image_url="https://source.unsplash.com/featured/?reclinersofa", created_at=datetime.utcnow()),

        Product(name="Hampton King Oak Bedframe", category="bed", color="oak", material="wood", price=799.00, image_url="https://source.unsplash.com/featured/?bed", created_at=datetime.utcnow()),
        Product(name="Crystal White Upholstered Bed", category="bed", color="white", material="fabric", price=899.00, image_url="https://source.unsplash.com/featured/?upholsteredbed", created_at=datetime.utcnow()),
        Product(name="Tuscan Metal Platform Bed", category="bed", color="black", material="metal", price=699.00, image_url="https://source.unsplash.com/featured/?metalbed", created_at=datetime.utcnow()),
        Product(name="Desert Brown Leather Bed", category="bed", color="brown", material="leather", price=1299.00, image_url="https://source.unsplash.com/featured/?leatherbed", created_at=datetime.utcnow()),
        Product(name="Leafy Green Canopy Bed", category="bed", color="green", material="wood", price=1499.00, image_url="https://source.unsplash.com/featured/?canopybed", created_at=datetime.utcnow()),
        Product(name="Polar Grey Storage Bed", category="bed", color="grey", material="wood", price=999.00, image_url="https://source.unsplash.com/featured/?storagebed", created_at=datetime.utcnow()),

        Product(name="Breeze Blue Fabric Bench", category="bench", color="blue", material="fabric", price=220.00, image_url="https://source.unsplash.com/featured/?bench", created_at=datetime.utcnow()),
        Product(name="Harbor Brown Wooden Bench", category="bench", color="brown", material="wood", price=180.00, image_url="https://source.unsplash.com/featured/?woodenbench", created_at=datetime.utcnow()),
        Product(name="Aurora White Leather Bench", category="bench", color="white", material="leather", price=320.00, image_url="https://source.unsplash.com/featured/?leatherbench", created_at=datetime.utcnow()),
        Product(name="Slate Grey Outdoor Metal Bench", category="bench", color="grey", material="metal", price=150.00, image_url="https://source.unsplash.com/featured/?outdoorbench", created_at=datetime.utcnow()),
        Product(name="Marble Top Entryway Bench", category="bench", color="white", material="stone", price=400.00, image_url="https://source.unsplash.com/featured/?marblebench", created_at=datetime.utcnow()),
        Product(name="Rustic Green Garden Bench", category="bench", color="green", material="wood", price=199.00, image_url="https://source.unsplash.com/featured/?gardenbench", created_at=datetime.utcnow()),
    ]

    db.session.add_all(products)
    db.session.commit()

    print("30 тестовых товаров добавлены!")
