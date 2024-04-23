import copy
import os
import requests
import yaml
import json
from gentccode.produce_case_code import ProduceCaseCode
from gentccode.filter_cp_result import produce_cp_param_by_node
from gentccode.read_swagger_rule import NoneRule, SwaggerRule
from gentccode.merge_api import merge_api_params
from http_content_parser.req_data import ReqData
from http_content_parser.api_parser import ApiModelParser


SOURCE_CURL = "curl"
SOURCE_POSTMAN = "postman"
SOURCE_SWAGGER = "swagger"
SOURCE_OPENAPI = "openapi"


class ProduceUseCase(object):
    def __init__(self) -> None:
        self.pcc = ProduceCaseCode()
        self.api_parser = ApiModelParser()

    def produce_case_for_postman(self, json_file_path, yaml_file, use_case_file):
        with open(json_file_path, "r") as f:
            postman_dict = json.load(f)
        self.init_file(py_file=use_case_file, yaml_file=yaml_file)
        payload_list = self.api_parser.get_api_model_for_postman(
            postman_dict, yaml_file
        )
        none_rule = NoneRule()
        code_str = self.pcc.produce_code_for_api_dict(
            add_after_assert_response_str="",
            api_info_dict=postman_dict,
            rule_tool=none_rule,
        )
        # write api info to yaml
        self.write_api_content_to_yaml(req_list=payload_list, yaml_file=yaml_file)
        # write use case to py
        self.write_use_case_to_py(code_str=code_str, py_file=use_case_file)

    def produce_case_for_swagger2(self, swagger_json_path, yaml_file, use_case_file):
        # 读取 doc.json 文件
        with open(swagger_json_path, "r") as f:
            swagger2_dict = json.load(f)
        self.init_file(py_file=use_case_file, yaml_file=yaml_file)
        payload_list = self.api_parser.get_api_model_for_swagger(
            swagger2_dict, yaml_file
        )
        none_rule = NoneRule()
        code_str = self.pcc.produce_code_for_api_dict(
            add_after_assert_response_str="",
            api_info_dict=swagger2_dict,
            rule_tool=none_rule,
        )
        # write api info to yaml
        self.write_api_content_to_yaml(req_list=payload_list, yaml_file=yaml_file)
        # write use case to py
        self.write_use_case_to_py(code_str=code_str, py_file=use_case_file)

    def produce_case_for_curl(
        self,
        curl_file: str,
        yaml_file: str,
        use_case_file: str,
        add_after_assert_response_str: str,
        curl_filter=None,
    ):
        self.init_file(py_file=use_case_file, yaml_file=yaml_file)
        payload_list = self.api_parser.get_api_model_for_curl(
            curl_file=curl_file, curl_filter=curl_filter
        )
        node_assert_res_str = self.pcc.handle_response_assert_node_str(
            add_after_assert_response_str
        )
        code_str = self.pcc.produce_code_for_api_model(
            req_datas=payload_list,
            add_after_assert_response_str=node_assert_res_str,
        )
        # write api info to yaml
        self.write_api_content_to_yaml(req_list=payload_list, yaml_file=yaml_file)
        # write use case to py
        self.write_use_case_to_py(code_str=code_str, py_file=use_case_file)

    def produce_case_by_param_type_for_curl(
        self,
        payload_list,
        curl_file,
        use_case_file,
        param_type,
        add_after_assert_response_str,
        add_method_name_suffix_str=False,
    ):
        self.init_file(py_file=use_case_file, yaml_file="")
        # read from curl
        http_payload_list = self.api_parser.get_api_model_for_curl(curl_file=curl_file)
        # modify api's param
        new_payloads = []
        for p in payload_list:
            for payload in http_payload_list:
                temp = copy.deepcopy(payload)
                if param_type == "body":
                    temp.body = p
                elif param_type == "query":
                    temp.query_param = p
                new_payloads.append(temp)
        # generate code
        code_str = self.pcc.produce_code_for_api_model(
            req_datas=new_payloads,
            add_method_name_suffix_str=add_method_name_suffix_str,
            add_after_assert_response_str=add_after_assert_response_str,
        )
        # write api info to yaml
        # self.write_api_content_to_yaml(req_list=http_payload_list, yaml_file=)
        # write use case to py
        self.write_use_case_to_py(code_str=code_str, py_file=use_case_file)

    def get_payload_body(self, curl_file):
        # read from curl
        http_payloads = self.api_parser.convert_curl_data_to_model(
            curl_file_path=curl_file
        )
        return [payload.body for payload in http_payloads]

    def get_query_param_from_curl(self, curl_file):
        # read from curl
        http_payloads = self.api_parser.convert_curl_data_to_model(
            curl_file_path=curl_file
        )
        return [payload.query_param for payload in http_payloads]

    def produce_merged_case_for_openapi_and_curl(self, curl_file_path):
        # 从curl文件中生成yaml
        curl_yaml_file_path = "script/generated_result/curl_merge.yaml"
        with open(curl_yaml_file_path, "w") as f:
            f.write("")  # 先清空之前的内容
        self.api_parser.produce_api_yaml_for_curl(
            curl_file=curl_file_path, yaml_file=curl_yaml_file_path
        )
        with open(curl_yaml_file_path, "r") as f:
            data2 = yaml.safe_load(f)
        api_dict = dict(data2)

        # 从rap上获取openapi
        openapi_dict = self.download_openapi3_json()
        openapi_yaml_file_path = "script/generated_result/openapi_merge.yaml"
        with open(openapi_yaml_file_path, "w") as f:
            f.write("")  # 先清空之前的内容
        self.api_parser.produce_api_yaml_for_openapi3(
            openapi_dict=openapi_dict, yaml_file=openapi_yaml_file_path
        )
        with open(openapi_yaml_file_path, "r") as f:
            data = yaml.safe_load(f)
        openapi_dict = dict(data)

        # 合并上面两个yaml,生成合并后yaml
        res = merge_api_params(openapi_dict, api_dict)
        print(json.dumps(res[1]))
        merged_yaml_path = "./script/generated_result/merged.yaml"
        with open(merged_yaml_path, "w") as f:
            yaml.dump(res[0], f, encoding="UTF-8")

        # 根据merge后的yaml,生成用例代码
        # case_file_path = 'testcase/swagger/test_toc_swagger.py'
        case_file_path = "./script/generated_result/openapi_curl.py"
        swagger_rule = SwaggerRule()
        self.pcc.produce_code_for_api_dict(
            case_code_file_path=case_file_path,
            yaml_file_path=merged_yaml_path,
            rule_tool=swagger_rule,
            split_respone_assert_to_new_method=True,
        )

    def produce_merged_case_for_swagger_and_curl(self, curl_file_path):
        # 从curl文件中生成yaml
        curl_yaml_file_path = "script/generated_result/curl_merge.yaml"
        with open(curl_yaml_file_path, "w") as f:
            f.write("")  # 先清空之前的内容
        self.api_parser.produce_api_yaml_for_curl(
            curl_file=curl_file_path, yaml_file=curl_yaml_file_path
        )
        with open(curl_yaml_file_path, "r") as f:
            data2 = yaml.safe_load(f)
        api_dict = dict(data2)

        # 从swagger中生成yaml
        with open("doc.json", "r") as f:
            swagger2_dict = json.load(f)
        swagger_yaml_file_path = "script/generated_result/swagger_merge.yaml"
        with open(swagger_yaml_file_path, "w") as f:
            f.write("")  # 先清空之前的内容
        self.api_parser.produce_api_yaml_for_swagger2(
            swagger2_dict=swagger2_dict, yaml_file=swagger_yaml_file_path
        )
        with open(swagger_yaml_file_path, "r") as f:
            data = yaml.safe_load(f)
        swagger_dict = dict(data)

        # 合并上面两个yaml,生成合并后yaml
        res = merge_api_params(swagger_dict, api_dict)
        print(json.dumps(res[1]))
        merged_yaml_path = "./script/generated_result/merged.yaml"
        with open(merged_yaml_path, "w") as f:
            yaml.dump(res[0], f)

        # 根据merge后的yaml,生成用例代码
        case_file_path = "testcase/swagger/test_toc_swagger.py"
        swagger_rule = SwaggerRule()
        self.pcc.produce_code_for_api_dict(
            case_code_file_path=case_file_path,
            yaml_file_path=merged_yaml_path,
            rule_tool=swagger_rule,
            split_respone_assert_to_new_method=True,
        )

    def download_swagger_json(self, url):
        d = {}
        try:
            d = requests.get(url=url).json()
        except Exception as ex:
            print(ex)
        return d

    def download_openapi3_json(self, url=""):
        d = {}
        h = {"Cookie": ""}
        d = requests.get(url=url, headers=h).json()
        if not d.get("isOk", True):
            raise Exception("get openapi result error")
        return d

    def produce_cp_case(
        self,
        param_type: str,
        source_type: str,
        node: str,
        curl_file_path: str,
        use_case_file_path: str,
        add_after_assert_response_str: str,
    ):
        PARAM_TYPE_QUERY = "query"
        PARAM_TYPE_BODY = "body"
        if param_type == PARAM_TYPE_BODY:
            payload_params = self.get_payload_body(curl_file=curl_file_path)
            cp_param_list = produce_cp_param_by_node(node, payload_params)
        elif param_type == PARAM_TYPE_QUERY:
            payload_params = self.get_query_param_from_curl(curl_file=curl_file_path)
            cp_param_list = produce_cp_param_by_node(node, payload_params)
        else:
            print("param type is not exist")
        if source_type == SOURCE_CURL:
            node_assert_res_str = self.pcc.handle_response_assert_node_str(
                add_after_assert_response_str
            )
            self.produce_case_by_param_type_for_curl(
                payload_list=cp_param_list,
                param_type=param_type,
                curl_file=curl_file_path,
                use_case_file=use_case_file_path,
                add_method_name_suffix_str=True,
                add_after_assert_response_str=node_assert_res_str,
            )
        elif source_type == SOURCE_POSTMAN:
            pass
        elif source_type == SOURCE_SWAGGER:
            pass
        elif source_type == SOURCE_OPENAPI:
            pass
        else:
            print("source type is not exsit")

    def write_api_content_to_yaml(self, yaml_file: str, req_list: list[ReqData]):
        api_obj = {}
        yaml_obj = {}
        for req_model in req_list:
            with open(yaml_file, "at") as f:
                api_obj["original_url"] = req_model.original_url
                api_obj["path"] = req_model.path
                api_obj["query_param"] = req_model.query_param
                api_obj["path_param"] = req_model.path_param
                api_obj["header"] = req_model.header
                api_obj["body"] = req_model.body
                api_obj["method"] = req_model.method
                api_obj["response"] = req_model.response
                yaml_obj[req_model.temp_api_label] = api_obj
                yaml.dump(yaml_obj, f)

    def write_use_case_to_py(self, py_file: str, code_str: str):
        with open(py_file, "at") as f:
            f.write(code_str)

    def init_file(self, py_file, yaml_file):
        if os.path.exists(py_file):
            with open(py_file, "w") as f:
                f.write("")
        if os.path.exists(yaml_file):
            with open(yaml_file, "w") as f:
                f.write("")
