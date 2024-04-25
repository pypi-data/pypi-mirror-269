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

    split_base = baseprompt.split("COMPOUND_NAME")
    prompt = split_base[0] + str(name) + split_base[1] + str(input_text)
    prompt = prompt[:max_length]

    response = client.chat.completions.create(
        model=gpt_model,
        messages=[{"role": "system", "content": prompt}]
        )
    
    return response.choices[0].message.content