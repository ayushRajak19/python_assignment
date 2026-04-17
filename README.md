# 🤖 Smart Learning Role-Based Chatbot

## 📌 Overview
This project is a **Python-based chatbot** that supports multiple user roles and improves over time by learning from user interactions.

It is designed using a **config-driven approach**, making it flexible and easy to update without modifying code.

---

## 🎯 Features

- 👤 **Role-Based System**
  - Student
  - Teacher
  - Admin

- ⚙️ **Config-Driven Design**
  - All responses stored in `config.json`

- 🔍 **Keyword Matching**
  - Stopword removal
  - Keyword normalization
  - Fuzzy matching (for single-word queries)

- 🧠 **Learning Mode**
  - Learns new responses from user input
  - Stores them for future use

- 🔄 **Role Switching**
  - Switch roles using `switch` command

- 📝 **Logging System**
  - Stores:
    - User input
    - Bot response
    - Timestamp
  - Saved in `chat_log.txt`

- 💬 **Command Support**
  - `add` → add new response
  - `view` → view stored data
  - `switch` → change role
  - `exit` → exit chatbot

---

## 📂 Project Structure
