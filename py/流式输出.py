from openai import OpenAI
client = OpenAI(api_key="sk-93nWYhI8SrnXad5m9932CeBdDeDf4233B21d93D217095f22", base_url="http://10.2.8.77:3000/v1")


# Round 1
messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]
response = client.chat.completions.create(
    model="DeepSeek-R1",
    messages=messages,
    stream=True
)

reasoning_content = ""
content = ""

for chunk in response:
    content += chunk.choices[0].delta.content
    print(chunk.choices[0].delta.content,end='')

