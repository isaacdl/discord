import openai as ia
import os

ia.api_key = "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"

messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

def generate_gpt3_response(input_message):
    messages = [{"role": "user", "content": input_message}]
    chat = ia.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    reply = chat.choices[0].message.content
    return reply



