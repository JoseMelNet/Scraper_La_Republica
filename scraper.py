import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co'

# Xpath of elements in Web "La República"
XPATH_LINK_TO_ARTICLE = '//h2/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/a/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'

# Functions that execute the script

# Functions that enter to link-notice and obtain Title, Summary and Boddy
def parse_notice(link, today):
    try:
        response = requests.get(link)                             # Get answer of server
        if response.status_code == 200:                           # Answer is OK
            notice = response.content.decode('utf-8')             # Obtains HTML-file and decodes characters
            parsed = html.fromstring(notice)                      # Parsing HTML-file to could apply xpath

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


# Obtain the News Links
def parse_home():
    try:
        response = requests.get(HOME_URL)                           # Get answer of server
        if response.status_code == 200:                             # Answer is OK
            home = response.content.decode('utf-8')                 # Obtains HTML-file and decodes characters
            parsed = html.fromstring(home)                          # Parsing HTML-file to could apply xpath
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)  # Obtaing News-links
            links_to_notices.remove('')                             # Delete empty elments
            #print(links_to_notices)
            
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):                           # Cheking if exists a directory with these date-name
                os.mkdir(today)                                    # Create a new directory
            
            for link in links_to_notices:
              parse_notice(link, today)                            # Calling "parse-notice" function
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


# Main Function
def run():
    parse_home()


if __name__ == "__main__":
    run()
