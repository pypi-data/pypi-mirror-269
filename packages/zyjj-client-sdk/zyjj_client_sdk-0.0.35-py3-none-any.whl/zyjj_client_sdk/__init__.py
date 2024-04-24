import json
import logging
import traceback

from zyjj_client_sdk.base import Base, ApiService, MqttServer, MqttEventType
from zyjj_client_sdk.base.entity import TaskInfo, TaskStatus
from zyjj_client_sdk.flow import FlowBase, FlowService


# 本地服务端
class Service:
    # 初始化基本服务
    def __init__(self):
        self.__base = Base()
        self.__api = ApiService(self.__base)
        self.__handle = {}
        self.__mqtt = MqttServer(self.__api)
        self.__global_data = {}

    # 添加全局变量
    def add_global(self, key: str, value: any) -> 'Service':
        self.__global_data[key] = value
        return self

    # 启动服务
    def start(self) -> 'Service':
        # 后台启动mqtt
        self.__mqtt.start_backend()
        return self

    # 停止服务
    def stop(self) -> 'Service':
        self.__mqtt.close()
        return self

    # 执行任务
    def execute_task(self) -> dict:
        # 拉取任务
        task_info = self.__api.task_pull_task()
        if task_info is None:
            logging.info("[task] task not found")
            return {"msg": "task not found"}
        logging.info(f'[task] pull task is {task_info}')
        # 获取任务信息
        task_info = TaskInfo(
            task_info['id'],
            task_info['uid'],
            task_info['task_type'],
            json.loads(task_info['input']),
        )
        try:
            # 拉取任务流程信息
            flow_info = self.__api.task_pull_flow(task_info.task_type)
            # 初始化流程服务
            service = FlowService(
                FlowBase(
                    self.__base,
                    self.__api,
                    self.__mqtt,
                    self.__global_data,
                    task_info,
                    flow_info["code_map"]
                ),
                flow_info["flow_info"]
            )
            # 触发流程
            data = service.tiger()
            self.__api.task_update_task(
                task_info.task_id,
                status=TaskStatus.Success,
                output=json.dumps(data, ensure_ascii=False)
            )
            self.__mqtt.send_task_event(
                task_info.uid,
                task_info.task_id,
                MqttEventType.Success,
                data
            )
            return data
        except Exception as e:
            traceback.print_exc()
            self.__api.task_update_task(task_info.task_id, status=TaskStatus.Fail, extra=str(e))
            self.__mqtt.send_task_event(task_info.uid, task_info.task_id, MqttEventType.Fail, str(e))
            return {"msg": str(e)}
