import logging
from xml.etree import ElementTree
from requests import Response
import requests
from typing import Union

from .URLs import URLs

# Configure the logging format
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

class MissingIdError(Exception):
    """Exception raised when a product ID is missing."""

class IncorrectIdError(Exception):
    """Exception raised when an incorrect product ID format is provided."""

class fake_store:
    """
    The main class providing authenticated access to the Fake Store API.

    This class allows access to the supported GET and POST requests provided by Fake Store.
    It handles authentication, handling requests, and processing responses.

    Parameters
    ----------
    response_format : str, optional
        The format of the API response. Valid values are 'xml' and 'json'.
        Defaults to 'json', which returns responses in JSON format.
        Specifying 'xml' returns responses in an ElementTree containing XML data.
    """
    
    def __init__(self,
                 response_format: str = "json"):
        """
        Initializes the fake_store object.

        Parameters
        ----------
        response_format : str, optional
            The format of the API response. Valid values are 'xml' and 'json'.
            Defaults to 'json', which returns responses in JSON format.
            Specifying 'xml' returns responses in an ElementTree containing XML data.
        """
        self.format = response_format
        self.url = URLs()
        
    def __to_format(self, response: Response, xml: bool = False):
        """
        Converts the API response to the desired format.

        Parameters
        ----------
        response : Response
            The response received from the API request.
        xml : bool, optional
            Determines whether to parse the response as XML (default is False for JSON format).

        Returns
        -------
        dict or ElementTree.Element
            Returns the API response in the desired format:
            - If the response status code is not 200, it handles specific status codes (429, 414, 404) and exits.
            - If the response is None, it returns False.
            - If the desired format is JSON and 'xml' is False, it returns the JSON representation of the response.
            - If 'xml' is True or the format is not JSON, it returns the ElementTree.Element from the response content.

        Notes
        -----
        - This private method converts the API response to the desired format (JSON or XML).
        - It handles specific HTTP status codes (429, 414, 404) by displaying appropriate messages and exiting.
        - If the response status code is not 200, the method exits with a message.
        - If the response is None, it returns False.
        - Based on the 'xml' parameter and the 'format' attribute, it returns the response content
        in either JSON format or as an ElementTree.Element.
        """
        if response.status_code != 200:
            if response.status_code == 429:
                logging.error("Too many requests, exiting.")
                exit()
            elif response.status_code == 414:
                logging.error(
                    "URI too long, please chunk ticker symbols. Exiting.")
                exit()
            elif response.status_code == 404:
                logging.error(
                    f"404 error! Error Content:\n{response.text}. Exiting.")
                exit()
        elif response is None:
            return False

        if self.format == "json" and not xml:
            return response.json()
        else:
            return ElementTree.fromstring(response.content)
        
    def __get_data(self,
                   url: str,
                   parameters: dict = None,
                   headers: dict = None
                   ) -> Union[dict, None]:
        """
        Retrieves data from a specified URL endpoint in the requested format.

        Parameters
        ----------
        url : str
            The URL endpoint from which data will be retrieved.
        parameters : dict, optional
            A dictionary containing optional parameters to be sent with the request (default is None).
        headers : dict, optional
            A dictionary containing optional headers to be sent with the request (default is None).

        Returns
        -------
        dict or None
            Returns the retrieved data in dictionary format if successful.
            Returns None if data retrieval encounters issues.

        Notes
        -----
        - This is a private method used internally to fetch data from the specified URL.
        - The retrieved data is processed and returned in the desired format using the private method '__to_format()'.
        """
        headers = headers if headers else {}
        params = parameters if parameters else {}

        return self.__to_format(
            requests.get(url, headers=headers, params=params))
        
    """
    PRODUCTS
    """
    def products(self, category: str = None, sort='desc', limit=5) -> Union[dict, None]:
        """
        Retrieves products from the API.

        Parameters
        ----------
        category : str, optional
            The category of products to retrieve.
        sort : str, optional
            The sorting order for the products (default is 'desc').
        limit : int, optional
            The maximum number of products to retrieve (default is 5).

        Returns
        -------
        dict or None
            Returns the retrieved products in dictionary format if successful.
            Returns None if data retrieval encounters issues.
        """
        params = {
            'sort': sort,
            'limit': limit
        }
        
        url = self.url.products_url()
        
        if category:
            url = url + f"/category/{category}" 
            
        return self.__get_data(url,
                               parameters=params)
        
    def product_categories(self) -> Union[dict, None]:
        """
        Retrieves available product categories from the API.

        Returns
        -------
        dict or None
            Returns the retrieved product categories in dictionary format if successful.
            Returns None if data retrieval encounters issues.
        """
        return self.__get_data(self.url.product_categories_url())
        
    def product(self, product_id=None, sort='desc', limit=5) -> Union[dict, None]:
        """
        Retrieves a specific product from the API.

        Parameters
        ----------
        product_id : int
            The ID of the product to retrieve.
        sort : str, optional
            The sorting order for the product (default is 'desc').
        limit : int, optional
            The maximum number of products to retrieve (default is 5).

        Returns
        -------
        dict or None
            Returns the retrieved product in dictionary format if successful.
            Returns None if data retrieval encounters issues.

        Raises
        ------
        MissingIdError
            If the product ID is missing.
        IncorrectIdError
            If the product ID is not of the expected format (integer).
        """
        if not product_id:
            raise MissingIdError("Missing a product ID! Please enter an ID for an existing product.")
        
        if not isinstance(product_id, int):
            raise IncorrectIdError(f"The ID: {product_id} is not of expected format: int.")

        params = {
            'sort': sort,
            'limit': limit
        }
            
        return self.__get_data(self.url.products_url() + f"/{product_id}",
                               parameters=params)
        
    """
    CARTS
    """
    def carts(self, start_date=None, end_date=None, sort='desc', limit=5) -> Union[dict, None]:
        """
        Retrieves cart data from the API.

        Parameters
        ----------
        start_date : str, optional
            The start date for filtering cart data.
        end_date : str, optional
            The end date for filtering cart data.
        sort : str, optional
            The sorting order for the cart data (default is 'desc').
        limit : int, optional
            The maximum number of cart items to retrieve (default is 5).

        Returns
        -------
        dict or None
            Returns the retrieved cart data in dictionary format if successful.
            Returns None if data retrieval encounters issues.
        """
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
            
        params['sort'] = sort
        params['limit'] = limit
            
        return self.__get_data(self.url.carts_url(),
                               parameters=params)
