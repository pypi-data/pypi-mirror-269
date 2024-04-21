import fire


def hello(name="world"):
    print(f"hello, {name}!")


def main():
    fire.Fire(
        dict(
            hello=hello,
        )
    )


if __name__ == "__main__":
    main()
