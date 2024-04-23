import re
import jieba.posseg as pseg


class InformationExtractor:
    def __init__(self):
        # 更宽泛的电话号码匹配规则
        self.phone_pattern = re.compile(r'\b(?:\+?\d{1,3}[-.●]?)?\(?(?:\d{1,4}\)?[-.●]?)?\d{6,}\b')

    def extract_phone_numbers(self, text):
        # 从文本中提取更宽泛的手机号
        return re.findall(self.phone_pattern, text)

    def extract_locations(self, text):
        # 使用结巴分词和词性标注提取地名
        locations = []
        words = pseg.cut(text)
        for word, flag in words:
            if flag == 'ns':  # 'ns' 表示地名
                locations.append(word)
        return locations
