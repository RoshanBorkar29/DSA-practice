from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


# ============================================================
# CUSTOM EXCEPTIONS
# ============================================================

class InvalidPriceError(Exception):
    pass


class InsufficientStockError(Exception):
    pass


class InvalidQuantityError(Exception):
    pass


class ItemUnavailableError(Exception):
    pass


class EmptyCartError(Exception):
    pass


class InvalidOrderTransitionError(Exception):
    pass

class PaymentFailedError(Exception):
    pass


class InvalidPaymentTransitionError(Exception):
    pass

class DeliveryPartnerBusyError(Exception):
    pass
# ============================================================
# CART ITEM
# ============================================================

class CartItem:

    def __init__(self, item, quantity):
        self.item = item
        self.quantity = quantity

    def add_quantity(self, quantity):

        if quantity <= 0:
            raise InvalidQuantityError(
                "Quantity must be greater than 0"
            )

        self.quantity += quantity

    def sub_quantity(self, quantity):

        if quantity <= 0:
            raise InvalidQuantityError(
                "Quantity must be greater than 0"
            )

        if quantity > self.quantity:
            raise InvalidQuantityError(
                "Cannot reduce quantity below 0"
            )

        self.quantity -= quantity

    def get_subtotal(self):

        return self.item[0] * self.quantity


# ============================================================
# CART
# ============================================================

class Cart:

    def __init__(self):
        self.items = []

    def add_item(self, item, quantity):

        if quantity <= 0:
            raise InvalidQuantityError(
                "Quantity must be greater than 0"
            )

        # item = [price, category, availability]

        if not item[2]:
            raise ItemUnavailableError(
                "Item is currently unavailable"
            )

        # If item already exists in cart
        for cart_item in self.items:

            if cart_item.item == item:

                cart_item.add_quantity(quantity)
                return

        # Otherwise create new CartItem
        cart_item = CartItem(
            item,
            quantity
        )

        self.items.append(cart_item)

    def remove_item(self, item):

        for cart_item in self.items:

            if cart_item.item == item:

                self.items.remove(cart_item)

                print("Item removed!!")
                return

        print("Item not present!!")

    def increase_quantity(self, item, quantity):

        for cart_item in self.items:

            if cart_item.item == item:

                cart_item.add_quantity(quantity)
                return

        print("Item not present!!")

    def decrease_quantity(self, item, quantity):

        for cart_item in self.items:

            if cart_item.item == item:

                cart_item.sub_quantity(quantity)

                if cart_item.quantity == 0:
                    self.items.remove(cart_item)

                return

        print("Item not present!!")

    def clear(self):

        self.items.clear()

    def calculate_total(self):

        total = 0

        for cart_item in self.items:

            total += cart_item.get_subtotal()

        return total

    def __len__(self):

        return len(self.items)


# ============================================================
# USER
# ============================================================

class User(ABC):

    def __init__(
        self,
        userId,
        name,
        no,
        email
    ):

        self.userId = userId
        self.name = name
        self.no = no
        self.email = email

    @abstractmethod
    def user_type(self):
        pass


# ============================================================
# ORDER ITEM
# ============================================================

class OrderItem:

    def __init__(
        self,
        item,
        quantity,
        price
    ):

        self.item = item
        self.quantity = quantity

        # Price at the time of ordering
        self.price = price

    def get_subtotal(self):

        return self.price * self.quantity


# ============================================================
# ORDER
# ============================================================

