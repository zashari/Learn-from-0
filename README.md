<!-- ABOUT THE PROJECT -->
## About The Project

Learn From 0 is an AI-powered Telegram bot designed to provide educational assistance across a range of topics. It leverages the power of Google's Gemini language model to offer comprehensive and engaging answers to user queries, integrating advanced capabilities like recent knowledge access, and calculations. 

Here's why this project stands out:
* **Multi-topic Expertise**: Learn From 0 specializes in four key areas: Business, Law, Coding, and Math, offering users a versatile learning experience.
* **Gemini Integration**:  Utilizes the powerful Gemini model for natural language processing, ensuring informative and contextual responses.
* **Personalized Learning**: Remembers previous interactions to tailor responses and maintain conversation context for individual users. 
* **Safety Focused**: Incorporates safety settings within Gemini to filter harmful content and ensure a positive user experience.
* **Easy to Use**:  Simply interact with the bot via Telegram to access its learning capabilities. 

[!DemoVideo](https://raw.githubusercontent.com/zashari/Learn-from-0/blob/main/assets/Demo_video.mp4)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [Python](https://www.python.org/)
* [Telegram Bot API](https://core.telegram.org/bots/api)
* [Google Gemini API](https://developers.generativeai.google/)
* [MongoDB](https://www.mongodb.com/)
* [Python-dotenv](https://pypi.org/project/python-dotenv/)
* [RestrictedPython](https://pypi.org/project/RestrictedPython/)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Before you can run this bot locally, you'll need:

* **Python 3.7 or higher**: Ensure Python is installed on your system. 
* **A Telegram Bot**:  Create a Telegram bot and obtain its API token (Refer to Telegram's Bot API documentation for guidance).
* **Google Gemini API Key**:  Obtain an API key for Google's Gemini (refer to Google Gemini's documentation for details).
* **MongoDB Atlas Account**: Create a free account on MongoDB Atlas and get your connection string (MongoDB URI).

### Installation

1. **Clone the Repository**: 
   ```sh
   git clone https://github.com/yourusername/LearnFrom0.git 
   ```
2. **Navigate to the Project Directory**:
   ```sh
   cd LearnFrom0
   ```
3. **Install Dependencies**: Use pip to install the required Python packages. 
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables**:
   * Create a file named `.env` in the project's root directory.
   * Populate it with the following environment variables, replacing the placeholders with your actual values:
     ```
     BOT_URI={YOUR_TELEGRAM_BOT_TOKEN}
     GEMINI_API={YOUR_GEMINI_API_KEY}
     MONGODB_URI={YOUR_MONGODB_URI}
     ```
5. **Run the Bot**: Start the Telegram bot. 
   ```sh
   python app.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

1. **Start the Bot**: Open Telegram and find your bot.  
2. **Initiate the Interaction**: Type `/start` or `/topics` to begin. The bot will display the list of available topics (Business, Law, Coding, and Math).
3. **Choose a Topic**:  Select a topic of your interest. 
4. **Ask Questions**: Start asking questions related to the chosen topic. The bot will provide comprehensive answers, leveraging its knowledge base and Gemini's language processing capabilities.
5. **Review Past Interactions (Optional)**:  The bot will offer to review past discussions for continued learning.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


**Replace the following:**

* `{YOUR_TELEGRAM_BOT_TOKEN}` with your actual Telegram Bot token.
* `{YOUR_GEMINI_API_KEY}` with your actual Gemini API Key.
* `{YOUR_MONGODB_URI}` with your actual MongoDB connection URI. 
* `yourusername/LearnFrom0.git` with your GitHub repository URL (if you plan to host it there).

**Note:** I've added placeholders for badge links ([Python.org], etc.) to commonly used resources in the "Built With" section. You'll need to update those URLs to point to the correct locations for badges.  Also, adjust the "About the Project" section to provide more specifics as needed.

