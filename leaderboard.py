from bs4 import BeautifulSoup
import requests

class Team:
    def __init__(self, name, owner, cats):
        self.name = name
        self.owner = owner
        self.cats = cats

    def printInfo(self):
        print(', '.join([self.name, self.owner] + [str(val) for val in cats.values()]))

response = requests.get('https://www.fleaflicker.com/nba/leagues/20730')
assert(response.status_code == 200)

soup = BeautifulSoup(response.content, 'html.parser')

leagueTable = soup.find(id='body-center-main').table

for row in leagueTable.find_all('tr'):
    nameCell = row.find(class_='league-name')
    if nameCell is not None:
        name = nameCell.get_text()
        maybeOwner = row.find(class_='user-name')
        owner = 'N/A' if maybeOwner is None else maybeOwner.get_text()
        
        cells = row.contents
        cats = dict()
        cats['fgpct'] = float(cells[3].span.get_text())
        cats['ftpct'] = float(cells[4].span.get_text())
        cats['threes'] = int(cells[5].span.get_text().replace(',',''))
        cats['reb'] = int(cells[6].span.get_text().replace(',',''))
        cats['stl'] = int(cells[7].span.get_text().replace(',',''))
        cats['blk'] = int(cells[8].span.get_text().replace(',',''))
        cats['ast'] = int(cells[9].span.get_text().replace(',',''))
        cats['to'] = int(cells[10].span.get_text().replace(',',''))
        cats['pts'] = int(cells[11].span.get_text().replace(',',''))

        team = Team(name, owner, cats)
        team.printInfo()

    
        
        
        
        