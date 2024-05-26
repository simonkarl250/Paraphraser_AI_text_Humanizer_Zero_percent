import tkinter as tk
from tkinter import messagebox
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize
import random
import nltk

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

# Get English stopwords
stop_words = set(stopwords.words('english'))

# Function to get simple synonyms of a word
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace('_', ' ')
            if synonym.isalpha() and len(synonym.split()) == 1 and len(synonym) <= 10:  # Filter out complex synonyms
                synonyms.add(synonym)
    return synonyms

# Function to introduce human-like errors in text
def introduce_human_errors(text):
    words = text.split()
    for i in range(len(words)):
        if i % 10 == 0 and i != 0:
            # Introduce a double space
            words[i] = " " + words[i]
        elif i % 15 == 0 and i != 0:
            # Introduce a random typo by duplicating a letter
            word = words[i]
            if len(word) > 2:
                pos = random.randint(1, len(word) - 2)
                words[i] = word[:pos] + word[pos] * 2 + word[pos + 1:]
    return ' '.join(words)

# Function to paraphrase text
def paraphrase_text():
    input_text = text_area.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Input Error", "Please enter text to paraphrase.")
        return

    paraphrase_button.config(state=tk.DISABLED)
    clear_button.config(state=tk.DISABLED)
    copy_button.config(state=tk.DISABLED)

    words = word_tokenize(input_text)
    pos_tags = nltk.pos_tag(words)
    new_sentence = []

    num_words_to_replace = int(len(words) * 0.6)  # Replace approximately 60% of the words
    words_replaced = 0

    for word, tag in pos_tags:
        if words_replaced >= num_words_to_replace:
            new_sentence.append(word)
        elif tag.startswith('NN') or tag.startswith('VB') or tag.startswith('JJ') or tag.startswith('RB'):
            if word.lower() not in stop_words:
                synonyms = get_synonyms(word)
                if synonyms:
                    synonym = random.choice(list(synonyms))
                    new_sentence.append(synonym)
                    words_replaced += 1
                else:
                    new_sentence.append(word)
            else:
                new_sentence.append(word)
        else:
            new_sentence.append(word)

    paraphrased_text = ' '.join(new_sentence)
    paraphrased_text_with_errors = introduce_human_errors(paraphrased_text)

    output_text_area.config(state=tk.NORMAL)  # Enable editing to update text
    output_text_area.delete("1.0", tk.END)    # Clear existing text
    output_text_area.insert(tk.END, paraphrased_text_with_errors)
    output_text_area.config(state=tk.DISABLED)  # Disable editing again

    paraphrase_button.config(state=tk.NORMAL)
    clear_button.config(state=tk.NORMAL)
    copy_button.config(state=tk.NORMAL)

# Function to copy paraphrased text to clipboard
def copy_to_clipboard():
    root.clipboard_clear()  # Clear the clipboard
    output_text = output_text_area.get("1.0", tk.END).strip()
    root.clipboard_append(output_text)  # Append the text to the clipboard

# Function to clear all text areas
def clear_all():
    text_area.delete("1.0", tk.END)  # Clear the input text area
    output_text_area.config(state=tk.NORMAL)  # Enable editing to clear text
    output_text_area.delete("1.0", tk.END)    # Clear the output text area
    output_text_area.config(state=tk.DISABLED)  # Disable editing again

# Create the main window
root = tk.Tk()
root.title("Paraphrasing Tool")
root.geometry("800x600")  # Set the window size to 800x600 pixels

# Create a frame for the input text area with a scrollbar
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

text_area = tk.Text(input_frame, width=80, height=10, wrap=tk.WORD)
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

input_scrollbar = tk.Scrollbar(input_frame, command=text_area.yview)
input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_area.config(yscrollcommand=input_scrollbar.set)

# Create a button to trigger the paraphrasing
paraphrase_button = tk.Button(root, text="Paraphrase", command=paraphrase_text)
paraphrase_button.pack(pady=5)

# Create a frame for the output text area with a scrollbar
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

# Create a button to clear all text areas
clear_button = tk.Button(root, text="Clear All", command=clear_all)
clear_button.pack(pady=5)

# Run the main loop
root.mainloop()
