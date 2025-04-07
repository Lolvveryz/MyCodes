from openai import OpenAI
from people_chats import get_mess, add_system_message, add_user_message


def gpt4(text, api, id_):
    add_user_message(id_, text)

    client = OpenAI(api_key=api)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=get_mess(id_),
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    
    add_system_message(id_, response.choices[0].message.content)
    
    return response.choices[0].message.content
 