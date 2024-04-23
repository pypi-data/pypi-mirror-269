# -*- coding: utf-8 -*-
import os
import re
import time
from pathlib import Path
from datetime import datetime

import requests
import json
import ast
from binascii import b2a_hex
from typing import Dict, List, Union, Any

from knext.builder.operator import (
    ExtractOp,
    SPGRecord,
    PromptOp,
    OneKE_KGPrompt,
    OneKE_EEPrompt, EEPrompt, REPrompt,
)
from knext.builder.operator.sub_graph import SubGraph
from knext.schema.client import SchemaClient
from knext.schema.marklang.schema_ml import SPGSchemaMarkLang
from knext.schema.model.base import SpgTypeEnum

# from knext.common import arks_pb2
from Crypto.Cipher import AES

PWD = os.path.dirname(__file__)


class SchemaPrompt(PromptOp):
    template: str = """
你是知识图谱领域的建模专家，从下述文本中整理出相关的schema（包括事件类型EventType和实体类型EntityType），schema类型尽量丰富，且尽量多的定义出实体和实体、事件和实体之间的依赖关系。
文本：
${input}
输出格式要求：
1. 不需要返回额外说明和注释
2. 基本属性类型只允许为Text
3. 事件类型的主体和客体必须为已经定义的实体类型，并且事件类型必须定义subject(主体)属性
4. 注意缩进，实体/事件类型定义在第一层缩进，属性/关系定义在第三层缩进
5. 使用constraint: MultiValue表示属性支持多值。
6. 属性英文名必须定义为驼峰式，不允许包括下划线
输出示例：
Company(公司): EntityType
    properties:
        alias(别名): Text
        address(地址): Text
Person(人物): EntityType
    properties:
        alias(别名): Text
        workAt(就职于): Company
FiredEvent(公司解雇事件): EventType
    properties:
        subject(主体): Company
        object(客体): Person
            constraint: MultiValue
        eventTime(发生时间): Text
"""

    def build_prompt(self, variables: Dict[str, str]) -> str:
        return self.template.replace("${input}", variables.get("input"))


class AntGPTClient(object):
    def __init__(self, config: Union[str, dict]):
        if isinstance(config, str) and Path(config).is_file():
            with open(config, "r") as f:
                self.nn_config = json.load(f)
        else:
            self.nn_config = config

        self.param = {k: v for k, v in self.nn_config.items()}
        self.url = self.param.pop("url")
        self.api_key = self.param.pop("apiKey")
        self.key = self.param.pop("key")
        self.model = self.param.pop("model")
        self.temperature = self.param.pop("temperature")
        self.max_tokens = self.param.pop("maxToken")
        self.n = self.param.pop("n")

        self.service_names = {
            "sync": "chatgpt_prompts_completions_query_dataview",
            "async": "asyn_chatgpt_prompts_completions_query_dataview",
            "query": "chatgpt_response_query_dataview",
        }

    def aes_encrypt(self, data):
        """aes加密函数，如果data不是16的倍数【加密文本data必须为16的倍数！】，那就补足为16的倍数
        :param key:
        :param data:
        """
        # print(len(iv.encode('utf-8')))
        iv = "1234567890123456"
        cipher = AES.new(
            self.key.encode("utf-8"), AES.MODE_CBC, iv.encode("utf-8")
        )  # 设置AES加密模式 此处设置为CBC模式
        block_size = AES.block_size

        # 判断data是不是16的倍数，如果不是用b'\0'补足
        if len(data) % block_size != 0:
            add = block_size - (len(data) % block_size)
        else:
            add = 0
        data = data.encode("utf-8") + b"\0" * add
        encrypted = cipher.encrypt(data)  # aes加密
        result = b2a_hex(encrypted)  # b2a_hex encode  将二进制转换成16进制
        return result.decode("utf-8")

    def sync_request(self, prompt):
        # import pdb; pdb.set_trace()
        encodeurl = "%s" % self.url.encode("utf8")

        self.param["serviceName"] = self.service_names["sync"]
        self.param["queryConditions"] = {
            "url": encodeurl,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "n": self.n,
            "api_key": self.api_key,
            "messages": prompt,
        }
        data = json.dumps(self.param)
        post_data = {"encryptedParam": self.aes_encrypt(data)}
        response = requests.post(
            self.url,
            data=json.dumps(post_data),
            headers={"Content-Type": "application/json"},
        )
        print(response.json())
        x = response.json()["data"]["values"]["data"]
        ast_str = ast.literal_eval("'" + x + "'")
        js = ast_str.replace("&quot;", '"')
        js = js.replace("&#39;", "'")
        data = json.loads(js)
        content = data["choices"][0]["message"]["content"]
        content = content.replace("&rdquo;", "”").replace("&ldquo;", "“")
        content = content.replace("&middot;", "")
        print(content)
        return content

    def async_request(self, prompt, message_key):
        # import pdb; pdb.set_trace()
        encodeurl = "%s" % self.url.encode("utf8")
        self.param["serviceName"] = self.service_names["async"]
        self.param["queryConditions"] = {
            "url": encodeurl,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "n": self.n,
            "api_key": self.api_key,
            "messages": prompt,
            "messageKey": message_key,
            "outputType": "PULL",
        }
        data = json.dumps(self.param)
        post_data = {"encryptedParam": self.aes_encrypt(data)}
        response = requests.post(
            self.url,
            data=json.dumps(post_data),
            headers={"Content-Type": "application/json"},
        )
        return response

    def query_async_response(self, message_key, interval=5, timeout=120):
        self.param["serviceName"] = self.service_names["query"]
        self.param["queryConditions"] = {
            "messageKey": message_key,
        }
        data = json.dumps(self.param)
        post_data = {"encryptedParam": self.aes_encrypt(data)}

        start_time = time.time()
        count = 1
        while True:
            print(f"{count} attempts to query asynchronous gpt_client response...")
            response = requests.post(
                self.url,
                data=json.dumps(post_data),
                headers={"Content-Type": "application/json"},
            )
            values = response.json()["data"]["values"]
            if values:
                print(response.json())
                x = response.json()["data"]["values"]["response"]
                ast_str = ast.literal_eval("'" + x + "'")
                js = ast_str.replace("&quot;", '"')
                js = js.replace("&#39;", "'")
                data = json.loads(js)
                content = data["choices"][0]["message"]["content"]
                content = content.replace("&rdquo;", "”").replace("&ldquo;", "“")
                return content

            if time.time() - start_time > timeout:
                raise TimeoutError(f"Polling timed out, exceeding {timeout} seconds.")
            time.sleep(interval)
            count += 1

    def __call__(self, prompt):
        return self.sync_request(prompt)

    def mock_response(self):
        return """
Person(人物): EntityType
    properties:
        name(姓名): Text
        birthDate(出生日期): Text
        birthPlace(出生地): Text
        graduateFrom(毕业学校): Text
        ancestorPlace(祖籍): Text
        professions(职业): Text
            constraint: MultiValue

Album(音乐专辑): EntityType
    properties:
        name(名称): Text
        releaseDate(发行日期): Text
        artist(艺术家): Person

Concert(巡回演唱会): EntityType
    properties:
        name(名称): Text
        startDate(开始日期): Text

Award(奖项): EntityType
    properties:
        name(名称): Text
        relevancePerson(相关人物): Person

Movie(电影): EntityType
    properties:
        name(名称): Text
        actors(演员): Person
            constraint: MultiValue

Company(公司): EntityType
    properties:
        name(名称): Text
        founder(创始人): Person

ReleaseAlbumEvent(发布音乐专辑事件): EventType
    properties:
        subject(主体): Person
        object(客体): Album
        eventTime(发生时间): Text

WinAwardEvent(获奖事件): EventType
    properties:
        subject(主体): Person
        object(客体): Award
        eventTime(发生时间): Text

ConcertEvent(演唱会事件): EventType
    properties:
        subject(主体): Person
        object(客体): Concert
        eventTime(发生时间): Text

ActingEvent(演戏事件): EventType
    properties:
        subject(主体): Person
        object(客体): Movie
        eventTime(发生时间): Text

FoundCompanyEvent(创建公司事件): EventType
    properties:
        subject(主体): Person
        object(客体): Company
        eventTime(发生时间): Text        
        """


