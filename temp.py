def print(str_item):
    xbot_visual.programing.log(type="info", text=lambda: str_item, _block=("main", 1, "打印日志"))
    # 导入xbot和xbot_visual模块，用于机器人的视觉功能和对话框展示
import xbot
import xbot_visual
# 从当前目录导入package模块
from . import package
# 从package模块导入variables并命名为glv
from .package import variables as glv
# 导入time模块，用于控制时间相关的功能
import time
# 导入操作系统接口模块
import os
# 导入sys模块，用于访问与Python解释器密切相关的变量和函数
import sys

# 从typing模块导入List，用于类型注解
from typing import List

# 导入阿里云OCR API客户端
from alibabacloud_ocr_api20210707.client import Client as ocr_api20210707Client
# 导入阿里云OpenAPI模型
from alibabacloud_tea_openapi import models as open_api_models
# 导入阿里云Darabonba流客户端
from alibabacloud_darabonba_stream.client import Client as StreamClient
# 导入阿里云OCR API模型
from alibabacloud_ocr_api20210707 import models as ocr_api_20210707_models
# 导入阿里云工具模型
from alibabacloud_tea_util import models as util_models
# 导入阿里云工具客户端
from alibabacloud_tea_util.client import Client as UtilClient

# 导入SQLAlchemy的创建引擎模块
from sqlalchemy import create_engine, text
# 导入pandas模块，用于数据处理
import pandas as pd

# 弹出选择对话框，让用户选择操作
select_dialog = xbot_visual.dialog.show_select_dialog(
    title=None,  # 对话框标题
    label=None,  # 对话框标签
    select_type="list",  # 选择类型为列表
    select_model="single",  # 选择模式为单选
    values=lambda: ["爬取商品详情页图片", "OCR识别"],  # 提供给用户的选项
    is_selected_first=True,  # 默认选中第一个
    storage_key="498910e4-268c-4b57-a1fe-065daf8f9be8",  # 存储键值
    _block=("main", 1, "打开选择对话框")  # 日志记录块信息
)
# 如果用户选择了"爬取商品详情页图片"并且有按下按钮
if xbot_visual.workflow.multiconditional_judgment(
        relation="and",  # 逻辑关系为"与"
        conditionals=[  # 条件数组
            {"operand1": select_dialog.values, "operand2": lambda: "商品详情页图片爬取", "operator": "=="},
            {"operand1": select_dialog.pressed_button, "operand2": lambda: None, "operator": "!="}
        ],
        _block=("main", 2, "IF 多条件")  # 日志记录块信息
):
    # 打印日志，表示正在进行OCR识别
    xbot_visual.programing.log(type="info", text=lambda: "正在进行商品详情页图片爬取", _block=("main", 3, "打印日志"))
    # 打印出用户按下的按钮
    xbot_visual.programing.log(type="info", text=select_dialog.pressed_button, _block=("main", 4, "打印日志"))
# 如果用户选择了"OCR识别"并且有按下按钮
elif xbot_visual.workflow.multiconditional_judgment(
        relation="and",  # 逻辑关系为"与"
        conditionals=[  # 条件数组
            {"operand1": select_dialog.values, "operand2": lambda: "OCR识别", "operator": "=="},
            {"operand1": select_dialog.values, "operand2": lambda: None, "operator": "!="}
        ],
        _block=("main", 5, "Else IF 多条件")  # 日志记录块信息
):
    # 打印日志，表示正在进行OCR识别
    xbot_visual.programing.log(type="info", text=lambda: "正在进行OCR识别", _block=("main", 3, "打印日志"))
    # 打印出用户按下的按钮
    xbot_visual.programing.log(type="info", text=select_dialog.pressed_button, _block=("main", 4, "打印日志"))
    # 弹出选择文件夹对话框
    select_folder_dialog = xbot_visual.dialog.show_select_folder_dialog(
        title="\"请选择商品ID所对应的文件夹\"",  # 对话框标题
        folder="",  # 默认文件夹为空
        _block=("main", 6, "打开选择文件夹对话框")  # 日志记录块信息
    )
    # 打印选择的文件夹路径
    xbot_visual.programing.log(type="info", text=select_folder_dialog.folder, _block=("main", 7, "打印日志"))


