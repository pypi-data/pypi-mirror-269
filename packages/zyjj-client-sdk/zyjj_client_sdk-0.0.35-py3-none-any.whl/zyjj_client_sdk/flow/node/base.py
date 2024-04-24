import logging
from typing import Optional

from zyjj_client_sdk.flow.base import FlowBase


# 输入节点
def node_input(base: FlowBase, data: dict, extra: Optional[dict]) -> dict:
    input_data = {}
    user_input = base.input_get()
    for unique in extra["uniques"]:
        if unique in user_input:
            input_data[unique] = user_input[unique]
        else:
            input_data[unique] = None

    return input_data


# 输出节点
def node_output(base: FlowBase, data: dict, extra: Optional[dict]) -> dict:
    return data


# 代码节点
def node_code(base: FlowBase, data: dict, extra: Optional[dict]) -> dict:
    code_info = base.code_info_get(extra["id"])
    logging.info(f"execute code {code_info}")
    local_data = {
        "inputs": [data[unique] for unique in code_info.inputs],
    }
    output_set = [f'"{unique}":handle_res[{idx}]' for idx, unique in enumerate(code_info.outputs)]
    exec(f"{code_info.code}\nhandle_res = handle(*inputs)\noutputs={{{','.join(output_set)}}}", {}, local_data)
    return local_data["outputs"]
