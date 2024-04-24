#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
publish_ppl.py
"""

import os
from argparse import ArgumentParser
from gaea_operator.pipelines import category_to_ppls
from windmillclient.client.windmill_client import WindmillClient
from windmillartifactv1.client.artifact_api_artifact import ArtifactContent
from windmilltrainingv1.client.training_api_pipeline import PipelineName


# python create_ppl.py --windmill-endpoint http://windmill.baidu-int.com:8340 --windmill-ak e0415220bbc94902b89fa3ceba3d4ca7 --windmill-sk 25f9ad7065b041598ce7711a2e591a2f

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--windmill-endpoint", type=str, default=os.environ.get("WINDMILL_ENDPOINT"))
    parser.add_argument("--windmill-ak", type=str, default=os.environ.get("WINDMILL_AK"))
    parser.add_argument("--windmill-sk", type=str, default=os.environ.get("WINDMILL_SK")) 

    parser.add_argument("--workspace-id", type=str, default="public")
    parser.add_argument("--project-name", type=str, default="default")
    args, _ = parser.parse_known_args()

    client = WindmillClient(endpoint=args.windmill_endpoint, ak=args.windmill_ak, sk=args.windmill_sk)
    workspace_id = args.workspace_id
    project_name = args.project_name

    for cat, ppls in category_to_ppls.items():
        for p in ppls:
            print("pipeline name: {}".format(p.name))
            filepath = "./pipelines/{}_pipeline.yaml".format(p.name)
            p.compile(save_path=filepath)

            ppl_name = PipelineName(workspace_id=workspace_id, project_name=project_name, local_name=p.name)
            location = client.create_location_with_uri(uri=filepath, object_name=ppl_name.get_name())

            artifact = ArtifactContent(uri=location)

            try:
                resp = client.create_pipeline(
                    workspace_id=workspace_id,
                    project_name=project_name,
                    local_name=p.name,
                    category=cat,
                    artifact=artifact)
                print("pipeline: {} created.".format(resp.get("name")))
            except Exception as e:
                print(e)
        
