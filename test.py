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
