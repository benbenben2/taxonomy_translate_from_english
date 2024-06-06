import googletrans
from googletrans import Translator
import sys
from httpcore._exceptions import ReadTimeout


def translate_to_language(text: str) -> str:
    # restart upon failure, in case of latency or network issue
    i = 0
    while i < 2:
        try:
            translation = translator.translate(text, src='en', dest=tgt_lc)
        except ReadTimeout:
            i += 1
        else:
            print(f"translate_to_language, translated '{text}' into '{translation.text}'")
            return translation.text
    print("Error with translation call")
    sys.exit(1)


def translate_line(lines: list) -> str:
    translated_line = ""
    for line in lines:
        if line.startswith('en:'):
            text = line[3:].split(',')[0].strip()

            translation = translate_to_language(text.lower())

            # convention categories start by upper character, ingredients lower character.
            if taxonomy == "categories":
                translation = translation[0].upper() + translation[1:]

            translated_line = f'{tgt_lc}:{translation}'

    return translated_line


def append_translation_in_block(new_line: str, lines: list) -> None:
    appended = False
    # assume it is by alphabetical order
    # and English is always first
    for i, line in enumerate(lines):
        # cannot be before "en:"
        if f"{tgt_lc}:" < line and "en:" not in line:
            # lines.insert(i, f'{tgt_lc}:{translation}')
            lines.insert(i, new_line)
            appended = True
            break

    # language is last in alphabetical order 
    # append at the end of the lines with languages
    if not appended:
        index_of_last_lang = 0
        for i in range(len(lines)):
            if len(lines[i]) > 2 and lines[i][2] == ":":
                    index_of_last_lang = i

        # lines.insert(index_of_last_lang+1, f'{tgt_lc}:{translation}')
        lines.insert(index_of_last_lang+1, new_line)


def process_block(block: str) -> str:
    lines = block.split('\n')
    
    # skip if translation already exists, 
    translation_exists = any(f'{tgt_lc}:' in element or element.startswith('xx:') for element in lines)

    # skip if only english and another language 
    # example: french cheese from a given region only in English and French
    languages_nb = [i for i in lines if len(i) > 3]
    # ignore if entry is commented out or is a property
    languages_nb = [i for i in languages_nb if i[2] == ':']
    # skip if English is not in the list of languages
    english_and_another_language_only = (len(languages_nb) <= 2 and any(element.startswith('en:') for element in languages_nb))

    if translation_exists or english_and_another_language_only:
        return '\n'.join(lines)

    translated_line = translate_line(lines)

    if translated_line:
        append_translation_in_block(translated_line, lines)

        global counter
        counter += 1

    return '\n'.join(lines)


def taxonomy_translate_from_english() -> None:
    with open(f"{taxonomy}.txt", 'r') as f:
        text = f.read()

    # Split the text into blocks
    blocks = text.split('\n\n')

    updated_file = ""
    
    global counter
    counter = 0


    for i, block in enumerate(blocks):
        if counter < limit_counter:
            # not always translated
            # counter is incremented when translation is done
            updated_file += process_block(block)
        # end of file unchanged
        else:
            updated_file += block

        # join back the blocks with \n\n, except for last block
        if i < len(blocks) - 1:
            updated_file += '\n\n'

    with open(f"{taxonomy}_updated.txt", 'w') as f:
        f.write(updated_file)


if __name__ == "__main__":
    # keep small number
    # need to be reviewed by you
    # need to be reviewed by peer
    # too much changes will not be showed on Github PR
    limit_counter = 200

    # set the desired language abbreviation ISO 639
    tgt_lc = 'hr'

    # categories, ingredients, etc.
    taxonomy = "ingredients"

    # Initialize the translator
    translator = Translator()

    taxonomy_translate_from_english()