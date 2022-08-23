from collections import deque
import requesting_urls
import filter_urls
import re
from bs4 import BeautifulSoup
import time

from multiprocessing.pool import ThreadPool
from multiprocessing import Manager

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' # The letters will be used in a dictionary containing visited links

def get_linking_articles(url):
    """
    Finds all Wikipedia articles that link to a given Wikipedia article.
    Is used to avoid unnecesary steps when searching for the end url.

    Args:
        url (string): The url to the Wikipedia article to find links to.

    Returns:
        list: All the articles that link to the given url.
    """
    page_path = url[30:]
    html = requesting_urls.get_html(f"https://en.wikipedia.org/w/index.php?title=Special:WhatLinksHere/{page_path}&limit=5000&namespace=0")
    # Insert the path of the end article into a general link for a Wiki page that shows links to all articles that link to the provided Wiki article.

    soup = BeautifulSoup(html, "html.parser")

    links = None

    links_section = soup.find(id="mw-whatlinkshere-list")
    links = re.findall(r"<li><a href=\"([^ ]*)\"", str(links_section))

    return links

def manage_paths(path, page, link, end):
    """
    Stores and manages paths.

    Args:
        path (dict): A dictionary of all paths. Key is a certain url and value is a list of urls leading to that url.
        page (string): The current page that has been popped from the queue.
        link (string): A link found on that page.
        end (string): The end url. 

    Returns:
        list: all urls leading to the end url, OR
        string: the current link.
    """
    if link == end:
        return path[page] + [link]
    if (link not in path) and (link != page):
        path[link] = path[page] + [link]
        return link

def get_links(url):
    """
    Helping function that calls needed functions from other files, 
    in order to retrieve the Wiki links from an article.

    Args:
        url (string): url to the Wiki article to retrieve links from.

    Returns:
        list: all links found. 
    """
    links = filter_urls.find_en_articles(requesting_urls.get_html(url))
    if len(links) < 2: # Only one link, in combination with threading, may cause problems,
        return [" ", " "] # so in that case I return a list of two empty strings
    return links

def find_shortest_path(start, end):
    """
    Finds the shortest path between two Wikipedia articles.

    Args:
        start (string): The start article.
        end (string): The end article.

    Returns:
        list: The links along the shortest path, or None
    """
    path = Manager().dict() # Dictionary that supports multiprocessing
    path[start] = [start]
    Q = deque(path[start])
    visited = set([start])

    links_to_end = set(get_linking_articles(end))

    priority = False 

    while len(Q) != 0:
        page = Q.popleft() 

        links = get_links(page)

        pool = ThreadPool(processes=len(links))
        results = [pool.apply(manage_paths, args=(path, page, link, end)) for link in links]
        pool.terminate()

        for result in results:
            if type(result) == list:
                return result
            if not result or len(result) < 31: # If result is None or not valid link
                continue
            page_path = result[24:] # Stores only part of link from '/wiki/...'
            if result not in visited:
                if page_path in links_to_end and not priority: # If this link links to the end article, and no other page is already prioritized
                    priority = True 
                    Q.appendleft(result) # Adds that link to the start of the queue
                    visited.add(result)
                    break # Break the loop to skip the rest
                else:
                    Q.append(result)
                visited.add(result)

    return None

if __name__ == "__main__":
    starting_url = input("Enter starting url > ")
    end_url = input("Enter end url > ")

    start = time.time()

    path = find_shortest_path(starting_url, end_url)

    end = time.time()
    tot = str(end - start) + " s"

    [print(url + "\n") for url in path]
    print("Time: " + tot)