import openai
import os
import requests
import json
from crawler import crawl
from chatgpt import summarize_replies


def main(domain="community.whattoexpect.com/forums/march-2023-babies.html",
         html_prefix="https://community.whattoexpect.com",
         folder_crawled="pages_crawled/whattoexpect_mar"):
    full_url = f"https://{domain}"
    print(full_url)

    # 1. Crawl forums for topics and replies
    session = requests.Session()
    ans_all = crawl(full_url, session, max_next_pages=100,
                    folder_crawled=folder_crawled, html_prefix=html_prefix)

    # 2. Summarize posts to a topic with GPT-3.5 prompt-chat-completion model
    response = dict()
    final_dict = dict()
    counter = 0
    for i in range(len(ans_all)):
        for j in range(len(ans_all[i])):
            print(counter)
            response[counter] = summarize_replies(ans_all[i][j],
                                                  model="gpt-3.5-turbo-0613",
                                                  temperature=0.7,
                                                  max_tokens=1000)
            print(f"{response[counter]}\n\n\n\n")
            final_dict[counter] = {'prompt': ans_all[i][j], 'completion': response[counter]}
            counter += 1

    # Write summaries to json
    with open(f'{folder_crawled}/responses.json', 'w') as fp:
        json.dump(final_dict, fp)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    openai.api_key = os.environ['OPENAI_API_KEY']
    main(domain="community.whattoexpect.com/forums/march-2023-babies.html",
         html_prefix="https://community.whattoexpect.com",
         folder_crawled="apps/web-crawl-q-and-a/pages_crawled/whattoexpect_mar")
