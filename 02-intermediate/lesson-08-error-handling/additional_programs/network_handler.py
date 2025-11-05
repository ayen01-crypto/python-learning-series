#!/usr/bin/env python3
"""
Network Request Handler with Error Handling
A program that handles network requests with comprehensive error handling and timeouts.
"""

import time
import random
from typing import Dict, Any, Optional
from urllib.parse import urlparse


class NetworkError(Exception):
    """Custom exception for network-related errors."""
    pass


class TimeoutError(NetworkError):
    """Exception for timeout errors."""
    pass


class NetworkRequestHandler:
    """A robust network request handler with comprehensive error handling."""
    
    def __init__(self, default_timeout: int = 30):
        """
        Initialize network request handler.
        
        Args:
            default_timeout (int): Default timeout in seconds
        """
        self.default_timeout = default_timeout
        self.request_history = []
        self.errors = []
        self.successful_requests = 0
        self.failed_requests = 0
    
    def make_request(self, url: str, method: str = "GET", 
                    timeout: Optional[int] = None, 
                    retries: int = 3) -> Dict[str, Any]:
        """
        Make a network request with error handling and retries.
        
        Args:
            url (str): URL to request
            method (str): HTTP method (GET, POST, etc.)
            timeout (int): Timeout in seconds
            retries (int): Number of retry attempts
            
        Returns:
            dict: Response data
            
        Raises:
            NetworkError: If request fails after all retries
        """
        if timeout is None:
            timeout = self.default_timeout
        
        # Validate URL
        if not self._is_valid_url(url):
            raise NetworkError(f"Invalid URL format: {url}")
        
        attempt = 0
        last_error = None
        
        while attempt <= retries:
            try:
                # Simulate network request with potential failures
                response = self._simulate_network_request(url, method, timeout)
                
                # Record successful request
                self.successful_requests += 1
                self._record_request(url, method, "SUCCESS", response.get("status_code", 200))
                
                print(f"✅ Request successful: {method} {url}")
                return response
                
            except TimeoutError as e:
                attempt += 1
                last_error = e
                self._handle_retry(attempt, retries, f"Timeout: {e}")
                
            except NetworkError as e:
                attempt += 1
                last_error = e
                self._handle_retry(attempt, retries, f"Network error: {e}")
                
            except Exception as e:
                attempt += 1
                last_error = NetworkError(f"Unexpected error: {e}")
                self._handle_retry(attempt, retries, f"Unexpected error: {e}")
        
        # All retries exhausted
        self.failed_requests += 1
        error_msg = f"Request failed after {retries + 1} attempts: {last_error}"
        self.errors.append(error_msg)
        self._record_request(url, method, "FAILED", None, error_msg)
        raise NetworkError(error_msg)
    
    def _simulate_network_request(self, url: str, method: str, timeout: int) -> Dict[str, Any]:
        """
        Simulate a network request with various potential issues.
        
        Args:
            url (str): URL to request
            method (str): HTTP method
            timeout (int): Timeout in seconds
            
        Returns:
            dict: Simulated response
            
        Raises:
            TimeoutError: If request times out
            NetworkError: If other network error occurs
        """
        # Simulate network delay
        delay = random.uniform(0.1, 2.0)
        
        # Check if request should timeout
        if delay > timeout:
            raise TimeoutError(f"Request to {url} timed out after {timeout} seconds")
        
        # Simulate processing time
        time.sleep(min(delay, 0.5))  # Cap at 0.5 seconds for demo purposes
        
        # Randomly simulate different network issues
        error_chance = random.random()
        
        if error_chance < 0.1:  # 10% chance of DNS error
            raise NetworkError(f"DNS resolution failed for {url}")
        elif error_chance < 0.2:  # 10% chance of connection refused
            raise NetworkError(f"Connection refused by {url}")
        elif error_chance < 0.25:  # 5% chance of SSL error
            raise NetworkError(f"SSL certificate verification failed for {url}")
        elif error_chance < 0.3:  # 5% chance of rate limiting
            raise NetworkError(f"Rate limited by {url}")
        
        # Simulate successful response
        status_codes = [200, 201, 204]  # Common success codes
        status_code = random.choice(status_codes)
        
        # Simulate response data
        response_data = {
            "status_code": status_code,
            "headers": {
                "Content-Type": "application/json",
                "Server": "DemoServer/1.0"
            },
            "data": self._generate_sample_response_data(url),
            "response_time": round(delay * 1000, 2)  # in milliseconds
        }
        
        return response_data
    
    def _generate_sample_response_data(self, url: str) -> Dict[str, Any]:
        """Generate sample response data based on URL."""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        if "api.github.com" in domain:
            return {
                "login": "demo-user",
                "id": 12345,
                "name": "Demo User",
                "public_repos": 15,
                "followers": 100
            }
        elif "jsonplaceholder.typicode.com" in domain:
            return {
                "userId": 1,
                "id": 1,
                "title": "Sample Post Title",
                "body": "This is a sample post body for demonstration purposes."
            }
        elif "httpbin.org" in domain:
            return {
                "origin": "127.0.0.1",
                "url": url,
                "method": "GET",
                "headers": {
                    "User-Agent": "DemoClient/1.0",
                    "Accept": "*/*"
                }
            }
        else:
            return {
                "message": f"Hello from {domain}",
                "timestamp": time.time(),
                "request_url": url
            }
    
    def _is_valid_url(self, url: str) -> bool:
        """
        Validate URL format.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    def _handle_retry(self, attempt: int, max_retries: int, error_msg: str):
        """
        Handle retry logic with exponential backoff.
        
        Args:
            attempt (int): Current attempt number
            max_retries (int): Maximum number of retries
            error_msg (str): Error message
        """
        if attempt <= max_retries:
            backoff_time = min(2 ** attempt, 10)  # Max 10 seconds backoff
            print(f"⚠️  Attempt {attempt} failed: {error_msg}")
            print(f"🔄 Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)
        else:
            print(f"❌ All {max_retries + 1} attempts failed: {error_msg}")
    
    def _record_request(self, url: str, method: str, status: str, 
                       status_code: Optional[int], error: str = None):
        """
        Record request in history.
        
        Args:
            url (str): Request URL
            method (str): HTTP method
            status (str): Request status (SUCCESS/FAILED)
            status_code (int): HTTP status code
            error (str): Error message if failed
        """
        record = {
            "timestamp": time.time(),
            "url": url,
            "method": method,
            "status": status,
            "status_code": status_code,
            "error": error
        }
        self.request_history.append(record)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get request statistics."""
        total_requests = self.successful_requests + self.failed_requests
        success_rate = (self.successful_requests / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "total_requests": total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": round(success_rate, 2),
            "recent_errors": self.errors[-5:] if self.errors else []  # Last 5 errors
        }
    
    def clear_statistics(self):
        """Clear request statistics."""
        self.request_history.clear()
        self.errors.clear()
        self.successful_requests = 0
        self.failed_requests = 0
        print("Statistics cleared.")


