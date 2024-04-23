
import requests
import logging
from typing import Optional, Dict, Any
import json

logging.basicConfig(level=logging.INFO)


# Colour printing for the console setup:
class ANSIColors:
    RESET = "\033[0m"  # Reset to default color
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"


# Define the API call function
def api_call(
    url: str,
    method: str,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None,
    timeout: int = 10,
) -> Optional[requests.Response]:
    """
    Sends a request to a specified URL and logs the response.

    Parameters:
    - url (str): The URL to send the request to.
    - method (str): The HTTP method to use (e.g., 'GET', 'POST').
    - headers (Optional[Dict[str, str]]): Optional headers to include in the request.
    - data (Optional[Dict[str, Any]]): Optional JSON payload for the request.
    - timeout (int): The timeout for the request in seconds.

    Returns:
    Optional[requests.Response]: The response object from requests if successful, None otherwise.

    Raises:
    - requests.exceptions.HTTPError: For HTTP errors.
    - requests.exceptions.ConnectionError: For connection problems.
    - requests.exceptions.Timeout: For timeouts.
    - requests.exceptions.RequestException: For other types of request-related errors.
    """
    try:
        response = requests.request(
            method, url, headers=headers, json=data, timeout=timeout
        )
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        return e
    except requests.exceptions.ConnectionError as e:
        return e
    except requests.exceptions.Timeout as e:
        return e
    except requests.exceptions.RequestException as e:
        return e


# Define the load_json function
def load_json(inputfile):
    """Load JSON data from a file.
    Parameters:
    - inputfile (str): The path to the input file.

    Returns:
    - json_data (Dict[str, Any]): The JSON data loaded from the file.
    """
    with open(inputfile, "r") as file:
        json_data = json.load(file)
    return json_data


# Define the format_json_response function
def format_json_response(response: requests.Response) -> str:
    try:
        pretty_json = json.dumps(response.json(), indent=4)
        return f"{ANSIColors.CYAN}{pretty_json}{ANSIColors.RESET}"
    except ValueError:
        return f"{ANSIColors.RED}Response is not valid JSON.{ANSIColors.RESET}"


# Define the print_response function
def print_response(response: requests.Response, print_full_response: bool = True):
    """Prints the response status code, response time, and response text, with colours and formatting,
    Parameters:
    - response (requests.Response): The response object from requests.
    - print_full_response (bool): Whether to print the full response text or just a snippet.
    """

    response_time = response.elapsed.total_seconds()
    status_code_color = (
        ANSIColors.GREEN if response.status_code == 200 else ANSIColors.RED
    )
    print(f"{status_code_color}Status Code: {response.status_code}{ANSIColors.RESET}")
    print(f"{ANSIColors.CYAN}Response Time: {response_time} seconds{ANSIColors.RESET}")
    print(
        f"{ANSIColors.YELLOW}Response Text (snippet):{ANSIColors.RESET} {response.text[:250]} ..."
    )
    if "application/json" in response.headers.get("Content-Type", ""):
        formatted_response = format_json_response(response)
    else:
        formatted_response = response.text[:250] + "..."

    # Print response details
    print(f"{ANSIColors.CYAN}Response Time: {response.elapsed.total_seconds()} seconds{ANSIColors.RESET}")
    print(f"{ANSIColors.YELLOW}Response Text (snippet):{ANSIColors.RESET} {formatted_response}")

    if print_full_response:
        # If full response printing is requested, print the entire content appropriately
        full_content = response.text if "application/json" not in response.headers.get("Content-Type", "") else formatted_response
        print(full_content)


# Define the echo_endpoint function, the main entrypoint
def echo_endpoint(
    url: str,
    method: str,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None,
    timeout: int = 10,
    print_full_response: bool = True,
):
    """
    Calls the API using the provided parameters and prints the response.

    Parameters:
    - url (str): The URL to send the request to.
    - method (str): The HTTP method to use (e.g., 'GET', 'POST').
    - headers (Optional[Dict[str, str]]): Optional headers to include in the request.
    - data (Optional[Dict[str, Any]]): Optional JSON payload for the request.
    - timeout (int): The timeout for the request in seconds.
    - print_full_response (bool): Whether to print the full response text or just a snippet.

    The function handles making the API call, error handling, and printing the response.
    """
    # Make the API call
    response = api_call(url, method, headers=headers, data=data, timeout=timeout)

    # Check if the response is not None
    if response:
        # Check for errors in the response:
        if isinstance(response, requests.exceptions.RequestException):
            print(f"{ANSIColors.RED}Request failed. Check the error message for details{ANSIColors.RESET}")
            print(f"{ANSIColors.RED}{response}{ANSIColors.RESET}")
        else:
            # Print the response
            print_response(response, print_full_response)
    else:
        print("Failed to get a response.")
    return response
