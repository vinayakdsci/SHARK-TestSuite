# Copyright 2024 Advanced Micro Devices, Inc.
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from pathlib import Path

from e2e_testing.registry import register_test
from e2e_testing.storage import load_test_txt_file
from ..helper_classes import OnnxModelZooDownloadableModel
from .azure_models import custom_registry


this_file = Path(__file__)
lists_dir = (this_file.parent).joinpath("external_lists")
onnx_zoo_non_validated = load_test_txt_file(lists_dir.joinpath("onnx_model_zoo_nlp.txt"))
onnx_zoo_non_validated += load_test_txt_file(lists_dir.joinpath("onnx_model_zoo_graph_ml.txt"))
onnx_zoo_non_validated += load_test_txt_file(lists_dir.joinpath("onnx_model_zoo_gen_ai.txt"))
for i in range(5):
    onnx_zoo_non_validated += load_test_txt_file(
        lists_dir.joinpath(f"onnx_model_zoo_computer_vision_{i+1}.txt")
    )

onnx_zoo_validated = load_test_txt_file(lists_dir.joinpath("onnx_model_zoo_validated_text.txt"))
onnx_zoo_validated += load_test_txt_file(lists_dir.joinpath("onnx_model_zoo_validated_vision.txt"))


# Putting this inside the class contructor will
# call this repeatedly, which is wasteful.
model_path_map = {}
def build_model_to_path_map():
    for name in onnx_zoo_non_validated:
        test_name = name.split("/")[-2]
        model_path_map[test_name] = name

    for name in onnx_zoo_validated:
        test_name = '.'.join((name.split("/")[-1]).split('.')[:-2])
        model_path_map[test_name] = name


build_model_to_path_map()



for t in set(onnx_zoo_non_validated).difference(custom_registry):
    t_split = t.split("/")[-2]
    register_test(OnnxModelZooDownloadableModel, t_split)

for t in set(onnx_zoo_validated).difference(custom_registry):
    t_split = ".".join((t.split("/")[-1]).split(".")[:-2])
    register_test(OnnxModelZooDownloadableModel, t_split)
