import requests
from bs4 import BeautifulSoup




class Covid(object):
    def covid(self, x):
        try:
            url = 'https://www.mohfw.gov.in/'
            # make a GET request to fetch the raw HTML content
            web_content = requests.get(url).content
            flag = 0
            # parse the html content
            soup = BeautifulSoup(web_content, "html.parser")
            # remove any newlines and extra spaces from left and right
            extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
            # find all table rows and data cells within
            stats = []
            all_rows = soup.find_all('tr')
            for row in all_rows:
                stat = extract_contents(row.find_all('td'))
                # notice that the data that we require is now a list of length 5
                if len(stat) == 5:
                    stats.append(stat)
            for i in range(stats.__len__()):
                if str(stats[i][1]).lower() == x.lower():
                    id = i
                    flag = 1
                    break
            if flag == 1:
                message = "State: " + stats[id][1] + "\nConfirmed cases: " + stats[id][2] + "\nRecovered: " + stats[id][3] + "\nDeceased: " + stats[id][3]
                print(message)
                return message
            else:
                message = "You have entered a invalid input please try again!"
                return message
        except:
            message = "We had some technical problem! Please try again! :)"
            return message
