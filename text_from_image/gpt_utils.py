from extensions import openai

# Specify the message you want to send to ChatGPT

def ask_question(user_input, system_prompt):
    # Make a request to the ChatGPT model
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system",
                                                       "content": system_prompt},

                                                      {"role": "user", "content": user_input}])
    # Extract and print the model's response
    reply = response.choices[0].message.content
    return reply


