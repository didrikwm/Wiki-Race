import re
import requesting_urls

def find_urls(html_string, base_url="https://en.wikipedia.org"):
    """
    Finds all URLs in a given HTML code.

    Args:
        html_string (String): Containing the HTML code.
        base_url (String, optional): The base URL to be used. Defaults to None.
        output (String, optional): The file to save the URLs to. Defaults to None.

    Returns:
        List: All the URLs found in the HTML code. 
    """
    
    urls = re.findall(r"<a[^>]*href=\"(.*?)[\#\"][^>]*>", html_string)
    """Starting with 'a', followed by any amount of any character but '>', followed by
    'href="', followed by any amount of characters, which I capture in a group, followed by
    either '#' or '"', followed by any amount of any character but '>', followed by '>'."""

    urls = list(filter(None, dict.fromkeys(urls))) # Removes duplicates and empty strings, whilst maintaining order.

    # The following could be done with regex
    for i, url in enumerate(urls):
        if url[0] == "/" and url[1] != "/" and base_url != None:
            urls[i] = base_url + url
        elif url[:2] == "//":
            urls[i] = "https:" + url

    return urls

def find_articles(html_string):
    """
    Finds all Wikipedia URLs in a given HTML code.
    Either returns it or saves it to a file, based on the user's choice. 

    Args:
        html_string (String): Containing the HTML code.
        output (String, optional): The file to save the URLs to. Defaults to None.

    Returns:
        List: All the Wikipedia URLs found in the HTML code. 
    """
    urls = find_urls(html_string)

    #r = re.compile(r".*\w*\.wikipedia.org/")
    r = re.compile(r"^https?:\/\/\w+(?:[\-\.]\w+)?\.wikipedia\.org(?!.*:)")
    """At start of a line: starting with 'http' or 'https', followed by '//', followed by
    1 or more word characters, maybe followed by ('-' or '.' and 1 or more word characters), 
    followed by '.wikipedia.org', and ignoring every match that contain any amount of characters
    followed by ':'. 

    Note: I could not find any good overview of all possible country codes that Wikipedia uses.
    Normally it's just two letters, but sometimes more (and sometimes separated by a "-").
    So to avoid being too specific I assume it's one or more letters that may or may not be 
    followed by a "-" or "." and one or more letters.
    """

    article_url_list = list(filter(r.match, urls)) # Uses RegEx in filter() function to extract directly from list

    return article_url_list

def find_en_articles(html_string):
    """
    New version of the one above, only dealing with English articles.
    Used in the last task of the assignment.

    Args:
        html_string (String): Containing the HTML code.
        output (String, optional): The file to save the URLs to. Defaults to None.

    Returns:
        List: All the English Wikipedia URLs found in the HTML code. 
    """
    urls = find_urls(html_string)

    r = re.compile(r"^https?:\/\/en.wikipedia\.org/wiki/(?!.*:)")

    article_url_list = list(filter(r.match, urls)) # Uses RegEx in filter() function to extract directly from list

    return article_url_list

def test_find_urls():
    html = """
    <a href="#fragment-only">anchor link</a>
    <a id="some-id" href="/relative/path#fragment">relative link</a>
    <a href="//other.host/same-protocol">same-protocol link</a>
    <a href="https://example.com">absolute URL</a>
    """

    urls = find_urls(html, base_url="https://en.wikipedia.org")
    
    assert urls == [
    "https://en.wikipedia.org/relative/path",
    "https://other.host/same-protocol",
    "https://example.com"
    ]

def test_find_articles():
    html = """
    <a href="https://no.wikipedia.org/wiki/Nobel_Prize">Non-English Wiki page</a>
    <a id="some-id" href="https://en.wikipedia.org/relative/path#1234">Wiki page with hashtag</a>
    <a href="https://regex101.com/r/tr9Zqc/1/">Not Wiki page</a>
    <a href="https://vg.no">Not Wiki page</a>
    """

    urls = find_articles(html)
    
    assert urls == [
    "https://no.wikipedia.org/wiki/Nobel_Prize",
    "https://en.wikipedia.org/relative/path"
    ]