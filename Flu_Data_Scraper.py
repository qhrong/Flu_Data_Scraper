from bs4 import BeautifulSoup as soup
import selenium.webdriver as webdriver
import html2text
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Look for "Submit" button and click the button (leads to search page)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path=r"/home/qhrong/PycharmProjects/MA664_AI_Project/chromedriver", chrome_options=options)
driver.get('https://www.fludb.org/brc/influenza_humanSurveillanceData_search.spg?method=ShowCleanSearch&decorator=influenza')
driver.set_window_size(1024, 768)
window_one = driver.current_window_handle
# print(window_one)
search = driver.find_element_by_link_text('Search')

#ActionChains(driver)\
#    .key_down(Keys.CONTROL)\
#    .click(search)\
#    .key_up(Keys.CONTROL)\
#    .perform()

driver.implicitly_wait(5)

search.click()

driver.switch_to.window(driver.current_window_handle)
window_two = driver.current_window_handle

# Loop through pages
#page_num = int((driver.find_element_by_xpath("//*[@id='surveillanceRecordBeanResult']/div[7]/text()")).text)
#print(page_num)

loop_res = []

while True:

    driver.switch_to.window(driver.window_handles[-1])

    # Loop through rows in table in each page

    # table_soup = soup(driver.page_source, 'html.parser')
    # h = table_soup.select('#search-result-table > tbody > tr')
    table = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[2]/form/div[6]/div/table")
    loop_list = []
    for row in table.find_elements_by_xpath(".//tbody/tr"):
        loop_list.append((row.find_element_by_xpath(".//td[3]/a")).text)

    for i in range(len(loop_list)):
        result = driver.find_element_by_xpath("//*[@id='search-result-table']/tbody/tr[%i]/td[3]/a" % (i+1))
        driver.implicitly_wait(5)

        ActionChains(driver)\
            .key_down(Keys.CONTROL)\
            .click(result)\
            .key_up(Keys.CONTROL)\
            .perform()

        # result.click()
        driver.switch_to.window(driver.window_handles[-1])

        # Capture subject information
        info_soup = soup(driver.page_source, 'html.parser')
        h = html2text.HTML2Text()
        loop_res.append(h.handle(str(info_soup.select("#content > div:nth-of-type(4) > table > tbody"))))
        print(h.handle(str(info_soup.select("#content > div:nth-of-type(4) > table > tbody"))))
        # print(h.handle(str(info_soup.select("#content > div:nth-of-type(4) > table > tbody"))))

        # Age = info_soup.select("#content > div:nth-of-type(4) > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2)")
        # Age = (str(Age).split('\n')[1][:-6]).strip() #format before spliting and trimming 80</td>]
        #
        # Sex = info_soup.select("#content > div:nth-of-type(4) > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2)")
        # Sex = (str(Sex).split('\n')[1][:-6]).strip()
        #
        # Temp = info_soup.select("#content > div:nth-of-type(4) > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2)")
        # Temp = (str(Temp).split('\n')[1][:-6]).strip()
        #
        # Fever = info_soup.select("#content > div:nth-of-type(4) > table > tbody > tr:nth-of-type(4) > td:nth-of-type(2)")
        # Fever = (str(Fever).split('\n')[1][:-6]).strip()
        #
        # Symptoms = info_soup.select("#content > div:nth-of-type(4) > table > tbody > tr:nth-of-type(5) > td:nth-of-type(2)")
        # Symptoms = (str(Symptoms).split('\n')[1][:-6]).strip()
        #
        # Med = info_soup.select("#content > div:nth-of-type(4) > table > tbody > tr:nth-of-type(6) > td:nth-of-type(2)")
        # Med = (str(Med).split('\n')[1][:-6]).strip()
        #
        # Diag = info_soup.select("#content > div:nth-of-type(4) > table > tbody > tr:nth-of-type(7) > td:nth-of-type(2)")
        # Diag = (str(Diag).split('\n')[1][:-6]).strip()
        #
        # Post = info_soup.select("#content > div:nth-of-type(4) > table > tbody > tr:nth-of-type(8) > td:nth-of-type(2)")
        # Post = (str(Post).split('\n')[1][:-6]).strip()

        # res = [Age, Sex, Temp, Fever, Symptoms, Med, Diag, Post]
        # loop_res.append(res)

        # Close current tab
        driver.close()
        # Switch to current handle
        driver.switch_to.window(driver.window_handles[-1])

    # Go to next page
    try:
        next_page = driver.find_element_by_xpath("//*[@id='surveillanceRecordBeanResult']/div[7]/a[8]")
        driver.implicitly_wait(5)
        ActionChains(driver) \
            .click(next_page) \
            .perform()
    except:
        break


# Close chrome and driver
options.close()
options.quit()

with open("Influ_data.txt", "w") as output:
    output.write(str(loop_res))
