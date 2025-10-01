"""
Datos de prueba centralizados para el framework de automatización
"""

from typing import Dict, List, Any
from config.config import Config


class TestData:
    """Clase para manejar datos de prueba centralizados"""
    
    # Usuarios de prueba
    USERS = {
        "valid_user": {
            "username": "test",
            "password": "test"
        },
        "invalid_user": {
            "username": "invalid",
            "password": "invalid"
        }
    }
    
    # Productos de prueba
    PRODUCTS = {
        "phones": [
            "Samsung galaxy s6",
            "Nokia lumia 1520",
            "Nexus 6",
            "Samsung galaxy s7",
            "Iphone 6 32gb",
            "Sony xperia z5",
            "HTC One M9"
        ],
        "laptops": [
            "Sony vaio i5",
            "Sony vaio i7",
            "MacBook air",
            "Dell i7 8gb",
            "2017 Dell 15.6 Inch",
            "MacBook Pro"
        ],
        "monitors": [
            "Apple monitor 24",
            "ASUS Full HD"
        ]
    }
    
    # Datos de checkout
    CHECKOUT_DATA = {
        "valid": {
            "name": "John Doe",
            "country": "United States",
            "city": "New York",
            "credit_card": "4111111111111111",
            "month": "12",
            "year": "2025"
        },
        "invalid_card": {
            "name": "Jane Smith",
            "country": "Canada",
            "city": "Toronto",
            "credit_card": "1234567890123456",
            "month": "13",
            "year": "2020"
        }
    }
    
    # Mensajes esperados
    MESSAGES = {
        "login_success": "Welcome test",
        "login_error": "Wrong password.",
        "product_added": "Product added",
        "order_success": "Thank you for your purchase!",
        "order_error": "Please fill out Name and Creditcard."
    }
    
    # URLs de navegación
    URLS = {
        "home": "https://www.demoblaze.com/",
        "cart": "https://www.demoblaze.com/cart.html",
        "login_modal": "https://www.demoblaze.com/#"
    }
    
    # Selectores comunes
    SELECTORS = {
        "login_modal": {
            "username_input": "loginusername",
            "password_input": "loginpassword",
            "login_button": "//button[text()='Log in']",
            "close_button": "//button[text()='Close']"
        },
        "navigation": {
            "home_link": "//a[text()='Home ']",
            "cart_link": "//a[text()='Cart']",
            "logout_link": "//a[text()='Log out']"
        },
        "products": {
            "product_card": "//div[@class='card h-100']",
            "product_title": ".card-title",
            "product_price": ".card-text",
            "add_to_cart": "//a[text()='Add to cart']"
        }
    }
    
    @classmethod
    def get_user(cls, user_type: str = "valid_user") -> Dict[str, str]:
        """Retorna datos de usuario específicos"""
        return cls.USERS.get(user_type, cls.USERS["valid_user"])
    
    @classmethod
    def get_products(cls, category: str = "phones", count: int = 2) -> List[str]:
        """Retorna lista de productos de una categoría específica"""
        products = cls.PRODUCTS.get(category, cls.PRODUCTS["phones"])
        return products[:count]
    
    @classmethod
    def get_checkout_data(cls, data_type: str = "valid") -> Dict[str, str]:
        """Retorna datos de checkout específicos"""
        return cls.CHECKOUT_DATA.get(data_type, cls.CHECKOUT_DATA["valid"])
    
    @classmethod
    def get_expected_message(cls, message_type: str) -> str:
        """Retorna mensaje esperado específico"""
        return cls.MESSAGES.get(message_type, "")
    
    @classmethod
    def get_url(cls, page: str) -> str:
        """Retorna URL específica de una página"""
        return cls.URLS.get(page, cls.URLS["home"])
    
    @classmethod
    def get_selector(cls, section: str, element: str) -> str:
        """Retorna selector específico de un elemento"""
        return cls.SELECTORS.get(section, {}).get(element, "")
    
    @classmethod
    def get_all_products(cls) -> List[str]:
        """Retorna todos los productos disponibles"""
        all_products = []
        for category_products in cls.PRODUCTS.values():
            all_products.extend(category_products)
        return all_products
