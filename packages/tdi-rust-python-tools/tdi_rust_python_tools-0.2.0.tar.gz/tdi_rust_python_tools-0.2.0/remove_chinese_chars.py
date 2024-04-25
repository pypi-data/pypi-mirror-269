import re

from tdi_rust_python_tools import remove_chinese_chars

from shared.shared import timeit

CHINESE_CHARS = re.compile(r"[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]")


TEST_VALUES: list[str] = [
    "",
    "ABC  Antibody",
    "ABC Antibody (兔抗體)",
    "Hello, 世界",
    "你好, World",
    "Rust语言",
    "我爱编程",
    "12345",
    "混合 English 和 中文",
    "NoChineseHere",
]


def remove_chinese_chars_old_python(value: str) -> str:
    """Removes all Chinese characters from `value`."""
    return CHINESE_CHARS.sub("", value)


@timeit
def process_python_old() -> None:
    for _ in range(10_000_000):
        for value in TEST_VALUES:
            _ = remove_chinese_chars_old_python(value)


@timeit
def process_rust() -> None:
    for _ in range(10_000_000):
        for value in TEST_VALUES:
            _ = remove_chinese_chars(value)


def main() -> None:
    process_python_old()
    process_rust()


if __name__ == "__main__":
    main()
