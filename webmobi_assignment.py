# -*- coding: utf-8 -*-
"""Webmobi Assignment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1adqjJkTxjsYnOAGHLujodmL-dAQRiFWj
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load pre-trained model and tokenizer
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_response(conversation_history, new_user_input):
    # Encode the new user input and add the eos_token
    new_user_input_ids = tokenizer.encode(new_user_input + tokenizer.eos_token, return_tensors='pt')

    # Append the new user input tokens to the chat history
    bot_input_ids = torch.cat([conversation_history, new_user_input_ids], dim=-1) if conversation_history is not None else new_user_input_ids

    # Generate a response
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # Decode the response
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    return response, chat_history_ids

def interact_with_bot():
    conversation = {
        "name": "",
        "email": "",
        "company": ""
    }
    conversation_history = None

    # Greeting
    print("Bot: Hello! Welcome to our service. What's your name?")
    user_input = input("user: ")
    conversation["name"] = user_input
    conversation_history = tokenizer.encode("Hello! Welcome to our service. What's your name? " + user_input + tokenizer.eos_token, return_tensors='pt')

    # Asking for email
    email_prompt = f"Nice to meet you, {conversation['name']}! Can I have your email address?"
    print(f"Bot: {email_prompt}")
    user_input = input("User: ")
    conversation["email"] = user_input
    conversation_history = torch.cat([conversation_history, tokenizer.encode(email_prompt + user_input + tokenizer.eos_token, return_tensors='pt')], dim=-1)

    # Asking for company
    company_prompt = f"Thanks, {conversation['name']}. Lastly, could you tell me the name of your company?"
    print(f"Bot: {company_prompt}")
    user_input = input("User: ")
    conversation["company"] = user_input
    conversation_history = torch.cat([conversation_history, tokenizer.encode(company_prompt + user_input + tokenizer.eos_token, return_tensors='pt')], dim=-1)

    # Confirmation
    confirmation = f"Great! Thank you, {conversation['name']}. I have your details as {conversation['name']}, {conversation['email']}, {conversation['company']}."
    print(f"Bot: {confirmation}")

# Run the bot interaction
interact_with_bot()

