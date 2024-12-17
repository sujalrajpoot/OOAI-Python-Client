import json
import requests
import cloudscraper
from typing import List, Dict, Any
from dataclasses import dataclass, field

# Custom Exception Classes
class OOAIException(Exception):
    """Base class for other exceptions in the OOAI module."""
    pass

class InvalidQueryException(OOAIException):
    """Raised when the query string is invalid or malformed."""
    pass

@dataclass
class OOAIResponse:
    """
    Dataclass for holding OOAI response data.

    Attributes:
        streaming_response (str): The streaming response received from the OOAI API.
        results (List[Dict[str, Any]]): A list of dictionaries containing the results of the query.
    """
    streaming_response: str = ''
    results: List[Dict[str, Any]] = field(default_factory=list)

# Request Handler Class for OOAI
class OOAIRequestHandler:
    """
    This class handles the requests to the OOAI API.
    It uses the CloudScraper library to make the requests.
    """

    def __init__(self):
        """
        Initializes an instance of OOAIRequestHandler.

        This method creates a CloudScraper instance for handling requests to the OOAI API.
        """
        self.scraper = cloudscraper.create_scraper()

    def make_request(self, query: str, timezone: str = "Asia/Calcutta") -> requests.Response:
        """
        Makes a GET request to the OOAI API with the provided query and timezone.

        This method encodes the query string, sets up the request headers, and sends a GET request to the OOAI API. The request is streamed to allow for real-time processing of the response.

        Args:
            query (str): The query string to be sent to the OOAI API.
            timezone (str, optional): The timezone to use for the query. Defaults to "Asia/Calcutta".

        Returns:
            requests.Response: The response object from the request.

        Raises:
            OOAIException: If an error occurs during the request.
        """
        query = self._encode_query(query)

        headers = {
            'accept': 'text/event-stream',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        try:
            response = self.scraper.get(
                f'https://oo.ai/api/search?q={query}&lang=en-US&tz={timezone}',
                headers=headers,
                timeout=None,
                stream=True
            )
        except Exception as e:
            raise OOAIException(f"Error during request: {e}")
        return response
    
    def process_stream(self, response, stream: bool) -> OOAIResponse:
        """
        Processes the streamed response from the OOAI service.

        This method iterates over the lines of the response, decoding Unicode characters. It checks each line for the "data:" prefix, indicating a JSON payload. The JSON is then parsed and checked for specific keys based on its 'type'. If the 'type' is 'answer', the 'content' is appended to the streaming response and optionally printed to the console if streaming is enabled. If the 'type' is 'result', the 'references' are stored as the results and the loop is exited.

        Args:
            response: The response object from the request.
            stream (bool): Indicates whether to stream the response to the console.

        Returns:
            OOAIResponse: An instance of OOAIResponse containing the processed streaming response and results.
        """
        response_dict = OOAIResponse()

        for value in response.iter_lines(decode_unicode=True):
            if value and value.startswith("data:"):
                try:
                    parsed_json = json.loads(value[5:])
                    
                    # Check if 'type' and 'content' keys exist in the parsed JSON
                    if 'type' in parsed_json:
                        if parsed_json['type'] == 'answer' and 'content' in parsed_json:
                            response_dict.streaming_response += parsed_json['content']
                            if stream:
                                print(parsed_json['content'], end='', flush=True)
                        elif parsed_json['type'] == 'result' and 'references' in parsed_json:
                            response_dict.results = parsed_json['references']
                            break
                except:continue

        return response_dict

    def _encode_query(self, query: str) -> str:
        """
        Encodes the given query string to ensure it is properly formatted for URL use.

        This method replaces special characters in the query string with their corresponding URL encoded values.
        The characters replaced include space, plus sign, forward slash, question mark, ampersand, number sign, equals sign, colon, and comma.

        Args:
            query (str): The query string to be encoded.

        Returns:
            str: The encoded query string.
        """
        return query.replace(" ", "%20").replace("+", "%2B").replace("/", "%2F").replace("?", "%3F") \
                    .replace("&", "%26").replace("#", "%23").replace("=", "%3D").replace(":", "%3A").replace(",", "%2C")


# Main Service for OOAI
class OOAIService:

    """
    Initializes an instance of OOAIService with a given OOAIRequestHandler.

    Args:
        handler (OOAIRequestHandler): The handler responsible for making requests and processing streams.
    """
    def __init__(self, handler: OOAIRequestHandler):
        """
        Initializes an instance of OOAIService with a given OOAIRequestHandler.

        Args:
            handler (OOAIRequestHandler): The handler responsible for making requests and processing streams.
        """
        self.handler = handler

    def get_ooai_response(self, query: str, timezone: str = "Asia/Calcutta", stream: bool = True) -> OOAIResponse:
        """
        This method is used to get the response from the OOAI service.

        Args:
            query (str): The query to be sent to the OOAI service.
            timezone (str, optional): The timezone to be used for the query. Defaults to "Asia/Calcutta".
            stream (bool, optional): Whether to stream the response. Defaults to True.

        Returns:
            OOAIResponse: The response from the OOAI service.
        """
        try:
            response = self.handler.make_request(query, timezone)
            response_dict = self.handler.process_stream(response, stream)
            return response_dict
        except OOAIException as e:
            print(f"OOAI exception: {e}")
            return OOAIResponse()

# Example Usage
if __name__ == "__main__":
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
