#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""export model for YOLO"""
import os

import numpy as np
from mindspore import Tensor
from mindspore import context
from mindspore import dtype as mstype
from mindspore.train.serialization import export
from mindspore.train.serialization import load_checkpoint
from mindspore.train.serialization import load_param_into_net

from model_utils.config import config
from model_utils.moxing_adapter import moxing_wrapper
from src.yolo import YOLOv3Inference


def modelarts_pre_process():
    """modelarts pre process function."""
    config.file_name = os.path.join(config.output_path, config.file_name)


@moxing_wrapper(pre_process=modelarts_pre_process)
def run_export():
    """export model to ir file"""
    context.set_context(mode=context.GRAPH_MODE, device_target=config.device_target)
    if config.device_target == "Ascend":
        context.set_context(device_id=config.device_id)
    network = YOLOv3Inference(config.test_img_shape)
    param_dict = load_checkpoint(config.ckpt_file)
    load_param_into_net(network, param_dict)
    shape = [config.batch_size, 3] + config.test_img_shape
    input_data = Tensor(np.zeros(shape), mstype.float32)
    export(network, input_data, file_name=config.file_name, file_format=config.file_format)


if __name__ == "__main__":
    run_export()
