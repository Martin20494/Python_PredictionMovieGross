"""Program name: Movie Gross Prediciton.

Student name: Thong Minh Nguyen (Martin)
Student ID: 68623131
Tutor: Liam Laing

Description: This program uses the training data gathered from the past to build 
             model that helps movie executive producers predict the gross
             of the movie with provided genre and budget, compare with other
             genres.
             
File: Web scraping

"""
import requests
import csv
from bs4 import BeautifulSoup

PAGE = 5802
URL = "https://www.the-numbers.com/movie/budgets/all/"

def get_page(url):
    ''' Collecting the pages of the website
    '''
    pages = []
    for i in range(5801, PAGE, 100):
        url_page = url + str(i)
        pages.append(url_page)
    return pages

def get_table(url):
    ''' Finding table in the website inspection
    '''
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    last_links = soup.find(class_="pagination")
    last_links.decompose()
    table = soup.find("table")    
    return table

def get_length(url):
    '''Number of values in each page
    '''
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    last_links = soup.find(class_="pagination")
    last_links.decompose()
    number_of_values = soup.find("table").find_all("tr")   
    return len(number_of_values)  

def get_year(table, number):
    ''' Collecting year value from website
    '''
    years = table.find_all("tr")[number].find_all("td")[1].find("a")
    years_list = years.contents[0]
    if years_list != 'Unknown':
        years_value = years_list.split(',')
        if len(years_value) > 1:
            each_year = int(years_value[1])
            return each_year
        else:
            return int(years_value[0])    

def get_budget(table, number):
    ''' Collecting budget value from website
    '''
    budget = table.find_all("tr")[number].find_all("td")[3]
    return budget.contents[0]    

def get_domestic(table, number):
    ''' Collecting domestic gross value from website
    '''
    domestic = table.find_all("tr")[number].find_all("td")[4]
    return domestic.contents[0]

def get_worldwide(table, number):
    ''' Collecting worldwide gross value from website
    '''
    worldwide = table.find_all("tr")[number].find_all("td")[5]
    return worldwide.contents[0]

def get_link(table, number):
    ''' Collecting link of genre
    '''
    link_code = table.find_all("tr")[number].find_all("td")[2].find("b")
    link = 'https://www.the-numbers.com' + link_code.contents[0].get('href')
    return link     

def get_genre(url_genre):
    ''' Collecting genre from website from the link
    '''
    page = requests.get(url_genre)
    soup = BeautifulSoup(page.text, "html.parser")
    table_list = soup.find('div', {'id':'summary'}).find_all("table")
    for val in range(4):
        try:
            table = table_list[val]
            newlist = []
            for num in range(len(table.find_all("tr"))):
                genre_link = table.find_all("tr")[num].find_all("td")[0].find("b")
                genre = genre_link.contents[0]
                if str(genre) == 'Genre:':
                    element = table.find_all("tr")[num].find_all("td")[1].find("a").contents[0]
                    newlist.append(element)
                else:
                    newlist.append("Unknown")
            newset = set(newlist)
            if len(newset) > 1:
                newset.remove("Unknown")
                result1 = newset.pop()
                return result1
            else:
                result2 = newset.pop()
                return result2              
        except IndexError:
            pass

def get_value(values, page):
    ''' Creating value list that contains year, budget, domestic_gross,
        worldwide_gross and genre
    '''
    table = get_table(page)
    length = get_length(page)
    for num in range(1, length):
        year = get_year(table, num)
        if year != None and year < 2019:
            budget = get_budget(table, num).strip().replace("$","").replace(",", "")
            domestic_gross = get_domestic(table, num).strip().replace("$","").replace(",", "")
            worldwide_gross = get_worldwide(table, num).strip().replace("$","").replace(",", "")
            link = get_link(table, num)
            genre = get_genre(link)
            values.append([year, budget, domestic_gross, worldwide_gross, genre])  

def csv_file(values):
    ''' Writing values into csv file
    '''
    with open('Movie.csv', 'w', encoding='utf8') as file:
        file_writer = csv.writer(file)
        file_writer.writerow(['Year', 'Budget', 'Domestic gross', 'Worldwide gross', 'Genre'])
        for year, budget, domestic, worldwide, genre in values:
            file_writer.writerow([year, budget, domestic, worldwide, genre])
                                       
def main():
    ''' Main function
    '''
    pages = get_page(URL)
    values = []
    for page in pages:
        get_value(values, page)
    csv_file(values)
            
        
    

    