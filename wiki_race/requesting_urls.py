# import what you need
import requests as req

def get_html(url, params=None):
    """
    Gets the HTML from a given URL, with optional parameters.

    Args:
        url (String): The URL to get the HTML from.
        params (Dict, optional): The parameters that are passed to the get function. Defaults to None.
        output (String, optional): The file to save the HTML to. Defaults to None.

    Returns:
        String: The source code (HTML) of the URL. 
    """
    if url != None:
        response = req.get(url, params=params)
    else:
        return ""

    if response.status_code != 200:
        return "" # Had to switch the assert statement to this one to avoid dead links messing up in 5.6

    src = response.text
    return src


