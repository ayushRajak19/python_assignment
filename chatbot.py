import json
import datetime
from difflib import get_close_matches

CONFIG_FILE = "config.json"
LOG_FILE = "chat_log.txt"


class Chatbot:
    def __init__(self):
        self.data = self.load_data()
        self.role = None


    #  LOAD & SAVE
    def load_data(self):
        try:
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
        except:
            return {"student": {}, "teacher": {}, "admin": {}}

    def save_data(self):
        with open(CONFIG_FILE, "w") as file:
            json.dump(self.data, file, indent=4)

    # LOGGING 
    def log(self, user_input, bot_response):
        with open(LOG_FILE, "a") as file:
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{time}] Role: {self.role}\n")
            file.write(f"User: {user_input}\n")
            file.write(f"Bot: {bot_response}\n\n")

    # ROLE 
    def select_role(self):
        while True:
            role = input("Select role (student/teacher/admin): ").strip().lower()
            if role in self.data:
                self.role = role
                print(f"Logged in as {role}")
                break
            else:
                print("Invalid role. Try again.")

    # KEYWORD EXTRACTION 
    def extract_keyword(self, text):
        text = text.lower().replace("?", "")
        words = text.split()

        stopwords = ["what", "is", "the", "my", "when", "where", "how",
                         "for", "will", "be", "are", "was", "were",
                        "a", "an", "of", "to", "in", "on", "at",
                        "can", "could", "should", "please", "tell"]

        keywords = [w for w in words if w not in stopwords]
        keywords.sort()

        return " ".join(keywords)

    # MATCHING 
    def find_best_match(self, user_input):
        keywords = list(self.data[self.role].keys())
        cleaned_input = self.extract_keyword(user_input)

        # Exact match
        if cleaned_input in keywords:
            return cleaned_input

        # Multi-word  .. no fuzy 
        if len(cleaned_input.split()) > 1:
            return None

        # Fuzzy match .. single word
        matches = get_close_matches(cleaned_input, keywords, n=1, cutoff=0.8)
        return matches[0] if matches else None
    



    #  LEARNING
    def learn(self, user_input):
        print("Bot: I don’t know this. Please provide the correct response.")
        new_response = input("You: ").strip()

        keyword = self.extract_keyword(user_input)

        if keyword not in self.data[self.role]:
            self.data[self.role][keyword] = [new_response]
        else:
            self.data[self.role][keyword].append(new_response)

        self.save_data()

        print("Bot: Got it! I will remember this.")
        self.log(user_input, new_response)



    # COMMANDS
    def handle_command(self, user_input):
        if user_input == "exit":
            print("Bot: Goodbye!")
            return True

        elif user_input == "switch":
            self.select_role()
            return False

        elif user_input == "view":
            print("\nCurrent Data:")
            print(json.dumps(self.data[self.role], indent=4))
            return False

        elif user_input.startswith("add"):
            try:
                _, key, response = user_input.split(",", 2)
                key = key.strip().lower()
                response = response.strip()

                if key not in self.data[self.role]:
                    self.data[self.role][key] = []

                self.data[self.role][key].append(response)
                self.save_data()

                print("Bot: Added successfully!")
            except:
                print("Usage: add,keyword,response")

            return False

        return None

    # CHAT LOOP
    def chat(self):
        self.select_role()

        while True:
            try:
                user_input = input("You: ").strip().lower()
            except KeyboardInterrupt:
                print("\nBot: Goodbye!")
                break

            command = self.handle_command(user_input)
            if command is True:
                break
            elif command is False:
                continue

            key = self.find_best_match(user_input)

            if key:
                response = self.data[self.role][key][0]
                print("Bot:", response)
                self.log(user_input, response)
            else:
                self.learn(user_input)


if __name__ == "__main__":
    bot = Chatbot()
    bot.chat()