class MayaHttpClient(object):
    """
    通过http服务访问MAYA服务
    不支持Batch调用, features需为Dict
    """

    def __init__(
            self,
            scene_name,
            chain_name="v1",
            use_pre=False,
    ):
        """

        Args:
            scene_name: 所部署的服务的名字
            chain_name: 所部署的服务的版本
            use_pre: 是否调用预发环境服务
        """
        self.service_name = scene_name
        self.chain_name = chain_name
        self.query_service_id_token = "d9d0dd30-2c86-4329-8317-33cb617c184d"
        self.query_service_id_url = 'https://aistudio.alipay.com/api/v1/mpsMayaService/queryModelService'
        self.model_service_id = self.get_service_id_by_service_name()
        self.client_headers = {
            "Content-Type": "application/json;charset=utf-8",
            "MPS-app-name": "test",
            "MPS-http-version": "1.0",
            "MPS-debug": "true",
        }
        if use_pre:
            self.client_url = f"https://paiplusinferencepre.alipay.com/inference/{self.model_service_id}/{self.chain_name}"
        else:
            self.client_url = f"https://paiplusinference.alipay.com/inference/{self.model_service_id}/{self.chain_name}"

    def get_service_id_by_service_name(self):
        # 通过service name查询service id
        params = {"sceneName": self.service_name, "token": self.query_service_id_token}
        result = requests.post(self.query_service_id_url, json=params)
        if result.status_code == 200:
            model_service_id = result.json()['data'][0]['modelServiceId']
            # logger.info(f'get_service_id_by_service_name succeed: {model_service_id}')
            return model_service_id
        else:
            raise RuntimeError(f'get_service_id_by_service_name Error: {json.dumps(result.json(), indent=4)}')

    def call_service(self, prompt: Dict, debug=False, keep_origin_features=False):
        """
        args:
            features: 进行预测的特征, 应为一个Dict, 当传入List时仅使用features[0]进行预测服务
            debug: 是否打印日志
            keep_origin_features: 是否保留原始特质, 即不进行in_string/out_string封装
        """
        if isinstance(prompt, List):
            features = prompt[0]
            # logger.warning(f"MayaHttpClient.call_service 'features' should be a Dict, but get List. "
            #                "call_service use features[0]")
        elif isinstance(prompt, str):
            features = {"message": prompt}
        else:
            features = prompt
        if self.model_service_id:
            if keep_origin_features:
                input_dict = {"features": features}
            else:
                in_string = json.dumps(features, ensure_ascii=False)
                input_dict = {"features": {'in_string': in_string}}
            if debug:
                # logger.info(
                #     f"================= request =================\n"
                #     f"{input_dict}\n"
                #     f"================= request end ================="
                # )
                pass
            r = requests.post(self.client_url, json=input_dict, headers=self.client_headers)
            if debug:
                pass
                # logger.info(
                #     f'================= response =================\n'
                #     f'{json.dumps(r.json(), indent=4)}\n'
                #     f'================= response end ================='
                # )
            if r.status_code == 200:
                if r.json()['success']:
                    if keep_origin_features:
                        result = r.json()['resultMap']
                        return result
                    else:
                        result = r.json()['resultMap']['out_string']
                        json_result = json.loads(result)
                        return json_result
                else:
                    raise RuntimeError(f'Call Service Failed. \n{json.dumps(r.json(), indent=4)}')
            else:
                raise RuntimeError(f'Call {self.model_service_id} failed. Error: {json.dumps(r.json(), indent=4)}')
        else:
            raise RuntimeError(f'Service {self.service_name} client create failed. Try to create maya client later')

    def update_fn(self, pre_process_fn=None, post_process_fn=None):
        import inspect
        input_dict = {
            'update_user_handler': True,
        }
        if pre_process_fn:
            input_dict['preprocess_code'] = inspect.getsource(pre_process_fn)
        if post_process_fn:
            input_dict['postprocess_code'] = inspect.getsource(post_process_fn)
        return self.call_service(input_dict)

    def mock_ae_response(self):
        return [' {"巡回演唱会": {"周杰伦": {"开始日期": "2002年"}}}', ' {"音乐专辑": {"周杰伦": {}, "Jay": {"发行日期": "2000年"}, "范特西": {}, "叶惠美": {}, "七里香": {}, "魔杰座": {}, "跨时代": {}}}', ' {"电影": {"周杰伦": {}, "头文字D": {"演员": "周杰伦"}, "不能说的秘密": {"演员": "周杰伦"}}}', ' {"人物": {"周杰伦": {"毕业学校": "淡江中学", "祖籍": "福建省永春县", "出生地": "台湾省新北市", "职业": ["华语流行乐男歌手", "音乐人", "演员", "导演", "编剧"], "出生日期": "1979年1月18日"}}}', ' {"公司": {"周杰伦": {}, "杰威尔音乐有限公司": {}}}', ' {"奖项": {"周杰伦": {}, "叶惠美": {"奖项": "台湾金曲奖最佳流行音乐演唱专辑奖"}, "周杰伦": {}, "七里香": {"奖项": "世界音乐大奖中国区最畅销艺人奖"}, "头文字D": {"奖项": "香港电影金像奖和第42届台湾电影金马奖的最佳新演员奖"}, "不能说的秘密": {"奖项": "台湾金曲奖最佳作曲人奖"}, "魔杰座": {"奖项": "台湾金曲奖最佳国语男歌手奖"}, "跨时代": {"奖项": "台湾金曲奖最佳国语男歌手奖"}}}']


    def mock_ee_response(self):
        return [' {"演戏事件": []}', ' {"发布音乐专辑事件": [{"trigger": "发行", "arguments": {"客体": "音乐专辑", "发生时间": "2000年", "主体": "周杰伦"}}, {"trigger": "发行", "arguments": {"客体": "音乐专辑", "发生时间": "2003年", "主体": "周杰伦"}}, {"trigger": "发行", "arguments": {"客体": "音乐专辑", "发生时间": "2004年", "主体": "周杰伦"}}, {"trigger": "发行", "arguments": {"客体": "音乐专辑", "发生时间": "2014年", "主体": "周杰伦"}}, {"trigger": "发行", "arguments": {"客体": "音乐专辑", "发生时间": "2023年", "主体": "周杰伦"}}]}', ' {"演唱会事件": [{"trigger": "演唱会", "arguments": {"客体": "NAN", "发生时间": "2002年", "主体": "周杰伦"}}]}', ' {"创建公司事件": [{"trigger": "成立", "arguments": {"客体": "杰威尔音乐有限公司", "发生时间": "2007年", "主体": "周杰伦"}}]}']


