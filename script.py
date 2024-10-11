import requests
from bs4 import BeautifulSoup

docURL = 'https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub'

def handleGetURL(URL):
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except:
        return 'There was an error with the URL when fetching content.'
    else:
        return response.text
    
def handleParseData(data):
    parsedData = BeautifulSoup(data, "lxml")
    grid = {}

    tables = parsedData.find_all('table')

    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 3:  
                try:
                    x = int(cells[0].get_text(strip=True))
                    unicode_char = cells[1].get_text(strip=True)
                    y = int(cells[2].get_text(strip=True))
                except ValueError:
                    print(f'Invalid coordinate or character data in row: {row.get_text(strip=True)}')
                    continue

                if x not in grid:
                    grid[x] = {}
                grid[x][y] = unicode_char

    return grid

def displayGrid(grid):
    if not grid:
        print("No data to display.")
        return
    
    max_x = max(grid.keys())
    max_y = max(max(row.keys()) for row in grid.values())

    display_grid = [[' ' for _ in range(max_y + 1)] for _ in range(max_x + 1)]

    for x in grid:
        for y in grid[x]:
            display_grid[x][y] = grid[x][y]

    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            row.append(display_grid[x][y])
        print(' '.join(row))

def displayMessage(URL):
    
    urlContent = handleGetURL(URL)
    grid = handleParseData(urlContent)
    displayGrid(grid)

displayMessage(docURL)
