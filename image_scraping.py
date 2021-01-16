import requests
from bs4 import BeautifulSoup


def get_google_image_link(word):
    """
    Function returns a url for the movie image in google search resoults
    Returns second image as first is a search_url
    :param word: search word
    :return: url
    """
    url = 'https://www.google.com/search?q=' + word + '&client=opera&hs=cTQ&source=lnms&tbm=isch&sa=X&ved=0ahUKEwig3LOx4PzKAhWGFywKHZyZAAgQ_AUIBygB&biw=1920&bih=982'
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return soup.find_all('img')[1].get('src')


def get_movie_details(movieId):
    """
    Function searches for movie description on the IMDb website, returns a dictionary of movie data
    Function partly taken from: https://dev.to/magesh236/scrape-imdb-movie-rating-and-details-3a7c
    :param movieId: movieId from IMDb
    :return: dict('description': str(),
                  'credits': Dict('Director': list(dict('link': , 'name': ), ...),
                                  'Writers': list(dict('link': , 'name': ), ...),
                                  'Stars'; list(dict('link': , 'name': ), ...))
    """
    url = "https://www.imdb.com/title/{}/".format(movieId)
    data = {}
    r = requests.get(url=url)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(r.text, 'html.parser')

    # summary
    summary_text = soup.find("div", {'class':'summary_text'})
    data["description"] = summary_text.string.strip()

    credit_summary_item = soup.find_all("div", {'class':'credit_summary_item'})
    data["credits"] = {}
    for i in credit_summary_item:
        item = i.find("h4")
        names = i.find_all("a")
        data["credits"][item.string] = []
        for i in names:
            data["credits"][item.string].append({
                "link": i["href"],
                "name": i.string
            })
    return data