class LLMClient(object):
    def __init__(self, config: Union[str, dict]):
        if isinstance(config, str) and Path(config).is_file():
            with open(config, "r") as f:
                self.nn_config = json.load(f)
        else:
            self.nn_config = config

        self.param = {k: v for k, v in self.nn_config.items()}
        self.url = self.param.pop("url")
        self.temperature = self.param.pop("temperature", 0)
        self.max_tokens = self.param.pop("max_tokens", 4096)
        self.stream = self.param.pop("stream", False)

    def call_service(self, prompt):
        data = {
            'text_input': prompt,
            'parameters': {
                'stream': self.stream,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens,
            }
        }

        response = requests.post(
            url=self.url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )

        if response.status_code == 200:
            response_result = response.json()['text_output']
            response_result = response_result.replace(prompt, '')
            newline_pos = response_result.find('\n')
            if newline_pos != -1:
                return response_result[newline_pos + 1:]
            else:
                return response_result
        else:
            return (f'Error: {response.status_code} - {response.text}')


class AutoSchemaBuilder(ExtractOp):
    def __init__(self, params: Dict[str, str] = None):
        super().__init__()
        self.gpt_client = AntGPTClient(config=os.path.join(PWD, "gpt4.json"))
        # self.extract_client = LLMClient(config=os.path.join(PWD, "humming.json"))
        self.extract_client = MayaHttpClient(
            scene_name="knowlm_ie_full_v2",
            chain_name="v1",
            use_pre=True,
        )
        self.extract_client2 = AntGPTClient(config=os.path.join(PWD, "gpt3_5.json"))
        self.max_retry_times = 3
        self.namespace = params.get("namespace", "DEFAULT") if params else "DEFAULT"
        self.project_id = params.get("project_id", 1) if params else 1
        # instruction = params.get("instruction", "帮我基于以上文本建模，humming抽取数据，并使用gpt补充")
        self.schema_build = True
        self.humming_extract = True
        self.gpt_extract = True
        os.environ["KNEXT_PROJECT_ID"] = str(self.project_id)

    def remove_punctuation(self, text: str) -> str:
        brackets_pattern = r"\([^\)]*\)"

        matches = re.findall(brackets_pattern, text)

        for match in matches:
            cleaned_match = re.sub(r"[\.,;:\'\"!?/、-]", "", match)
            text = text.replace(match, cleaned_match)
        return text

    def format_line(self, line):
        pattern = r"([\u4e00-\u9fa5]+)\(([A-Za-z\s]+)\)"

        def swap_cn_en(match):
            chinese = match.group(1)
            english = match.group(2)
            return f"{english}({chinese})"

        line = re.sub(pattern, swap_cn_en, line)
        if all(i not in line for i in ["EntityType", "EventType"]):
            pattern = r"([A-Za-z])[A-Za-z]*\([^\)]*\)"

            def replace_first_letter(match):
                first_letter_lower = match.group(1).lower()
                return first_letter_lower + match.group(0)[1:]

            line = re.sub(pattern, replace_first_letter, line)
        return line

    def print_logs(self, title, content):
        print(f"---------------------{title}---------------------")
        print(content)
        print(f"---------------------{title}---------------------")

    def build_schema(self, record):
        schema_prompt = SchemaPrompt()
        schema_query = schema_prompt.build_prompt(record)
        spg_types = None
        retry_times = 0
        self.print_logs("Schema Prompt", schema_query)
        while retry_times < self.max_retry_times:
            print("\nAutomatic schema constructing...\n")
            try:
                if self.schema_build:
                    content = [{"role": "user", "content": schema_query}]
                    now = datetime.now()
                    timestamp = datetime.timestamp(now)
                    async_message_key = "KNEXT_" + str(timestamp * 1000).split(".")[0]
                    if os.getenv("KNEXT_DEBUG_MODE") == "True":
                        schema_response = self.gpt_client.mock_response()
                    else:
                        response = self.gpt_client.async_request(content, async_message_key)
                        if response:
                            schema_response = self.gpt_client.query_async_response(
                                async_message_key
                            )
                        else:
                            raise ValueError("Async request error.")
                else:
                    pass

            except Exception as e:
                retry_times += 1
                print("GPT4 invoke failed. Error msg: " + str(e))
                continue
            if self.schema_build:
                self.print_logs("Schema Response", schema_response)
            try:
                if self.schema_build:
                    schema_response = f"namespace {self.namespace}\n" + schema_response
                schema_file = os.path.join(PWD, ".tmp.schema." + str(self.project_id))
                if not self.schema_build:
                    with open(os.path.join(PWD, schema_file)) as file:
                        schema_response = file.read()
                lines = schema_response.split("\n")
                filtered_response = ""
                is_filtered = False
                for line in lines:
                    line = self.remove_punctuation(line)
                    line = self.format_line(line)
                    if re.search(r"[ \t](id|name|description|eventTime)\(", line):
                        is_filtered = True
                        continue
                    if is_filtered and re.search(r"[ \t]desc:", line):
                        is_filtered = False
                        continue
                    filtered_response += line + "\n"
                with open(schema_file, "w", encoding="utf-8") as file:
                    file.write(filtered_response)
                ml = SPGSchemaMarkLang(schema_file)

                ml.sync_schema()
                schema = SchemaClient()
                session = schema.create_session()
                spg_types = session.spg_types
            except Exception as e:
                retry_times += 1
                print("Parse schema failed. Error msg: " + str(e))
            if spg_types:
                break
        if retry_times >= self.max_retry_times:
            raise ValueError(
                "Exceeded maximum retry count, entity and event extract failed."
            )
        if not spg_types:
            raise ValueError(
                "Exceeded maximum retry count, automatic schema construction failed."
            )
        print("\nAutomatic schema construction finished.\n")

        return spg_types

    def extract_by_humming(self, record, spg_types):
        entity_types, entity_records, event_types, event_records = [], [], [], []
        if not self.humming_extract:
            return [], []
        for spg_type in spg_types.values():
            if spg_type.spg_type_enum == SpgTypeEnum.Entity:
                entity_types.append(spg_type.name)
            if spg_type.spg_type_enum == SpgTypeEnum.Event:
                event_types.append(spg_type.name)
        ae = OneKE_KGPrompt(entity_types, split_num=1)
        ae_prompts = ae.build_prompt(record)
        ee = OneKE_EEPrompt(event_types, split_num=1)
        ee_prompts = ee.build_prompt(record)

        self.print_logs("Entity Extract Prompt", ae_prompts)
        self.print_logs("Event Extract Prompt", ee_prompts)
        retry_times = 0
        while retry_times < self.max_retry_times:
            print("\n[Humming]Entity extracting...\n")
            ae_responses = []
            try:
                if os.getenv("KNEXT_DEBUG_MODE") == "True":
                    ae_responses = self.extract_client.mock_ae_response()
                else:
                    for idx, ae_prompt in enumerate(ae_prompts):
                        print(str(idx + 1) + ': ' + ae_prompt)
                        try:
                            ae_response = self.extract_client.call_service(
                                prompt=ae_prompt,
                            )
                            ae_responses.append(ae_response)
                        except:
                            continue
            except Exception as e:
                retry_times += 1
                print("Humming invoke failed. Error msg: " + str(e))
                continue
            self.print_logs("Entity Extract Response", ae_responses)

            try:
                entity_records = []
                for ae_response in ae_responses:
                    entity_records.extend(ae.parse_response(ae_response))
            except Exception as e:
                retry_times += 1
                print("Parse entity extract response failed. Error msg: " + str(e))
                continue

            print("\n[Humming]Entity extract finished.\n")
            print("\n[Humming]Event extracting...\n")
            ee_responses = []
            try:
                if os.getenv("KNEXT_DEBUG_MODE") == "True":
                    ee_responses = self.extract_client.mock_ee_response()
                else:
                    # for idx, ee_prompt in enumerate(ee_prompts):
                    #     print(str(idx + 1) + ': ' + ee_prompt)
                    #     try:
                    #         ee_response = self.extract_client.call_service(
                    #             prompt=ee_prompt,
                    #         )
                    #         ee_responses.append(ee_response)
                    #     except:
                    #         continue
                    pass
            except Exception as e:
                retry_times += 1
                print("Humming invoke failed. Error msg: " + str(e))
                continue

            self.print_logs("Event Extract Response", ee_responses)
            try:
                event_records = []
                for ee_response in ee_responses:
                    event_records.extend(ee.parse_response(ee_response))
            except Exception as e:
                retry_times += 1
                print("Parse event extract response failed. Error msg: " + str(e))
                continue
            print("\n[Humming]Event extract finished.\n")
            break
        if retry_times >= self.max_retry_times:
            raise ValueError(
                "Exceeded maximum retry count, entity and event extract failed."
            )
        return entity_records, event_records

    def extract_by_gpt(self, record, spg_types, entity_records, event_records):
        if not self.gpt_extract:
            return entity_records, event_records
        entity_types, event_types = [], []
        for spg_type in spg_types.values():
            if spg_type.spg_type_enum == SpgTypeEnum.Entity:
                entity_types.append(spg_type.name)
            if spg_type.spg_type_enum == SpgTypeEnum.Event:
                event_types.append(spg_type.name)
        start_time = time.time()
        retry_times = 0
        while retry_times < self.max_retry_times:
            # print("\n[GPT3.5]Entity extracting...\n")
            # unresolved_entity_types = [i for i in entity_types if i not in [r.spg_type_name for r in entity_records]]
            #
            # try:
            #     for idx, entity_type in enumerate(unresolved_entity_types):
            #         if set(spg_types.get(entity_type).properties.keys()) == {"id", "name", "description"}:
            #             continue
            #         re_prompt = REPrompt(entity_type)
            #         _prompt = re_prompt.build_prompt(record)
            #         print(f'[gpt3.5] re_prompt_retry_{str(idx + 1)}: ' + entity_type)
            #         print(_prompt)
            #         _content = [{"role": "user", "content": _prompt}]
            #         _response = self.extract_client2.sync_request(_content)
            #         _record = re_prompt.parse_response(_response)
            #         if _record:
            #             print(f'[gpt3.5] re_result_{str(idx + 1)}: \n')
            #             print(_record)
            #             entity_records.extend(_record)
            # except Exception as e:
            #     retry_times += 1
            #     print("GPT3.5 invoke failed. Error msg: " + str(e))
            #     continue
            # print("\n[GPT3.5]Entity extracting finished.\n")
            print("\n[GPT3.5]Event extracting...\n")
            unresolved_event_types = [i for i in event_types if i not in [r.spg_type_name for r in event_records]]

            try:
                for idx, event_type in enumerate(unresolved_event_types):
                    ee_prompt = EEPrompt(event_type)
                    _prompt = ee_prompt.build_prompt(record)
                    print(f'[gpt3.5] ee_prompt_retry_{str(idx + 1)}: ' + event_type)
                    print(_prompt)
                    _content = [{"role": "user", "content": _prompt}]
                    _response = self.extract_client2.sync_request(_content)
                    _record = ee_prompt.parse_response(_response)
                    if _record:
                        print(f'[gpt3.5] ee_result_{str(idx + 1)}: \n')
                        print(_record)
                        event_records.extend(_record)
            except Exception as e:
                retry_times += 1
                print("GPT3.5 invoke failed. Error msg: " + str(e))
                continue
            print("\n[GPT3.5]Event extracting finished.\n")
            break
        if retry_times >= self.max_retry_times:
            raise ValueError(
                "Exceeded maximum retry count, entity and event extract failed."
            )
        end_time = time.time()
        print("extra time cost: {} s".format(end_time - start_time))
        return entity_records, list(set(event_records))

    def invoke(self, record: Dict[str, str]) -> List[SPGRecord]:
        # schema = SchemaClient()
        # session = schema.create_session()
        # spg_types = session.spg_types
        spg_types = self.build_schema(record)

        entity_records, event_records = self.extract_by_humming(record, spg_types)

        entity_records, event_records = self.extract_by_gpt(record, spg_types, entity_records, event_records)

        filtered_event_records = []
        for event in event_records:
            is_filtered = False
            for entity in entity_records:
                if event.spg_type_name == entity.spg_type_name and event.get_property("name", "") == entity.get_property("name", ""):
                    is_filtered = True
                    print("filtered_event_record:")
                    print(event)
            if not is_filtered:
                filtered_event_records.append(event)

        spg_records = entity_records + filtered_event_records
        subgraph = SubGraph.from_spg_record(spg_types, spg_records)

        self.print_logs("SubGraph", subgraph)
        return subgraph


