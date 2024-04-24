#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__init__.py
"""
from gaea_operator.pipelines.ocrnet_pipeline.ocrnet_pipeline import pipeline as ocrnet_pipeline
from gaea_operator.pipelines.ppyoloe_plus_pipeline.ppyoloe_plus_pipeline import pipeline as ppyoloe_plus_pipeline
from gaea_operator.pipelines.resnet_pipeline.resnet_pipeline import pipeline as resnet_pipeline
from gaea_operator.pipelines.codetr_pipeline.codetr_pipeline import pipeline as codetr_pipeline

category_to_ppls = {
    "Image/SemanticSegmentation": [ocrnet_pipeline()],
    "Image/ObjectDetection": [ppyoloe_plus_pipeline(), codetr_pipeline()],
    "Image/ImageClassification/MultiClass": [resnet_pipeline()]
}
