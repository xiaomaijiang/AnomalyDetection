#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask
from flask_restful import Api

from api.postMultiStreamData import post_multi_stream_data
from api.postStreamData import post_stream_data

app = Flask(__name__)
api = Api(app)

# api.add_resource(get_HTM_parameters, "/api/HTM/v1.0/HTMParametes")
# api.add_resource(post_stream_parameters, "/api/HTM/v1.0/streamParameters")
# api.add_resource(post_stream_data, "/api/HTM/v1.0/anomalyDetection")


# 修改为从DB读取配置
ResourceForPostStreamData = {
    'demo': post_stream_data()
}

ResourceForMultiPostStreamData = {
    'demo': post_multi_stream_data()
}


@app.route("/api/HTM/v1.0/anomalyDetection/<string:model_id>", methods=['POST'])
def post(model_id):
    targetModel = ResourceForPostStreamData[model_id]
    result = targetModel.post()
    return result


# allocating the resource for "multiple post stream data".
@app.route("/api/HTM/v1.0/multiAnomalyDetection/<string:model_id>", methods=['POST'])
def postMulti(model_id):
    targetModel = ResourceForMultiPostStreamData[model_id]
    result = targetModel.post()
    return result


if __name__ == '__main__':
    app.run(debug=True)
