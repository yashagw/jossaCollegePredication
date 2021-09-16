import time
import csv
import os

import click
from selenium import webdriver
from bs4 import BeautifulSoup

chromedriver = "chromedriver.exe"


def save_html(names, year):
    driver = webdriver.Chrome(f"{chromedriver}")
    for name in names:
        driver.get("https://www.collegepravesh.com/cutoff/nit-{}-cutoff-{}/".format(name, year))

        driver.find_element_by_xpath("//select[@id='cat']/option[text()='General']").click()
        driver.find_element_by_xpath("//select[@id='seat-pool']/option[text()='Gender Neutral']").click()
        driver.find_element_by_xpath("//a[@id='cp-cut-go']").click()
        time.sleep(2)

        html = driver.page_source
        f = open("{}_data/{}_{}.html".format(year, name, year), 'w+')
        f.write(html)

    driver.close()


def get_info(soup, branch_want, minClosingRank, home_state, collegename, round_no):
    opgn = soup.find('div', id='op-gn')
    post_tabs = opgn.find('div', class_="post-tabs")

    panes = post_tabs.find_all('div', class_="pane")
    round_table = panes[round_no - 1].find('table')

    tr_rows = round_table.find_all('tr')[2:]
    final_os_rows = []

    for tr in tr_rows:
        td_rows = tr.find_all('td')
        if collegename == home_state:
            check = "HS"
        else:
            check = "OS"

        if td_rows[0].get_text() == check and td_rows[1].get_text() in branch_want and int(td_rows[3].get_text()) > minClosingRank:
            with open('colleges.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([td_rows[1].get_text(), td_rows[2].get_text(), td_rows[3].get_text()])
                final_os_rows.append(tr)


def main(year, minClosingRank, home_state, round_no):
    college_list = ['nagpur', 'jaipur', 'delhi']
    branch_want = ['Computer Science and Engineering', 'Electrical Engineering',
                   'Electronics and Communication Engineering', 'Mechanical Engineering',
                   'Electrical and Electronics Engineering', 'Information Technology']

    save_html(college_list, year)

    with open('colleges.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Year - " + str(year), "Min Closing Rank - " + str(minClosingRank)])

    for filename in os.listdir("{}_data/".format(year)):
        if filename.endswith('.html'):
            fname = filename.split("_")
            collegename = fname[0]
            collegeext = fname[1]

            f_location = "{}_data/{}_{}".format(year, collegename, collegeext)
            print(f_location)
            with open(f_location, 'r') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

                with open('colleges.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([])
                    writer.writerow(["NIT {}".format(collegename.upper())])
                    writer.writerow(["Branch Name", "Open", "Close"])

                get_info(soup, branch_want, minClosingRank, home_state, collegename, round_no)

year = 2018
minClosingRank = 15500
home_state = 'surathkal'
round_no = 5
main(year, minClosingRank, home_state, round_no)
