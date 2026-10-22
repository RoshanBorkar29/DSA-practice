from abc import ABC,abstractmethod
from dataclasses import dataclass


@dataclass
class Address:
    street:str
    city:str
    state:str
    pincode:str

class InvalidPriceError(Exception):
    pass

class InsufficientStockError(Exception):
    pass


class InvalidQuantityError(Exception):
    pass



class Product(ABC):
    store_name="ABC Store"
    total_products=0
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        Product.total_products += 1

    def __str__(self):
        return f"{self.name}-${self.price}"

    @abstractmethod
    def get_product_type(self):
        pass

    @abstractmethod
    def get_delivery_info(self):
        pass

    @property
    def price(self):
        return self._price## it is use to retrun teh price getter method we can call

    @price.setter
    def price(self, value):
        if value<=0:
            raise InvalidPriceError("Price must be greater than 0")
        self._price = value

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        if value < 0:
            raise InvalidQuantityError("Stock cannot be negative")
        self._stock = value

    
    def display_details(self):
        print(f"Product ID: {self.product_id}")
        print(f"Product Name: {self.name}")
        print(f"Price: ₹{self.price}")
        print(f"Stock: {self.stock}")

    def add_stock(self, quantity):
        if quantity <= 0:
            raise InvalidQuantityError("Quantity must be greater that 0")
            return

        self.stock += quantity
        print(f"Stock added successfully! Current stock: {self.stock}")

    def remove_stock(self, quantity):
        if quantity <= 0:
           raise InvalidQuantityError("Quantity must be greater that 0")
           return

        if quantity > self.stock:
            raise InsufficientStockError("Not enough stock available")
            return

        self.stock -= quantity
        print(f"Stock removed successfully! Current stock: {self.stock}")

    @classmethod
    def from_string(cls,data):
        product_id, name, price, stock = data.split(",")
        return cls(product_id, name, int(price), int(stock))
        

class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock,weight):
        self.weight=weight
        super().__init__(product_id, name, price, stock)

    def get_product_type(self):
        return "Physical product"

    def get_delivery_info(self):
        return "Must be shipped in 3 business days"

    def display_details(self):
        super().display_details()
        print(f"Weight: {self.weight} kg")
    
class DigitalProduct(Product):
    def __init__(self,product_id,name,price,stock,file_size):
        self.file_size=file_size
        super().__init__(product_id,name,price,stock)
        
    def get_product_type(self):
        return "Digital product"
    
    def get_delivery_info(self):
            return "Avalible for instant download"
    
    def display_details(self):
        super().display_details()
        print(f"File Size: {self.file_size} MB")

class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def increase_quantity(self, quantity):
        if quantity <= 0:
            print("Invalid quantity!")
            return

        self.quantity += quantity

    def decrease_quantity(self, quantity):
        if quantity <= 0 or quantity > self.quantity:
            print("Invalid quantity!")
            return

        self.quantity -= quantity

    def get_subtotal(self):
        return self.product.price * self.quantity


class Cart:
    def __init__(self):
        self.items = []

    def add_product(self, product, quantity):
        if quantity <= 0:
            raise InvalidQuantityError("Quantity must be greater than 0")

        if quantity > product.stock:
            raise InsufficientStockError("Not enough stock available")

        cart_item = CartItem(product, quantity)
        self.items.append(cart_item)

    def remove_product(self, product):
        for item in self.items:
            if item.product == product:
                self.items.remove(item)
                print("Product removed from cart!")
                return

        print("Product not present in cart!")

    def calculate_total(self):
        total = 0

        for item in self.items:
            total += item.get_subtotal()

        return total

    def display_cart(self):
        if not self.items:
            print("Cart is empty!")
            return

        print("\n----- CART -----")

        for item in self.items:
            print(f"Product: {item.product.name}")
            print(f"Price: ₹{item.product.price}")
            print(f"Quantity: {item.quantity}")
            print(f"Subtotal: ₹{item.get_subtotal()}")
            print("----------------")

        print(f"Total: ₹{self.calculate_total()}")


class Customer:
    def __init__(self, customer_id, name, email, cart):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.cart = cart

    def display_details(self):
        print(f"Customer ID: {self.customer_id}")
        print(f"Customer Name: {self.name}")
        print(f"Customer Email: {self.email}")


# -----------------------------
# Creating Products
# -----------------------------

product1 = PhysicalProduct(
    "P101",
    "Mechanical Keyboard",
    2500,
    20,
    0.8
)


product2 = PhysicalProduct(
    "P102",
    "Wireless Mouse",
    1000,
    15,
    0.1
)

product3 = DigitalProduct(
    "P103",
    "Python file",
    1200,
    20,
    5
)

product3.display_details()

# -----------------------------
# Creating Cart
# -----------------------------

cart1 = Cart()


# Add products to cart
cart1.add_product(product1, 2)
cart1.add_product(product2, 3)
cart1.add_product(product3,1)

# -----------------------------
# Creating Customer
# # -----------------------------


customer1 = Customer(
    "C101",
    "RON",
    "ron@gmail.com",
    cart1
)


# -----------------------------
# Display
# -----------------------------

customer1.display_details()

print()

product1.display_details()

print()

cart1.display_cart()
print(Product.store_name)
print(Product.total_products)


product=[
    product1,product2,product3

]

for p in product:
    print(p.get_product_type())

try:
    product1.price=500
except (InvalidPriceError) as Error:
    print(f"Could not add product:{Error}")

print(product1)
print(product2)
print(product3)
print(isinstance(product1,DigitalProduct))
