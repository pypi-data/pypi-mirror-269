from fei_crypto.discord_webhook import send
import typer


def run():
    typer.run(send)


if __name__ == '__main__':
    run()
