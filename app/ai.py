from openai import AsyncOpenAI


from config import AI_TOKEN, SYSTEM_PROMT, POSTING_PROMT


async def get_completion(content):
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=AI_TOKEN,
    )

    completion = await client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
        },
        extra_body={},
        model="google/gemini-2.0-flash-lite-001",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMT
            },
            {
                "role": "user",
                "content": content
            }
        ]
    )
    return completion.choices[0].message.content


async def post_for_tg_chanel(post):
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=AI_TOKEN,
    )

    completion = await client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
        },
        extra_body={},
        model="google/gemini-2.0-flash-lite-001",
        messages=[
            {
                "role": "system",
                "content": POSTING_PROMT
            },
            {
                "role": "user",
                "content": post
            }
        ]
    )
    return completion.choices[0].message.content