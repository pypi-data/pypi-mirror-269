import json
import logging
import time

from zyjj_client_sdk.flow.base import FlowBase, FlowNode, FlowRelation, node_define
import zyjj_client_sdk.flow.node as Node


class FlowService:
    def __init__(self, base: FlowBase, flow_data: dict):
        # 不同类型的节点处理函数
        self.__node_type_handle: dict[int, node_define] = {
            0: Node.node_input,
            1: Node.node_output,
            2: Node.node_code,
            3: Node.node_get_config,
            4: Node.node_check_point,
            5: Node.node_cost_point,
            6: Node.node_upload_file,
            7: Node.node_download_file,
            8: Node.node_file_parse,
            9: Node.node_file_export,
            10: Node.node_get_tencent_token,
            11: Node.node_generate_local_path,
            12: Node.node_download_url
        }
        # 基本服务
        self.__base = base
        # 所有节点对应的信息
        self.__node_id_info: dict[str, FlowNode] = {}
        # 开始节点
        self.__start_node_id = ""
        self.__end_node_id = ""
        # 当前节点对应的后继节点
        self.__node_next: dict[str, list[FlowRelation]] = {}
        # 当前节点对应的前驱节点
        self.__node_prev: dict[str, list[FlowRelation]] = {}
        # 每个节点的输出数据
        self.__node_output: dict[str, dict[str, str]] = {}
        # 已经完成的节点
        self.__node_finish = []
        # 先解析所有node对应的type
        for node in flow_data["nodes"]:
            node_data = node["data"] if "data" in node else "{}"
            flow_node = FlowNode(node["node_id"], node["node_type"], node_data)
            self.__node_id_info[flow_node.node_id] = flow_node
            if flow_node.node_type == 0:
                self.__start_node_id = flow_node.node_id
            elif flow_node.node_type == 1:
                self.__end_node_id = flow_node.node_id
            # 节点类型全部初始化
            self.__node_output[flow_node.node_id] = {}
            self.__node_prev[flow_node.node_id] = []
            self.__node_next[flow_node.node_id] = []

        # 解析出所有节点的依赖关系
        for relation in flow_data["relations"]:
            flow_relation = FlowRelation(
                relation["from"],
                relation["from_output"],
                relation["to"],
                relation["to_input"]
            )
            self.__node_prev[flow_relation.to_id].append(flow_relation)
            self.__node_next[flow_relation.from_id].append(flow_relation)

    @staticmethod
    def __filter_dict_bytes(data: dict) -> dict:
        new_dict = {}
        for key, value in data.items():
            if isinstance(value, bytes):
                new_dict[key] = f'bytes({len(value)})'
            else:
                new_dict[key] = value
        return new_dict

    def __execute_node(self, node_id: str):
        # 当前节点如果执行过就直接返回
        if node_id in self.__node_finish:
            return
        # 获取当前节点的信息
        info = self.__node_id_info[node_id]
        # 获取当前节点的处理函数
        handle = self.__node_type_handle[info.node_type]
        handle_intput = {}
        # 先判断一下当前节点前驱节点都处理完了，并获取到输出
        for before in self.__node_prev.get(node_id, []):
            self.__execute_node(before.from_id)
            handle_intput[before.to_input] = self.__node_output[before.from_id][before.from_output]
        # 执行前再检查一下
        if node_id not in self.__node_finish:
            node_start = time.time()
            handle_extra = {}
            # data不为空不设置exta信息
            if info.data is not None and info.data != '':
                handle_extra = json.loads(info.data)
            # 设置当前节点的依赖信息，并传递给base，方便子模块调用
            self.__base.set_flow_relation(
                self.__node_id_info[node_id],
                self.__node_prev.get(node_id, []),
                self.__node_next.get(node_id, []),
            )
            # 执行当前节点
            self.__node_output[node_id] = handle(self.__base, handle_intput, handle_extra)
            # 标记当前节点已完成
            self.__node_finish.append(node_id)
            logging.info(
                f"execute node {node_id} cost {(time.time()-node_start)*1000}ms\n"
                f"input {self.__filter_dict_bytes(handle_intput)} \n"
                f"extra {info.data} \n"
                f"response {self.__filter_dict_bytes(self.__node_output[node_id])}"
            )
        # 执行当前节点的后继节点
        for after in self.__node_next.get(node_id, []):
            self.__execute_node(after.to_id)

    # 触发流程
    def tiger(self) -> dict:
        flow_start = time.time()
        self.__execute_node(self.__start_node_id)
        logging.info(f"flow cost {(time.time()-flow_start)}s")
        # 直接返回结束节点的结果
        return self.__node_output[self.__end_node_id]
