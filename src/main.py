
#before running this program ensure the following libraries have being installed


#in your pc run the following in your terminal
#pip install nltk requests




import tkinter as tk
from tkinter import messagebox
import nltk
from nltk.corpus import wordnet
import random


# Ensure necessary NLTK resources are downloaded by uncommenting this lines
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

# Function to get synonyms of a word
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms


# Function to introduce humanize the paragraph
def humanizer(word):
    errors = [
        lambda x: x + ' ',
        lambda x: ' ' + x,
        lambda x: x + ',',
        lambda x: x + '  ',
        lambda x: x[:len(x) // 2] + ' ' + x[len(x) // 2:]
    ]
    if random.random() < 0.1:
        error_function = random.choice(errors)
        return error_function(word)
    return word


# Function to paraphrase a sentence word by word
def paraphrase_word_by_word():
    global words, pos_tags, word_index
    if word_index < len(words):
        word, tag = pos_tags[word_index]
        if tag.startswith('NN') or tag.startswith('VB') or tag.startswith('JJ') or tag.startswith('RB'):
            synonyms = get_synonyms(word)
            if synonyms:
                synonym = random.choice(list(synonyms))
                new_word = synonym
            else:
                new_word = word
        else:
            new_word = word

        new_word = humanizer(new_word)
        new_sentence.append(new_word)

        output_text_area.config(state=tk.NORMAL)
        output_text_area.insert(tk.END, new_word + " ")
        output_text_area.config(state=tk.DISABLED)

        word_index += 1
        root.after(100, paraphrase_word_by_word)  # Call this function again after 100ms
    else:
        # When all words are processed, enable buttons and clear the list
        paraphrase_button.config(state=tk.NORMAL)
        clear_button.config(state=tk.NORMAL)
        copy_button.config(state=tk.NORMAL)
        new_sentence.clear()


# handle the paraphrasing
def paraphrase_text():
    global words, pos_tags, word_index, new_sentence
    input_text = text_area.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Input Error", "Please enter text to paraphrase.")
        return

    paraphrase_button.config(state=tk.DISABLED)
    clear_button.config(state=tk.DISABLED)
    copy_button.config(state=tk.DISABLED)

    words = nltk.word_tokenize(input_text)
    pos_tags = nltk.pos_tag(words)
    word_index = 0
    new_sentence = []

    output_text_area.config(state=tk.NORMAL)  # Enable editing to update text
    output_text_area.delete("1.0", tk.END)  # Clear existing text
    output_text_area.config(state=tk.DISABLED)  # Disable editing again

    paraphrase_word_by_word()


# Function
def copy_to_clipboard():
    root.clipboard_clear()  # Clear the clipboard
    output_text = output_text_area.get("1.0", tk.END).strip()
    root.clipboard_append(output_text)  # Append the text to the clipboard


# Functi
def clear_all():
    text_area.delete("1.0", tk.END)  # Clear the input text area
    output_text_area.config(state=tk.NORMAL)  # Enable editing to clear text
    output_text_area.delete("1.0", tk.END)  # Clear the output text area
    output_text_area.config(state=tk.DISABLED)  # Disable editing again


#
root = tk.Tk()
root.title("Paraphrasing Tool")
root.geometry("800x600")  # Set the window size to 800x600 pixels

#
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

text_area = tk.Text(input_frame, width=80, height=10, wrap=tk.WORD)
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

input_scrollbar = tk.Scrollbar(input_frame, command=text_area.yview)
input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_area.config(yscrollcommand=input_scrollbar.set)

# trigger the paraphrasing
paraphrase_button = tk.Button(root, text="Paraphrase", command=paraphrase_text)
paraphrase_button.pack(pady=5)

#  scrollbar
output_frame = tk.Frame(root)
output_frame.pack(pady=10)

output_text_area = tk.Text(output_frame, width=80, height=10, wrap=tk.WORD, state=tk.DISABLED)
output_text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

output_scrollbar = tk.Scrollbar(output_frame, command=output_text_area.yview)
output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text_area.config(yscrollcommand=output_scrollbar.set)

# Create a button to copy the output text to the clipboard
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(pady=5)

#  clear all text areas
clear_button = tk.Button(root, text="Clear All", command=clear_all)
clear_button.pack(pady=5)

# Initialize
words = []
pos_tags = []
word_index = 0
new_sentence = []

#main loop
root.mainloop()
