import openai


# Use GPT-3 prompt-completion model to summarize posts to a topic
def summarize_replies(
        context_dict,
        model="gpt-3.5-turbo-0613",
        temperature=0.7,
        max_tokens=1000):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    topic = context_dict['topic']
    question = context_dict['question']
    context = f"""Topic: {topic}
        {question}
        {chr(10).join(context_dict['replies'])}
        """
    try:
        prompt = f'''Summarize the answer to the question based on the context below, 
        and if the question can't be answered based on the context, say "I don't know"
        Context: {context}

        ---

        Question: {topic}
        Answer:'''
        print(prompt)
        messages = [{"role": "user", "content": prompt}]
        # Create a completions using the question and context
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=1,
            max_tokens=max_tokens)
        top_response = response.choices[0].message["content"]
        # If using the Completion model (don't use - it's 10x more expensive)
        # response = openai.Completion.create(
        #     prompt=prompt,
        #     temperature=temperature,
        #     max_tokens=max_tokens,
        #     top_p=1,
        #     frequency_penalty=0,
        #     presence_penalty=0,
        #     stop=None,
        #     model=model,
        # )
        # top_response = response["choices"][0]["text"].strip()
    except Exception as e:
        print(e)
        top_response = None
    return top_response
