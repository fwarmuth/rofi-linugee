import sys
from bs4 import BeautifulSoup as soup
import requests
import subprocess as sp
import re
import pickle


class Example:
    def __init__(self, s, t):
        # string in source language
        self.source = s
        # string in target language
        self.target = t

    def pretty_str(self):
        return self.source + " ~ " + self.target


class TranslationEntry:
    """ Represents an entry on linguee.com"""

    def __init__(self, input_word, original_word, original_word_type, translated_word, examples):
        self.input_word = input_word
        self.original_word = original_word
        # Verb noun etc...
        self.original_word_type = original_word_type

        self.translated_word = translated_word
        self.examples = examples

    def __repr__(self):
        return str(self.input_word) + " -> " + str(self.original_word) + " -> " + str(self.translated_word)

    def __str__(self):
        return str(self.original_word) + ", " + str(self.original_word_type) + " -> " + str(self.translated_word)

    def pretty_str(self):
        example_str = ""
        for example in self.examples:
            example_str += example.pretty_str() + ", "
        return "<b>" + str(self.translated_word) + "</b>, <i>" + str(self.original_word_type) +  "</i> -> " + example_str


def extract_translation_sortablemg_featured(input_html):
    # name of translation, real translation
    translation_desc = input_html.h3.a.contents[0]
    # examples
    examples = []
    if input_html.find("div", {'class': "example_lines"}):
        example_lines = input_html.find("div", {'class': "example_lines"}).contents
        for example_line in example_lines:
            # get source
            tag_s = example_line.find("span", {"class": "tag_s"}).contents[0]
            # get target
            tag_t = example_line.find("span", {"class": "tag_t"}).contents[0]
            examples.append(Example(tag_s, tag_t))

    return translation_desc, examples


def extract_lemma_featured(input_html, input_word):
    """
    extracts lemma featured from input html and puts it in translations_entries
    :param input_html:
    :param input_word:
    :return:
    """
    original_word = input_html.h2.span.a.contents[0]

    # create tag_lemma_context string
    if input_html.find_all('span', {'class': 'tag_lemma_context'}):
        tag_lemma_context = ""
        for element in input_html.find_all('span', {'class': 'tag_lemma_context'})[0].contents:
            # if element is a tag and has content
            try:
                tag_lemma_context += str(element.contents[0])
            except:
                tag_lemma_context += str(element)

    # find and save word type, noun, verb, adjective..
    original_word_type = ""
    for element in input_html.find_all('span', {'class': 'tag_wordtype'}):
        original_word_type = element.contents[0]

    # extract translation_lines
    translation_lines = input_html.find_all('div', {'class': 'translation sortablemg featured'})
    translation_sortablemg_featured_list = []
    for translation_sortablemg_featured in translation_lines:
        translation_sortablemg_featured_list.append(
            extract_translation_sortablemg_featured(translation_sortablemg_featured))

    # holds translated words from one original_word
    translations = []
    for t in translation_sortablemg_featured_list:
        # create translations_entry for ech translation, t[0] translation_desc, t[1] - examples
        translations.append(TranslationEntry(input_word, original_word, original_word_type, t[0], t[1]))

    return translations


def translate(input_word):
    """ Retruns a dict of all original words and their translation of the input word.
    :param word:
    :return:
    """
    # get paramters
    get_parameter = {"source": "auto", "query": input_word}

    # create request, without ssl verification
    r = requests.get('https://www.linguee.com/english-german/search', verify=False, params=get_parameter)
    # pickle.dump(r.content, open("r.content.p", "wb"))
    #r_content = pickle.load(open("r.content.p", "rb"))
    r_content = r.content
    # put html in a soup object
    suppe = soup(r_content, "html.parser")
    # find result container all container
    result_featured = suppe.findAll("div", {"class": "lemma featured"})
    result_ = suppe.findAll("div", {"class": "lemma"})
    # fector of translations
    translations = {}
    for lemma in result_featured:
        entry_list = extract_lemma_featured(lemma, input_term)
        for entry in entry_list:
            translations[entry.translated_word] = entry
    return translations


if __name__ == "__main__" :

    query_history = ""
    saved_queries = {}
    if sys.argv.__len__() == 2:
        input_term = sys.argv[1]
    else:
        # Run the command then remove the ending newline, and decode the bytestring as a normal utf-8 string
        CMD_run_rofi = "echo ' ' | rofi -dmenu -p 'Translate'"
        input_term = sp.run(CMD_run_rofi, shell=True, stdout=sp.PIPE).stdout[:-1].decode('utf-8')
        if input_term == " ":
            # no input found
            exit(0)
    while input_term != "":
        # update query history
        query_history += input_term + "->"
        # check if input_term was already searched
        if saved_queries.__contains__(input_term):
            trans_struct = saved_queries[input_term]
        else:
            # translate new input_term
            trans_struct = translate(input_term)
            saved_queries[input_term] = trans_struct

        # create rofi output...
        #######################
        output_str = ""
        for translation in trans_struct:
            output_str += trans_struct[translation].pretty_str() + "\n"
        # remove last newline
        output_str = output_str[:-1]

        # open rofi with outputs:
        print_translation_cmd = "echo \"{}\" | rofi -markup-rows -i -dmenu -p \"{}\"".format(output_str, query_history)
        selected = sp.run(print_translation_cmd, shell=True, stdout=sp.PIPE)

        # shorten selected item:
        selected = selected.stdout.decode("utf-8")
        selected = re.split(r'</b>', selected)
        selected = selected[0]
        # remove formatting chars
        selected = selected[3:]
        # use selcted as new input_term
        input_term = selected
