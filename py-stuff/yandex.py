import sys
import subprocess as sp

import locale
import requests

import pickle
import pyperclip

class Translater(object):

    def __init__(self, key_translate=None, key_dictionary=None, text=None,
                 from_lang=None, to_lang=None,
                 hint=[], ui=None):
        self.valid_lang = ['az', 'sq', 'am', 'en', 'ar', 'hy', 'af', 'eu', 'ba', 'be', 'bn', 'my',
                           'bg', 'bs', 'cy', 'hu', 'vi', 'ht', 'gl', 'nl', 'mrj', 'el', 'ka', 'gu',
                           'da', 'he', 'yi', 'id', 'ga', 'it', 'is', 'es', 'kk', 'kn', 'ca', 'ky',
                           'zh', 'ko', 'xh', 'km', 'lo', 'la', 'lv', 'lt', 'lb', 'mg', 'ms', 'ml',
                           'mt', 'mk', 'mi', 'mr', 'mhr', 'mn', 'de', 'ne', 'no', 'pa', 'pap', 'fa',
                           'pl', 'pt', 'ro', 'ru', 'ceb', 'sr', 'si', 'sk', 'sl', 'sw', 'su', 'tg',
                           'th', 'tl', 'ta', 'tt', 'te', 'tr', 'udm', 'uz', 'uk', 'ur', 'fi', 'fr',
                           'hi', 'hr', 'cs', 'sv', 'gd', 'et', 'eo', 'jv', 'ja']

        self.valid_format = ['plain', 'html']
        self.valid_default_ui = ['ru', 'en', 'tr']

        self.default_ui = locale.getlocale()[0].split('_')[0]

        if not self.default_ui in self.valid_lang:
            self.default_ui = 'en'

        if not ui: self.ui = self.default_ui
        self.hint = hint
        self.base_url_translate = 'https://translate.yandex.net/api/v1.5/tr.json/'
        self.key_translate = key_translate
        self.base_url_dictionary = 'https://dictionary.yandex.net/api/v1/dicservice.json/'
        self.key_dictionary = key_dictionary
        self.text = text
        self.from_lang = from_lang
        self.to_lang = to_lang

    def set_key_translate(self, key_translate):
        if key_translate: self.key_translate = key_translate

    def set_key_dictionary(self, key_dictionary):
        if key_dictionary: self.key_translate = key_dictionary

    def set_text(self, text):
        if text: self.text = text

    def set_default_ui(self, lang):
        if lang and lang in self.valid_lang:
            self.ui = lang
        else:
            self.default_ui = self.default_ui

    def set_ui(self, lang):
        if lang and lang in self.valid_lang:
            self.ui = lang
        else:
            self.ui = self.default_ui

    def set_hint(self, *langs):
        for lang in langs:
            if lang in self.valid_lang:
                self.hint.append(lang)

    def set_from_lang(self, lang):
        if lang and lang in self.valid_lang: self.from_lang = lang

    def set_to_lang(self, lang):
        if lang and lang in self.valid_lang: self.to_lang = lang

    def translate(self):
        if not self.key_translate:
            return "Please set Api key"
        if not self.text:
            return "Please set Text"
        if not self.from_lang:
            return "Please set source lang"
        if not self.to_lang:
            return "Please set destination lang"

        data = {'key': self.key_translate, 'text': self.text,
                'lang': '{}-{}'.format(self.from_lang, self.to_lang)}
        query = 'translate?'
        url = self.base_url_translate + query
        response = requests.get(url, data)
        if response.status_code == 401: return 'Invalid API key'
        if response.status_code == 402: return 'Blocked API key'
        if response.status_code == 403: return 'Exceeded the daily limit on the amount of translated text'
        if response.status_code == 413: return "Exceeded the maximum text size"
        if response.status_code == 422: return "The text cannot be translated"
        if response.status_code == 501: return "The specified translation direction is not supported"
        if not response.status_code == 200: return "Failed to translate text! {}".format(response.reason)
        result = response.json()
        return result

    def lookup(self):
        if not self.key_translate:
            return "Please set Api key"
        if not self.text:
            return "Please set Text"
        if not self.from_lang:
            return "Please set source lang"
        if not self.to_lang:
            return "Please set destination lang"

        data = {'key': self.key_translate, 'text': self.text,
                'lang': '{}-{}'.format(self.from_lang, self.to_lang)}
        query = 'lookup?'
        url = self.base_url_dictionary + query
        response = requests.get(url, data)
        if response.status_code == 401: return 'Invalid API key'
        if response.status_code == 402: return 'Blocked API key'
        if response.status_code == 402: return 'Exceeded the daily limit on the amount of translated text'
        if response.status_code == 413: return "Exceeded the maximum text size"
        if response.status_code == 422: return "The text cannot be translated"
        if response.status_code == 501: return "The specified translation direction is not supported"
        if not response.status_code == 200: return "Failed to translate text! {}".format(response.reason)
        result = response.json()
        return result

    def synonym(self):
        if not self.key_translate:
            return "Please set Api key"
        if not self.text:
            return "Please set Text"
        if not self.from_lang:
            return "Please set source lang"

        data = {'key': self.key_translate, 'text': self.text,
                'lang': '{}-{}'.format(self.from_lang, self.from_lang)}
        query = 'lookup?'
        url = self.base_url_dictionary + query
        response = requests.get(url, data)
        if response.status_code == 401: return 'Invalid API key'
        if response.status_code == 402: return 'Blocked API key'
        if response.status_code == 402: return 'Exceeded the daily limit on the amount of translated text'
        if response.status_code == 413: return "Exceeded the maximum text size"
        if response.status_code == 422: return "The text cannot be translated"
        if response.status_code == 501: return "The specified translation direction is not supported"
        if not response.status_code == 200: return "Failed to translate text! {}".format(response.reason)
        result = response.json()
        return result

    def detect_lang(self):
        if not self.key_translate:
            "Please set Api key"

        if not self.text:
            return "Please set a text"

        data = {'key': self.key_translate, 'text': self.text, 'hint': ','.join(self.hint)}
        query = 'detect?'
        url = self.base_url_translate + query
        response = requests.get(url, data)
        if response.status_code == 401: return "Invalid API key"
        if response.status_code == 402: return "Blocked API key"
        if response.status_code == 404: return "Exceeded the daily limit on the amount of translated text"
        if not response.status_code == 200:
            return "Failed to detect the language! (response code {}".format(response.reason)
        result = response.json()
        return result['lang']

    def get_langs(self):
        if not self.key_translate:
            return "please set Api key"

        data = {'key': self.key_translate, 'ui': self.ui}
        query = 'getLangs?'
        url = self.base_url_translate + query
        response = requests.get(url, data)
        if response.status_code == 401: return "Invalid API key"
        if response.status_code == 402: return "Blocked API key"
        if not response.status_code == 200:
            return "Failed to get list of supported languages! (response code {})".format(response.reason)
        result = response.json()
        return result['dirs']



