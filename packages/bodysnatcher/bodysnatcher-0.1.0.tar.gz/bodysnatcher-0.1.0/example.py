import logging

from bodysnatcher import Bodysnatcher


def fn():
    logging.basicConfig(level="DEBUG")
    with Bodysnatcher("/tmp/lol") as bs:
        foo = {"Hello": "World"}
        bar = 1, 2, 3
        assert 0


if __name__ == "__main__":
    fn()
