# Skincare Routine Assistant

### This is a simple GenAI application that recommends a skincare routine based on a user's skin type and skin issues.

#### Setup
To try out the app on your local machine...
1. First clone the repo into your desired location:
```git clone https://github.com/mackenziemitchell6/SkincareRoutineAssistant.git```
2. Navigate to the repo's location on your local
```cd SkincareRoutineAssistant```
3. Create a venv
   1. ```python3 -m venv venv```
   2. ```source venv/bin/activate```
4. Pip install all needed libraries
   1. ```pip install requirements.txt```
5. Setup streamlit secrets with OpenAI API KEY
   1. Generate an OpenAI API key here: https://platform.openai.com/api-keys
   2. Create a directory under the root ```SkincareRoutineAssistant``` dir called ```.streamlit```
   3. Create a file under the ```.streamlit``` dir called ```secrets.toml```
   4. Add your OpenAI API key to the ```.streamlit/secrets.toml``` file in the following format:
   ```
   [openai]
    API_KEY="{OPENAI_API_KEY}"
   ```
6. Ensure you are in the SkincareRoutineAssistant root directory, and run
```streamlit run app/app.py```

