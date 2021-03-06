from bs4 import BeautifulSoup
import csv
import operator
import requests
import sys

class Team:
    def __init__(self, name, owner, cats):
        self.name = name
        self.owner = owner
        self.categories = cats # value of each stat category
        self.points = {} # points for each category
        self.total = 0

    def sumPoints(self):
        self.total = sum([val for key, val in self.points.items()])

    def printInfo(self):
        print(', '.join([self.name, self.owner] + [str(val) for val in categories.values()]))

def loadHtmlPages(leagueUrls):
    pages = []
    for url in leagueUrls:
        response = requests.get(url.strip())
        assert(response.status_code == 200)
        pages.append(response.content)
    return pages

def scrapeTeamDataForLeague(htmlPage):
    soup = BeautifulSoup(htmlPage, 'html.parser')
    leagueTable = soup.find(id='body-center-main').table

    teams = []
    for row in leagueTable.find_all('tr'):
        nameCell = row.find(class_='league-name')
        if nameCell is not None:
            name = nameCell.get_text()
            maybeOwner = row.find(class_='user-name')
            owner = 'N/A' if maybeOwner is None else maybeOwner.get_text()
            
            cells = row.contents
            cats = dict()
            cats['FG%'] = float(cells[3].span.get_text())
            cats['FT%'] = float(cells[4].span.get_text())
            cats['3Pt'] = int(cells[5].span.get_text().replace(',',''))
            cats['Reb'] = int(cells[6].span.get_text().replace(',',''))
            cats['Stl'] = int(cells[7].span.get_text().replace(',',''))
            cats['Blk'] = int(cells[8].span.get_text().replace(',',''))
            cats['Ast'] = int(cells[9].span.get_text().replace(',',''))
            cats['TO'] = int(cells[10].span.get_text().replace(',',''))
            cats['Pts'] = int(cells[11].span.get_text().replace(',',''))

            team = Team(name, owner, cats)
            teams.append(team)
    return teams

def addCategoryRanks(teams, categories):
    for cat in categories:
        team_value = {team: team.categories[cat] for team in teams}

        sort_descending = (cat != 'TO')
        sorted_dict = sorted(team_value.items(), key=operator.itemgetter(1), reverse=sort_descending)
        
        prev = -1
        current_points = 0
        teamsToScore = []
        for idx, (team, value) in enumerate(sorted_dict):
            if 0.0001 > abs(value - prev): # tied with current teamsToScore
                if len(teamsToScore) == 1:
                    current_points -= 0.5
                teamsToScore.append(team)
            else: # not tied with above group, can now score those teams
                for t in teamsToScore:
                    t.points[cat] = current_points
                current_points = len(teams) - idx
                teamsToScore = [team]
            prev = value
        for t in teamsToScore: # score the final group left after last iteration
            t.points[cat] = current_points

def writeToCSV(output, teams, cats):
    with open(output, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        cat_header = [c for cat in zip(cats, [s + ' Rank' for s in cats]) for c in cat]
        writer.writerow(['Rank', 'Team', 'Owner', 'Overall'] + cat_header)
        for idx, team in enumerate(teams):
            val_rank = [(team.categories[cat], team.points[cat]) for cat in cats] # category value paired with rank points
            cat_row = list(sum(val_rank, ())) # flatten list of value/rank pairs
            writer.writerow([idx+1, team.name, team.owner, team.total] + cat_row )

def main():
    categories = ['FG%', 'FT%', '3Pt', 'Reb', 'Stl', 'Blk', 'Ast', 'TO', 'Pts']
    leagueUrls = []
    for inputFile in sys.argv[1].split(','):
        with open(inputFile, 'r') as f:
            leagueUrls.extend(f.readlines())
    
    leaguePages = loadHtmlPages(leagueUrls)
    teams = []
    for page in leaguePages:
        teams.extend(scrapeTeamDataForLeague(page))

    addCategoryRanks(teams, categories) 
    for team in teams:
        team.sumPoints()

    teams.sort(key=lambda t: t.total, reverse=True)
    # for idx, team in enumerate(teams):
    #     print "{0}) {1}: {2}".format(idx+1, team.owner, team.total)

    writeToCSV(sys.argv[2], teams, categories)

if __name__ == "__main__":
    main()

    
        
        
        
        