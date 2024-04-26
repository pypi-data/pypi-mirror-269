import requests
import pandas as pd


# 定义项目工具类
class Dispider:
    # 初始化
    def __init__(self, worker, project=str):
        # 设置请求主站地址
        self.host = 'http://localhost:8000/'
        # 检测项目名的存在性
        name_permission = requests.post(url=self.host + 'project/check/', data={'project': project.lower()}).json()[
            '反馈']
        # 初始化项目名或抛出报错
        if name_permission:
            self.project_name = project
            print(f'欢迎进入{project}项目')
        else:
            raise ValueError("错误: 项目名未被注册，请联系管理员")
        self.mission_name = f'{self.project_name}_mi'
        self.result_name = f'{self.project_name}_re'
        self.worker = worker
        self.mission_id = None
        self.batch_start = 0

    # 检验文件格式
    @staticmethod
    def check_csv(file_path):
        if not file_path.endswith('.csv'):
            raise ValueError('错误：请选择一个 CSV 文件进行上传。')

    # 新建任务表
    def new_mission(self, file_path):
        # 检验文件格式
        self.check_csv(file_path)
        # 读取文件并请求新建任务表
        files = {'file': (f'{self.mission_name}.csv', open(file_path, 'rb'))}
        res = requests.post(url=self.host + 'project/new/', data={'sort': 'mission'}, files=files).text
        return res

    # 新建结果表
    def new_result(self, file_path):
        # 检验文件格式
        self.check_csv(file_path)
        # 读取文件并请求新建任务表
        files = {'file': (f'{self.result_name}.csv', open(file_path, 'rb'))}
        res = requests.post(url=self.host + 'project/new/', data={'sort': 'result'}, files=files).text
        return res

    # 获取任务
    def get_mission(self):
        # 参数构建
        data = {'mission_table': self.mission_name,
                'worker': self.worker,
                }
        # 发起请求
        res = requests.post(url=self.host + 'project/mission/', data=data).json()
        # 拆分响应数据
        mission_id = res['任务id']
        mission_content = res['任务']
        message = res['反馈']
        # 更新实例任务id
        self.mission_id = mission_id
        # 打印反馈
        print(f'{message}: No.{mission_id}')
        return mission_content

    # 提交任务
    def submit_mission(self, file_path):
        # 检验文件格式
        self.check_csv(file_path)
        # 读取文件并构建参数
        files = {'file': (f'{self.result_name}.csv', open(file_path, 'rb'))}
        data = {'mission_table': self.mission_name,
                'result_table': self.result_name,
                'mission_id': self.mission_id,
                }
        # 发起请求提交数据
        res = requests.post(url=self.host + 'project/submit/', data=data, files=files).text
        return res

    # 获取结果进行分析
    def get_result(self, batch):
        # 构建起止数组
        batch_start = self.batch_start
        batch_end = self.batch_start + batch
        # 设置参数
        data = {'result_table': self.result_name, 'batch_start': batch_start, 'batch_end': batch_end}
        # 发起请求
        res = requests.post(url=self.host + '/project/result/', data=data).json()
        # 打印反馈
        print(res['反馈'])
        data_result = res['数据']
        df = pd.DataFrame(data_result)
        # 更新起始点
        self.batch_start += batch
        return df

    # 获取结果表长度
    def get_length(self):
        res = requests.post(url=self.host + 'project/length/', data={'result_table': self.result_name}).json()
        return res['长度']
