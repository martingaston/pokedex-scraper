from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from time import time, sleep
import re
import requests
import os
import csv


def generate_driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    return driver


def site_connect(driver, scrape_number):
    attempts = 0
    while attempts < 3:
        try:
            driver.get("https://www.pokemon.com/uk/pokedex/" +
                       '{:03}'.format(scrape_number))
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'img.active'))
            )
            return True
        except Exception:
            print("Failure connecting to https://www.pokemon.com/uk/pokedex/" +
                  '{:03}'.format(scrape_number))
            attempts += 1


def pokedex_write_csv(output_file, filename, fieldnames):
    for row in output_file:
        with open(filename, "a") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(row)


def pokedex_parse(driver, scrape_number):
    site_connect(driver, scrape_number)
    sleep(2)
    # scrape variables
    pokemon_title = driver.find_element_by_css_selector(
        '.pokedex-pokemon-pagination-title > div:nth-child(1)').text
    pokemon_name = re.search("^[A-Z][a-z]+", pokemon_title).group(0)
    pokemon_number = re.search("[0-9]+$", pokemon_title).group(0)
    pokemon_description_y = driver.find_element_by_css_selector(
        'p.version-y').text
    #pokemon_description_x = driver.find_element_by_css_selector('p.version-x').text
    pokemon_height = driver.find_element_by_css_selector(
        'div.column-7:nth-child(1) > ul:nth-child(1) > li:nth-child(1) > span:nth-child(2)').text
    pokemon_height_m = re.search("^[0-9.]+", pokemon_height).group(0)
    pokemon_weight = driver.find_element_by_css_selector(
        'div.column-7:nth-child(1) > ul:nth-child(1) > li:nth-child(2) > span:nth-child(2)').text
    pokemon_weight_kg = re.search("^[0-9.]+", pokemon_weight).group(0)
    pokemon_category = driver.find_element_by_css_selector(
        'div.column-7:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > span:nth-child(2)').text
    pokemon_stats_hp = driver.find_element_by_xpath(
        '/html/body/div[4]/section[3]/div[1]/div[3]/ul/li[1]/ul/li[1]').get_attribute("data-value")
    pokemon_stats_attack = driver.find_element_by_xpath(
        '/html/body/div[4]/section[3]/div[1]/div[3]/ul/li[2]/ul/li[1]').get_attribute("data-value")
    pokemon_stats_defense = driver.find_element_by_xpath(
        '/html/body/div[4]/section[3]/div[1]/div[3]/ul/li[3]/ul/li[1]').get_attribute("data-value")
    pokemon_stats_spattack = driver.find_element_by_xpath(
        '/html/body/div[4]/section[3]/div[1]/div[3]/ul/li[4]/ul/li[1]').get_attribute("data-value")
    pokemon_stats_spdefense = driver.find_element_by_xpath(
        '/html/body/div[4]/section[3]/div[1]/div[3]/ul/li[5]/ul/li[1]').get_attribute("data-value")
    pokemon_stats_speed = driver.find_element_by_xpath(
        '/html/body/div[4]/section[3]/div[1]/div[3]/ul/li[6]/ul/li[1]').get_attribute("data-value")
    # can this be done with a list comprehension?
    pokemon_ability = []
    for ability in driver.find_elements_by_class_name('moreInfo'):
        # Script returning '' on some abilities - see Gyrados (#130), this is a dirty hack
        if ability.text is not '':
            pokemon_ability.append(ability.text)
    pokemon_type = driver.find_element_by_css_selector(
        '.dtm-type > ul:nth-child(2)').text.split("\n")
    pokemon_weaknesses = driver.find_element_by_css_selector(
        '.dtm-weaknesses > ul:nth-child(2)').text.split("\n")
    # grab the image, don't save if it already exists
    pokemon_image_url = driver.find_element_by_css_selector(
        'img.active').get_attribute('src')
    pokemon_path = "images/" + pokemon_number + "_" + pokemon_name + ".png"
    if (os.path.isfile(pokemon_path) == False):
        with open(pokemon_path, "wb") as f:
            r = requests.get(pokemon_image_url)
            f.write(r.content)
    # add to dictionary
    pokedex_entry = {
        "number": pokemon_number,
        "name": pokemon_name,
        "description_y": pokemon_description_y,
        "type": pokemon_type,
        "weakness": pokemon_weaknesses,
        "ability": pokemon_ability,
        "category": pokemon_category,
        "height": pokemon_height_m,
        "weight": pokemon_weight_kg,
        "stats_hp": pokemon_stats_hp,
        "stats_attack": pokemon_stats_attack,
        "stats_defense": pokemon_stats_defense,
        "stats_spattack": pokemon_stats_spattack,
        "stats_spdefense": pokemon_stats_spdefense,
        "stats_speed": pokemon_stats_speed
    }
    return pokedex_entry


def pokedex_scraper(start=1, finish=150):
    # setup variables
    pokedex = []
    current_pokedex = start
    start_time = time()
    print("Scraping Pokedex #" +
          '{:03}'.format(start) + " to #" + '{:03}'.format(finish))
    driver = generate_driver()
    driver.get("https://www.pokemon.com/uk/pokedex/")
    sleep(2)
    # start scraping
    while current_pokedex <= finish:
        print("Scraping Pokedex #" +
              '{:03}'.format(current_pokedex) + "/#" + str(finish) + "...")
        pokedex.append(pokedex_parse(driver, current_pokedex))
        current_pokedex += 1
    # write the CSV
    pokedex_fields = [
        "number", "name", "description_y",
        "type", "weakness", "ability", "category", "height",
        "weight", "stats_hp", "stats_attack", "stats_defense",
        "stats_spattack", "stats_spdefense", "stats_speed"
    ]
    pokedex_write_csv(pokedex, "pokedex.csv", pokedex_fields)
    # pack up
    driver.quit()
    end_time = time()
    elapsed_time = end_time - start_time
    print("Total run time: " + str(elapsed_time) + " seconds")


if __name__ == '__main__':
    pokedex_scraper()
