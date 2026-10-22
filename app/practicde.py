class Animal:
    def sound(self):
        print("Animal makes a sound")


class Dog(Animal):
    def sound(self):
        print("Dog barks")


class Cat(Animal):
    pass


dog = Dog()
cat = Cat()

dog.sound()
cat.sound()