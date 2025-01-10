import requests
from app import create_app, db
from app.models import Product
from datetime import datetime

app = create_app()

def generate_image_url(query):
    api_key = "48137281-a5c5d3942631ca08e7933d1da"  # Ваш API-ключ
    url = f"https://pixabay.com/api/?key={api_key}&q={query.replace(' ', '+')}&image_type=photo&per_page=3"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка успешности запроса
        data = response.json()
        
        if data.get("hits"):
            return data["hits"][0]["webformatURL"]  # URL первой картинки
        else:
            print(f"No images found for query: {query}")
            return "https://via.placeholder.com/600x400?text=No+Image"
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return "https://via.placeholder.com/600x400?text=Error"

with app.app_context():
    # Clear database list
    Product.query.delete()
    db.session.commit()

    products = [
        Product(name="Aurora Linen Lounge Chair", category="chair", stock_quantity=10, color="beige", material="fabric", price=179.00, image_url=generate_image_url("Aurora Linen Lounge Chair"), created_at=datetime.utcnow()),
        Product(name="Granite Frame Wooden Armchair", category="chair", stock_quantity=10, color="dark brown", material="wood", price=249.00, image_url=generate_image_url("Granite Frame Wooden Armchair"), created_at=datetime.utcnow()),
        Product(name="Skyfall Velvet Accent Chair", category="chair", stock_quantity=10, color="teal", material="fabric", price=199.00, image_url=generate_image_url("Skyfall Velvet Accent Chair"), created_at=datetime.utcnow()),
        Product(name="Cinder Modern Metal Stool", category="chair", stock_quantity=10, color="black", material="metal", price=89.99, image_url=generate_image_url("Cinder Modern Metal Stool"), created_at=datetime.utcnow()),
        Product(name="Meadow Wicker Dining Chair", category="chair", stock_quantity=10, color="light brown", material="wicker", price=129.00, image_url=generate_image_url("Meadow Wicker Dining Chair"), created_at=datetime.utcnow()),
        Product(name="Serenity White Plastic Chair", category="chair", stock_quantity=10, color="white", material="plastic", price=49.99, image_url=generate_image_url("Serenity White Plastic Chair"), created_at=datetime.utcnow()),

        Product(name="Verona Oak Dining Table", category="table", stock_quantity=10, color="oak", material="wood", price=499.00, image_url=generate_image_url("Verona Oak Dining Table"), created_at=datetime.utcnow()),
        Product(name="Crystal Glass Coffee Table", category="table", stock_quantity=10, color="clear", material="glass", price=299.00, image_url=generate_image_url("Crystal Glass Coffee Table"), created_at=datetime.utcnow()),
        Product(name="Lunar White Work Desk", category="table", stock_quantity=10, color="white", material="wood", price=199.00, image_url=generate_image_url("Lunar White Work Desk"), created_at=datetime.utcnow()),
        Product(name="Cast Iron Bistro Table", category="table", stock_quantity=10, color="black", material="metal", price=220.00, image_url=generate_image_url("Cast Iron Bistro Table"), created_at=datetime.utcnow()),
        Product(name="Marina Blue Side Table", category="table", stock_quantity=10, color="blue", material="wood", price=150.00, image_url=generate_image_url("Marina Blue Side Table"), created_at=datetime.utcnow()),
        Product(name="Sienna Rustic Kitchen Table", category="table", stock_quantity=10, color="brown", material="wood", price=399.00, image_url=generate_image_url("Sienna Rustic Kitchen Table"), created_at=datetime.utcnow()),

        Product(name="Milano Grey Velvet Sofa", category="sofa", stock_quantity=10, color="grey", material="fabric", price=999.00, image_url=generate_image_url("Milano Grey Velvet Sofa"), created_at=datetime.utcnow()),
        Product(name="Opal Leather Chesterfield Sofa", category="sofa", stock_quantity=10, color="brown", material="leather", price=1299.00, image_url=generate_image_url("Opal Leather Chesterfield Sofa"), created_at=datetime.utcnow()),
        Product(name="Emerald Green Sectional Sofa", category="sofa", stock_quantity=10, color="green", material="fabric", price=1199.00, image_url=generate_image_url("Emerald Green Sectional Sofa"), created_at=datetime.utcnow()),
        Product(name="Blossom Blue Loveseat", category="sofa", stock_quantity=10, color="blue", material="fabric", price=850.00, image_url=generate_image_url("Blossom Blue Loveseat"), created_at=datetime.utcnow()),
        Product(name="Snowflake White Modular Sofa", category="sofa", stock_quantity=10, color="white", material="fabric", price=1100.00, image_url=generate_image_url("Snowflake White Modular Sofa"), created_at=datetime.utcnow()),
        Product(name="Onyx Black Leather Recliner Sofa", category="sofa", stock_quantity=10, color="black", material="leather", price=2000.00, image_url=generate_image_url("Onyx Black Leather Recliner Sofa"), created_at=datetime.utcnow()),

        Product(name="Hampton King Oak Bedframe", category="bed", stock_quantity=10, color="oak", material="wood", price=799.00, image_url=generate_image_url("Hampton King Oak Bedframe"), created_at=datetime.utcnow()),
        Product(name="Crystal White Upholstered Bed", category="bed", stock_quantity=10, color="white", material="fabric", price=899.00, image_url=generate_image_url("Crystal White Upholstered Bed"), created_at=datetime.utcnow()),
        Product(name="Tuscan Metal Platform Bed", category="bed", stock_quantity=10, color="black", material="metal", price=699.00, image_url=generate_image_url("Tuscan Metal Platform Bed"), created_at=datetime.utcnow()),
        Product(name="Desert Brown Leather Bed", category="bed", stock_quantity=10, color="brown", material="leather", price=1299.00, image_url=generate_image_url("Desert Brown Leather Bed"), created_at=datetime.utcnow()),
        Product(name="Leafy Green Canopy Bed", category="bed", stock_quantity=10, color="green", material="wood", price=1499.00, image_url=generate_image_url("Leafy Green Canopy Bed"), created_at=datetime.utcnow()),
        Product(name="Polar Grey Storage Bed", category="bed", stock_quantity=10, color="grey", material="wood", price=999.00, image_url=generate_image_url("Polar Grey Storage Bed"), created_at=datetime.utcnow()),

        Product(name="Breeze Blue Fabric Bench", category="bench", stock_quantity=10, color="blue", material="fabric", price=220.00, image_url=generate_image_url("Breeze Blue Fabric Bench"), created_at=datetime.utcnow()),
        Product(name="Harbor Brown Wooden Bench", category="bench", stock_quantity=10, color="brown", material="wood", price=180.00, image_url=generate_image_url("Harbor Brown Wooden Bench"), created_at=datetime.utcnow()),
        Product(name="Aurora White Leather Bench", category="bench", stock_quantity=10, color="white", material="leather", price=320.00, image_url=generate_image_url("Aurora White Leather Bench"), created_at=datetime.utcnow()),
        Product(name="Slate Grey Outdoor Metal Bench", category="bench", stock_quantity=10, color="grey", material="metal", price=150.00, image_url=generate_image_url("Slate Grey Outdoor Metal Bench"), created_at=datetime.utcnow()),
        Product(name="Marble Top Entryway Bench", category="bench", stock_quantity=10, color="white", material="stone", price=400.00, image_url=generate_image_url("Marble Top Entryway Bench"), created_at=datetime.utcnow()),
        Product(name="Rustic Green Garden Bench", category="bench", stock_quantity=10, color="green", material="wood", price=199.00, image_url=generate_image_url("Rustic Green Garden Bench"), created_at=datetime.utcnow()),
    ]

    db.session.add_all(products)
    db.session.commit()

    print("30 test items were added")
