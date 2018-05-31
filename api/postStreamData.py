#! /usr/bin/python
# -*- coding:utf-8 -*-

import json

from flask import jsonify
from flask_restful import Resource, reqparse

from algorithm.streamAnomalyDetect import stream_anomaly_detect


class post_stream_data(Resource):
    """
    post stream data for anomaly detection with one field.

    predictStep 是当前预测值回溯到多少步之前，其实表示就是当前的预测受过去多少步的影响；
    enablePredict 是让HTM在做检测时输出预测值；
    metricData，maxValue，minValue，minResolution是为HTM生成一定尺度大小的模型，其实就是HTM算法接收的数据范围这些，方便HTM内部模型生成。
    """

    def __init__(self,
                 predictStep=2,
                 enablePredict=True,
                 maxValue=4200.0,
                 minValue=-4200.0,
                 minResolution=0.1
                 ):
        # initial the parameters and the target object.
        self.dataName = None
        self.timestamp = None
        self.actualValue = None
        self.predictValue = None
        self.anomalyScore = None
        self.output = []
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("streamData", type=str)
        self.detectObject = stream_anomaly_detect(
            predictStep=predictStep,
            enablePredict=enablePredict,
            maxValue=maxValue,
            minValue=minValue,
            minResolution=minResolution
        )

    def post(self):
        # parser the input data.
        args = self.parser.parse_args()["streamData"]
        # convert the json into proper type.
        inputData = json.loads(args)
        # get the target data.
        self.timestamp = inputData["timestamp"]
        self.actualValue = inputData["actualValue"]
        # compute the anomaly score and predict value.
        self.output = self.detectObject.anomalyDetect(self.timestamp, self.actualValue)
        self.predictValue = self.output["predictValue"]
        self.anomalyScore = self.output["anomalyScore"]

        return jsonify(
            timestamp=self.timestamp,
            actualValue=self.actualValue,
            predictValue=self.predictValue,
            anomalyScore=self.anomalyScore
        )
