from bs4 import BeautifulSoup
import os, sys


def scrape_page(url, session, folder_crawled="pages_crawled", html_prefix="https://community.whattoexpect.com"):
    # TODO: add try-catching
    # Get urls on current page
    soup = BeautifulSoup(session.get(url).text, "html.parser")
    links_on_current_page = soup.find_all('a', class_="linkDiscussion", href=True)
    ans = dict()
    for i in range(len(links_on_current_page)):
        link = f"{html_prefix}{links_on_current_page[i]['href']}"
        print(link)  # for debugging and to see the progress
        # Save text from the url to a <url>.txt file
        with open(f'{folder_crawled}/{link[8:].replace("/", "_")}.txt', "w", encoding="UTF-8") as f:
            # Get the text from the URL using BeautifulSoup
            soup = BeautifulSoup(session.get(link).text, "html.parser")
            post_title = soup.find('h1', class_="discussion-original-post__title")
            if post_title:
                text_topic = post_title.get_text().encode('utf-16', 'surrogatepass').decode('utf-16')
                post_text = soup.find('div', class_="discussion-original-post__content")
                text_question = post_text.get_text().encode('utf-16', 'surrogatepass').decode(
                    'utf-16') if post_text else None
                text_posts = soup.find_all('div',
                                           class_="wte-reply__content__message __messageContent fr-element fr-view")
                posts_in_topic = [t.get_text().encode('utf-16', 'surrogatepass').decode('utf-16') for t in text_posts]
                context = f"""Topic: {text_topic}
                    {text_question}
                    {chr(10).join(posts_in_topic)}
                    """
                f.write(context)
                ans[i] = dict()
                ans[i]['topic'] = text_topic
                ans[i]['question'] = text_question
                ans[i]['replies'] = posts_in_topic
    return ans


def get_next_page_link(url, session, html_prefix="https://community.whattoexpect.com"):
    soup = BeautifulSoup(session.get(url).text, "html.parser")
    next_page = soup.find('a', class_="page-link", href=True)
    if next_page:
        next_page_url = f"{html_prefix}{next_page.get('href')}"
        return next_page_url
    else:
        return None


# Function to crawl all the URLs within a page and its max_next_pages
def crawl(url, session, max_next_pages=10,
          folder_crawled="pages_crawled",
          html_prefix="https://community.whattoexpect.com"):
    # Parse the URL and get the domain
    # html_prefix = urlparse(url).netloc
    # Create a directory to store the text files
    if not os.path.exists(folder_crawled):
        os.mkdir(folder_crawled)
    ans_all = dict()
    # Get urls on current page
    current_page = url
    ans_all[0] = scrape_page(current_page, session, folder_crawled=folder_crawled, html_prefix=html_prefix)
    next_pages = 1
    while next_pages < max_next_pages:
        # Get url of next page
        next_page_url = get_next_page_link(current_page, session, html_prefix=html_prefix)
        current_page = next_page_url
        if current_page:
            # Get urls on next page
            ans_all[next_pages] = scrape_page(current_page, session, folder_crawled=folder_crawled,
                                              html_prefix=html_prefix)
        next_pages += 1
    return ans_all