class SchemaBuilder(ExtractOp):

    def __init__(self, params: Dict[str, str]):
        super().__init__(params)
        self.gpt_client = AntGPTClient(config=os.path.join(PWD, "gpt4.json"))
        self.max_retry_times = 3
        self.namespace = params.get("namespace", "DEFAULT") if params else "DEFAULT"
        self.project_id = params.get("project_id", 1) if params else 1
        self.schema_build = True
        os.environ["KNEXT_PROJECT_ID"] = str(self.project_id)

    def remove_punctuation(self, text: str) -> str:
        brackets_pattern = r"\([^\)]*\)"

        matches = re.findall(brackets_pattern, text)

        for match in matches:
            cleaned_match = re.sub(r"[\.,;:\'\"!?/、-]", "", match)
            text = text.replace(match, cleaned_match)
        return text

    def format_line(self, line):
        pattern = r"([\u4e00-\u9fa5]+)\(([A-Za-z\s]+)\)"

        def swap_cn_en(match):
            chinese = match.group(1)
            english = match.group(2)
            return f"{english}({chinese})"

        line = re.sub(pattern, swap_cn_en, line)
        if all(i not in line for i in ["EntityType", "EventType"]):
            pattern = r"([A-Za-z])[A-Za-z]*\([^\)]*\)"

            def replace_first_letter(match):
                first_letter_lower = match.group(1).lower()
                return first_letter_lower + match.group(0)[1:]

            line = re.sub(pattern, replace_first_letter, line)
        return line

    def print_logs(self, title, content):
        print(f"---------------------{title}---------------------")
        print(content)
        print(f"---------------------{title}---------------------")

    def build_schema(self, record):
        schema_prompt = SchemaPrompt()
        schema_query = schema_prompt.build_prompt(record)
        spg_types = None
        retry_times = 0
        self.print_logs("Schema Prompt", schema_query)
        while retry_times < self.max_retry_times:
            print("\nAutomatic schema constructing...\n")
            try:
                if self.schema_build:
                    content = [{"role": "user", "content": schema_query}]
                    now = datetime.now()
                    timestamp = datetime.timestamp(now)
                    async_message_key = "KNEXT_" + str(timestamp * 1000).split(".")[0]
                    if os.getenv("KNEXT_DEBUG_MODE") == "True":
                        schema_response = self.gpt_client.mock_response()
                    else:
                        response = self.gpt_client.async_request(content, async_message_key)
                        if response:
                            schema_response = self.gpt_client.query_async_response(
                                async_message_key
                            )
                        else:
                            raise ValueError("Async request error.")
                else:
                    pass

            except Exception as e:
                retry_times += 1
                print("GPT4 invoke failed. Error msg: " + str(e))
                continue
            if self.schema_build:
                self.print_logs("Schema Response", schema_response)
            try:
                if self.schema_build:
                    schema_response = f"namespace {self.namespace}\n" + schema_response
                schema_file = os.path.join(PWD, ".tmp.schema." + str(self.project_id))
                if not self.schema_build:
                    with open(os.path.join(PWD, schema_file)) as file:
                        schema_response = file.read()
                lines = schema_response.split("\n")
                filtered_response = ""
                is_filtered = False
                for line in lines:
                    line = self.remove_punctuation(line)
                    line = self.format_line(line)
                    if re.search(r"[ \t](id|name|description|eventTime)\(", line):
                        is_filtered = True
                        continue
                    if is_filtered and re.search(r"[ \t]desc:", line):
                        is_filtered = False
                        continue
                    filtered_response += line + "\n"
                with open(schema_file, "w", encoding="utf-8") as file:
                    file.write(filtered_response)
                ml = SPGSchemaMarkLang(schema_file)

                ml.sync_schema()
                schema = SchemaClient()
                session = schema.create_session()
                spg_types = session.spg_types
            except Exception as e:
                retry_times += 1
                print("Parse schema failed. Error msg: " + str(e))
            if spg_types:
                break
        if retry_times >= self.max_retry_times:
            raise ValueError(
                "Exceeded maximum retry count, entity and event extract failed."
            )
        if not spg_types:
            raise ValueError(
                "Exceeded maximum retry count, automatic schema construction failed."
            )
        print("\nAutomatic schema construction finished.\n")

        return spg_types

    def invoke(self, record: Dict[str, Any]) -> List[SPGRecord]:
        # self.build_schema(record)
        return []


