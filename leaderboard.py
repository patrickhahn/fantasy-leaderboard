from bs4 import BeautifulSoup
import requests

response = requests.get('https://www.fleaflicker.com/nba/leagues/20730')
assert(response.status_code == 200)

soup = BeautifulSoup(response.content, 'html.parser')

leagueTable = soup.find(id="body-center-main")

print(leagueTable.prettify())