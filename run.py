import sys
import subprocess as sp
import re
import pyperclip

from src import deepl, linguee


if __name__ == "__main__":
    print("Translating")
    # if no input term was given use rofi to get one, else use the given one.
    if sys.argv.__len__() == 1:
        # Run the command then remove the ending newline, and decode the bytestring as a normal utf-8 string
        CMD_run_rofi = "echo ' ' | rofi -dmenu -p 'Translate'"
        input_term = sp.run(CMD_run_rofi, shell=True, stdout=sp.PIPE).stdout[:-1].decode('utf-8')
        if input_term == " ":
            # no input found
            exit(0)
    else:
        input_term = sys.argv[1]

    # if input is more than one word use deepl.com else use linguee
    if input_term.split(' ').__len__() > 1:
        ####################### DEEPL
        translator = deepl.DeepL()
        result = translator.translate(input_term)

        # create rofi output...
        #######################
        print_translation_cmd = "echo \"{}\" | rofi -markup-rows -i -dmenu -p \"{}\"".format(result, input_term)
        selected = sp.run(print_translation_cmd, shell=True, stdout=sp.PIPE)

        # shorten selected item:
        selected = selected.stdout.decode("utf-8")
        selected = re.split(r'</b>', selected)
        selected = selected[0]
        # use selcted as new input_term
        pyperclip.copy(str(selected))

    else:
        ####################### LINGUEEE
        translator = linguee.Linguee()

        query_history = ""
        saved_queries = {}
        while input_term != "":
            # update query history
            query_history += input_term + "->"
            # check if input_term was already searched
            if saved_queries.__contains__(input_term):
                trans_struct = saved_queries[input_term]
            else:
                trans_struct = translator.translate(input_term)
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
