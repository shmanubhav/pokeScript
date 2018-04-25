from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sys, collections, time

usr = 'cowmcgee'
pas = 'cowmcgee'
browser = webdriver.Chrome()

def login(usr,pas):

    browser.get('https://www.pokemon-vortex.com/login/')
    username = browser.find_element_by_id('myusername')
    username.send_keys(usr)
    password = browser.find_element_by_id('mypassword')
    password.send_keys(pas)
    password.submit()

def goToMaps():
    maps = browser.find_element_by_link_text('MAPS')
    maps.click()
    mapChosen = browser.find_element_by_link_text('View Larger Map Select')
    mapChosen.click()

def openRandomMap():
    random = browser.find_element_by_link_text('Random Map')
    random.click()

def isPokemonPresent():
    try:
        appear = browser.find_element_by_xpath("//input[@value='Battle!']")
        return True
    except NoSuchElementException:
        # print('Nothing found')
        return False

def battle():
    appear = browser.find_element_by_xpath("//input[@value='Battle!']")
    appear.click()

def getName(pokemon):
    return pokemon.splitlines()[0]

def getLevel(pokemon):
    return pokemon.splitlines()[2].split(' ')[1]

def faintOnPage():
    try:
        faint = browser.find_element_by_css_selector('div.attackOutput')
        return True
    except NoSuchElementException:
        return False

def getPokeDictionary():
    levels = {}
    lvl = browser.find_element_by_xpath("//td[@class='battle-poke-selected slot']")
    levels.update({getLevel(lvl.text):getName(lvl.text)})
    lvls = browser.find_elements_by_xpath("//td[@class='battle-poke-select slot']")
    for unselected in lvls:
        levels.update({getLevel(unselected.text):getName(unselected.text)})
    return levels

def getOpponent():
    level = {}
    lvl = browser.find_element_by_xpath("//td[@class='battle-poke-select']")
    level.update({getLevel(lvl.text):getName(lvl.text)})
    return level

def getPokemonObj(name):
    obj = browser.find_element_by_xpath("//td[@class='battle-poke-selected slot']")
    if getName(obj.text) == name:
        return obj
    else:
        objs = browser.find_elements_by_xpath("//td[@class='battle-poke-select slot']")
        for obj in objs:
            if getName(obj.text) == name:
                return obj
    print('No pokemon found')



def battleWith(name):
    pokemon = getPokemonObj(name)
    pokemon.click()
    cont = browser.find_element_by_xpath("//input[@value='Continue']")
    cont.click()

def attack():
    attack = browser.find_element_by_xpath("//input[@class='button-maroon button-small'][@value='Attack!']")
    attack.click()

def continueForm():
    cont = browser.find_element_by_xpath("//input[@class='button-maroon button-small'][@value='Continue']")
    cont.click()

def choosePokemon():
    levels = collections.OrderedDict(sorted(getPokeDictionary().items()))
    # print(levels)
    level = getOpponent()
    # print(level)
    for lvl,pok in levels.items():
        battleWith(pok)
        while faintOnPage() == False:
            time.sleep(5)
            attack()
            continueForm()
        continueForm()

def main():
    login(usr,pas)

    while True:
        goToMaps()
        openRandomMap()
        if isPokemonPresent():
            print('Found!')
            battle()
            choosePokemon()

main()
