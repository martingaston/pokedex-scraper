# Scraping the pokedex using Python and Selenium :snake:

Like everyone on planet Earth I'm kind of interested in all that cool data stuff you can do with Python, so I've really wanted to learn some web scraping lately - and for most of my education projects that usually means making something to do with Pokemon :joy:

This is a relatively simple script that uses **Python**, **Selenium** and a **Headless Firefox Browser** to scrape the OG Pokemon (the first 150, obv) from the [pokemon.com/pokedex](pokemon.com/pokedex) page and then output:

- The collated stats into a CSV file (I'm more familiar with JSON in general so fancied playing with another file format)
- Their image as a PNG into an /image directory

The script is looking to be gracious rather than performant, so there's a couple of seconds of delay between requests.

I used data collected here to [create a scatterplot graph of each Pokemon's height v weight](https://t.co/0H7SwAjocW), which was **super fun**. Down the line I'd like to integrate this into D3 and make an interactive visualisation :heart_eyes:

:warning: In the real world I would obviously recommend the [PokeAPI](https://pokeapi.co/) for your Pokedex needs :warning:
