from bs4 import BeautifulSoup
import requests

class Team:
    def __init__(self, name, fgpct, ftpct, threes, reb, stl, blk, ast, to, pts):
        self.name = name
        self.owner = owner
        self.fgpct = fgpct
        self.ftpct = ftpct
        self.threes = threes
        self.reb = reb
        self.stl = stl
        self.blk = blk
        self.ast = ast
        self.to = to
        self.pts = pts

    def printInfo(self):
        print(', '.join([self.name, self.owner, str(self.fgpct), str(self.ftpct), str(self.threes), str(self.reb), str(self.stl), str(self.blk), str(self.ast), str(self.to), str(self.pts)]))

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
        fgpct = float(cells[3].span.get_text())
        ftpct = float(cells[4].span.get_text())
        threes = int(cells[5].span.get_text().replace(',',''))
        reb = int(cells[6].span.get_text().replace(',',''))
        stl = int(cells[7].span.get_text().replace(',',''))
        blk = int(cells[8].span.get_text().replace(',',''))
        ast = int(cells[9].span.get_text().replace(',',''))
        to = int(cells[10].span.get_text().replace(',',''))
        pts = int(cells[11].span.get_text().replace(',',''))

        team = Team(name, fgpct, ftpct, threes, reb, stl, blk, ast, to, pts)
        team.printInfo()

    
        
        
        
        