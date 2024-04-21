import typer

app = typer.Typer()

@app.command()
def say_hello(name: str):
    print(f"Hello {name}!")

@app.command()
def say_goodbye(name: str):
    print(f"Goodbye {name}!")

if __name__ == "__main__":
    app()