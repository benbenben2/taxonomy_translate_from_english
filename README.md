# Open Food Facts taxonomies translation

# Why to use this script?
You want to do a bulk translation in the taxonomy for a given language using Google Translate.


# How to use this script?
## Prerequisites
- Python
- pip install:
  - pip3 install googletrans
  - pip3 install httpcore

## Setup
Open the **taxonomy_translate_from_english.py** file. Update the variables:
- **limit_counter = 200** -> number of translation to perform in the file
- **tgt_lc = 'hr'** -> desired target language abbreviation (ISO 639)
- **taxonomy = "ingredients"** -> desired taxonomy to translate (ingredients, categories, etc.)

**Remark:** it is advice to keep **limit_counter** small otherwise the changes may not be visible on the Github pull request.

**Remark:** it is advice to review and eventually correct translations before to make a pull request.

Copy the taxonomy file from https://github.com/openfoodfacts/openfoodfacts-server (example: ingredients.txt) in the current folder.

## Run
Finally, run the script.

After the run, copy the **\<taxonomy>_updated.txt** file back to the project and rename it (remove '_updated'), commit changes, push and make a PR to https://github.com/openfoodfacts/openfoodfacts-server.