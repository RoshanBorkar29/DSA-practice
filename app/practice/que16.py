 # ============================================================
# RIDE SHARING SYSTEM
# OOP PRACTICE: CLASSES, INHERITANCE, ABSTRACTION, ENUMS,
# COMPOSITION, ASSOCIATION, POLYMORPHISM AND CUSTOM EXCEPTIONS
# ============================================================

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class VehicleType(Enum):
    BIKE = "BIKE"
    AUTO = "AUTO"
    SEDAN = "SEDAN"
    SUV = "SUV"


class RideStatus(Enum):
    REQUESTED = "REQUESTED"
    DRIVER_ASSIGNED = "DRIVER_ASSIGNED"
    ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class PaymentStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class User(ABC):

    def __init__(self, user_id, name, email, phone):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone

    @abstractmethod
    def user_type(self):
        pass


@dataclass
class Location:
    latitude: str
    longitude: str


class Vehicle:

    def __init__(self, vehicle_number, vehicle_type, capacity):
        self.vehicle_number = vehicle_number
        self.vehicle_type = vehicle_type
        self.capacity = capacity

    def display_vehicle(self):
        print(f"Vehicle Number: {self.vehicle_number}")
        print(f"Vehicle Type: {self.vehicle_type.value}")
        print(f"Capacity: {self.capacity}")


class Rider(User):

    def __init__(self, user_id, name, email, phone, location):
        self.location = location
        self.ride_history = []

        super().__init__(
            user_id,
            name,
            email,
            phone
        )

    def user_type(self):
        return "USER_TYPE-->RIDER IT IS!!"

    def request_ride(self, ride):
        self.ride_history.append(ride)
        return ride

    def cancel_ride(self, ride):
        if ride not in self.ride_history:
            raise InvalidRideStateError(
                "This ride does not belong to this rider"
            )

        ride.update_status(RideStatus.CANCELLED)

    def view_ride_history(self):
        for ride in self.ride_history:
            ride.display_ride()


class Driver(User):

    def __init__(
        self,
        user_id,
        name,
        email,
        phone,
        location,
        vehicle,
        is_available
    ):
        self.location = location
        self.vehicle = vehicle
        self.is_available = is_available
        self.ride_history = []
        self.earnings = 0

        super().__init__(
            user_id,
            name,
            email,
            phone
        )

    def user_type(self):
        return "USER_TYPE-->DRIVER HU BHAI!!"

    def accept_ride(self, ride):

        if not self.is_available:
            raise DriverUnavailableError("CANT ACCEPT!!")

        if ride.driver != self:
            raise InvalidRideStateError(
                "This ride is not assigned to this driver"
            )

        if ride.status != RideStatus.DRIVER_ASSIGNED:
            raise InvalidRideStateError(
                "Ride cannot be accepted"
            )

        self.is_available = False
        ride.update_status(RideStatus.ACCEPTED)

    def start_ride(self, ride):

        if ride.driver != self:
            raise InvalidRideStateError(
                "This ride is not assigned to this driver"
            )

        if ride.status != RideStatus.ACCEPTED:
            raise InvalidRideStateError(
                "Ride cannot be started"
            )

        ride.update_status(RideStatus.IN_PROGRESS)

    def complete_ride(self, ride):

        if ride.driver != self:
            raise InvalidRideStateError(
                "This ride is not assigned to this driver"
            )

        if ride.status != RideStatus.IN_PROGRESS:
            raise InvalidRideStateError(
                "Ride cannot be completed"
            )

        ride.update_status(RideStatus.COMPLETED)

        self.is_available = True
        self.earnings += ride.fare
        self.ride_history.append(ride)

    def view_earnings(self):
        return self.earnings

    def view_ride_history(self):
        for ride in self.ride_history:
            ride.display_ride()


class Ride:

    def __init__(
        self,
        ride_id,
        rider,
        driver,
        pickup,
        drop,
        vehicle_type,
        status,
        fare
    ):
        self.ride_id = ride_id
        self.rider = rider
        self.driver = driver
        self.pickup = pickup
        self.drop = drop
        self.vehicle_type = vehicle_type
        self.status = status
        self.fare = fare

    def calculate_fare(self):

        base_fare = 50

        if self.vehicle_type == VehicleType.BIKE:
            rate = 10

        elif self.vehicle_type == VehicleType.AUTO:
            rate = 15

        elif self.vehicle_type == VehicleType.SEDAN:
            rate = 20

        elif self.vehicle_type == VehicleType.SUV:
            rate = 25

        else:
            raise InvalidVehicleTypeError(
                "Invalid vehicle type"
            )

        distance = 10

        self.fare = base_fare + (distance * rate)

        return self.fare

    def update_status(self, new_status):

        valid_transitions = {

            RideStatus.REQUESTED: [
                RideStatus.DRIVER_ASSIGNED,
                RideStatus.CANCELLED
            ],

            RideStatus.DRIVER_ASSIGNED: [
                RideStatus.ACCEPTED,
                RideStatus.CANCELLED
            ],

            RideStatus.ACCEPTED: [
                RideStatus.IN_PROGRESS,
                RideStatus.CANCELLED
            ],

            RideStatus.IN_PROGRESS: [
                RideStatus.COMPLETED
            ],

            RideStatus.COMPLETED: [],

            RideStatus.CANCELLED: []
        }

        if new_status not in valid_transitions[self.status]:
            raise InvalidRideStateError(
                f"Cannot change ride from "
                f"{self.status.value} "
                f"to "
                f"{new_status.value}"
            )

        self.status = new_status

    def display_ride(self):

        print(f"Ride ID: {self.ride_id}")
        print(f"Rider: {self.rider.name}")

        if self.driver:
            print(f"Driver: {self.driver.name}")
        else:
            print("Driver: Not assigned")

        print(f"Pickup: {self.pickup}")
        print(f"Drop: {self.drop}")
        print(f"Vehicle: {self.vehicle_type.value}")
        print(f"Status: {self.status.value}")
        print(f"Fare: ₹{self.fare}")


