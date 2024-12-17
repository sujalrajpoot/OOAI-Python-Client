# OOAI Python Client

This Python client provides an interface to interact with the OOAI API. It includes functionality for making requests, processing streamed responses, and handling errors related to the OOAI service. The client utilizes the `cloudscraper` library to manage requests, providing a robust mechanism for working with websites that have anti-bot protection.

## Features
- Make requests to the OOAI API with a query string.
- Stream responses in real-time and process them as they arrive.
- Handle potential errors gracefully through custom exception classes.
- Supports encoding of queries for URL compatibility.

## Installation
- To clone the repository and navigate to the project directory, use the following commands in your terminal:

```bash
git clone https://github.com/sujalrajpoot/OOAI-Python-Client.git
cd OOAI-Python-Client
```

## Requirements

- Python 3.6+
- `requests` library
- `cloudscraper` library

You can install the required dependencies by running:

```bash
pip install requests cloudscraper
```

# Components
## 1. Custom Exception Classes
- OOAIException: A base class for custom exceptions in the OOAI client.
- InvalidQueryException: Raised for malformed or invalid queries.

## 2. OOAIResponse Dataclass
### This class stores the response data:
- streaming_response: The raw streaming content.
- results: A list of references or results fetched by the query.

## 3. OOAIRequestHandler Class
### This class is responsible for:

- Making requests to the OOAI API with a given query string.
- Processing streamed responses in real-time.
- Handling and parsing the response to extract useful data.

## 4. OOAIService Class
- This service class integrates the OOAIRequestHandler and provides a convenient method to retrieve responses from the OOAI API.

# Usage
### Here's an example of how to use the client to query the OOAI API:

```python
from ooai_client import OOAIRequestHandler, OOAIService

# Initialize the handler and service
handler = OOAIRequestHandler()
service = OOAIService(handler)

# Define the query string
query = "What is thermodynamics?"

# Get the response (streaming set to False for simplicity)
response = service.get_ooai_response(query, stream=True)

# Print the response data
print(f"Response: {response.streaming_response}")
for index, result in enumerate(response.results, start=1):
    print(f"Result {index}: {result}")
```

# Example Output:
```
Response: Thermodynamics is the branch of physics that deals with the relationship between heat, work, and energy.
Result 1: {"reference": "https://en.wikipedia.org/wiki/Thermodynamics"}
```

# Error Handling
- The OOAIRequestHandler class handles various exceptions:

- OOAIException: Raised for any issues with the request process.
- InvalidQueryException: Raised when the query string is invalid or malformed.

# Acknowledgements
- Cloudscraper for bypassing bot protection.
- OOAI API for providing the API used in this client.

## Disclaimer ⚠️

**IMPORTANT: EDUCATIONAL PURPOSE ONLY**

This library interfaces with the OOAI search API for educational purposes only. It is not intended to harm or exploit the https://oo.ai/ website in any way.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact
For questions or support, please open an issue or reach out to the maintainer.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the project repository.
