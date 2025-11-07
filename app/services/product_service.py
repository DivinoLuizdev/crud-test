from app.model.models import Product, db
import requests

class ProductService:
    @staticmethod
    def create_product(data):
        product = Product(
            id=data.get("id_product"),
            name=data.get("name"),
            price=data.get("price"),
            description=data.get("description"),
            category=data.get("category"),
            image_url=data.get("image_url"),
        )
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def get_all_products():
        return Product.query.all()

    @staticmethod
    def get_product_by_id(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def update_product(product_id, data):
        product = Product.query.get(product_id)
        if not product:
            return None
        product.name = data.get("name", product.name)
        product.price = data.get("price", product.price)
        product.description = data.get("description", product.description)
        product.category = data.get("category", product.category)
        product.image_url = data.get("image_url", product.image_url)
        db.session.commit()
        return product

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return None
        db.session.delete(product)
        db.session.commit()
        return product

    # 🔍 BUSCAS AVANÇADAS
    @staticmethod
    def search_products(name=None, category=None):
        query = Product.query
        if name:
            query = query.filter(Product.name.ilike(f"%{name}%"))
        if category:
            query = query.filter(Product.category.ilike(f"%{category}%"))
        return query.all()

    @staticmethod
    def get_products_by_category(category):
        return Product.query.filter(Product.category.ilike(f"%{category}%")).all()

    @staticmethod
    def get_products_with_image(has_image=True):
        if has_image:
            return Product.query.filter(Product.image_url.isnot(None)).all()
        return Product.query.filter(Product.image_url.is_(None)).all()

    #   IMPORTAÇÃO DE PRODUTOS DE API EXTERNA
    @staticmethod
    def import_products_from_api(api_url):
        """Importa produtos da FakeStoreAPI e salva no banco"""
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            products_data = response.json()

            imported = 0
            for item in products_data:
                name = item.get("title")                    
                price = item.get("price")
                description = item.get("description")
                category = item.get("category")
                image_url = item.get("image")                 

                # Ignora produtos sem nome ou preço
                if not name or price is None:
                    continue

                # Evita duplicatas (mesmo nome)
                existing = Product.query.filter_by(name=name).first()
                if existing:
                    continue

                product = Product(
                    name=name,
                    price=price,
                    description=description or "Sem descrição",
                    category=category or "Sem categoria",
                    image_url=image_url
                )
                db.session.add(product)
                imported += 1

            db.session.commit()
            return {"message": f"{imported} produtos importados com sucesso."}, 200

        except requests.RequestException as e:
            return {"error": f"Erro ao acessar a API externa: {str(e)}"}, 500
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500