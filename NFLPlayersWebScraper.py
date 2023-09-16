import requests
from bs4 import BeautifulSoup
from functools import reduce


playerInfoList = ["Name", "Position", "Age", "Height", "Weight", "Experience", "College"]

def soupObject(URL):
    headers = {'User-Agent': '...'}
    r = requests.get(url=URL, headers=headers)
    
    return BeautifulSoup(r.content, 'html5lib')

def parsePlayers(playerInfo): 
    def anonimous(tableHtml):
        players = []
        for row in tableHtml.findAll('tr'):
            player = {}
            count = 0
            columns = row.findAll('td', attrs={'class': 'Table__TD'})
            
            player[playerInfo[count]] = columns[count + 1].a.text
            count = count + 1
            
            for info in playerInfo[1:]:
                player[playerInfo[count]] = columns[count + 1].find('div').text
                count = count + 1
            
            players.append(player)
        
        return players
    return anonimous

def scrapeTeamPlayers(URL):
    print("Team url is" + URL)
    soup = soupObject(URL)
    allPlayers = [soup.find('div', attrs={'class':'ResponsiveTable Offense'}).find('tbody'),
    soup.find('div', attrs={'class':'ResponsiveTable Defense'}).find('tbody'),
    soup.find('div', attrs={'class':'ResponsiveTable Special Teams'}).find('tbody')]

    parsingFunction = parsePlayers(playerInfoList)
    parsedPlayers = reduce(lambda a,b: a + b, map(parsingFunction, allPlayers))
    
    return parsedPlayers
    
def scrapeNFLTeamURL(URL):
    nflTeamBoxes = soupObject(URL).find('div', attrs={"id": "my-players-table"}).findAll('div', attrs={"class", "span-2"})
    allTeamsList = reduce(lambda x,y: x + y, map(lambda a:  a.findAll('li'), list(nflTeamBoxes)))
    allTeamsURL = map(lambda a: a.find('div').a['href'], allTeamsList)
    
    return allTeamsURL
     
def writeAllPlayers(fileName, parsedPlayers):
    playerOutFile = open(fileName, "w")

    for row in parsedPlayers:
        lineToWrite = ""
        for column in row:
            lineToWrite += row[column] + ','
           
        playerOutFile.write(lineToWrite[:-1])
        playerOutFile.write('\n')
        
    playerOutFile.close()
        
def composeScraping():
    rootURL = "https://www.espn.com/nfl/players"

    for team in scrapeNFLTeamURL(rootURL):
        teamName = team.split("/")[-1]
        fileName = f"Players/{teamName}.txt"

        writeAllPlayers(fileName, scrapeTeamPlayers(f"https://espn.com{team}")) 
    
composeScraping()