class Order:

    # Valid transitions
    VALID_TRANSITIONS = {

        "PLACED": [
            "CONFIRMED",
            "CANCELLED"
        ],

        "CONFIRMED": [
            "PREPARING",
            "CANCELLED"
        ],

        "PREPARING": [
            "READY_FOR_PICKUP"
        ],

        "READY_FOR_PICKUP": [
            "OUT_FOR_DELIVERY"
        ],

        "OUT_FOR_DELIVERY": [
            "DELIVERED"
        ],

        "DELIVERED": [],

        "CANCELLED": []
    }

    def __init__(
        self,
        orderId,
        customer,
        restaurant,
        order_items,
        notification,
        payment
    ):

        self.order_id = orderId
        self.customer = customer
        self.restaurant = restaurant
        self.order_items = order_items

        self.order_time = datetime.now()

        self.status = "PLACED"
        self.notification=notification
        self.payment=payment

    # --------------------------------------------------------
    # Calculate total
    # --------------------------------------------------------

    def calculate_total(self):

        total = 0

        for item in self.order_items:

            total += item.get_subtotal()

        return total

    # --------------------------------------------------------
    # Change order status
    # --------------------------------------------------------

    def update_status(self, new_status):

        if new_status not in self.VALID_TRANSITIONS[self.status]:

            raise InvalidOrderTransitionError(
                f"Cannot change order status "
                f"from {self.status} to {new_status}"
            )

        self.status = new_status

        print(
            f"Order {self.order_id} status changed "
            f"to {self.status}"
        )
        self.notification.send(f"Order{self.order_id}is now {self.status}")

    # --------------------------------------------------------
    # Display order
    # --------------------------------------------------------

    def display_order(self):

        print("\n========== ORDER ==========")

        print(
            f"Order ID: {self.order_id}"
        )

        print(
            f"Restaurant: {self.restaurant.name}"
        )

        print(
            f"Customer: {self.customer.name}"
        )

        print(
            f"Status: {self.status}"
        )

        print(
            f"Order Time: {self.order_time}"
        )

        print("\nItems:")

        for item in self.order_items:

            print(
                f"Item: {item.item[3]} | "
                f"Price: ₹{item.price} | "
                f"Qty: {item.quantity} | "
                f"Subtotal: ₹{item.get_subtotal()}"
            )

        print("---------------------------")

        print(
            f"Total: ₹{self.calculate_total()}"
        )


# ============================================================
# CUSTOMER
# ============================================================

class Customer(User):

    def __init__(
        self,
        userId,
        name,
        no,
        email,
        address,
        cart
    ):

        self.address = address
        self.cart = cart

        self.orders = []

        super().__init__(
            userId,
            name,
            no,
            email
        )

    def user_type(self):

        return "User Type is Customer"

    # --------------------------------------------------------
    # Add item
    # --------------------------------------------------------

    def add_item(
        self,
        item,
        quantity
    ):

        self.cart.add_item(
            item,
            quantity
        )

    # --------------------------------------------------------
    # Remove item
    # --------------------------------------------------------

    def remove_item(self, item):

        self.cart.remove_item(item)

    # --------------------------------------------------------
    # Browse restaurant
    # --------------------------------------------------------

    def browse_restaurants(self, restaurant):

        restaurant.display_menu()

    # --------------------------------------------------------
    # Place order
    # --------------------------------------------------------

    def place_order(
        self,
        order_id,
        restaurant,
        payment,notification
    ):

        if len(self.cart) == 0:

            raise EmptyCartError(
                "Cart is empty. Add something "
                "to place an order!"
            )

        order_items = []

        # Convert CartItem → OrderItem
        for cart_item in self.cart.items:

            # Check availability again
            if not cart_item.item[2]:

                raise ItemUnavailableError(
                    f"{cart_item.item[3]} "
                    "is no longer available"
                )

            order_item = OrderItem(

                item=cart_item.item,

                quantity=cart_item.quantity,

                # Save current price
                price=cart_item.item[0]
            )

            order_items.append(order_item)

        # Create Order
        order = Order(

            orderId=order_id,

            customer=self,

            restaurant=restaurant,

            order_items=order_items,
            notification=notification,
            payment=payment
        )

        # Save order
        self.orders.append(order)
        payment.pay()

        # Clear cart
        self.cart.clear()

        print(
            f"Order {order_id} placed successfully!!"
        )

        return order

    # --------------------------------------------------------
    # Cancel order
    # --------------------------------------------------------

    def cancel_order(self, order,payment):

        payment.refund()
        order.update_status("CANCELLED")

    # --------------------------------------------------------
    # Previous orders
    # --------------------------------------------------------

    def view_previous_orders(self):

        if not self.orders:

            print("No previous orders")
            return

        print(
            "\n========== ORDER HISTORY =========="
        )

        for order in self.orders:

            print(
                f"Order ID: {order.order_id} | "
                f"Restaurant: {order.restaurant.name} | "
                f"Status: {order.status} | "
                f"Amount: ₹{order.calculate_total()}"
            )


