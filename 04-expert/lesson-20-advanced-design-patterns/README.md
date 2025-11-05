# Lesson 20: Advanced Design Patterns

## Overview
In this final lesson, we'll explore advanced design patterns that are commonly used in professional Python development. These patterns help solve complex design problems and create more maintainable, scalable code.

## Topics Covered
- Singleton Pattern with Thread Safety
- Factory Pattern and Abstract Factory
- Observer Pattern with Event Systems
- Strategy Pattern for Algorithm Selection
- Decorator Pattern for Extending Functionality
- Command Pattern for Action Encapsulation
- Template Method Pattern
- Flyweight Pattern for Memory Optimization
- Proxy Pattern for Access Control
- Adapter Pattern for Interface Compatibility

## Learning Objectives
By the end of this lesson, you should be able to:
1. Implement thread-safe singleton patterns
2. Design flexible factory systems
3. Create event-driven architectures using observer patterns
4. Apply strategy patterns for algorithm selection
5. Use decorator patterns to extend object functionality
6. Implement command patterns for undoable operations
7. Design template methods for algorithm frameworks
8. Apply flyweight patterns for memory optimization
9. Use proxy patterns for access control and lazy loading
10. Implement adapter patterns for interface compatibility

## Prerequisites
- All previous lessons in the Python Learning Series
- Strong understanding of OOP concepts
- Experience with decorators and metaclasses

## Project: Pattern Implementation Framework
The project for this lesson is to create a comprehensive framework that demonstrates all the design patterns covered. This framework will allow users to easily implement and test various design patterns in their applications.

## Files in This Lesson
- [README.md](README.md) - This file
- [examples.py](examples.py) - Code examples for all design patterns
- [project_pattern_framework.py](project_pattern_framework.py) - Implementation framework project

## Examples Walkthrough

### 1. Thread-Safe Singleton Pattern
```python
import threading

class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[instance.__class__] = instance
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "Connected to database"
    
    def query(self, sql):
        return f"Executing: {sql}"
```

### 2. Factory Pattern
```python
from abc import ABC, abstractmethod

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
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")
```

### 3. Observer Pattern with Event System
```python
class EventManager:
    def __init__(self):
        self._observers = {}

    def subscribe(self, event_type, observer):
        if event_type not in self._observers:
            self._observers[event_type] = []
        self._observers[event_type].append(observer)

    def unsubscribe(self, event_type, observer):
        if event_type in self._observers:
            self._observers[event_type].remove(observer)

    def notify(self, event_type, data):
        if event_type in self._observers:
            for observer in self._observers[event_type]:
                observer.update(data)

class EventObserver:
    def update(self, data):
        print(f"Received event data: {data}")
```

### 4. Strategy Pattern
```python
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data):
        pass

class BubbleSort(SortStrategy):
    def sort(self, data):
        # Simplified bubble sort
        arr = data.copy()
        for i in range(len(arr)):
            for j in range(0, len(arr) - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

class QuickSort(SortStrategy):
    def sort(self, data):
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

    def sort(self, data):
        return self._strategy.sort(data)
```

### 5. Decorator Pattern
```python
class Component:
    def operation(self):
        pass

class ConcreteComponent(Component):
    def operation(self):
        return "ConcreteComponent"

class Decorator(Component):
    def __init__(self, component: Component):
        self._component = component

    def operation(self):
        return self._component.operation()

class ConcreteDecoratorA(Decorator):
    def operation(self):
        return f"ConcreteDecoratorA({self._component.operation()})"

class ConcreteDecoratorB(Decorator):
    def operation(self):
        return f"ConcreteDecoratorB({self._component.operation()})"
```