def main():
    """Main network request handler program."""
    handler = NetworkRequestHandler(default_timeout=5)
    
    print("🌐 Network Request Handler with Error Handling")
    print("This program demonstrates handling network requests with comprehensive error handling.")
    
    while True:
        print("\n" + "=" * 40)
        print("🌐 NETWORK REQUEST MENU")
        print("=" * 40)
        print("1. Make GET Request")
        print("2. Make POST Request")
        print("3. Custom Request")
        print("4. Show Statistics")
        print("5. Clear Statistics")
        print("6. Demo Various Scenarios")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        try:
            if choice == '1':
                url = input("Enter URL (default: https://api.github.com/users/demo): ").strip()
                if not url:
                    url = "https://api.github.com/users/demo"
                
                timeout = input("Enter timeout in seconds (default: 5): ").strip()
                timeout = int(timeout) if timeout.isdigit() else 5
                
                retries = input("Enter retry attempts (default: 3): ").strip()
                retries = int(retries) if retries.isdigit() else 3
                
                response = handler.make_request(url, "GET", timeout, retries)
                print(f"\n📄 Response:")
                print(f"  Status Code: {response['status_code']}")
                print(f"  Response Time: {response['response_time']} ms")
                print(f"  Data: {response['data']}")
            
            elif choice == '2':
                url = input("Enter URL (default: https://jsonplaceholder.typicode.com/posts): ").strip()
                if not url:
                    url = "https://jsonplaceholder.typicode.com/posts"
                
                timeout = input("Enter timeout in seconds (default: 5): ").strip()
                timeout = int(timeout) if timeout.isdigit() else 5
                
                retries = input("Enter retry attempts (default: 3): ").strip()
                retries = int(retries) if retries.isdigit() else 3
                
                response = handler.make_request(url, "POST", timeout, retries)
                print(f"\n📄 Response:")
                print(f"  Status Code: {response['status_code']}")
                print(f"  Response Time: {response['response_time']} ms")
                print(f"  Data: {response['data']}")
            
            elif choice == '3':
                url = input("Enter URL: ").strip()
                if not url:
                    print("❌ URL cannot be empty.")
                    continue
                
                method = input("Enter HTTP method (GET/POST/PUT/DELETE, default: GET): ").strip().upper()
                if not method:
                    method = "GET"
                
                timeout = input("Enter timeout in seconds (default: 5): ").strip()
                timeout = int(timeout) if timeout.isdigit() else 5
                
                retries = input("Enter retry attempts (default: 3): ").strip()
                retries = int(retries) if retries.isdigit() else 3
                
                response = handler.make_request(url, method, timeout, retries)
                print(f"\n📄 Response:")
                print(f"  Status Code: {response['status_code']}")
                print(f"  Response Time: {response['response_time']} ms")
                print(f"  Data: {response['data']}")
            
            elif choice == '4':
                stats = handler.get_statistics()
                print(f"\n📊 Request Statistics:")
                print(f"  Total Requests: {stats['total_requests']}")
                print(f"  Successful: {stats['successful_requests']}")
                print(f"  Failed: {stats['failed_requests']}")
                print(f"  Success Rate: {stats['success_rate']}%")
                if stats['recent_errors']:
                    print("  Recent Errors:")
                    for error in stats['recent_errors']:
                        print(f"    - {error}")
            
            elif choice == '5':
                handler.clear_statistics()
            
            elif choice == '6':
                print("\n🧪 Demonstrating various network scenarios...")
                
                # Test cases with different scenarios
                test_cases = [
                    ("https://api.github.com/users/octocat", "GET"),
                    ("https://invalid-domain-that-does-not-exist-12345.com", "GET"),
                    ("https://httpbin.org/delay/2", "GET"),  # Will sometimes timeout
                    ("https://jsonplaceholder.typicode.com/posts/1", "GET"),
                ]
                
                for url, method in test_cases:
                    try:
                        print(f"\nTesting: {method} {url}")
                        response = handler.make_request(url, method, timeout=3, retries=2)
                        print(f"  ✅ Success - Status: {response['status_code']}")
                    except NetworkError as e:
                        print(f"  ❌ Failed - Error: {e}")
                
                # Show final statistics
                stats = handler.get_statistics()
                print(f"\n📊 Final Demo Statistics:")
                print(f"  Success Rate: {stats['success_rate']}%")
            
            elif choice == '7':
                print("Thank you for using Network Request Handler!")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-7.")
        
        except NetworkError as e:
            print(f"❌ Network Error: {e}")
        except ValueError as e:
            print(f"❌ Value Error: {e}")
        except KeyboardInterrupt:
            print("\n⚠️  Request interrupted by user.")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    main()