class RofiOutput():
    def __init__(self):
        self.entries = []

    def __str__(self):
        s = ""
        for entry in self.entries:
            # add translation and tye to string
            s += entry[1]["text"] + ", " + entry[1]["pos"]

            # add synonyms
            try:
                entry[1]["syn"]
                s += " ["
                for syn in entry[1]["syn"]:
                    s += syn["text"] + ", "
                s = s[:-2]
                s += "] "
            except KeyError:
                pass
                #print("No synonums for " + s + " found.")

            # add meanings
            try:
                entry[1]["mean"]
                s += "["
                for mean in entry[1]["mean"]:
                    s += mean["text"] + ", "
                s = s[:-2]
                s += "] "
            except KeyError:
                pass
                #print("No meanings for " + s + " found.")

            s += "\n"

        return s

    def __repr__(self):
        s = ""
        for entry in self.entries:
            s += ', ' + str(entry)

        return s

    def add_entry(self, input, translation):
        self.entries.append((input, translation))


if __name__ == "__main__":

    query_history = ""
    saved_queries = {}
    if sys.argv.__len__() > 1:
        input_term = sys.argv[1]
    else:
        # Run the command then remove the ending newline, and decode the bytestring as a normal utf-8 string
        CMD_run_rofi_get_string = "echo ' ' | rofi -dmenu -p 'Translate'"
        input_term = sp.run(CMD_run_rofi_get_string, shell=True, stdout=sp.PIPE).stdout[:-1].decode('utf-8')
        if input_term == " ":
            # no input found
            exit(0)
    # initialize translater
    yandex = Translater()
    # Api key found on https://translate.yandex.com/developers/keys
    yandex.set_key_translate('trnsl.1.1.20181113T234817Z.8ce6c4f007289dc9.10aa800b2eb0bdbaee6e7cbf5ce16457a9150469')
    # https://tech.yandex.com/keys/?service=dict
    yandex.set_key_dictionary('dict.1.1.20181114T000638Z.c1b6d5571c55f920.50af3dbb542d15a688a2196dc315330755359012')

    # Main Loop
    while input_term:
        yandex.set_from_lang('de')
        yandex.set_to_lang('en')
        yandex.set_text(input_term)

        #result_trans = yandex.translate()
        result_dict = yandex.lookup()
        #result_syno = yandex.synonym()

        # result exists
        if result_dict['def']:
            result_dict = result_dict['def'][0]
            # extract only relevant information
            #pickle.dump(result_dict, open("Ziehen.p", "wb"))
            #result_dict = pickle.load( open( "Ziehen.p", "rb" ) )

            # extract result
            input_text = result_dict['text']
            input_text_type = result_dict['pos']
            input_translations = result_dict['tr']
            output = RofiOutput()
            for tr in input_translations:
                output.add_entry((input_text, input_text_type), tr)

        else:
            output = "No translation found"
        # open rofi with result:
        cmd = "echo \"{}\" | rofi -markup-rows -i -dmenu -p \"{}\"".format(str(output), "results")
        selected = sp.run(cmd, shell=True, stdout=sp.PIPE)

        #format selected:
        selected_text = selected.stdout.decode("utf-8")
        selected_text = selected_text[:-1]
        selected_text = selected_text.split(",")
        selected_text = selected_text[:-1]
        cmd = "echo {} | xsel -b -i".format(selected_text[0])

        sp.run(cmd, shell=True, stdout=sp.PIPE)
        print("fertig")
        input_term = None