class Payment(ABC):

    def __init__(self, payment_id, amount, status):
        self.payment_id = payment_id
        self.amount = amount
        self.status = status

    @abstractmethod
    def payment_type(self):
        pass

    @abstractmethod
    def pay(self):
        pass

    @abstractmethod
    def refund(self):
        pass


class CashPayment(Payment):

    def __init__(self, payment_id, amount, status):
        super().__init__(
            payment_id,
            amount,
            status
        )

    def payment_type(self):
        return "Payment Type is -->CASH"

    def pay(self):

        if self.status != PaymentStatus.PENDING:
            raise PaymentError(
                "Payment cannot be processed"
            )

        self.status = PaymentStatus.SUCCESS

        return True

    def refund(self):

        if self.status != PaymentStatus.SUCCESS:
            raise PaymentError(
                "Payment cannot be refunded"
            )

        self.status = PaymentStatus.REFUNDED

        return True


class UPIPayment(Payment):

    def __init__(
        self,
        payment_id,
        amount,
        status,
        upi_id
    ):
        self.upi_id = upi_id

        super().__init__(
            payment_id,
            amount,
            status
        )

    def payment_type(self):
        return "UPI"

    def pay(self):

        if self.status != PaymentStatus.PENDING:
            raise PaymentError(
                "Payment cannot be processed"
            )

        self.status = PaymentStatus.SUCCESS

        return True

    def refund(self):

        if self.status != PaymentStatus.SUCCESS:
            raise PaymentError(
                "Payment cannot be refunded"
            )

        self.status = PaymentStatus.REFUNDED

        return True


class RideService:

    def __init__(self):
        self.drivers = []
        self.rides = []

    def register_driver(self, driver):
        self.drivers.append(driver)

    def find_driver(self, vehicle_type):

        for driver in self.drivers:

            if (
                driver.is_available
                and driver.vehicle.vehicle_type == vehicle_type
            ):
                return driver

        raise NoDriverAvailableError(
            "No driver available for this vehicle type"
        )

    def request_ride(
        self,
        rider,
        pickup,
        drop,
        vehicle_type
    ):

        ride = Ride(
            ride_id=len(self.rides) + 1,
            rider=rider,
            driver=None,
            pickup=pickup,
            drop=drop,
            vehicle_type=vehicle_type,
            status=RideStatus.REQUESTED,
            fare=0
        )

        ride.calculate_fare()

        self.rides.append(ride)

        rider.request_ride(ride)

        return ride

    def assign_driver(self, ride):

        driver = self.find_driver(
            ride.vehicle_type
        )

        ride.driver = driver

        ride.update_status(
            RideStatus.DRIVER_ASSIGNED
        )

        return driver


class RideSharingError(Exception):
    pass


class NoDriverAvailableError(RideSharingError):
    pass


class InvalidRideStateError(RideSharingError):
    pass


class DriverUnavailableError(RideSharingError):
    pass


class InvalidVehicleTypeError(RideSharingError):
    pass


class PaymentError(RideSharingError):
    pass



location1 = Location("18.5204", "73.8567")
location2 = Location("18.5314", "73.8446")

vehicle1 = Vehicle(
    "MH12AB1234",
    VehicleType.SEDAN,
    4
)

vehicle2 = Vehicle(
    "MH12CD5678",
    VehicleType.BIKE,
    1
)



rider = Rider(
    1,
    "Rahul",
    "rahul@gmail.com",
    "9876543210",
    location1
)

driver1 = Driver(
    101,
    "Amit",
    "amit@gmail.com",
    "9876543211",
    location2,
    vehicle1,
    True
)

driver2 = Driver(
    102,
    "Rohan",
    "rohan@gmail.com",
    "9876543212",
    location2,
    vehicle2,
    True
)

service=RideService()
service.register_driver(driver1)
service.register_driver(driver2)

ride=service.request_ride(rider,location1,location2,VehicleType.SEDAN)

ride.display_ride()
driver=service.assign_driver(ride)

ride.display_ride()

driver.accept_ride(ride)
driver.start_ride(ride)
ride.display_ride()
driver.complete_ride(ride)
ride.display_ride()


payment = UPIPayment(
    "P001",
    ride.fare,
    PaymentStatus.PENDING,
    "rahul@upi"
)

payment.pay()

print("\n--- PAYMENT ---")
print(payment.payment_type())
print(payment.status.value)
print("Amount:", payment.amount)


print("\n--- DRIVER EARNINGS ---")
print(driver.view_earnings())


print("\n--- RIDER HISTORY ---")
rider.view_ride_history()


print("\n--- DRIVER HISTORY ---")
driver.view_ride_history()