# ============================================================
# RESTAURANT
# ============================================================

class Restaurant(User):

    def __init__(
        self,
        userId,
        name,
        no,
        email,
        typeOfRestaurant
    ):

        self.typeOfRestaurant = typeOfRestaurant

        # item -> [price, category, availability, name]
        self.menu = {}

        # order_id -> Order
        self.incoming_orders = {}

        super().__init__(
            userId,
            name,
            no,
            email
        )

    def user_type(self):

        return "User type is Restaurant!!"

    # --------------------------------------------------------
    # Display menu
    # --------------------------------------------------------

    def display_menu(self):

        print(
            "\n" + "=" * 20 +
            " MENU " +
            "=" * 20
        )

        if not self.menu:

            print("Menu is empty")
            return

        for item, details in self.menu.items():

            price = details[0]
            category = details[1]
            availability = details[2]
            name = details[3]

            print(
                f"Item: {name} | "
                f"Price: ₹{price} | "
                f"Category: {category} | "
                f"Available: {availability}"
            )

    # --------------------------------------------------------
    # Add menu item
    # --------------------------------------------------------

    def add_menu_items(
        self,
        item,
        price,
        typeOfItem
    ):

        if price <= 0:

            raise InvalidPriceError(
                "Price can't be zero or negative!!"
            )

        # price
        # category
        # availability
        # name

        self.menu[item] = [
            price,
            typeOfItem,
            True,
            item
        ]

        print(
            "Item added to menu!!"
        )

    # --------------------------------------------------------
    # Remove menu item
    # --------------------------------------------------------

    def remove_menu_items(self, item):

        if item in self.menu:

            del self.menu[item]

            print(
                "Item removed from menu!!"
            )

            return

        print(
            "Item not present in menu!!"
        )

    # --------------------------------------------------------
    # Change price
    # --------------------------------------------------------

    def change_item_price(
        self,
        item,
        new_price
    ):

        if new_price <= 0:

            raise InvalidPriceError(
                "Price can't be zero or negative!!"
            )

        if item in self.menu:

            self.menu[item][0] = new_price

            print(
                "Price changed!!"
            )

            return

        print(
            "Item not present in menu!!"
        )

    # --------------------------------------------------------
    # Change availability
    # --------------------------------------------------------

    def change_item_availability(
        self,
        item,
        status
    ):

        if item not in self.menu:

            print(
                "Item not present in menu!!"
            )

            return

        self.menu[item][2] = status

        print(
            f"Item availability changed to {status}"
        )

    # --------------------------------------------------------
    # Incoming orders
    # --------------------------------------------------------

    def add_incoming_order(self, order):

        self.incoming_orders[
            order.order_id
        ] = order

    def view_incoming_orders(self):

        if len(self.incoming_orders) == 0:

            print(
                "No orders placed till now!!"
            )

            return

        print(
            "\n========== INCOMING ORDERS =========="
        )

        for order_id, order in self.incoming_orders.items():

            print(
                f"Order ID: {order_id} | "
                f"Customer: {order.customer.name} | "
                f"Status: {order.status} | "
                f"Amount: ₹{order.calculate_total()}"
            )


# ============================================================
# DELIVERY PARTNER
# ============================================================

class DeliveryAgent(User):

    def __init__(
        self,
        userId,
        name,
        no,
        email
    ):

        self.available=True
        self.current_order=None
        self.ordersDelivered =[]
        super().__init__(
            userId,
            name,
            no,
            email
        )

    def user_type(self):

        return "User type is Delivery Agent!!"

    def accept_delivery(self,order):
        if not self.available:
            raise DeliveryPartnerBusyError(
            "Delivery partner already has an active order"
        )
        if order.status!="READY_FOR_PICKUP":
            print(
            "Order is not ready for pickup"
                )

            return
        self.current_order=order
        self.available=False
        order.update_status(
        "OUT_FOR_DELIVERY"
    )

        print(
            f"Order {order.order_id} accepted for delivery!"
        )
    

    def reject_delivery(self,order):
        if order.status != "READY_FOR_PICKUP":

            print(
                "Order is not available for delivery"
            )

            return

        print(
            f"Order {order.order_id} rejected"
        )
        

    def view_available_orders_to_pick(
        self,
        orders,
    ):
        print("\n========== AVAILABLE ORDERS ==========")
        found=False
        for order in orders:
            if order.status=="READY_FOR_PICKUP":
                print(
                f"Order ID: {order.order_id} | "
                f"Restaurant: {order.restaurant.name} | "
                f"Customer: {order.customer.name}"
            )

            found = True
        if not found:
            print("NO orders avaliblae for pickup")



    def complete_delivery(
        self,
        
    ):
        if self.current_order is None:
            print("No active delivery.")
        order=self.current_order
        if order.status != "OUT_FOR_DELIVERY":

            print(
                "Order is not currently out for delivery."
            )

            return
        order.update_status("DELIVERED")
        self.ordersDelivered.append(order)
        self.current_order=None
        self.available=True

    

