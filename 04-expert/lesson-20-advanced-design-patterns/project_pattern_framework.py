"""
Project: Pattern Implementation Framework
This project demonstrates a comprehensive framework for implementing and testing
various design patterns in Python applications.
"""

import threading
import weakref
from abc import ABC, abstractmethod
from typing import List, Any, Dict, Callable
import time


class PatternFramework:
    """
    A comprehensive framework for implementing and testing design patterns.
    """

    def __init__(self):
        self.patterns: Dict[str, Any] = {}
        self.results: Dict[str, Any] = {}

    def register_pattern(self, name: str, implementation: Any) -> None:
        """Register a pattern implementation."""
        self.patterns[name] = implementation
        print(f"Registered pattern: {name}")

    def run_pattern(self, name: str, *args, **kwargs) -> Any:
        """Run a registered pattern implementation."""
        if name not in self.patterns:
            raise ValueError(f"Pattern '{name}' not registered")
        
        print(f"Running pattern: {name}")
        start_time = time.time()
        result = self.patterns[name](*args, **kwargs)
        end_time = time.time()
        
        self.results[name] = {
            'result': result,
            'execution_time': end_time - start_time
        }
        
        return result

    def get_results(self) -> Dict[str, Any]:
        """Get results of all pattern executions."""
        return self.results

    def benchmark_patterns(self) -> None:
        """Benchmark all registered patterns."""
        print("\n=== Pattern Benchmark Results ===")
        for name, result in self.results.items():
            print(f"{name}: {result['execution_time']:.6f} seconds")


# 1. Singleton Pattern Implementation
class SingletonMeta(type):
    """
    Thread-safe Singleton metaclass.
    """
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "Connected to database"
        self.queries_executed = 0

    def execute_query(self, sql: str) -> str:
        self.queries_executed += 1
        return f"Executed: {sql} (Total queries: {self.queries_executed})"


def singleton_demo():
    """Demonstrate Singleton pattern."""
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"db1 is db2: {db1 is db2}")
    print(db1.execute_query("SELECT * FROM users"))
    print(db2.execute_query("SELECT * FROM products"))
    return db1.queries_executed


# 2. Factory Pattern Implementation
class Shape(ABC):
    @abstractmethod
    def draw(self) -> str:
        pass


class Circle(Shape):
    def draw(self) -> str:
        return "Drawing Circle"


class Rectangle(Shape):
    def draw(self) -> str:
        return "Drawing Rectangle"


class ShapeFactory:
    @staticmethod
    def create_shape(shape_type: str) -> Shape:
        if shape_type.lower() == "circle":
            return Circle()
        elif shape_type.lower() == "rectangle":
            return Rectangle()
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")


def factory_demo():
    """Demonstrate Factory pattern."""
    shapes = ["circle", "rectangle", "circle"]
    results = []
    
    for shape_type in shapes:
        shape = ShapeFactory.create_shape(shape_type)
        results.append(shape.draw())
    
    return results


# 3. Observer Pattern Implementation
class EventManager:
    def __init__(self):
        self._observers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, observer: Callable) -> None:
        if event_type not in self._observers:
            self._observers[event_type] = []
        self._observers[event_type].append(observer)

    def unsubscribe(self, event_type: str, observer: Callable) -> None:
        if event_type in self._observers:
            self._observers[event_type].remove(observer)

    def notify(self, event_type: str, data: Any) -> None:
        if event_type in self._observers:
            for observer in self._observers[event_type]:
                observer(data)


class Logger:
    @staticmethod
    def log_event(data: Any) -> None:
        print(f"[LOG] Event received: {data}")


class EmailNotifier:
    @staticmethod
    def send_notification(data: Any) -> None:
        print(f"[EMAIL] Notification sent: {data}")


def observer_demo():
    """Demonstrate Observer pattern."""
    event_manager = EventManager()
    logger = Logger()
    email_notifier = EmailNotifier()
    
    event_manager.subscribe("user_registered", logger.log_event)
    event_manager.subscribe("user_registered", email_notifier.send_notification)
    
    event_manager.notify("user_registered", {"user_id": 123, "email": "user@example.com"})
    return "Notifications sent"


# 4. Strategy Pattern Implementation
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass


class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} using Credit Card"