### 6. Command Pattern
```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class Light:
    def turn_on(self):
        print("Light is ON")

    def turn_off(self):
        print("Light is OFF")

class TurnOnCommand(Command):
    def __init__(self, light: Light):
        self._light = light

    def execute(self):
        self._light.turn_on()

    def undo(self):
        self._light.turn_off()

class TurnOffCommand(Command):
    def __init__(self, light: Light):
        self._light = light

    def execute(self):
        self._light.turn_off()

    def undo(self):
        self._light.turn_on()

class RemoteControl:
    def __init__(self):
        self._history = []

    def submit(self, command: Command):
        command.execute()
        self._history.append(command)

    def undo_last(self):
        if self._history:
            command = self._history.pop()
            command.undo()
```

### 7. Template Method Pattern
```python
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    def process(self, data):
        data = self.read_data(data)
        data = self.process_data(data)
        return self.write_data(data)

    def read_data(self, data):
        print("Reading data")
        return data

    @abstractmethod
    def process_data(self, data):
        pass

    def write_data(self, data):
        print("Writing data")
        return data

class TextProcessor(DataProcessor):
    def process_data(self, data):
        print("Processing text data")
        return data.upper()

class NumberProcessor(DataProcessor):
    def process_data(self, data):
        print("Processing number data")
        return [x * 2 for x in data]
```

### 8. Flyweight Pattern
```python
import weakref

class Flyweight:
    def __init__(self, intrinsic_state):
        self._intrinsic_state = intrinsic_state

    def operation(self, extrinsic_state):
        return f"Flyweight: Intrinsic = {self._intrinsic_state}, Extrinsic = {extrinsic_state}"

class FlyweightFactory:
    _flyweights = weakref.WeakValueDictionary()

    @classmethod
    def get_flyweight(cls, intrinsic_state):
        if intrinsic_state not in cls._flyweights:
            cls._flyweights[intrinsic_state] = Flyweight(intrinsic_state)
        return cls._flyweights[intrinsic_state]
```

### 9. Proxy Pattern
```python
class RealSubject:
    def request(self):
        return "RealSubject: Handling request."

class Proxy:
    def __init__(self, real_subject: RealSubject):
        self._real_subject = real_subject

    def request(self):
        if self.check_access():
            result = self._real_subject.request()
            self.log_access()
            return result
        else:
            return "Proxy: Access denied."

    def check_access(self):
        print("Proxy: Checking access prior to firing a real request.")
        return True

    def log_access(self):
        print("Proxy: Logging the time of request.")
```

### 10. Adapter Pattern
```python
class EuropeanSocketInterface:
    def voltage(self):
        pass

    def live(self):
        pass

    def neutral(self):
        pass

    def earth(self):
        pass

class Socket(EuropeanSocketInterface):
    def voltage(self):
        return 230

    def live(self):
        return 1

    def neutral(self):
        return -1

    def earth(self):
        return 0

class USASocketInterface:
    def voltage(self):
        pass

    def live(self):
        pass

    def neutral(self):
        pass

class Adapter(USASocketInterface):
    def __init__(self, socket):
        self.socket = socket

    def voltage(self):
        return 110

    def live(self):
        return self.socket.live()

    def neutral(self):
        return self.socket.neutral()
```

## Best Practices
1. Choose patterns based on actual problems, not because they seem cool
2. Don't over-engineer solutions with unnecessary patterns
3. Document why you chose a specific pattern
4. Keep patterns simple and understandable
5. Test pattern implementations thoroughly
6. Consider thread safety in concurrent environments
7. Use composition over inheritance when possible
8. Prefer Python's built-in features when they solve the problem

## Common Pitfalls
1. Overusing patterns where simple solutions would suffice
2. Implementing patterns incorrectly due to misunderstanding
3. Creating overly complex hierarchies
4. Ignoring Python's specific features and idioms
5. Not considering performance implications
6. Failing to document pattern usage and rationale

## Further Reading
- "Design Patterns: Elements of Reusable Object-Oriented Software" by Gang of Four
- "Head First Design Patterns" by Eric Freeman
- Python documentation on design patterns
- Real Python articles on design patterns