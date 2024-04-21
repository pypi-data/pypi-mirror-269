import zhconv


def ToSimplifiedChinese(string: str) -> str:
    """
    转为简体中文
    """
    return zhconv.convert(string, "zh-cn")