#!/usr/bin/env python
# ******************************************************************************
# Copyright 2024 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
This module allows to create a ViT model for Urbansound8k dataset.
"""

__all__ = ["vit_urbansound_pretrained"]


from ..utils import fetch_file
from ..model_io import load_model, get_model_path


def vit_urbansound_pretrained(quantized=True):
    """
    Helper method to retrieve an `vit_urbansound` model that was trained on Urbansound8k dataset.

    Args:
        quantized (bool, optional): a boolean indicating whether the model should be loaded
            quantized or not. Defaults to True.

    Returns:
        keras.Model: a Keras Model instance.

    """
    if quantized:
        model_name_v2 = 'bc_vit_urbansound_i8_w8_a8.h5'
        file_hash_v2 = '8c519dd1a6a924ec3d07d01199b8c0187a422b028a3869f7d4f611c6ec74498c'
    else:
        model_name_v2 = 'bc_vit_urbansound.h5'
        file_hash_v2 = '388454c922139d9813dae378f5e4084f4a4cb2d0dea57566cc53fc779ac8932c'

    model_path, model_name, file_hash = get_model_path("audio_vit", model_name_v2=model_name_v2,
                                                       file_hash_v2=file_hash_v2)
    model_path = fetch_file(model_path, fname=model_name, file_hash=file_hash,
                            cache_subdir='models')
    return load_model(model_path)
