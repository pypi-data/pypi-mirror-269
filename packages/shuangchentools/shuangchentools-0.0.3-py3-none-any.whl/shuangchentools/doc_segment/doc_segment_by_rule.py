"""
@Author: shuangchen
@Time: 2024/3/12
@File: doc_segment_by_rule.py
@Description: 通过规则分割文档
"""

import re


SEGMENT_DEPTH_ERROR_MSG = '分割的深度应当在1-3之间'
FILE_TYPE_ERROR_MSG = '只支持.txt格式'


def merge_sentences(sentences: list[str], title_pattern: str = None) -> list[str]:
    """
    合并句子的不正确的换行，以句尾标点为依据
    :param sentences: 合并前句子列表
    :param title_pattern: 需要忽略合并的句子规则（一般为标题）
    :return: 合并前句子列表
    """
    merged = []
    temp = ''
    for sentence in sentences:
        if title_pattern is None and re.match(title_pattern, sentence):
            if temp:
                merged.append(temp)
                temp = ''
            merged.append(sentence)
        else:
            if not re.search(r'[.!?。，？；！:：）)]$', sentence):  # $确定表达符号处于句子的最后
                temp += sentence
            else:
                if temp:
                    merged.append(temp + sentence)
                    temp = ''
                else:
                    merged.append(sentence)
    if temp:
        merged.append(temp)
    return merged


class DocSegmentByRule:
    def __init__(self, patterns: list[str], merge_sentences: bool = True, ignore_pattern: str = '', ignore_title_front: bool = False) -> None:
        """
        使用规则匹配文章标题，按标题进行分割
        :param patterns: 标题匹配规则，按一级标题、二级标题、三级标题顺序排列
        :param merge_sentences: 是否进行句子不正确换行的合并（慎用）
        :param ignore_pattern: 需要忽略的句子规则
        :param ignore_title_front: 是否忽略标题前的内容
        """
        self.depth = len(patterns)
        assert 1 <= self.depth <= 3, SEGMENT_DEPTH_ERROR_MSG
        self.patterns = patterns
        self.title_pattern = '|'.join([f'({p})' for p in patterns])  # 用于合并句子时忽略标题
        self.merge_sentences = merge_sentences
        self.ignore_pattern = ignore_pattern
        self.ignore_title_front = ignore_title_front

    def solve(self, files: str | list[str]) -> list[str] | dict[str, list[str]]:
        """
        对文件进行分割
        :param files: 文件或文件列表
        :return: 每份文件的段落列表，以字典文件名：列表格式返回
        """
        if isinstance(files, str):
            files = [files]

        result = {}

        for file in files:
            assert file.endswith('.txt'), FILE_TYPE_ERROR_MSG
            f = open(file, 'r', encoding='utf-8')
            lines = [line.strip() for line in f.readlines()]
            if self.merge_sentences:
                lines = merge_sentences(lines, self.title_pattern)
            f.close()

            paragraphs = []
            temp = ''

            if self.depth == 1:
                title_front = True  # 因为没有title变量所以新加一个变量判断是否在标题前
                for line in lines:
                    if re.match(self.patterns[0], line):  # 一级标题
                        title_front = False
                        if temp:
                            paragraphs.append(temp.rstrip())
                            temp = ''
                    if title_front and self.ignore_title_front:
                        continue
                    temp += line + '\n'
                if temp:
                    paragraphs.append(temp.rstrip())

            elif self.depth == 2:
                title1 = ''
                for line in lines:
                    if re.match(self.patterns[1], line):  # 二级标题
                        if temp:
                            paragraphs.append(title1 + '\n' + temp.rstrip())
                            temp = ''
                        temp += line + '\n'
                    elif re.match(self.patterns[0], line):  # 一级标题
                        if temp:
                            paragraphs.append(title1 + '\n' + temp.rstrip())
                            temp = ''
                        elif len(title1) != 0:
                            paragraphs.append(title1)
                        title1 = line
                    else:  # 正文
                        if len(title1) == 0 and self.ignore_title_front:  # 忽略在正式标题前的内容
                            continue
                        temp += line + '\n'
                if temp:
                    paragraphs.append(title1 + '\n' + temp.rstrip())
                elif len(title1) != 0:
                    paragraphs.append(title1)

            elif self.depth == 3:
                title1, title2 = '', ''
                for line in lines:
                    if re.match(self.patterns[2], line):  # 三级标题
                        if temp:
                            paragraphs.append(title1 + '\n' + title2 + '\n' + temp.rstrip())
                            temp = ''
                        temp += line + '\n'  # 这里直接写成temp = line + '\n'也是可以的（上面的temp = ''也可以不要了）
                    elif re.match(self.patterns[1], line):  # 二级标题
                        if temp:
                            paragraphs.append(title1 + '\n' + title2 + '\n' + temp.rstrip())
                            temp = ''
                        elif len(title2) != 0:  # 假如没有三级标题，这里就会将二级标题作为正文
                            paragraphs.append(title1 + '\n' + title2)
                        title2 = line
                    elif re.match(self.patterns[0], line):  # 一级标题
                        if temp:
                            paragraphs.append(title1 + '\n' + title2 + '\n' + temp.rstrip())
                            temp = ''
                        elif len(title2) != 0:
                            paragraphs.append(title1 + '\n' + title2)
                        elif len(title1) != 0:
                            paragraphs.append(title1)
                        title1 = line
                        title2 = ''
                    else:  # 正文
                        if len(title1) == 0 and self.ignore_title_front:  # 忽略在正式标题前的内容 只需要title1即可
                            continue
                        temp += line + '\n'
                if temp:
                    paragraphs.append(title1 + '\n' + title2 + '\n' + temp.rstrip())
                elif len(title2) != 0:
                    paragraphs.append(title1 + '\n' + title2)
                elif len(title1) != 0:
                    paragraphs.append(title1)

            result[file] = paragraphs

        if len(result) == 1:
            return result[files[0]]
        return result


if __name__ == '__main__':
    pass
