from app.core.config import client, MODEL


def translate_to_english(text: str) -> str:
    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": "Translate the user's text into natural English. Return only the translation.",
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        temperature=0.1,
    )

    return response.output_text.strip()