#     # 弹出选择文件对话框
#     select_file_dialog = xbot_visual.dialog.show_select_file_dialog(
#         title=lambda: "请选择需要进行OCR的图片",  # 对话框标题
#         folder="",  # 默认文件夹为空
#         filter="所有文件|*.*",  # 文件过滤器设置为所有文件
#         is_multi=True,  # 允许多选
#         is_checked_exists=True,  # 检查文件是否存在
#         _block=("main", 8, "打开选择文件对话框")  # 日志记录块信息
#     )
#     # 获取选择的文件路径列表
#     select_file_path_list = select_file_dialog.file
# ```python
# # 打印ai_engine的字典属性（此行代码存在问题，因为ai_engine未在前文定义，可能是需要先定义ai_engine）
# xbot_visual.programing.log(type="info", text=lambda: ai_engine.__dict__, _block=("main", 10, "打印日志"))
# # 此处代码省略了循环体内的实现，可能是进行OCR识别的流程
# # workflow.forin
# # programing.log
# #endloop
# #endif
#
# # 定义Sample类
# class Sample:
#     # 初始化函数
#     def __init__(self):
#         pass
#
#     # 静态方法，创建阿里云OCR API客户端
#     @staticmethod
#     def create_client(
#             access_key_id: str,  # 阿里云账号AccessKey ID
#             access_key_secret: str,  # 阿里云账号AccessKey Secret
#     ) -> ocr_api20210707Client:
#         """
#         使用AK&SK初始化账号Client
#         @param access_key_id: 阿里云账号AccessKey ID
#         @param access_key_secret: 阿里云账号AccessKey Secret
#         @return: Client
#         @throws Exception
#         """
#         # 创建配置对象
#         config = open_api_models.Config(
#             access_key_id=access_key_id,  # 设置AccessKey ID
#             access_key_secret=access_key_secret  # 设置AccessKey Secret
#         )
#         # Endpoint 请参考 https://api.aliyun.com/product/ocr-api
#         config.endpoint = f'ocr-api.cn-hangzhou.aliyuncs.com'  # 设置服务端点
#         # 返回OCR API客户端实例
#         return ocr_api20210707Client(config)
#
#     # 静态方法，定义main函数
#     @staticmethod
#     def main(
#             args: List[str],  # 命令行参数列表
#     ) -> None:
#         """
#         主函数，执行OCR识别流程
#         @param args: 命令行参数列表
#         """
#         # 创建OCR API客户端实例，使用环境变量中的AccessKey
#         client = Sample.create_client(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'])
#         # 读取文件为流
#         body_stream = StreamClient.read_from_file_path(r'D:\Desktop\商品详情图片爬取\抖音店铺\3430145912763193664\jjtwbnYD_m_5889cbf6055c5fa543d0d16b396886fb_sx_362601_www790-1268_tplv-5mmsx3fupr-resize_790_1268.jpeg')
#         # 创建OCR识别请求对象
#         recognize_all_text_request = ocr_api_20210707_models.RecognizeAllTextRequest(
#             body=body_stream,  # 传入图片流
#             type='Commerce'  # 设置识别类型为商业
#         )
#         # 创建运行时选项对象
#         runtime = util_models.RuntimeOptions()
#         # 尝试执行OCR识别请求
#         try:
#             # 发起识别请求并获取响应
#             resp = client.recognize_all_text_with_options(recognize_all_text_request, runtime)
#             # 将响应转换为JSON字符串返回
#             return UtilClient.to_jsonstring(resp)
#         except Exception as error:
#             # 如果发生异常，打印错误信息和诊断地址
#             print(error.message)
#             print(error.data.get("Recommend"))
#             # 断言错误信息为字符串形式
#             UtilClient.assert_as_string(error.message)
#
# # 调用Sample类的main方法，并传入命令行参数
# object_test = Sample.main(sys.argv[1:])
# # 打印OCR识别的结果
# xbot_visual.programing.log(type="info", text=lambda: object_test, _block=("main", 16, "打印日志"))
#
# # 创建数据库连接
# engine = create_engine(f'mysql+pymysql://[用户名]:[密码]@域名/数据库名')
#
# # 使用SQLAlchemy执行查询
# with engine.connect() as connection:
#     # 执行查询并获取结果
#     result = connection.execute(text("SELECT * FROM feedback"))
#     # 将查询结果转换为DataFrame
#     df = pd.DataFrame(result.fetchall(), columns=result.keys())
#
# # 读取文件内容
# file_content = xbot_visual.file.read(
#     path="D:\\Desktop\\cookies_shadowbot.json",  # 文件路径
#     read_way="all_text",  # 读取方式为全文本
#     encoding="UTF-8",  # 编码方式为UTF-8
#     _block=("main", 2, "读取文件")  # 日志记录块信息
# )
#
# # 再次使用SQLAlchemy执行查询
# with engine.connect() as connection:
#     # 编写SQL查询语句
#     select_statement = text("SELECT cookies FROM douyin_shop_cookies WHERE id = 1")
#     # 执行查询
#     result = connection.execute(select_statement)
#     # 读取单条查询结果
#     file_content_select = result.fetchone()[0]
#
# # 比较两个文件内容是否相等
# is_equal = (file_content_select == file_content)
#
# # 打印比较结果
# xbot_visual.programing.log(type="info", text=lambda: is_equal, _block=("main", 4, "打印日志"))
#
# # 弹出输入对话框，提示用户输入抖音店铺的商品ID
# input_dialog = xbot_visual.dialog.show_input_dialog(
#     title="请输入抖店的商品ID",  # 对话框标题
#     label=None,  # 标签为空
#     type="multiInput",  # 输入类型为多行输入
#     value=None,  # 默认值为空
#     storage_key="17801cbf-9ba9-4b3c-86e8-de7a24641e2f",  # 存储键值
#     _block=("main", 1, "打开输入对话框")  # 日志记录块信息
# )
# # 使用正则表达式分割用户输入的商品ID字符串
# splited_list = re.split(r'\r\n|\r|\n', input_dialog.value)
#
# # 创建web browser对象，打开指定的网页
# web_page = xbot_visual.web.create(
#     web_type="cef",  # 使用cef浏览器
#     value="https://haohuo.jinritemai.com/ecommerce/trade/detail/index.html?id=3520886783468519177&origin_type=pc_compass_manage",  # 商品详情页URL
#     silent_running=False,  # 非静默运行
#     wait_load_completed=True,  # 等待页面加载完成
#     load_timeout="20",  # 加载超时设为20秒
#     stop_load_if_load_timeout="handleExcept",  # 加载超时处理方式
#     chrome_file_name=None,  # Chrome浏览器文件名
#     edge_file_name=None,  # Edge浏览器文件名
#     ie_file_name=None,  # IE浏览器文件名
#     bro360_file_name=None,  # 360浏览器文件名
#     firefox_file_name=None,  # Firefox浏览器文件名
#     arguments=None,  # 浏览器启动参数
#     _block=("main", 3, "打开网页")  # 日志记录块信息
# )
#
# # 使用Cookie登录
# xbot_visual.process.run(
#     process="xbot_extensions.cookie_login.process2",  # 指定要运行的流程
#     package=__name__,  # 当前包名
#     inputs={  # 输入参数
#         "网页对象": web_page,
#         "Cookie文件路径": "D:\\Desktop\\cookies_shadowbot.json",
#         "添加本地存储": False,
#     },
#     outputs=[  # 输出参数列表
#     ],
#     _block=("main", 4, "Cookie登录")  # 日志记录块信息
# )
#
# # 获取桌面目录路径
# dir_path = xbot_visual.dir.get_special_dir(
#     special_dir_name="DesktopDirectory",  # 指定系统特殊文件夹名
#     _block=("main", 5, "获取系统文件夹路径")  # 日志记录块信息
# )
#
# # 创建“商品详情图片爬取”文件夹
# spxq_folder = xbot_visual.dir.makedir(
#     parent=dir_path,  # 父目录路径
#     name="商品详情图片爬取",  # 文件夹名称
#     _block=("main", 6, "创建文件夹")  # 日志记录块信息
# )
#
# # 在“商品详情图片爬取”文件夹下创建“抖音店铺”文件夹
# dydp_folder = xbot_visual.dir.makedir(
#     parent=spxq_folder,  # 父目录路径
#     name="抖音店铺",  # 文件夹名称
#     _block=("main", 7, "创建文件夹")  # 日志记录块信息
# )
#
# # 等待随机时间，模拟用户操作，避免操作过快被检测为机器人
# xbot_visual.programing.sleep(
#     random_number=False,  # 是否使用随机数
#     seconds="3",  # 等待秒数
#     start_number="1",  # 随机数开始范围（不使用）
#     stop_number="5",  # 随机数结束范围（不使用）
#     _block=("main", 8, "等待")  # 日志记录块信息
# )
#
# # 循环处理用户输入的每一个商品ID
# for id_index, id_item in enumerate(xbot_visual.workflow.list_iterator(
#         list=lambda: splited_list,  # 用户输入的商品ID列表
#         loop_start_index="0",  # 循环起始索引
#         loop_end_index="-1",  # 循环结束索引
#         output_with_index=True,  # 输出循环索引
#         _block=("main", 9, "ForEach列表循环")
#         # 日志记录块信息
# )):
#     # 为每个商品ID创建对应的文件夹
#     temp_id_folder = xbot_visual.dir.makedir(
#         parent=dydp_folder,  # 父目录为之前创建的“抖音店铺”文件夹
#         name=id_item,  # 文件夹名称为商品ID
#         _block=("main", 10, "创建文件夹")  # 日志记录块信息
#     )
#     # 打印当前循环的索引
#     xbot_visual.programing.log(
#         type="info",
#         text=id_index,
#         _block=("main", 11, "打印日志")
#     )
#     # 构建商品详情页的URL
#     curr_url = f"https://haohuo.jinritemai.com/ecommerce/trade/detail/index.html?id={id_item}&origin_type=pc_compass_manage"
#     # 使用浏览器自动化打开商品详情页
#     web_page = xbot_visual.web.create(
#         web_type="cef",  # 使用cef浏览器
#         value=lambda: curr_url,  # 浏览器打开的URL
#         silent_running=False,
#         wait_load_completed=True,
#         load_timeout="20",
#         stop_load_if_load_timeout="handleExcept",
#         chrome_file_name=None,
#         edge_file_name=None,
#         ie_file_name=None,
#         bro360_file_name=None,
#         firefox_file_name=None,
#         arguments=None,
#         _block=("main", 13, "打开网页")
#     )
#     # 获取网页中的元素对象，这里假设是商品图片的容器
#     web_element_parent = xbot_visual.web.element.get_element(
#         browser=web_page,
#         select_type="xpath_selector",
#         selector=None,
#         css_selector="",
#         xpath_selector="//*[@class=\"partial-detail-wrapper\"]/div[1]",
#         is_related_parent=False,
#         parent=None,
#         timeout="20",
#         _block=("main", 14, "获取元素对象(web)")
#     )
#     # 获取商品图片的容器中所有图片元素
#     web_element_list = xbot_visual.web.element.get_associated_elements(
#         browser=web_page,
#         element=web_element_parent,
#         associated_kind="child",
#         child_access_kind="all",
#         child_index="0",
#         sibling_direction="next",
#         timeout="20",
#         _block=("main", 15, "获取关联元素(web)")
#     )
#     # 打印当前处理的商品ID
#     xbot_visual.programing.log(
#         type="info",
#         text=id_item,
#         _block=("main", 16, "打印日志")
#     )
#     # 循环下载图片元素指向的图片
#     for loop_index in xbot_visual.workflow.range_iterator(
#             start="0",
#             stop=lambda: len(web_element_list)-1,
#             step="1",
#             _block=("main", 17, "For次数循环")
#     ):
#         # 获取单个图片元素
#         web_element = xbot_visual.web.element.get_associated_elements(
#             browser=web_page,
#             element=web_element_parent,
#             associated_kind="child",
#             child_access_kind="index",
#             child_index=lambda: loop_index,
#             sibling_direction="next",
#             timeout="20",
#             _block=("main", 18, "获取关联元素(web)")
#         )
#         # 获取图片元素的src属性，即图片的URL
#         web_element_attribute = xbot_visual.web.element.get_details(
#             browser=web_page,
#             element=web_element,
#             operation="other",
#             absolute_url=False,
#             attribute_name="src",
#             relative_to="screen",
#             to96dpi=True,
#             timeout="20",
#             _block=("main", 19, "获取元素信息(web)")
#         )
#         # 打印图片索引和URL
#         xbot_visual.programing.log(
#             type="info",
#             text=loop_index,
#             _block=("main", 20, "打印日志")
#         )
#         xbot_visual.programing.log(
#             type="info",
#             text=web_element_attribute,
#             _block=("main", 21, "打印日志")
#         )
#         # 下载图片到本地指定文件夹
#         download_file_name2 = xbot_visual.web.element.download(
#             browser=web_page,
#             scene="Url",
#             download_button=None,
#             download_url=web_element_attribute,
#             file_folder=temp_id_folder,
#             use_custom_filename=False,
#             file_name="",
#             wait_complete=True,
#             wait_complete_timeout="300",
#             simulate=False,
#             clipboard_input=False,
#             input_type="automatic",
#             wait_dialog_appear_timeout="20",
#             force_ime_ENG=False,
#             send_key_delay="50",
#             focus_timeout="1000",
#             _block=("main", 22, "下载文件")
#         )
#     # 结束图片下载的循环
#     #endloop
#     # 暂停一定的时间后继续执行，模拟人的操作
#     xbot_visual.programing.sleep(
#         random_number=False,
#         seconds="1",
#         start_number="1",
#         stop_number="5",
#         _block=("main", 24, "等待")
#     )
#     # 关闭当前打开的浏览器页面
#     xbot_visual.web.browser.close(
#         operation="close_specified",
#         browser=web_page,
#         web_type="cef",
#         task_kill=False,
#         _block=("main", 25, "关闭网页")
#     )
# # 结束对商品ID列表的循环
# #endloop
#
# # 以下是另一个独立的部分，看起来是为了再次执行一些操作，但是没有足够的上下文来确定它和上面代码的关系
# # 弹出输入对话框，提示用户输入抖音店铺的商品ID
# input_dialog = xbot_visual.dialog.show_input_dialog(
#     title="请输入抖店的商品ID",  # 对话框标题
#     label=None,  # 标签为空
#     type="multiInput",  # 输入类型为多行输入
#     value=None,  # 默认值为空
#     storage_key="17801cbf-9ba9-4b3c-86e8-de7a24641e2f",  # 存储键值
#     _block=("main", 1, "打开输入对话框")  # 日志记录块信息
# )
# # 使用正则表达式切分输入的商品ID
# splited_list = re.split(r'\r\n|\r|\n', input_dialog.value)
#
# # 以下代码看起来是重复的，可能是为了处理不同的商品ID或是从另一个地方复制粘贴而未删除的
# # 因为它和上面的代码几乎完全相同
#
# # ...
# # 此处省略了重复的代码部分
# # ...
#
# # 调用xbot_visual.process.run来运行OCR识别流程
# OCR识别结果 = xbot_visual.process.run(
#     process="xbot_extensions.activity_179ea575.process1",  # 指定要运行的流程
#     package=__name__,  # 当前包名
#     inputs={  # 输入参数
#         "图片路径或图片url": "D:\\Desktop\\jjtwbnYD_m_a65cc55b0a5c730e7dd121a970ff63a7_sx_431434_www790-1147~tplv-5mmsx3fupr-resize_790_1147.jpeg",
#         "输出完整结果": False,
#         "文字检测框过滤的阈值": lambda: 0.1,
#         "文字检测框的大小": lambda: 200,
#     },
#     outputs=[  # 输出参数列表
#         "OCR识别结果",
#     ],
#     _block=("main", 27, "影刀离线OCR")  # 日志记录块信息
# )
# # 打印OCR识别结果
# xbot_visual.programing.log(
#     type="info",
#     text=OCR识别结果,
#     _block=("main", 28, "打印日志")
# )