class LLMExtractor(ExtractOp):

    def __init__(self, params: Dict[str, str]):
        super().__init__(params)
        self.extract_client = MayaHttpClient(
            scene_name="knowlm_ie_full_v2",
            chain_name="v1",
            use_pre=True,
        )
        self.extract_client2 = AntGPTClient(config=os.path.join(PWD, "gpt3_5.json"))
        self.max_retry_times = 3
        self.humming_extract = True
        self.gpt_extract = True
        self.namespace = params.get("namespace", "DEFAULT") if params else "DEFAULT"
        self.project_id = params.get("project_id", 1) if params else 1
        os.environ["KNEXT_PROJECT_ID"] = str(self.project_id)

    def print_logs(self, title, content):
        print(f"---------------------{title}---------------------")
        print(content)
        print(f"---------------------{title}---------------------")

    def extract_by_humming(self, record, spg_types):
        entity_types, entity_records, event_types, event_records = [], [], [], []
        if not self.humming_extract:
            return [], []
        for spg_type in spg_types.values():
            if spg_type.spg_type_enum == SpgTypeEnum.Entity:
                entity_types.append(spg_type.name)
            if spg_type.spg_type_enum == SpgTypeEnum.Event:
                event_types.append(spg_type.name)
        ae = OneKE_KGPrompt(entity_types, split_num=1)
        ae_prompts = ae.build_prompt(record)
        ee = OneKE_EEPrompt(event_types, split_num=1)
        ee_prompts = ee.build_prompt(record)

        self.print_logs("Entity Extract Prompt", ae_prompts)
        self.print_logs("Event Extract Prompt", ee_prompts)
        retry_times = 0
        while retry_times < self.max_retry_times:
            print("\n[Humming]Entity extracting...\n")
            ae_responses = []
            try:
                if os.getenv("KNEXT_DEBUG_MODE") == "True":
                    ae_responses = self.extract_client.mock_ae_response()
                else:
                    for idx, ae_prompt in enumerate(ae_prompts):
                        print(str(idx + 1) + ': ' + ae_prompt)
                        try:
                            ae_response = self.extract_client.call_service(
                                prompt=ae_prompt,
                            )
                            ae_responses.append(ae_response)
                        except:
                            continue
            except Exception as e:
                retry_times += 1
                print("Humming invoke failed. Error msg: " + str(e))
                continue
            self.print_logs("Entity Extract Response", ae_responses)

            try:
                entity_records = []
                for ae_response in ae_responses:
                    entity_records.extend(ae.parse_response(ae_response))
            except Exception as e:
                retry_times += 1
                print("Parse entity extract response failed. Error msg: " + str(e))
                continue

            print("\n[Humming]Entity extract finished.\n")
            print("\n[Humming]Event extracting...\n")
            ee_responses = []
            try:
                if os.getenv("KNEXT_DEBUG_MODE") == "True":
                    ee_responses = self.extract_client.mock_ee_response()
                else:
                    # for idx, ee_prompt in enumerate(ee_prompts):
                    #     print(str(idx + 1) + ': ' + ee_prompt)
                    #     try:
                    #         ee_response = self.extract_client.call_service(
                    #             prompt=ee_prompt,
                    #         )
                    #         ee_responses.append(ee_response)
                    #     except:
                    #         continue
                    pass
            except Exception as e:
                retry_times += 1
                print("Humming invoke failed. Error msg: " + str(e))
                continue

            self.print_logs("Event Extract Response", ee_responses)
            try:
                event_records = []
                for ee_response in ee_responses:
                    event_records.extend(ee.parse_response(ee_response))
            except Exception as e:
                retry_times += 1
                print("Parse event extract response failed. Error msg: " + str(e))
                continue
            print("\n[Humming]Event extract finished.\n")
            break
        if retry_times >= self.max_retry_times:
            raise ValueError(
                "Exceeded maximum retry count, entity and event extract failed."
            )
        return entity_records, event_records

    def extract_by_gpt(self, record, spg_types, entity_records, event_records):
        if not self.gpt_extract:
            return entity_records, event_records
        entity_types, event_types = [], []
        for spg_type in spg_types.values():
            if spg_type.spg_type_enum == SpgTypeEnum.Entity:
                entity_types.append(spg_type.name)
            if spg_type.spg_type_enum == SpgTypeEnum.Event:
                event_types.append(spg_type.name)
        start_time = time.time()
        retry_times = 0
        while retry_times < self.max_retry_times:
            # print("\n[GPT3.5]Entity extracting...\n")
            # unresolved_entity_types = [i for i in entity_types if
            #                            i not in [r.spg_type_name for r in entity_records]]
            #
            # try:
            #     for idx, entity_type in enumerate(unresolved_entity_types):
            #         if set(spg_types.get(entity_type).properties.keys()) == {"id", "name", "description"}:
            #             continue
            #         re_prompt = REPrompt(entity_type)
            #         _prompt = re_prompt.build_prompt(record)
            #         print(f'[gpt3.5] re_prompt_retry_{str(idx + 1)}: ' + entity_type)
            #         print(_prompt)
            #         _content = [{"role": "user", "content": _prompt}]
            #         _response = self.extract_client2.sync_request(_content)
            #         _record = re_prompt.parse_response(_response)
            #         if _record:
            #             print(f'[gpt3.5] re_result_{str(idx + 1)}: \n')
            #             print(_record)
            #             entity_records.extend(_record)
            # except Exception as e:
            #     retry_times += 1
            #     print("GPT3.5 invoke failed. Error msg: " + str(e))
            #     continue
            # print("\n[GPT3.5]Entity extracting finished.\n")
            print("\n[GPT3.5]Event extracting...\n")
            unresolved_event_types = [i for i in event_types if i not in [r.spg_type_name for r in event_records]]

            try:
                for idx, event_type in enumerate(unresolved_event_types):
                    ee_prompt = EEPrompt(event_type)
                    _prompt = ee_prompt.build_prompt(record)
                    print(f'[gpt3.5] ee_prompt_retry_{str(idx + 1)}: ' + event_type)
                    print(_prompt)
                    _content = [{"role": "user", "content": _prompt}]
                    _response = self.extract_client2.sync_request(_content)
                    _record = ee_prompt.parse_response(_response)
                    if _record:
                        print(f'[gpt3.5] ee_result_{str(idx + 1)}: \n')
                        print(_record)
                        event_records.extend(_record)
            except Exception as e:
                retry_times += 1
                print("GPT3.5 invoke failed. Error msg: " + str(e))
                continue
            print("\n[GPT3.5]Event extracting finished.\n")
            break
        if retry_times >= self.max_retry_times:
            raise ValueError(
                "Exceeded maximum retry count, entity and event extract failed."
            )
        end_time = time.time()
        print("extra time cost: {} s".format(end_time - start_time))
        return entity_records, event_records

    def invoke(self, record: Dict[str, str]) -> List[SPGRecord]:
        # schema = SchemaClient()
        # session = schema.create_session()
        # spg_types = session.spg_types
        spg_types = self.build_schema(record)

        entity_records, event_records = self.extract_by_humming(record, spg_types)

        entity_records, event_records = self.extract_by_gpt(record, spg_types, entity_records, event_records)

        filtered_event_records = []
        for event in event_records:
            is_filtered = False
            for entity in entity_records:
                if event.spg_type_name == entity.spg_type_name and event.get_property("name", "") == entity.get_property("name", ""):
                    is_filtered = True
                    print("filtered_event_record:")
                    print(event)
            if not is_filtered:
                filtered_event_records.append(event)

        spg_records = entity_records + filtered_event_records
        subgraph = SubGraph.from_spg_record(spg_types, spg_records)

        self.print_logs("SubGraph", subgraph)
        return subgraph

