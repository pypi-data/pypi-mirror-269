import asyncio

import click

from .helper import print_result
from .iwashi import tree


@click.command()
@click.argument("url", required=True)
def main(url: str) -> None:
    result = asyncio.run(tree(url))
    assert result
    print("\n" * 4)
    print_result(result)


if __name__ == "__main__":
    main()
