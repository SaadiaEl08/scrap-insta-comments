# Scrap-Insta-Comments

Scrap-Insta-Comments is a Python-based project that uses Selenium to scrape comments from Instagram posts. This tool automates the authentication process and extracts comments along with their authors from a specified Instagram profile. The scraped data is saved in a JSON file, which can be updated and used as needed.

## Features

- Automated Instagram login using Selenium.
- Scrapes comments from a specified Instagram profile.
- Saves comments and their authors to a JSON file.
- Provides an option to update and use the scraped data as an API.

## Prerequisites

- Python 3.x
- Google Chrome
- ChromeDriver

## Installation

1. **Clone the Repository**

   ```bash
   git clone hhttps://github.com/SaadiaEl08/scrap-insta-comments.git
   cd scrap-insta-comments
   ```

2. **Create a Virtual Environment (Optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory of the project with the following content:

   ```plaintext
   instagram_username=your_username
   instagram_password=your_password
   ```

   You can use the provided `env.example` file as a template:

   ```plaintext
   instagram_username=your_username
   instagram_password=your_password
   ```

## Usage

1. **Run the Scraper**

   Execute the `scrap.py` script:

   ```bash
   python scrap.py
   ```

2. **Enter Instagram Username**

   When prompted, enter the Instagram username of the profile you want to scrape comments from.

   ```
   Enter Instagram username to get its comments: <username>
   ```

3. **Output**

   The scraped comments will be saved in `instagram_comments.json`. Each entry in the file will have the following structure:

   ```json
   [
     {
       "comment_tex": "Comment text",
       "comment_writer": "Username"
     },
     ...
   ]
   ```

## Example

Here is an example of the JSON output:

```json
[
  {
    "comment_tex": "👍🏼🔥",
    "comment_writer": "ilham.aafif"
  },
  {
    "comment_tex": "❤️🔥",
    "comment_writer": "ahlam.ghofran"
  },
  ...
]
```

## Troubleshooting

- Ensure that you have provided correct Instagram credentials in the `.env` file.
- Make sure that ChromeDriver is compatible with your installed version of Google Chrome.
- If you encounter issues with the script, check the log messages for debugging information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please reach out to [saadiaelachguir@gmail.com](mailto:saadiaelachguir@gmail.com).