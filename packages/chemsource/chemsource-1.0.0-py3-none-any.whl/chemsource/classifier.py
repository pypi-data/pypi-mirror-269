from openai import OpenAI

def classify(name,
             input_text=None, 
             openaikey=None, 
             baseprompt=None,
             gpt_model='gpt-4-0125-preview', 
             max_length=250000):
    
    client = OpenAI(
                    api_key=(openaikey)
                    )

    prompt = baseprompt[0] + str(name) + baseprompt[1] + str(input_text)
    prompt = prompt[:max_length]

    response = client.chat.completions.create(
        model=gpt_model,
        messages=[{"role": "system", "content": prompt}]
        )
    
    return response.choices[0].message.content