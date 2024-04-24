import os
import dotenv
import typer
from rich import print
from rich.console import Console
from rich.panel import Panel
from yaspin import yaspin
from groq import Groq

console = Console()
app = typer.Typer()

dotenv.load_dotenv()
client = Groq(api_key="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")


def execute(prompt):
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None,
    )
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""
    return response


@app.command()
def main():
    while True:
        user_input = typer.prompt("Mensaje")
        if user_input.lower() in ["/exit", "/bye"]:
            raise typer.Exit()
        else:
            spinner = yaspin(text="Generando respuesta...")
            spinner.start()
            response = Panel(execute(
                f"Please response these questions: {user_input}"))
            # response = Panel(chat_mistral(user_input))
            spinner.stop()
            print(response)


if __name__ == "__main__":
    app()
