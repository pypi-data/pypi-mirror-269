import os
import json
from mysql.connector import Error
from flask import Flask, request, jsonify, make_response

# 默认配置
default_config = {
    'host': '0.0.0.0',
    'port': 8080,
    'debug': False,
}

# 设置环境变量
def set_environment_variable(name, value):
    """
    设置环境变量。

    参数:
    - name: 环境变量的名称。
    - value: 要设置的值。
    """
    os.environ[name] = value

# 去除空格
def trim(data, key, default=""):
    value = data.get(key, default)
    if isinstance(value, str):
        return value.strip()
    return value

# 默认为 None
def defNone(data, key):
    return data.get(key, None)

# 参数均不能为空
def haveAll(key1, key2):
    if not key1 or not key2:
        raise Error("参数均不能为空")
    
# 非空校验
def notNull(params):
    """非空校验"""
    if not params:
        raise Error("参数不能为空")
    
# 非空并且是列表
def isList(params):
    """非空并且是列表"""
    if not params or not isinstance(params, list):
        raise Error("参数必须是列表")
    
# 将数组转成 JSON 格式
def formatJson(array, key, value):
    try:
        annotations = []
        for text, label in array:
            annotation = {key: text, value: label}
            annotations.append(annotation)
        annotations_json = json.dumps(annotations)
        return annotations_json
    except Error as e:
        raise Error("数组转 JSON 格式失败")

# 预测的逻辑
def predictResult(server, text):
    try:
        result = server.predict(text)
        entities = result['ner'][0]
        return [{"key": entity[1], "value": entity[0]} for entity in entities]
    except Error:
        raise Error

# 必须是整数
def isInt(params):
    """必须是整数"""
    if not params or not isinstance(params, int):
        raise Error("参数必须是整数")

# 服务
def Service(__name__):
    return Flask(__name__)

# 解析参数
def get_request_data(params="body"):
    if params == "body":
        return request.get_json()
    else:
        return request.args

# 发送数据
def send_data(code=0, msg="数据获取成功。", data=None):
    response_content = {"code": code, "msg": msg}
    if data is not None:
        response_content["data"] = data
    status = 200 if code == 0 else code
    return make_response(jsonify(response_content), status)

# 运行服务
def run(app, config = default_config):
    final_config = {**default_config, **config}
    app.run(**final_config)