if __name__ == '__main__':
    #     client = MayaHttpClient(
    #         scene_name="Qwen1_5_72B_Chat_GPTQ_Int4",
    #         chain_name="v1",
    #         # use_offline=True,
    #         use_pre=True,
    #         # use_dns_filter=False,
    #     )
    #     input = """
    # 周杰伦（Jay Chou），1979年1月18日出生于台湾省新北市，祖籍福建省永春县，华语流行乐男歌手、音乐人、演员、导演、编剧，毕业于淡江中学。
    # 2000年，发行个人首张音乐专辑《Jay》 [26]。2001年，凭借专辑《范特西》奠定其融合中西方音乐的风格 [16]。2002年，举行“The One”世界巡回演唱会 [1]。2003年，成为美国《时代周刊》封面人物 [2]；同年，发行音乐专辑《叶惠美》 [21]，该专辑获得第15届台湾金曲奖最佳流行音乐演唱专辑奖 [23]。2004年，发行音乐专辑《七里香》 [29]，该专辑在亚洲的首月销量达到300万张 [316]；同年，获得世界音乐大奖中国区最畅销艺人奖 [320]。2005年，主演个人首部电影《头文字D》 [314]，并凭借该片获得第25届香港电影金像奖和第42届台湾电影金马奖的最佳新演员奖 [3] [315]。2006年起，连续三年获得世界音乐大奖中国区最畅销艺人奖 [4]。
    # 2007年，自编自导爱情电影《不能说的秘密》 [321]，同年，成立杰威尔音乐有限公司 [10]。2008年，凭借歌曲《青花瓷》获得第19届台湾金曲奖最佳作曲人奖 [292]。2009年，入选美国CNN“25位亚洲最具影响力人物” [6]；同年，凭借专辑《魔杰座》获得第20届台湾金曲奖最佳国语男歌手奖 [7]。2010年，入选美国《Fast Company》评出的“全球百大创意人物”。2011年，凭借专辑《跨时代》获得第22届台湾金曲奖最佳国语男歌手奖 [294]。2012年，登上福布斯中国名人榜榜首 [8]。2014年，发行个人首张数字音乐专辑《哎呦，不错哦》 [295]。2023年，凭借专辑《最伟大的作品》成为首位获得国际唱片业协会“全球畅销专辑榜”冠军的华语歌手 [287]。
    #     """
    #     message = """
    # {
    # 	"instruction": "你是专门进行实体抽取的专家。请从input中抽取出符合schema定义的实体，不存在的实体类型返回空列表。请按照JSON字符串的格式回答。",
    # 	"schema": ["人物", "音乐专辑", "电影", "演唱会", "公司"],
    # 	"input": "${input}"
    # }
    #         """.replace("${input}", input)
    #     feature = {
    #         "message": message,
    #     }
    #     # 调用线上模型服务
    #     result = client.call_service(feature, debug=False)
    #     print(result)
    #     os.environ["KNEXT_DEBUG_MODE"] = "True"
    a = AutoSchemaBuilder(params={"namespace": "Demo", "project_id": 2, "instruction": "请帮我构建知识图谱"})
    input = """
周杰伦（Jay Chou），1979年1月18日出生于台湾省新北市，祖籍福建省永春县，华语流行乐男歌手、音乐人、演员、导演、编剧，毕业于淡江中学。
2000年，发行个人首张音乐专辑《Jay》。2001年，凭借专辑《范特西》奠定其融合中西方音乐的风格。2002年，举行“The One”世界巡回演唱会。2003年，成为美国《时代周刊》封面人物；同年，发行音乐专辑《叶惠美》，该专辑获得第15届台湾金曲奖最佳流行音乐演唱专辑奖。2004年，发行音乐专辑《七里香》，该专辑在亚洲的首月销量达到300万张；同年，获得世界音乐大奖中国区最畅销艺人奖。2005年，主演个人首部电影《头文字D》，并凭借该片获得第25届香港电影金像奖和第42届台湾电影金马奖的最佳新演员奖。2006年起，连续三年获得世界音乐大奖中国区最畅销艺人奖。
2007年，自编自导爱情电影《不能说的秘密》，同年，成立杰威尔音乐有限公司。2007年，凭借歌曲《青花瓷》获得第19届台湾金曲奖最佳作曲人奖。2007年，入选美国CNN“25位亚洲最具影响力人物”；同年，凭借专辑《魔杰座》获得第20届台湾金曲奖最佳国语男歌手奖。2010年，入选美国《Fast Company》评出的“全球百大创意人物”。2011年，凭借专辑《跨时代》获得第22届台湾金曲奖最佳国语男歌手奖。2012年，登上福布斯中国名人榜榜首。2014年，发行个人首张数字音乐专辑《哎呦，不错哦》。2023年，凭借专辑《最伟大的作品》成为首位获得国际唱片业协会“全球畅销专辑榜”冠军的华语歌手。
"""
    record = {
        "input": input
    }
    a.invoke(record)
    # os.environ["KNEXT_PROJECT_ID"] = "1"
    # from knext.builder.operator.builtin.auto_prompt import REPrompt, EEPrompt
    # re = REPrompt(spg_type_name="DEFAULT.Organization")
