import json
import os

import typer
from openai import OpenAI, AuthenticationError
from rich import print


app = typer.Typer()


@app.command()
def generate(theme: str, palette_count: int = 1, color_count: int = 4, to_json: bool = False, json_file: str = None):
    api_key = os.getenv('OPENAI_KEY')
    if not api_key:
        raise typer.BadParameter("Please set your OpenAI API KEY as an env var named 'OPENAI_KEY'.")
    try:
        client = OpenAI(api_key=api_key)
        session = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a color specialist. You help people find colors that will work well based on a "
                        "given theme. The chosen colors are to be taken from the entire spectrum of hex colors that "
                        "are usable on the web. You will also find an appropriate name for the chosen color palette, "
                        "based only on the colors chosen and not on the theme. The name should not contain generic "
                        "terms like 'vibes'. The name should be based on real-world objects and not abstract "
                        "concepts, and must not contain the name of the given theme. It must consist of two to three "
                        "words. It may not include the following words: palette. You may be asked to create more than "
                        "1 palette. You will respond with a JSON-formatted string containing the name of the palette "
                        "as 'name' and an array of the chosen colors as 'colors'. The color should always be given as "
                        "hex values, as used in CSS. All the created palettes should be places in a list, even if "
                        "only 1 palette is present. Here is an example response: "
                        "[{\"name\": \"Electric Skyline\", \"colors\": [\"#FF00FF\", \"#00FF00\"]}]"
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Please create {palette_count} color palettes that fit into the '{theme}' theme "
                        f"and contain {color_count} colors."
                    )
                }
            ],
            temperature=0.8
        )
    except AuthenticationError:
        raise typer.BadParameter("Your API key was not valid - we could not authenticate with OpenAI.")
    response = session.choices[0].message.content

    json_list = json.loads(response)

    if to_json is True:
        pretty_json = json.dumps(json_list, indent=4)
        if json_file:
            with open(json_file, "w") as fh:
                fh.write(pretty_json)
            print(f"Palette data saved in {json_file}.")
        else:
            print(pretty_json)
        return

    for json_resp in json_list:
        print(json_resp["name"])
        for c in json_resp["colors"]:
            print(f"[on {c}]{c}        [/]")
        print()
