from zyjj_client_sdk.base import Base, ApiService, MqttServer, MqttEventType
from zyjj_client_sdk.base.entity import TaskInfo
from zyjj_client_sdk.lib import FFMpegService, OSSService
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class CodeInfo:
    name: str
    inputs: list[str]
    outputs: list[str]
    code: str


# 节点
@dataclass
class FlowNode:
    node_id: str
    node_type: int
    data: str


@dataclass
class FlowRelation:
    from_id: str
    from_output: str
    to_id: str
    to_input: str


# 给flow节点提供的基本方法
class FlowBase:
    def __init__(
            self,
            base: Base,  # 基本信息
            api: ApiService,  # api服务
            mqtt: MqttServer,  # mqtt服务
            global_data: dict,  # 全局数据
            task_info: TaskInfo,  # 任务数据
            code_map: dict,  # 代码映射
    ):
        # 一些私有变量，不暴露
        self.__base = base
        self.__ffmpeg = FFMpegService()
        self.__mqtt = mqtt
        self.__global_data = global_data
        self.__task_info = task_info
        self.__code_map = code_map
        self.__node_current = None
        self.__node_pre: list[FlowRelation] = []
        self.__node_next: list[FlowRelation] = []
        # 可以被外部模块使用的变量
        self.api = api
        self.uid = task_info.uid

    # 设置当前节点的关联关系
    def set_flow_relation(self, node: FlowNode, prev: list[FlowRelation], after: list[FlowRelation]):
        self.__node_current = node
        self.__node_pre = prev
        self.__node_next = after

    # 获取输入
    def input_get(self) -> dict:
        return self.__task_info.input

    # 获取代码内容
    def code_info_get(self, code_id: str) -> CodeInfo:
        code_info = self.__code_map[code_id]
        return CodeInfo(
            code_info["name"],
            code_info["inputs"],
            code_info["outputs"],
            code_info["code"]
        )

    # 获取当前节点需要哪些输出字段
    def node_output_need(self) -> list[str]:
        return [relation.from_output for relation in self.__node_next]

    # 生成一个本地路径
    def tool_generate_local_path(self, ext: str) -> str:
        return self.__base.generate_local_file(ext)

    # 获取存储服务
    def new_oss(self) -> OSSService:
        return OSSService(self.__base, self.api)


# 处理节点定义
node_define = Callable[[FlowBase, dict, Optional[dict]], dict]
