import csv
import requests
from bs4 import BeautifulSoup
from docx import Document

# Function to load banned phrases from a CSV file
def load_banned_phrases(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        banned_phrases = [row[0].strip() for row in reader if row]  # Read the first column
    return banned_phrases

# Function to read text from a Word document
def read_text_from_docx(filename):
    doc = Document(filename)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Function to get text from a webpage
def get_text_from_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # will raise an exception for HTTP error
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join(soup.stripped_strings)  # Extract text and remove extra whitespace
        return text
    except requests.RequestException as e:
        print(f"Error fetching webpage: {e}")
        return ""

# Function to check text for banned phrases
def check_for_banned_speech(text, banned_phrases):
    for phrase in banned_phrases:
        if phrase.lower() in text.lower():  # Case insensitive check
            return True
    return False

# Function to simulate an alert for banned speech
def alert_banned_speech():
    print("Alert: Banned speech detected!")

# Main function to tie everything together
def main():
    banned_phrases = load_banned_phrases("banned_speech.csv")
    
    # Example: Checking a Word document
    word_document_path = "path_to_your_document.docx"  # Replace with your Word document path
    document_text = read_text_from_docx(word_document_path)
    if check_for_banned_speech(document_text, banned_phrases):
        alert_banned_speech()

    # Example: Checking a webpage
    webpage_url = "https://expo.se/fordjupning/nazi-careerist-or-russian-agent/"  # Replace with the webpage URL you want to check
    webpage_text = get_text_from_webpage(webpage_url)
    if check_for_banned_speech(webpage_text, banned_phrases):
        alert_banned_speech()
    else:
        print("No banned speech detected in the webpage.")

if __name__ == "__main__":
    main()
