"""
Examples for Advanced Design Patterns Lesson
This file demonstrates all the design patterns covered in Lesson 20.
"""

import threading
import weakref
from abc import ABC, abstractmethod
from typing import List, Any

print("=== Advanced Design Patterns Examples ===\n")

# 1. Thread-Safe Singleton Pattern
print("1. Thread-Safe Singleton Pattern")


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    value: str = None

    def __init__(self, value: str) -> None:
        if not self.value:
            self.value = value


def test_singleton(value: str) -> None:
    singleton = Database(value)
    print(f"Singleton value: {singleton.value}")


# Testing singleton
process1 = threading.Thread(target=test_singleton, args=("FOO",))
process2 = threading.Thread(target=test_singleton, args=("BAR",))
process1.start()
process2.start()

print()

# 2. Factory Pattern
print("2. Factory Pattern")


class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass


class Dog(Animal):
    def speak(self):
        return "Woof!"


class Cat(Animal):
    def speak(self):
        return "Meow!"


class AnimalFactory:
    @staticmethod
    def create_animal(animal_type: str) -> Animal:
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")


# Testing factory
dog = AnimalFactory.create_animal("dog")
cat = AnimalFactory.create_animal("cat")
print(dog.speak())
print(cat.speak())

print()

# 3. Observer Pattern with Event System
print("3. Observer Pattern with Event System")


class EventManager:
    def __init__(self):
        self._observers = {}

    def subscribe(self, event_type: str, observer):
        if event_type not in self._observers:
            self._observers[event_type] = []
        self._observers[event_type].append(observer)

    def unsubscribe(self, event_type: str, observer):
        if event_type in self._observers:
            self._observers[event_type].remove(observer)

    def notify(self, event_type: str, data):
        if event_type in self._observers:
            for observer in self._observers[event_type]:
                observer.update(data)


class EventObserver:
    def __init__(self, name: str):
        self.name = name

    def update(self, data):
        print(f"{self.name} received event data: {data}")


# Testing observer
event_manager = EventManager()
observer1 = EventObserver("Observer 1")
observer2 = EventObserver("Observer 2")

event_manager.subscribe("click", observer1)
event_manager.subscribe("click", observer2)
event_manager.notify("click", {"x": 100, "y": 200})

print()

# 4. Strategy Pattern
print("4. Strategy Pattern")


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass


class BubbleSort(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        # Simplified bubble sort
        arr = data.copy()
        for i in range(len(arr)):
            for j in range(0, len(arr) - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


class QuickSort(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        # Simplified quick sort
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)


class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def sort(self, data: List[int]) -> List[int]:
        return self._strategy.sort(data)


# Testing strategy
data = [64, 34, 25, 12, 22, 11, 90]
bubble_sorter = Sorter(BubbleSort())
quick_sorter = Sorter(QuickSort())

print("Original data:", data)
print("Bubble sorted:", bubble_sorter.sort(data))
print("Quick sorted:", quick_sorter.sort(data))

print()

# 5. Decorator Pattern
print("5. Decorator Pattern")


class Component(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass


class ConcreteComponent(Component):
    def operation(self) -> str:
        return "ConcreteComponent"


class Decorator(Component):
    _component: Component = None

    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> Component:
        return self._component

    def operation(self) -> str:
        return self._component.operation()


class ConcreteDecoratorA(Decorator):
    def operation(self) -> str:
        return f"ConcreteDecoratorA({self.component.operation()})"


class ConcreteDecoratorB(Decorator):
    def operation(self) -> str:
        return f"ConcreteDecoratorB({self.component.operation()})"


# Testing decorator
simple = ConcreteComponent()
decorator1 = ConcreteDecoratorA(simple)
decorator2 = ConcreteDecoratorB(decorator1)
print("Client: Now I've got a decorated component:")
print(f"RESULT: {decorator2.operation()}")

print()

# 6. Command Pattern
print("6. Command Pattern")


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class Light:
    def turn_on(self) -> None:
        print("Light is ON")

    def turn_off(self) -> None:
        print("Light is OFF")


class TurnOnCommand(Command):
    def __init__(self, light: Light) -> None:
        self._light = light

    def execute(self) -> None:
        self._light.turn_on()

    def undo(self) -> None:
        self._light.turn_off()


class TurnOffCommand(Command):
    def __init__(self, light: Light) -> None:
        self._light = light

    def execute(self) -> None:
        self._light.turn_off()

    def undo(self) -> None:
        self._light.turn_on()


class RemoteControl:
    def __init__(self) -> None:
        self._history: List[Command] = []

    def submit(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def undo_last(self) -> None:
        if self._history:
            command = self._history.pop()
            command.undo()


# Testing command
light = Light()
remote = RemoteControl()

turn_on = TurnOnCommand(light)
turn_off = TurnOffCommand(light)

remote.submit(turn_on)
remote.submit(turn_off)
print("Undoing last command:")
remote.undo_last()

print()

# 7. Template Method Pattern
print("7. Template Method Pattern")


class DataProcessor(ABC):
    def process(self, data: Any) -> Any:
        data = self.read_data(data)
        data = self.process_data(data)
        return self.write_data(data)

    def read_data(self, data: Any) -> Any:
        print("Reading data")
        return data

    @abstractmethod
    def process_data(self, data: Any) -> Any:
        pass

    def write_data(self, data: Any) -> Any:
        print("Writing data")
        return data


class TextProcessor(DataProcessor):
    def process_data(self, data: str) -> str:
        print("Processing text data")
        return data.upper()


class NumberProcessor(DataProcessor):
    def process_data(self, data: List[int]) -> List[int]:
        print("Processing number data")
        return [x * 2 for x in data]


# Testing template method
text_processor = TextProcessor()
result = text_processor.process("hello world")
print(f"Text result: {result}")

number_processor = NumberProcessor()
result = number_processor.process([1, 2, 3, 4, 5])
print(f"Number result: {result}")

print()

# 8. Flyweight Pattern
print("8. Flyweight Pattern")


class Flyweight:
    def __init__(self, intrinsic_state: str) -> None:
        self._intrinsic_state = intrinsic_state

    def operation(self, extrinsic_state: str) -> str:
        return f"Flyweight: Intrinsic = {self._intrinsic_state}, Extrinsic = {extrinsic_state}"


class FlyweightFactory:
    _flyweights = weakref.WeakValueDictionary()

    @classmethod
    def get_flyweight(cls, intrinsic_state: str) -> Flyweight:
        if intrinsic_state not in cls._flyweights:
            cls._flyweights[intrinsic_state] = Flyweight(intrinsic_state)
        return cls._flyweights[intrinsic_state]


# Testing flyweight
factory = FlyweightFactory()
flyweight1 = factory.get_flyweight("state1")
flyweight2 = factory.get_flyweight("state2")
flyweight3 = factory.get_flyweight("state1")  # Same as flyweight1

print(flyweight1.operation("extra1"))
print(flyweight2.operation("extra2"))
print(flyweight3.operation("extra3"))
print(f"flyweight1 is flyweight3: {flyweight1 is flyweight3}")  # Should be True

print()

# 9. Proxy Pattern
print("9. Proxy Pattern")


class RealSubject:
    def request(self) -> str:
        return "RealSubject: Handling request."


class Proxy:
    def __init__(self, real_subject: RealSubject) -> None:
        self._real_subject = real_subject

    def request(self) -> str:
        if self.check_access():
            result = self._real_subject.request()
            self.log_access()
            return result
        else:
            return "Proxy: Access denied."

    def check_access(self) -> bool:
        print("Proxy: Checking access prior to firing a real request.")
        return True

    def log_access(self) -> None:
        print("Proxy: Logging the time of request.")


# Testing proxy
real_subject = RealSubject()
proxy = Proxy(real_subject)
print(proxy.request())

print()

# 10. Adapter Pattern
print("10. Adapter Pattern")


class EuropeanSocketInterface(ABC):
    @abstractmethod
    def voltage(self) -> int:
        pass

    @abstractmethod
    def live(self) -> int:
        pass

    @abstractmethod
    def neutral(self) -> int:
        pass

    @abstractmethod
    def earth(self) -> int:
        pass


class Socket(EuropeanSocketInterface):
    def voltage(self) -> int:
        return 230

    def live(self) -> int:
        return 1

    def neutral(self) -> int:
        return -1

    def earth(self) -> int:
        return 0


class USASocketInterface(ABC):
    @abstractmethod
    def voltage(self) -> int:
        pass

    @abstractmethod
    def live(self) -> int:
        pass

    @abstractmethod
    def neutral(self) -> int:
        pass


class Adapter(USASocketInterface):
    def __init__(self, socket: EuropeanSocketInterface) -> None:
        self.socket = socket

    def voltage(self) -> int:
        return 110

    def live(self) -> int:
        return self.socket.live()

    def neutral(self) -> int:
        return self.socket.neutral()


# Testing adapter
socket = Socket()
adapter = Adapter(socket)

print(f"European socket voltage: {socket.voltage()}")
print(f"USA adapter voltage: {adapter.voltage()}")

print("\n=== End of Examples ===")