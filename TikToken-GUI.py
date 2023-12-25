import PySimpleGUI as sg
import tiktoken

def count_tokens(text, model_name):
    model_to_encoding = {
        "gpt-4": "cl100k_base",
        "gpt-3.5-turbo": "cl100k_base",
        "gpt-35-turbo": "cl100k_base",
        "text-davinci-003": "p50k_base",
        "text-davinci-002": "p50k_base",
        "text-davinci-001": "r50k_base",
        "text-curie-001": "r50k_base",
        "text-babbage-001": "r50k_base",
        "text-ada-001": "r50k_base",
        "davinci": "r50k_base",
        "curie": "r50k_base",
        "babbage": "r50k_base",
        "ada": "r50k_base"
    }
    encoding = model_to_encoding[model_name]
    enc = tiktoken.get_encoding(encoding)
    tokens = enc.encode(text)
    token_count = len(tokens)
    return token_count

def count_chars_words(text):
    chars = len(text)
    words = len(text.split())
    return chars, words

def calculate_difference(limit, count):
    difference = count - limit
    if difference < 0:
        return f'{abs(difference)} remaining'
    else:
        return f'Exceeds by {difference}'

def create_window():
    sg.theme('BlueMono')

    layout = [
        [sg.Multiline(size=(40, 15), key='-TEXT-', enable_events=True, expand_x=True, expand_y=True)],
        [sg.Text('Model:'), sg.Combo(["gpt-4", "gpt-3.5-turbo", "gpt-35-turbo", "text-davinci-003", "text-davinci-002",
                                      "text-davinci-001", "text-curie-001", "text-babbage-001", "text-ada-001",
                                      "davinci", "curie", "babbage", "ada"], default_value="gpt-4", key='-MODEL-', readonly=True, expand_x=True),
         sg.Text('', size=(40, 3), key='-REPORT-', expand_x=True, expand_y=True)]
    ]

    return sg.Window('TikToken', layout, resizable=True, finalize=True)

window = create_window()

while True:
    event, values = window.read(timeout=100)

    if event == sg.WIN_CLOSED:
        break

    if event == '-TEXT-' or event == '-MODEL-':
        text = values['-TEXT-']
        model_name = values['-MODEL-']
        token_count = count_tokens(text, model_name)
        chars, words = count_chars_words(text)
        token_difference = calculate_difference(4096, token_count)
        char_difference = calculate_difference(160, chars)
        report = (f'Token count: {token_count}\n'
                  f'ChatGPT Plus: {token_difference}\n'
                  f'Character count: {chars}\n'
                  f'Twitter post: {char_difference}\n'
                  f'Word count: {words}')
        window['-REPORT-'].update(report)

window.close()
