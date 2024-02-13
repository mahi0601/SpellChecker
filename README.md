# SpellChecker
The Spell Checker Project is a robust text processing tool designed to identify and correct spelling errors in textual content. Leveraging advanced algorithms and linguistic analysis, this project aims to enhance the accuracy and readability of written material by providing automated spell-checking capabilities.

# Spell Checker Project

## Overview

The Spell Checker Project is a Python-based application that provides robust spell-checking capabilities to enhance the accuracy and readability of written content. Leveraging advanced algorithms and linguistic analysis, this project aims to be a versatile and efficient tool for identifying and correcting spelling errors in text.

## Features

- Trie-Based Spell Checking: The project utilizes a Trie data structure for efficient and fast spell-checking. The Trie allows for quick searches within a given edit distance, providing accurate suggestions for misspelled words.

- Symmetric Delete Distance Algorithm: The spell checker employs a symmetric delete distance algorithm to determine the similarity between two words. This algorithm helps identify the best spelling suggestions for a given misspelled word.

- User-Friendly Interface: The application comes with a user-friendly graphical interface built using Tkinter. Users can input text and check spelling with just a few clicks.

- Custom Dictionary Support: Users have the option to add words to a custom dictionary, allowing for a personalized spell-checking experience. The custom dictionary is considered during spell-checking, enhancing the flexibility of the tool.

- Performance Metrics: The project includes functionality to measure the response time of the spell-checking process, both in synchronous and asynchronous modes. This can be valuable for users seeking to optimize the performance of the spell checker.

## Algorithm

### Trie-Based Spell Checking

The Trie data structure is employed for efficient storage and retrieval of words. The `TrieNode` class represents each node in the Trie, and the `Trie` class provides methods for inserting words and searching within a specified edit distance.

### Symmetric Delete Distance Algorithm

The symmetric delete distance algorithm is utilized to calculate the similarity between two words. It helps identify the closest matching word within a given edit distance, enabling accurate spelling suggestions.

## How to Use

1. **Installation:**
   - Clone the repository to your local machine.
   - Ensure you have Python installed (preferably Python 3.x).

2. **Dependencies:**
   - Install the required dependencies using the provided `requirements.txt` file.

3. **Run the Application:**
   - Execute the `spell_checker_app.py` script.
   - The graphical interface will appear, allowing you to input text for spell checking.

4. **Check Spelling:**
   - Enter the text in the provided text entry area.
   - Click the "Check Spelling" button to initiate the spell-checking process.

5. **Performance Metrics:**
   - The application provides response time metrics for both synchronous and asynchronous spell-checking modes.

   ![Response Time Screenshot](screenshots/response_time_screenshot.png)

   *Response Time per 1000 words (Sync): [0.1] seconds*

   *Response Time per 1000 words (Async): [0.3] seconds*

6. **Add to Custom Dictionary:**
   - Click the "Add to Custom Dictionary" button to add words to the custom dictionary.

## Contributing

Contributions to the project are welcome! Whether you want to improve the algorithms, enhance the user interface, or add new features, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE.md).

## Acknowledgments

Special thanks to the open-source community and contributors for their valuable contributions and support in making the Spell Checker Project a reliable and efficient tool for textual refinement.
```

Replace `[Your Response Time Value]` with the actual response time values you want to display. Additionally, replace `screenshots/response_time_screenshot.png` with the correct path to your response time screenshot.
