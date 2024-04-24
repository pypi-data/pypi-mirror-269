import hanlp

# 映射表
entity_type_to_description = {
    'INTEGER': '整数',
    'ORDINAL': '序数',
    'LOCATION': '地点',
    'DATE': '日期',
    'ORGANIZATION': '组织',
    'PERSON': '人名',
    'MONEY': '金钱数额',
    'DURATION': '持续时间',
    'TIME': '时间',
    'LENGTH': '长度',
    'AGE': '年龄',
    'FREQUENCY': '频率',
    'ANGLE': '角度',
    'PHONE': '电话号码',
    'PERCENT': '百分比',
    'FRACTION': '分数',
    'WEIGHT': '重量',
    'AREA': '面积',
    'CAPACITY': '容量', 
    'DECIMAL': '小数',
    'MEASURE': '测量值',
    'SPEED': '速度',
    'TEMPERATURE': '温度',
    'POSTALCODE': '邮政编码',
    'RATE': '比率',
    'WWW': '网址'
}

class HanLPWrapper:
    def __init__(self, model_path):
        """
        初始化HanLPWrapper类。

        参数:
        - model_path: 模型的路径。
        """
        self.model = hanlp.load(model_path)

    def process_text(self, text, tasks='ner'):
        """
        使用加载的HanLP模型处理文本。

        参数:
        - text: 要处理的文本。
        
        返回:
        - 处理后的结果。
        """
        result = self.model(text, tasks=tasks)
        entities_list = []
        for entity in result['ner/msra']:
            entity_text = entity[0]  
            entity_type = entity[1] 
            description = entity_type_to_description.get(entity_type, "未知类型") 
            entities_list.append({
                'text': entity_text,
                'label': entity_type,
                'description': description
            })
        return entities_list