class PayPalPayment(PaymentStrategy):
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} using PayPal"


class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy

    def process_payment(self, amount: float) -> str:
        return self._strategy.pay(amount)


def strategy_demo():
    """Demonstrate Strategy pattern."""
    processor = PaymentProcessor(CreditCardPayment())
    result1 = processor.process_payment(100.0)
    
    processor.set_strategy(PayPalPayment())
    result2 = processor.process_payment(50.0)
    
    return [result1, result2]


# 5. Decorator Pattern Implementation
class TextComponent(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


class PlainText(TextComponent):
    def __init__(self, text: str):
        self._text = text

    def render(self) -> str:
        return self._text


class TextDecorator(TextComponent):
    def __init__(self, component: TextComponent):
        self._component = component

    def render(self) -> str:
        return self._component.render()


class BoldDecorator(TextDecorator):
    def render(self) -> str:
        return f"<b>{super().render()}</b>"


class ItalicDecorator(TextDecorator):
    def render(self) -> str:
        return f"<i>{super().render()}</i>"


def decorator_demo():
    """Demonstrate Decorator pattern."""
    plain_text = PlainText("Hello World")
    bold_text = BoldDecorator(plain_text)
    italic_bold_text = ItalicDecorator(bold_text)
    
    return italic_bold_text.render()


# 6. Command Pattern Implementation
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class Light:
    def __init__(self):
        self._is_on = False

    def turn_on(self) -> None:
        self._is_on = True
        print("Light is ON")

    def turn_off(self) -> None:
        self._is_on = False
        print("Light is OFF")

    def is_on(self) -> bool:
        return self._is_on


class LightOnCommand(Command):
    def __init__(self, light: Light):
        self._light = light

    def execute(self) -> None:
        self._light.turn_on()

    def undo(self) -> None:
        self._light.turn_off()


class LightOffCommand(Command):
    def __init__(self, light: Light):
        self._light = light

    def execute(self) -> None:
        self._light.turn_off()

    def undo(self) -> None:
        self._light.turn_on()


class SmartHomeController:
    def __init__(self):
        self._history: List[Command] = []

    def execute_command(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def undo_last_command(self) -> None:
        if self._history:
            command = self._history.pop()
            command.undo()


def command_demo():
    """Demonstrate Command pattern."""
    light = Light()
    controller = SmartHomeController()
    
    on_command = LightOnCommand(light)
    off_command = LightOffCommand(light)
    
    controller.execute_command(on_command)
    controller.execute_command(off_command)
    controller.undo_last_command()
    
    return f"Light is {'ON' if light.is_on() else 'OFF'}"


# 7. Template Method Pattern Implementation
class DataAnalyzer(ABC):
    def analyze(self, data: List[Any]) -> Dict[str, Any]:
        result = {}
        result['input_data'] = data
        result['preprocessed'] = self.preprocess(data)
        result['processed'] = self.process(result['preprocessed'])
        result['postprocessed'] = self.postprocess(result['processed'])
        return result

    def preprocess(self, data: List[Any]) -> List[Any]:
        print("Preprocessing data...")
        return data

    @abstractmethod
    def process(self, data: List[Any]) -> List[Any]:
        pass

    def postprocess(self, data: List[Any]) -> List[Any]:
        print("Postprocessing data...")
        return data


class NumberAnalyzer(DataAnalyzer):
    def process(self, data: List[int]) -> List[int]:
        print("Processing numbers...")
        return [x * 2 for x in data if isinstance(x, (int, float))]


class TextAnalyzer(DataAnalyzer):
    def process(self, data: List[str]) -> List[str]:
        print("Processing text...")
        return [s.upper() for s in data if isinstance(s, str)]


def template_method_demo():
    """Demonstrate Template Method pattern."""
    numbers = [1, 2, 3, 4, 5]
    texts = ["hello", "world", "python"]
    
    num_analyzer = NumberAnalyzer()
    text_analyzer = TextAnalyzer()
    
    num_result = num_analyzer.analyze(numbers)
    text_result = text_analyzer.analyze(texts)
    
    return {
        'number_analysis': num_result,
        'text_analysis': text_result
    }


# 8. Flyweight Pattern Implementation
class CharacterFlyweight:
    def __init__(self, char: str):
        self._char = char

    def render(self, font: str, size: int) -> str:
        return f"Character '{self._char}' rendered with {font} font at size {size}"


class CharacterFactory:
    _flyweights = weakref.WeakValueDictionary()

    @classmethod
    def get_character(cls, char: str) -> CharacterFlyweight:
        if char not in cls._flyweights:
            cls._flyweights[char] = CharacterFlyweight(char)
        return cls._flyweights[char]


def flyweight_demo():
    """Demonstrate Flyweight pattern."""
    chars = ['a', 'b', 'c', 'a', 'b']
    factory = CharacterFactory()
    
    results = []
    for char in chars:
        character = factory.get_character(char)
        result = character.render("Arial", 12)
        results.append(result)
    
    # Show that we're reusing objects
    a1 = factory.get_character('a')
    a2 = factory.get_character('a')
    results.append(f"a1 is a2: {a1 is a2}")
    
    return results


# 9. Proxy Pattern Implementation
class Image(ABC):
    @abstractmethod
    def display(self) -> str:
        pass


class RealImage(Image):
    def __init__(self, filename: str):
        self._filename = filename
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        print(f"Loading {self._filename} from disk...")
        time.sleep(0.1)  # Simulate loading time

    def display(self) -> str:
        return f"Displaying {self._filename}"


class ProxyImage(Image):
    def __init__(self, filename: str):
        self._filename = filename
        self._real_image = None

    def display(self) -> str:
        if self._real_image is None:
            self._real_image = RealImage(self._filename)
        return self._real_image.display()


def proxy_demo():
    """Demonstrate Proxy pattern."""
    image = ProxyImage("photo.jpg")
    
    # First display - loads from disk
    result1 = image.display()
    
    # Second display - uses cached image
    result2 = image.display()
    
    return [result1, result2]


# 10. Adapter Pattern Implementation
class EuropeanSocket:
    def voltage(self) -> int:
        return 230

    def live(self) -> int:
        return 1

    def neutral(self) -> int:
        return -1

    def earth(self) -> int:
        return 0


class USADevice:
    def __init__(self, name: str):
        self.name = name

    def connect(self, voltage: int) -> str:
        if voltage == 120:
            return f"{self.name} connected successfully"
        else:
            return f"{self.name} cannot connect - wrong voltage"


class SocketAdapter:
    def __init__(self, european_socket: EuropeanSocket):
        self.socket = european_socket

    def voltage(self) -> int:
        return 120  # Convert 230V to 120V

    def live(self) -> int:
        return self.socket.live()

    def neutral(self) -> int:
        return self.socket.neutral()


def adapter_demo():
    """Demonstrate Adapter pattern."""
    socket = EuropeanSocket()
    device = USADevice("Laptop Charger")
    
    # Try connecting directly (won't work)
    direct_result = device.connect(socket.voltage())
    
    # Use adapter (will work)
    adapter = SocketAdapter(socket)
    adapter_result = device.connect(adapter.voltage())
    
    return [direct_result, adapter_result]


def main():
    """Main function to run all pattern demonstrations."""
    print("=== Pattern Implementation Framework Demo ===\n")
    
    framework = PatternFramework()
    
    # Register all patterns
    framework.register_pattern("singleton", singleton_demo)
    framework.register_pattern("factory", factory_demo)
    framework.register_pattern("observer", observer_demo)
    framework.register_pattern("strategy", strategy_demo)
    framework.register_pattern("decorator", decorator_demo)
    framework.register_pattern("command", command_demo)
    framework.register_pattern("template_method", template_method_demo)
    framework.register_pattern("flyweight", flyweight_demo)
    framework.register_pattern("proxy", proxy_demo)
    framework.register_pattern("adapter", adapter_demo)
    
    # Run all patterns
    framework.run_pattern("singleton")
    framework.run_pattern("factory")
    framework.run_pattern("observer")
    framework.run_pattern("strategy")
    framework.run_pattern("decorator")
    framework.run_pattern("command")
    framework.run_pattern("template_method")
    framework.run_pattern("flyweight")
    framework.run_pattern("proxy")
    framework.run_pattern("adapter")
    
    # Show benchmark results
    framework.benchmark_patterns()
    
    print("\n=== All Patterns Demonstrated Successfully ===")


if __name__ == "__main__":
    main()