import openai


def ChatGPT(prompt, api_key):
    openai.api_key = api_key

    completion = openai.Completion.create(
        engine='gpt-3.5-turbo-instruct'
        , prompt=prompt
        , temperature=0.5
        , max_tokens=1024
        , top_p=1
        , frequency_penalty=0
        , presence_penalty=0)

    return completion['choices'][0]['text']


if __name__ == '__main__':
    prompt = "재무재표에 대해서 설명해줘"
    print(ChatGPT(prompt, "sk-").strip())
