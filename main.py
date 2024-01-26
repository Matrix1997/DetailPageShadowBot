# 标准库导入
import os
import re
import sys
import time
from typing import List

# 第三方库导入
import pandas as pd
from alibabacloud_darabonba_stream.client import Client as StreamClient
from alibabacloud_ocr_api20210707.client import Client as ocr_api20210707Client
from alibabacloud_ocr_api20210707 import models as ocr_api_20210707_models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_tea_util import models as util_models
from sqlalchemy import create_engine, text
from typing import List

# 本地应用/库导入
from . import package
from .package import variables as glv
import xbot
import xbot_visual


def main(args):
    try:
        # 设置单个商品爬取休眠时间常量（秒）
        sleep_sec = 3

        # 重写print方法，用来在shadowbot里打印日志
        def print(str_item):
            xbot_visual.programing.log(type="info", text=lambda: str_item, _block=("main", 1, "打印日志"))

        # 校验并分割字符串，输出商品id列表
        def process_input_ids(input_value):
            # 检查输入是否为非空字符串
            if not input_value.strip():
                print("输入不能为空")
                raise ValueError("输入不能为空")

            # 使用正则表达式分割用户输入的商品ID字符串
            id_list = re.split(r'\r\n|\r|\n', input_value)

            # 清洗和验证ID列表
            cleaned_ids = []
            for id in id_list:
                id = id.strip()
                if not id.isdigit():
                    print(f"ID '{id}' 不是一个纯数字字符串")
                    raise ValueError(f"ID '{id}' 不是一个纯数字字符串")
                cleaned_ids.append(id)

            # 检查是否至少有一个有效ID
            if not cleaned_ids:
                print("至少需要一个有效的商品ID")
                raise ValueError("至少需要一个有效的商品ID")

            return cleaned_ids

        # 调用阿里云接口进行OCR识别
        class OCRRecognizer:
            # Usage example:
            # recognizer = OCRRecognizer()
            # result = recognizer.recognize_image_from_path('path_to_image', [])
            # To run the test method:
            # OCRRecognizer.test_recognize_image_from_path()
            def __init__(self):
                pass

            @staticmethod
            def create_ocr_client(
                    access_key_id: str,
                    access_key_secret: str,
            ) -> ocr_api20210707Client:
                """
                Initialize the Aliyun OCR API client using Access Key and Secret Key.
                @param access_key_id: Aliyun AccessKey ID
                @param access_key_secret: Aliyun AccessKey Secret
                @return: Initialized OCR client
                @throws Exception
                """
                config = open_api_models.Config(
                    access_key_id=access_key_id,
                    access_key_secret=access_key_secret
                )
                config.endpoint = 'ocr-api.cn-hangzhou.aliyuncs.com'
                return ocr_api20210707Client(config)

            @staticmethod
            def recognize_image_from_path(
                    image_path: str,  # Path to the image file
                    args: List[str],  # Command line arguments list (if any)
            ) -> None:
                """
                Main function to perform OCR on a specific image from the given path.
                @param image_path: Path to the image file to be recognized
                @param args: Command line arguments list (if any)
                """
                client = OCRRecognizer.create_ocr_client(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'])
                body_stream = open(image_path, 'rb').read()  # Read the file content in binary mode
                recognize_text_request = ocr_api_20210707_models.RecognizeAllTextRequest(
                    body=body_stream,
                    type='Commerce'
                )
                runtime = util_models.RuntimeOptions()
                try:
                    response = client.recognize_all_text_with_options(recognize_text_request, runtime)
                    return UtilClient.to_jsonstring(response)
                except Exception as error:
                    print(error.message)
                    if 'Recommend' in error.data:
                        print(error.data.get("Recommend"))
                    UtilClient.assert_as_string(error.message)

            @staticmethod
            def test_recognize_image_from_path():
                """
                Test method to perform OCR on a hardcoded specific image path.
                """
                image_path = r'D:\Desktop\商品详情图片爬取\抖音店铺\3430145912763193664\jjtwbnYD_m_5889cbf6055c5fa543d0d16b396886fb_sx_362601_www790-1268_tplv-5mmsx3fupr-resize_790_1268.jpeg'
                recognizer = OCRRecognizer()
                result = recognizer.recognize_image_from_path(image_path, [])

                # Assuming xbot_visual.programing.log is a provided logging function:
                xbot_visual.programing.log(type="info", text=lambda: result, _block=("main", 16, "打印日志"))

        # 弹出选择对话框，让用户选择操作
        select_dialog = xbot_visual.dialog.show_select_dialog(
            title=None,  # 对话框标题
            label=None,  # 对话框标签
            select_type="list",  # 选择类型为列表
            select_model="single",  # 选择模式为单选
            values=lambda: ["商品详情页图片爬取", "OCR识别"],  # 提供给用户的选项
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

            # 弹出输入对话框，提示用户输入抖音店铺的商品ID
            input_dialog = xbot_visual.dialog.show_input_dialog(
                title="请输入抖店的商品ID，每行一个",  # 对话框标题
                label=None,  # 标签为空
                type="multiInput",  # 输入类型为多行输入
                value=None,  # 默认值为空
                storage_key="17801cbf-9ba9-4b3c-86e8-de7a24641e2f",  # 存储键值
                _block=("main", 1, "打开输入对话框")  # 日志记录块信息
            )
            try:
                processed_ids = process_input_ids(input_dialog.value)
                print(processed_ids)
            except:
                raise

            # 读取环境变量
            database_url = os.environ["DATABASE_URL"]
            engine = create_engine(database_url)
            # 再次使用SQLAlchemy执行查询
            with engine.connect() as connection:
                # 编写SQL查询语句
                douyin_shop_cookies_select_statement = text("SELECT cookies FROM douyin_shop_cookies WHERE id = 1")
                # 执行查询
                result = connection.execute(douyin_shop_cookies_select_statement)
                # 读取单条查询结果
                douyin_shop_cookies = result.fetchone()[0]

            # 更新本地的cookies文件
            # 获取当前文件所在的目录
            current_directory = os.path.dirname(__file__)
            # 构建 cookies_dy_shop.json 的完整路径
            cookies_file_path = os.path.join(current_directory, 'cookies_dy_shop.json')
            with open(cookies_file_path, "w", encoding="utf-8") as f:
                f.write(douyin_shop_cookies)

            print("成功获取最新版本cookies")

            print("正在打开抖音店铺商详页并导入cookies")
            # 创建web browser对象，打开指定的网页
            web_page = xbot_visual.web.create(
                web_type="cef",  # 使用cef浏览器
                value="https://haohuo.jinritemai.com/ecommerce/trade/detail/index.html?id=3520886783468519177&origin_type=pc_compass_manage",  # 商品详情页URL
                silent_running=False,  # 非静默运行
                wait_load_completed=True,  # 等待页面加载完成
                load_timeout="20",  # 加载超时设为20秒
                stop_load_if_load_timeout="handleExcept",  # 加载超时处理方式
                chrome_file_name=None,  # Chrome浏览器文件名
                edge_file_name=None,  # Edge浏览器文件名
                ie_file_name=None,  # IE浏览器文件名
                bro360_file_name=None,  # 360浏览器文件名
                firefox_file_name=None,  # Firefox浏览器文件名
                arguments=None,  # 浏览器启动参数
                _block=("main", 3, "打开网页")  # 日志记录块信息
            )
            # 使用Cookie登录
            xbot_visual.process.run(
                process="xbot_extensions.cookie_login.process2",  # 指定要运行的流程
                package=__name__,  # 当前包名
                inputs={  # 输入参数
                    "网页对象": web_page,
                    "Cookie文件路径": cookies_file_path,
                    "添加本地存储": False,
                },
                outputs=[  # 输出参数列表
                ],
                _block=("main", 4, "Cookie登录")  # 日志记录块信息
            )
            print("cookies导入成功")

            # 获取桌面目录路径
            desktop_dir_path = xbot_visual.dir.get_special_dir(
                special_dir_name="DesktopDirectory",  # 指定系统特殊文件夹名
                _block=("main", 5, "获取系统文件夹路径")  # 日志记录块信息
            )
            # 创建“商品详情图片爬取”文件夹（一级目录）
            desktop_spxq_folder = xbot_visual.dir.makedir(
                parent=desktop_dir_path,  # 父目录路径
                name="商品详情图片爬取",  # 文件夹名称
                _block=("main", 6, "创建文件夹")  # 日志记录块信息
            )
            # 在“商品详情图片爬取”文件夹下创建“抖音店铺”文件夹（二级目录）
            desktop_spxq_dydp_folder = xbot_visual.dir.makedir(
                parent=desktop_spxq_folder,  # 父目录路径
                name="抖音店铺",  # 文件夹名称
                _block=("main", 7, "创建文件夹")  # 日志记录块信息
            )
            # 等待随机时间，模拟用户操作，避免操作过快被检测为机器人
            xbot_visual.programing.sleep(
                random_number=False,  # 是否使用随机数
                seconds=str(sleep_sec),  # 等待秒数
                start_number="1",  # 随机数开始范围（不使用）
                stop_number="5",  # 随机数结束范围（不使用）
                _block=("main", 8, "等待")  # 日志记录块信息
            )
            # 首先打印总的商品ID个数
            total_ids = len(processed_ids)
            print(f"总共需要爬取 {total_ids} 个商品ID。")
            # 循环处理用户输入的每一个商品ID
            for id_index, id_item in enumerate(xbot_visual.workflow.list_iterator(
                    list=lambda: processed_ids,  # 用户输入的商品ID列表
                    loop_start_index="0",  # 循环起始索引
                    loop_end_index="-1",  # 循环结束索引
                    output_with_index=True,  # 输出循环索引
                    _block=("main", 9, "ForEach列表循环")
                    # 日志记录块信息
            )):
                # 为每个商品ID创建对应的文件夹
                curr_id_folder = xbot_visual.dir.makedir(
                    parent=desktop_spxq_dydp_folder,  # 父目录为之前创建的“抖音店铺”文件夹
                    name=id_item,  # 文件夹名称为商品ID
                    _block=("main", 10, "创建文件夹")  # 日志记录块信息
                )
                # 打印当前的爬取进度
                print(f"正在爬取第 {id_index + 1} 个商品ID: {id_item} (共 {total_ids} 个)")

                # 构建商品详情页的URL
                curr_url = f"https://haohuo.jinritemai.com/ecommerce/trade/detail/index.html?id={id_item}&origin_type=pc_compass_manage"
                # 使用浏览器自动化打开商品详情页
                web_page = xbot_visual.web.create(
                    web_type="cef",  # 使用cef浏览器
                    value=lambda: curr_url,  # 浏览器打开的URL
                    silent_running=False,
                    wait_load_completed=True,
                    load_timeout="20",
                    stop_load_if_load_timeout="handleExcept",
                    chrome_file_name=None,
                    edge_file_name=None,
                    ie_file_name=None,
                    bro360_file_name=None,
                    firefox_file_name=None,
                    arguments=None,
                    _block=("main", 13, "打开网页")
                )
                # 获取网页中的元素对象，这里假设是商品图片的容器
                web_element_parent = xbot_visual.web.element.get_element(
                    browser=web_page,
                    select_type="xpath_selector",
                    selector=None,
                    css_selector="",
                    xpath_selector="//*[@class=\"partial-detail-wrapper\"]/div[1]",
                    is_related_parent=False,
                    parent=None,
                    timeout="20",
                    _block=("main", 14, "获取元素对象(web)")
                )
                # 获取商品图片的容器中所有图片元素
                web_element_list = xbot_visual.web.element.get_associated_elements(
                    browser=web_page,
                    element=web_element_parent,
                    associated_kind="child",
                    child_access_kind="all",
                    child_index="0",
                    sibling_direction="next",
                    timeout="20",
                    _block=("main", 15, "获取关联元素(web)")
                )
                # 循环下载图片元素指向的图片
                for loop_index in xbot_visual.workflow.range_iterator(
                        start="0",
                        stop=lambda: len(web_element_list)-1,
                        step="1",
                        _block=("main", 17, "For次数循环")
                ):
                    # 获取单个图片元素
                    web_element = xbot_visual.web.element.get_associated_elements(
                        browser=web_page,
                        element=web_element_parent,
                        associated_kind="child",
                        child_access_kind="index",
                        child_index=lambda: loop_index,
                        sibling_direction="next",
                        timeout="20",
                        _block=("main", 18, "获取关联元素(web)")
                    )
                    # 获取图片元素的src属性，即图片的URL
                    web_element_attribute = xbot_visual.web.element.get_details(
                        browser=web_page,
                        element=web_element,
                        operation="other",
                        absolute_url=False,
                        attribute_name="src",
                        relative_to="screen",
                        to96dpi=True,
                        timeout="20",
                        _block=("main", 19, "获取元素信息(web)")
                    )
                    # 下载图片到本地指定文件夹
                    curr_download_image_full_path = xbot_visual.web.element.download(
                        browser=web_page,
                        scene="Url",
                        download_button=None,
                        download_url=web_element_attribute,
                        file_folder=curr_id_folder,
                        use_custom_filename=False,
                        file_name="",
                        wait_complete=True,
                        wait_complete_timeout="300",
                        simulate=False,
                        clipboard_input=False,
                        input_type="automatic",
                        wait_dialog_appear_timeout="20",
                        force_ime_ENG=False,
                        send_key_delay="50",
                        focus_timeout="1000",
                        _block=("main", 22, "下载文件")
                    )
                # 结束图片下载的循环
                #endloop
                # 暂停一定的时间后继续执行，模拟人的操作
                xbot_visual.programing.sleep(
                    random_number=False,
                    seconds="1",
                    start_number="1",
                    stop_number="5",
                    _block=("main", 24, "等待")
                )
                # 关闭当前打开的浏览器页面
                xbot_visual.web.browser.close(
                    operation="close_specified",
                    browser=web_page,
                    web_type="cef",
                    task_kill=False,
                    _block=("main", 25, "关闭网页")
                )
            # 结束对商品ID列表的循环
            #endloop

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

        #     # _________________________________________________________________________________________________________
        #     # _________________________________________________________________________________________________________
        #     # _________________________________________________________________________________________________________
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
    finally:
        pass
