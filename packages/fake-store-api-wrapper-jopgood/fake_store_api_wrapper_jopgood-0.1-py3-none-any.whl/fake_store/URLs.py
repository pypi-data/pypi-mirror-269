class URLs:
    """ The URLs class will handle all of the URLs. The purpose of this class is
        to essentially store and serve all of the URL strings useful to the
        FUGA API.

        There is no processing of the URLs or the URL parameters done in this class
        all of that logic is handled in the FUGA_API class.
    """

    def __init__(self):
        """The URLs class constructor which defines all of the URLs used by the API.

            When adding new API functionality the URL needs to be added here.
            Examples abound of the format used by this implementation of the API.

            @param self - the object pointer
            @param response_format - format of the response. Valid values are 'xml' and 'json'.
                Specifying 'xml' will return an ElementTree containing the response XML while
                'json' will return the response in the JSON format.
        """

        self.base_url = "https://fakestoreapi.com"

        # Products
        self.products = "/products"

        # Cart
        self.carts = "/carts"
        
        # User
        self.users = "/users"
        
        # Login
        self.login = "/auth/login"

    def base_url(self):
        """Returns the API request endpoint.
            @param self - the object pointer
        """
        return self.base_url

    def login_url(self):
        """Returns a cookie for future authenticated requests.
            @param self - the object pointer
        """
        return self.base_url + self.login

    """
        Products
    """

    def products_url(self):
        """Combines the request endpoint and trends list URL
            @param self - the object pointer
        """
        return self.base_url + self.products
    
    def product_categories_url(self):
        """Combines the request endpoint and trends list URL
            @param self - the object pointer
        """
        return self.base_url + self.products + "/categories"

    """
        Carts
    """

    def carts_url(self):
        """Combines the request endpoint and products URL
            @param self - the object pointer
        """
        return self.base_url + self.carts

    """
        Users
    """

    def users_url(self):
        """Combines the request endpoint and products URL
            @param self - the object pointer
        """
        return self.base_url + self.users