class Payment(ABC):
    VALID_TRANSITIONS = {

        "PENDING": [
            "SUCCESS",
            "FAILED"
        ],

        "SUCCESS": [
            "REFUNDED"
        ],

        "FAILED": [],

        "REFUNDED": []
    }

    def __init__(self,payment_id,amount):
        self.payment_id=payment_id
        self.amount=amount
        self.status="PENDING"

    @abstractmethod
    def pay(self):
        pass
    @abstractmethod
    def refund(self):
        pass

    def update_status(self,new_status):
        if new_status not in self.VALID_TRANSITIONS[self.status]:
            raise InvalidPaymentTransitionError(
            f"Cannot change payment status "
            f"from {self.status} to {new_status}"
        )
        self.status=new_status



class UPIPayment(Payment):

    def __init__(self, payment_id, amount, upi_id):
        super().__init__(payment_id, amount)
        self.upi_id = upi_id

    def pay(self):
        print(f"Payment of ₹{self.amount} using UPI")
        self.update_status("SUCCESS")

    def refund(self):
        print(f"Refunding ₹{self.amount}")
        self.update_status("REFUNDED")


class CardPayment(Payment):

    def __init__(
        self,
        payment_id,
        amount,
        card_number
    ):

        super().__init__(
            payment_id,
            amount
        )

        self.card_number = card_number

    def pay(self):

        self.update_status("SUCCESS")

        print(
            f"Card payment successful: ₹{self.amount}"
        )

    def refund(self):

        self.update_status("REFUNDED")

        print(
            f"Card payment refunded: ₹{self.amount}"
        )


class WalletPayment(Payment):

    def __init__(
        self,
        payment_id,
        amount,
        wallet_name
    ):

        super().__init__(
            payment_id,
            amount
        )

        self.wallet_name = wallet_name

    def pay(self):

        self.update_status("SUCCESS")

        print(
            f"Wallet payment successful: ₹{self.amount}"
        )

    def refund(self):

        self.update_status("REFUNDED")

        print(
            f"Wallet payment refunded: ₹{self.amount}"
        )


class Notification(ABC):

    @abstractmethod
    def send(self, message):
        pass

class EmailNotification(Notification):

    def __init__(self, email):
        self.email = email

    def send(self, message):

        print(
            f"Email sent to {self.email}: {message}"
        )


# ============================================================
# MOCK DATA / TESTING
# ============================================================

print("\n\n")
print("=" * 70)
print("                 FOOD DELIVERY SYSTEM")
print("=" * 70)


# ============================================================
# 1. CREATE CUSTOMER
# ============================================================

customer = Customer(
    userId="C101",
    name="Ron",
    no="9876543210",
    email="ron@gmail.com",
    address="Wakad, Pune",
    cart=Cart()
)


# ============================================================
# 2. CREATE RESTAURANT
# ============================================================

restaurant = Restaurant(
    userId="R101",
    name="Food Palace",
    no="9876500000",
    email="foodpalace@gmail.com",
    typeOfRestaurant="Fast Food"
)


# ============================================================
# 3. ADD MENU ITEMS
# ============================================================

restaurant.add_menu_items(
    "Burger",
    150,
    "Burger"
)

restaurant.add_menu_items(
    "Pizza",
    300,
    "Pizza"
)

restaurant.add_menu_items(
    "Coke",
    50,
    "Beverage"
)

restaurant.add_menu_items(
    "Biryani",
    250,
    "Main Course"
)


