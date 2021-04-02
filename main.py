import os
import re
import string
import urllib.request, urllib.parse, urllib.error
import http

crawl_dir = "J:\\test_films"
# crawl_dir = "J:\\KG5"
movie_formats = [".mkv", ".avi", ".mp4"]
found_movies = []

class movie(object):
    def __init__(self, path, raw_title, clean_title=None, parent_folders=None, year=None, director=None, synopsis=None, imdb_score=None):
        self.path = path
        self.raw_title = raw_title
        self.clean_title = clean_title
        self.parent_folders = parent_folders
        self.year = year
        self.director = director
        self.synopsis = synopsis
        self.imdb_score = imdb_score

bad_terms = [
    "xvid",
    "dvdrip",
    "dvd",
    "AC3",
    "AAC2",
    "web dl",
    "webdl",
    "sample",
    "extras",
    "trailer",
    "x264",
    "BRRip",
    "BluRay",
    "amzn",
    "skot013",
    "H264",
    "AAC",
    "CMYK",
    "REMUX",
    "REMUXED",
    "264",
    "HD4",
    "HD4U",
    "FLAC",
    "DDP5",
    "FSi",
    "DTS",
    "NTSC",
    "WEBRIP",
    "ACC",
    "DD5",
    "RIYE"


]

for folder in os.walk(crawl_dir):
    for found_file in folder[2]:
        if found_file[-4:].lower() in movie_formats:
            path = folder[0] + '\\' + found_file
            raw_title = found_file[:-4].replace(".", " ").replace("_", " ").replace("-", " ").replace("&", "And")
            parent_folders = folder[0][len(crawl_dir) + 1:].replace("\\", " ").replace(".", " ").replace("_", " ").replace("-", " ").replace("&", "And")
            for term in bad_terms:
                raw_title = re.sub(term, "", raw_title, flags=re.IGNORECASE)
                parent_folders = re.sub(term, "", parent_folders, flags=re.IGNORECASE)
            parent_folders = parent_folders.translate(str.maketrans('', '', string.punctuation))  # removes punctuation
            parent_folders = re.sub("([a-z])([A-Z])", "\g<1> \g<2>", parent_folders)  # spaces out joined up capitalised words
            parent_folders = re.sub("([0-9])([A-Z])", "\g<1> \g<2>", parent_folders)  # spaces out joined up capitalised words and numbers
            parent_folders = re.sub("[0-9]{3,4}p", "", parent_folders)  # removes resolution specification
            year = re.findall(("[0-9]{4}"), raw_title) # gets year but not if it looks like a resolution spec
            if year and year[0] != "1080" and year[0] != "2160":
                year = year[0]
            else:
                year = ""
            raw_title = raw_title.translate(str.maketrans('', '', string.punctuation))  # removes punctuation
            raw_title = re.sub("([a-z])([A-Z])","\g<1> \g<2>",raw_title) # spaces out joined up capitalised words
            raw_title = re.sub("([0-9])([A-Z])", "\g<1> \g<2>", raw_title) # spaces out joined up capitalised words and numbers
            raw_title = re.sub("[0-9]{3,4}p", "", raw_title) # removes resolution specification
            raw_title = re.sub("[0-9]{4}", "", raw_title)  # removes year specification
            if not year:
                parent_year_check = re.findall(("[0-9]{4}"), parent_folders)
                if parent_year_check and parent_year_check[0] != "1080" and parent_year_check[0] != "2660":
                    year = parent_year_check[0]

            if raw_title:
                found_movies.append(movie(path, raw_title, parent_folders=parent_folders, year=year))


def google_search_from_movie(movie):
    search_url = r"https://www.google.com/search?q="
    search_url += '+'.join(movie.raw_title.split())
    if movie.parent_folders:
        search_url += '+' + '+'.join(movie.parent_folders.split())
    if movie.year:
        search_url += '+' + movie.year
    search_url += '+imdb'

    return search_url

def webpage_to_string(url):
    """
    Returns a string of the raw HTML for an entire web page.

    :param url: (string or HTTPResponse object') The URL of the website as a string, or an HTTPResponse object (part of
    the http library) that has been requested before being passed as an argument. This function handles either.
    :return: (string) A string of the raw HTML for the URL provided.
    """
    if isinstance(url, str):
        return str(list(urllib.request.urlopen(url)))
    if isinstance(url, http.client.HTTPResponse):
        return str(list(url))
    return 'Error: URL provided is not a string or an HTTPResponse object'


# includes not yet implemented lines (commented out) for finding imdb entries for the movie via google search
if len(found_movies) > 0:
    for each_movie in found_movies:
        print(each_movie.raw_title, each_movie.path, each_movie.parent_folders, each_movie.year)
        # google_search = google_search_from_movie(each_movie)
        # print(google_search)
        print()

        # google_results_page = urllib.request.urlopen(google_search)
        # imdb_page = re.findall('https://www.imdb.com/title/(.+?)/', google_results_page)
        # if imdb_page:
        #     print(webpage_to_string(imdb_page))