# ============================================================
# 4. DISPLAY RESTAURANT MENU
# ============================================================

print("\n")
restaurant.display_menu()


# ============================================================
# 5. CUSTOMER BROWSES RESTAURANT
# ============================================================

print("\n")
customer.browse_restaurants(restaurant)


# ============================================================
# 6. GET ITEMS FROM RESTAURANT MENU
# ============================================================

burger = restaurant.menu["Burger"]
pizza = restaurant.menu["Pizza"]
coke = restaurant.menu["Coke"]


# ============================================================
# 7. ADD ITEMS TO CART
# ============================================================

customer.add_item(burger, 2)
customer.add_item(pizza, 1)
customer.add_item(coke, 2)


# ============================================================
# 8. DISPLAY CART
# ============================================================

print("\n")
print("=" * 30)
print("CART")
print("=" * 30)

for cart_item in customer.cart.items:

    print(
        f"Item: {cart_item.item[3]} | "
        f"Quantity: {cart_item.quantity} | "
        f"Price: ₹{cart_item.item[0]} | "
        f"Subtotal: ₹{cart_item.get_subtotal()}"
    )

print(
    f"Cart Total: ₹{customer.cart.calculate_total()}"
)


# ============================================================
# 9. CREATE PAYMENT
# ============================================================

payment = UPIPayment(
    payment_id="PAY101",
    amount=customer.cart.calculate_total(),
    upi_id="ron@upi"
)


# ============================================================
# 10. CREATE NOTIFICATION
# ============================================================

notification = EmailNotification(
    customer.email
)


# ============================================================
# 11. PLACE ORDER
# ============================================================

print("\n")
print("=" * 30)
print("PLACING ORDER")
print("=" * 30)

order = customer.place_order(
    order_id="ORD101",
    restaurant=restaurant,
    payment=payment,
    notification=notification
)


# ============================================================
# 12. RESTAURANT RECEIVES ORDER
# ============================================================

restaurant.add_incoming_order(order)

print("\n")
restaurant.view_incoming_orders()


# ============================================================
# 13. DISPLAY ORDER
# ============================================================

print("\n")
order.display_order()


# ============================================================
# 14. PAYMENT STATUS
# ============================================================

print("\n")
print(
    f"Payment Status: {payment.status}"
)


# ============================================================
# 15. RESTAURANT CONFIRMS ORDER
# ============================================================

print("\n")
print("=" * 30)
print("ORDER CONFIRMATION")
print("=" * 30)

order.update_status("CONFIRMED")


# ============================================================
# 16. RESTAURANT STARTS PREPARING
# ============================================================

order.update_status("PREPARING")


# ============================================================
# 17. FOOD READY
# ============================================================

order.update_status("READY_FOR_PICKUP")


# ============================================================
# 18. CREATE DELIVERY PARTNER
# ============================================================

delivery_agent = DeliveryAgent(
    userId="D101",
    name="Amit",
    no="9876123456",
    email="amit@gmail.com"
)


# ============================================================
# 19. DELIVERY PARTNER VIEWS AVAILABLE ORDERS
# ============================================================

print("\n")
delivery_agent.view_available_orders_to_pick(
    restaurant.incoming_orders.values()
)


# ============================================================
# 20. DELIVERY PARTNER ACCEPTS ORDER
# ============================================================

print("\n")
delivery_agent.accept_delivery(order)


# ============================================================
# 21. COMPLETE DELIVERY
# ============================================================

print("\n")
delivery_agent.complete_delivery()


# ============================================================
# 22. FINAL ORDER STATUS
# ============================================================

print("\n")
print("=" * 30)
print("FINAL ORDER")
print("=" * 30)

order.display_order()


# ============================================================
# 23. FINAL PAYMENT STATUS
# ============================================================

print("\n")
print(
    f"Payment Status: {payment.status}"
)


# ============================================================
# 24. CUSTOMER ORDER HISTORY
# ============================================================

print("\n")
customer.view_previous_orders()


# ============================================================
# 25. DELIVERY PARTNER STATUS
# ============================================================

print("\n")
print(
    f"Delivery Partner Available: "
    f"{delivery_agent.available}"
)

print(
    f"Orders Delivered: "
    f"{len(delivery_agent.ordersDelivered)}"
)