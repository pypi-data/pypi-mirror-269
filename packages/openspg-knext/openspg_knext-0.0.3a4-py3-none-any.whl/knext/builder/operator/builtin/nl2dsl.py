import json
import os
from typing import Dict, List

from knext.builder.operator.builtin.auto_schema_builder import MayaHttpClient
from knext.builder.operator import ExtractOp
from knext.schema.client import SchemaClient
from knext.schema.model.base import SpgTypeEnum

import json


def get_entities_with_Nodes_from_query(query, schema, client):
    # prompt="""Instructions: 你是一位知识图谱专家，请从Question中识别出所有实体，并依据Schema中的Node的内容，找到各个实体的类型。类型用“.”拼接。Answer的格式为：实体-类型。Answer中每一对"实体-类型"单独占一行。
    # """
    prompt="""Example: 
Schema: 
Node: {"X.Person(人物)": ["name(名称)", "birthPlace(出生地)", "graduateFrom(毕业于)", "job(职业)", "origination(祖籍)"],
       "X.Film(电影)": ["name(名称)", "actor(演员)", "title(电影标题)"],
       "X.Album(专辑)": ["name(名称)", "releaseDate(发行时间)", "salesVolume(销售量)"],
       "X.AlbumReleaseEvent(专辑发布事件)": ["eventTime(发生时间)"]
      }
Edge: ["X.Film-actor(演员)-X.Person"]

Question: 王家卫在2012年导演了哪些电影
Answer: 王家卫-Person(人物)
2012年-AlbumReleaseEvent(专辑发布事件)
电影-Film(电影)

Instructions: 你是一位知识图谱专家，也是一位语言专家。请参考上文Example中的匹配方式，从下文Question中识别出所有名词，并依据下文Question的语义在下文的Schema.Node中找到各名词的类型。类型仅从下文Schema.Node中选择。类型用“.”拼接。下文中Schema.Node中每对""都是一个整体。Answer的格式为：名词-类型。Answer中每一对"名词-类型"单独占一行。
"""

    prompt += schema
    prompt += """

Question：""" + query

    prompt_c = {
        "message": prompt,
        "max_input_len":1024,
        "max_output_len":1024
    }
    result = client.call_service(prompt_c, debug=False)

    return result


def get_type_of_first_entity(query, schema, client):
    prompt="""Instructions: 你是一位知识图谱专家，请从Question中识别出所有实体，依据Schema中的内容判定Question中实体的类别。Answer的格式为：实体-类别。
"""
    prompt += schema
    prompt += """

Question：""" + query

    prompt_c = {
        "message": prompt,
        "max_input_len":1024,
        "max_output_len":1024
    }
    result = client.call_service(prompt_c, debug=False)

    return result


def query_transfer_to_dsl(query, schema, client):
    # initial parameters
    nodes_dict = json.loads(schema.split("Node:")[1].split("Edge")[0])
    edges_list = json.loads(schema.split("Edge:")[-1])

    # nodes
    node_keys_dict = {}
    node_with_details_dict = {}
    for key in nodes_dict.keys():
        key_items = key.split(")")[0].split("(")
        node_keys_dict[key] = key
        node_keys_dict[key_items[0]] = key
        node_keys_dict[key_items[1]] = key
        init_nodes_list = nodes_dict[key]
        detail_dict = {}
        for init_item in init_nodes_list:
            init_items = init_item.split(")")[0].split("(")
            detail_dict[init_item] = init_items[0]
            detail_dict[init_items[0]] = init_items[0]
            detail_dict[init_items[1]] = init_items[0]
        node_with_details_dict[key] = detail_dict
    #edges
    edge_type_dict = {}
    edge_end_to_start = {}
    for edge_item in edges_list:
        edges_items = edge_item.split('-')
        edge_type_dict[edges_items[0] + '-' + edges_items[2]] = edges_items[1].split("(")[0].strip()
        edge_end_to_start[edges_items[2]] = edge_end_to_start.get(edges_items[2], []) + [edges_items[0]] # [edges_items[0], edges_items[0] + '-' + edges_items[2]]


    schema_entity_node = """Schema: \nNode: """
    schema_entity_node += str(list(nodes_dict.keys()))
    entities_nodes = get_entities_with_Nodes_from_query(query, schema, client)
    # entities_nodes = get_entities_with_Nodes_from_query(query, schema_entity_node, client)
    entities_nodes_list = entities_nodes.split('\n')
    # y = [chr(y) for y in range(65, 91)] # A-Z
    Node_ABC = 65

    # entities in dsl
    entities_in_dsl = []
    rule_in_dsl = []
    rule_index = 1
    entity_with_ABC = {}
    start_node_flag = True
    type_to_ABC_dict = {}
    no_matched_nodes = []
    for i in range(0, len(entities_nodes_list)):
        node_items = entities_nodes_list[i].split('-')
        return_type = node_items[1].split(".")
        node_key = ''
        # node_key = node_keys_dict[".".join(return_type[0:2])]
        if len(return_type) >= 2:
            return_type = ".".join(return_type[0:2])
        else:
            return_type = node_items[1]
        for key_in_note_type in node_keys_dict.keys():
            if return_type.strip() in key_in_note_type:
                node_key = node_keys_dict[key_in_note_type]
                break

        entity_type = node_key.split(")")[0].split("(")[0].strip()
        entity_dsl = chr(Node_ABC) + ' [' + entity_type
        entity = node_items[0]
        # 保存没有找到type的名词
        if nodes_dict.get(node_key, "NO_NODE_MATCHED") == "NO_NODE_MATCHED":
            no_matched_nodes.append(entity)
            continue
        schema_sub = nodes_dict[node_key]
        entity_subtype = get_type_of_first_entity(entity, str(schema_sub), client)
        subtype_name = entity_subtype.split('-')[-1]
        # subtype_name_in_dsl = node_with_details_dict[node_key][subtype_name]

        subtype_name_in_dsl = 'name'
        for key_in_subtype in node_with_details_dict[node_key]:
            if subtype_name in key_in_subtype:
                subtype_name_in_dsl = node_with_details_dict[node_key][key_in_subtype]
                break
        if start_node_flag and subtype_name_in_dsl.strip() == "name":
            entity_dsl += ', __start__="true"'
            dsl_line = 'R' + str(rule_index) + ': ' + chr(Node_ABC) + '.' + subtype_name_in_dsl + '=="' + entity + '"'
            rule_in_dsl.append(dsl_line)
            rule_index += 1
            start_node_flag = False
        else:
            if subtype_name_in_dsl.strip() != "name":
                dsl_line = 'R' + str(rule_index) + ': ' + chr(Node_ABC) + '.' + subtype_name_in_dsl + '=="' + entity + '"'
                rule_in_dsl.append(dsl_line)
                rule_index += 1
        entity_dsl += ']'

        entities_in_dsl.append(entity_dsl)
        entity_with_ABC[node_items[0]] = chr(Node_ABC)

        type_to_ABC_dict[entity_type] = type_to_ABC_dict.get(entity_type, []) + [chr(Node_ABC)]
        Node_ABC += 1

    # print("\n".join(entities_in_dsl))
    # print('*' * 20)
    # print("\n".join(rule_in_dsl))

    # relations in dsl
    relation_in_dsl = []
    relation_index = 1
    for relation_item in edge_type_dict.keys():
        relation_nodes = relation_item.split('-')
        if relation_nodes[0] in type_to_ABC_dict.keys() and relation_nodes[1] in type_to_ABC_dict.keys():
            start_node_list = type_to_ABC_dict[relation_nodes[0]]
            end_node_list = type_to_ABC_dict[relation_nodes[1]]
            realtion_type = edge_type_dict[relation_item]
            for item_s in start_node_list:
                for item_e in end_node_list:
                    if item_s != item_e:
                        dsl_line = item_s + ' -> ' + item_e + ' [' + realtion_type + '] as E' + str(relation_index)
                        relation_in_dsl.append(dsl_line)
                        relation_index += 1
    # 没有找到边，检索边
    if len(relation_in_dsl) < 1 or len(no_matched_nodes) > 0:
        if len(relation_in_dsl) > 0:
            for item_unmatched_entity in no_matched_nodes:
                for relation_item in relation_in_dsl:
                    nodes = relation_item.strip().split('[').strip().split('->')
                    node_s = nodes[0].strip()
                    node_e = nodes[1].strip()
                    node_s_t = ''
                    node_e_e = ''
                    # start node
                    for type_key in type_to_ABC_dict.keys():
                        if node_s in type_to_ABC_dict[type_key]:
                            node_s_t = type_key
                            break
                    schema_sub = nodes_dict[node_keys_dict[node_s_t]]
                    schema_sub_dict = {}
                    for item_schema in schema_sub:
                        items_schema = item_schema.strip().strip(")").split("(")
                        schema_sub_dict[item_schema] = items_schema[0]
                        schema_sub_dict[items_schema[0]] = items_schema[0]
                        schema_sub_dict[items_schema[1]] = items_schema[0]
                    entity_subtype = get_type_of_first_entity(item_unmatched_entity, str(schema_sub), client)
                    subtype_name = entity_subtype.split('-')[-1]
                    if subtype_name in list(schema_sub_dict.keys()):
                        dsl_line = 'R' + str(sub_rule_index) + ': ' + chr(sub_Node_ABC) + '.' + schema_sub_dict[subtype_name] + '=="' + item_unmatched_entity + '"'
                        relation_in_dsl.append(dsl_line)
                        relation_index += 1
                        break
                    # end node
                    for type_key in type_to_ABC_dict.keys():
                        if node_e in type_to_ABC_dict[type_key]:
                            node_e_e = type_key
                            break
                    schema_sub = nodes_dict[node_keys_dict[node_e_e]]
                    schema_sub_dict = {}
                    for item_schema in schema_sub:
                        items_schema = item_schema.strip().strip(")").split("(")
                        schema_sub_dict[item_schema] = items_schema[0]
                        schema_sub_dict[items_schema[0]] = items_schema[0]
                        schema_sub_dict[items_schema[1]] = items_schema[0]
                    entity_subtype = get_type_of_first_entity(item_unmatched_entity, str(schema_sub), client)
                    subtype_name = entity_subtype.split('-')[-1]
                    if subtype_name in list(schema_sub_dict.keys()):
                        dsl_line = 'R' + str(sub_rule_index) + ': ' + chr(sub_Node_ABC) + '.' + schema_sub_dict[subtype_name] + '=="' + item_unmatched_entity + '"'
                        relation_in_dsl.append(dsl_line)
                        relation_index += 1
                        break
        else:
            path_dict = {}
            path_node = {}
            for key_node in type_to_ABC_dict.keys():
                path_dict[key_node] = [{key_node:key_node}]
                path_node[key_node] = [key_node]
            for_index = 0
            same_set = []

            while len(same_set) < 1:
                # cur_start_nodes = {}
                no_path = True
                for key in path_dict.keys():
                    if list(path_dict[key][-1].keys())[0] not in edge_end_to_start.keys():
                        continue
                    start_nodes = edge_end_to_start[list(path_dict[key][-1].keys())[0]]
                    path_cur_pre = path_dict[key][-1][list(path_dict[key][-1].keys())[0]]
                    nodes = []
                    for node in start_nodes:
                        if node not in path_node[key_node]:
                            nodes.append(node)
                            path_node[key].append(node)
                            path_dict[key].append({node: path_cur_pre + "," + node})
                    if len(nodes) > 0:
                        no_path = False
                if no_path:
                    break
                for_index = 0
                for key in path_node.keys():
                    for_index += 1
                    if for_index == 1:
                        same_set = path_node[key]
                    else:
                        same_set = list(set(same_set) & set(path_node[key]))

            if len(same_set) > 0:
                # no_matched_nodes
                sub_rules_dict = {}
                sub_type_to_ABC_dict = {}
                sub_entity_with_ABC_dict = {}
                sub_entities_in_dsl_dict = {}
                sub_relation_in_dsl_dict = {}
                for start_node_type in same_set:
                    # start_node_type = same_set[0]
                    sub_rules_list = []
                    sub_sub_type_to_ABC_dict = {}
                    sub_sub_entity_with_ABC_dict = {}
                    sub_entities_in_dsl_list = []
                    sub_relation_in_dsl_list = []
                    sub_rule_index = rule_index
                    sub_Node_ABC = Node_ABC
                    sub_relation_index = relation_index
                    unmached_nodes = copy.deepcopy(no_matched_nodes)
                    relation_middle_list = []
                    for key in path_dict.keys():
                        for i_path in range(len(path_dict[key]) - 1, -1, -1):
                            item = path_dict[key][i_path]
                            # for item in path_dict[key]:
                            if list(item.keys())[0] == start_node_type:
                                path_cur = item[list(item.keys())[0]].split(',')
                                break
                        for i_node in range(len(path_cur) - 1, 0, -1):
                            relation_middle_list.append(path_cur[i_node].strip() + '-' + path_cur[i_node - 1].strip())
                            if path_cur[i_node].strip() not in list(type_to_ABC_dict.keys()) + list(sub_sub_type_to_ABC_dict.keys()):
                                sub_sub_type_to_ABC_dict[path_cur[i_node].strip()] = [chr(sub_Node_ABC)]
                                sub_sub_entity_with_ABC_dict[path_cur[i_node - 1].strip()] = chr(sub_Node_ABC)
                                entity_dsl = chr(sub_Node_ABC) + ' [' + path_cur[i_node].strip() + ']'
                                sub_entities_in_dsl_list.append(entity_dsl)
                                if len(unmached_nodes) > 0:
                                    unmached_nodes_sub = []
                                    for item_unmatched_entity in unmached_nodes:
                                        schema_sub = nodes_dict[node_keys_dict[path_cur[i_node].strip()]]
                                        schema_sub_dict = {}
                                        for item_schema in schema_sub:
                                            items_schema = item_schema.strip().strip(")").split("(")
                                            schema_sub_dict[item_schema] = items_schema[0]
                                            schema_sub_dict[items_schema[0]] = items_schema[0]
                                            schema_sub_dict[items_schema[1]] = items_schema[0]
                                        entity_subtype = get_type_of_first_entity(item_unmatched_entity, str(schema_sub), client)
                                        subtype_name = entity_subtype.split('-')[-1]
                                        if subtype_name in list(schema_sub_dict.keys()):
                                            dsl_line = 'R' + str(sub_rule_index) + ': ' + chr(sub_Node_ABC) + '.' + schema_sub_dict[subtype_name] + '=="' + item_unmatched_entity + '"'
                                            sub_rules_list.append(dsl_line)
                                            sub_rule_index += 1
                                        else:
                                            unmached_nodes_sub.append(item_unmatched_entity)
                                        unmached_nodes = unmached_nodes_sub
                                sub_Node_ABC += 1
                            if path_cur[i_node - 1].strip() not in list(type_to_ABC_dict.keys()) + list(sub_sub_type_to_ABC_dict.keys()):
                                sub_sub_type_to_ABC_dict[path_cur[i_node - 1].strip()] = [chr(sub_Node_ABC)]
                                sub_sub_entity_with_ABC_dict[path_cur[i_node - 1].strip()] = chr(sub_Node_ABC)
                                entity_dsl = chr(sub_Node_ABC) + ' [' + path_cur[i_node - 1].strip() + ']'
                                sub_entities_in_dsl_list.append(entity_dsl)
                                if len(unmached_nodes) > 0:
                                    unmached_nodes_sub = []
                                    for item_unmatched_entity in unmached_nodes:
                                        schema_sub = nodes_dict[node_keys_dict[path_cur[i_node].strip()]]
                                        schema_sub_dict = {}
                                        for item_schema in schema_sub:
                                            items_schema = item_schema.strip().strip(")").split("(")
                                            schema_sub_dict[item_schema] = items_schema[0]
                                            schema_sub_dict[items_schema[0]] = items_schema[0]
                                            schema_sub_dict[items_schema[1]] = items_schema[0]
                                        entity_subtype = get_type_of_first_entity(item_unmatched_entity, str(schema_sub), client)
                                        subtype_name = entity_subtype.split('-')[-1]
                                        if subtype_name in list(schema_sub_dict.keys()):
                                            dsl_line = 'R' + str(sub_rule_index) + ': ' + chr(sub_Node_ABC) + '.' + schema_sub_dict[subtype_name] + '=="' + item_unmatched_entity + '"'
                                            sub_rules_list.append(dsl_line)
                                            sub_rule_index += 1
                                        else:
                                            unmached_nodes_sub.append(item_unmatched_entity)
                                        unmached_nodes = unmached_nodes_sub
                                sub_Node_ABC += 1

                    relation_middle_list = list(set(relation_middle_list))
                    using_type_to_ABC_dict = copy.deepcopy(type_to_ABC_dict)
                    using_type_to_ABC_dict.update(sub_sub_type_to_ABC_dict)
                    for relation_item in relation_middle_list:
                        item_s = using_type_to_ABC_dict[relation_item.split('-')[0]][0]
                        item_e = using_type_to_ABC_dict[relation_item.split('-')[1]][0]
                        if item_s != item_e:
                            realtion_type = edge_type_dict[relation_item]
                            dsl_line = item_s + ' -> ' + item_e + ' [' + realtion_type + '] as E' + str(sub_relation_index)
                            sub_relation_in_dsl_list.append(dsl_line)
                            sub_relation_index += 1

                    if len(unmached_nodes) < 1:
                        rule_in_dsl = rule_in_dsl + sub_rules_list
                        type_to_ABC_dict.update(sub_sub_type_to_ABC_dict)
                        entity_with_ABC.update(sub_sub_entity_with_ABC_dict)
                        entities_in_dsl = entities_in_dsl + sub_entities_in_dsl_list
                        relation_in_dsl = relation_in_dsl + sub_relation_in_dsl_list
                        break
                    else:
                        sub_rules_dict[start_node_type + ',' + str(len(unmached_nodes))] = sub_rules_list
                        sub_type_to_ABC_dict[start_node_type] = sub_sub_type_to_ABC_dict
                        sub_entity_with_ABC_dict[start_node_type] = sub_sub_entity_with_ABC_dict
                        sub_entities_in_dsl_dict[start_node_type] = sub_entities_in_dsl_list
                        sub_relation_in_dsl_dict[start_node_type] = sub_relation_in_dsl_list

                if len(unmached_nodes) > 0:
                    min_unmached_key = ""
                    min_num = 1000000
                    for sub_rule_key in sub_rules_dict.keys():
                        sub_rule_items = sub_rule_key.split(",")
                        if int(sub_rule_items[1]) < min_num:
                            min_unmached_key = sub_rule_key
                            min_num = int(sub_rule_items[1])
                    key_num = min_unmached_key.split(',')
                    rule_in_dsl = rule_in_dsl + sub_rules_dict[min_unmached_key]
                    type_to_ABC_dict.update(sub_type_to_ABC_dict[key_num[0]])
                    entity_with_ABC.update(sub_entity_with_ABC_dict[key_num[0]])
                    entities_in_dsl = entities_in_dsl + sub_entities_in_dsl_dict[key_num[0]]
                    relation_in_dsl = relation_in_dsl + sub_relation_in_dsl_dict[key_num[0]]

    # DSL-1.0
    # dsl = """GraphStructure {\n"""
    # dsl += "\n".join(entities_in_dsl) + '\n'
    # dsl += "\n".join(relation_in_dsl) + '\n'
    # dsl += """}\nRule {\n"""
    # dsl += '\n'.join(rule_in_dsl) + '\n'
    # dsl += """}\nAction {\nget("""
    # res_list = []
    # for key_abc in entity_with_ABC.keys():
    #     res_list.append(entity_with_ABC[key_abc] + ".name")
    # res_list = sorted(res_list)
    # dsl += ','.join(res_list)
    # dsl += """)\n}"""

    # DSL-2.0
    res_list = []
    for key_abc in entity_with_ABC.keys():
        res_list.append(entity_with_ABC[key_abc] + ".name")
    res_list = sorted(res_list)
    dsl = dsl_v1_to_V2(entities_in_dsl, relation_in_dsl, rule_in_dsl, res_list)

    return dsl


def dsl_v1_to_V2(entities, relations, rules, actions):
    entities_with_index = {}
    for entity in entities:
        items = entity.strip().strip(']').split(',')[0].split('[')
        entities_with_index[items[0].strip()] = items[1].strip()

    res_relations = []
    entity_to_index = {}
    num_s = 1
    num_r = 1
    num_e = 1
    for relation in relations:
        items = relation.split("as")[0].strip().strip(']').split('[')
        entity_pair = items[0].strip().split('->')
        entity_s = entities_with_index[entity_pair[0].strip()]
        entity_e = entities_with_index[entity_pair[1].strip()]
        relation_m = items[1].strip()
        res_relations_line = ''

        if entity_s not in entity_to_index.keys():
            s_index = 's' + str(num_s)
            res_relations_line += '(' + s_index + ':' + entity_s + ')-'
            entity_to_index[entity_s] = s_index
            num_s += 1
        else:
            s_index = entity_to_index[entity_s]
            res_relations_line += '(' + s_index + ')-'

        res_relations_line += '[p' + str(num_r) + ':' + relation_m + ']->'
        num_r += 1

        if entity_e not in entity_to_index.keys():
            e_index = 'o' + str(num_e)
            res_relations_line += '(' + e_index + ':' + entity_e + ')'
            entity_to_index[entity_e] = e_index
            num_e += 1
        else:
            e_index = entity_to_index[entity_e]
            res_relations_line += '(' + e_index + ')'

        res_relations.append(res_relations_line)

    res_rule = []
    for rule in rules:
        items = rule.split(':')
        entity_index_old = items[1].strip().split('.')[0]
        entity_index_new = entity_to_index[entities_with_index[entity_index_old]]

        rule_list = [items[0]]
        rule_list.append(entity_index_new + '.' + items[1].strip().split('.')[1])
        res_rule.append(': '.join(rule_list))

    res_action = []
    for action in actions:
        items = action.split('.')
        entity_index_old = items[0]
        entity_index_new = entity_to_index[entities_with_index[entity_index_old]]
        res_action.append(entity_index_new + '.' + items[1])

    result_dsl = """Structure {\n"""
    result_dsl += '\n'.join(res_relations) + '\n'
    result_dsl += """}\nConstraint {\n"""
    result_dsl += '\n'.join(res_rule) + '\n'
    result_dsl += """}\nAction {\nget("""
    result_dsl += ','.join(res_action)
    result_dsl += """)\n}"""

    return result_dsl


class NL2DSL(ExtractOp):

    schema_template = """Schema: 
Node: ${nodes}
Edge: ${edges}"""

    def __init__(self, params: Dict[str, str]):
        super().__init__(params)
        self.nl2dsl_client = MayaHttpClient(
            scene_name="Qwen1_5_72B_Chat_GPTQ_Int4",
            chain_name="v1",
            use_pre=True,
        )
        self.namespace = params.get("namespace", "DEFAULT") if params else "DEFAULT"
        self.project_id = params.get("project_id", 1) if params else 1
        os.environ["KNEXT_PROJECT_ID"] = str(self.project_id)
        self.schema = self.render_schema()
        print(self.schema)

    def render_schema(self):
        schema = SchemaClient()
        session = schema.create_session()
        spg_types = session.spg_types
        nodes = {}
        edges = []
        for spg_type_name, spg_type in spg_types.items():
            props = []
            if spg_type.spg_type_enum == SpgTypeEnum.Entity:
                if "Person" not in spg_type_name:
                    props.append("name(名称)")
                else:
                    for prop_name, prop in spg_type.properties.items():
                        if prop_name in ["id", "description"]:
                            continue
                        props.append(f"{prop_name}({prop.name_zh})")
            if spg_type.spg_type_enum == SpgTypeEnum.Event:
                for prop_name, prop in spg_type.properties.items():
                    if prop_name in ["id", "description"]:
                        continue
                    props.append(f"{prop_name}({prop.name_zh})")
                for rel_name, rel in spg_type.relations.items():
                    if spg_type.spg_type_enum == SpgTypeEnum.Entity:
                        continue
                    edges.append(f"{spg_type_name}-{rel_name.split('_')[0]}({rel.name_zh})-{rel.object_type_name}")
            if props:
                name = f"{spg_type_name}({spg_type.name_zh})"
                nodes[name] = props
                json.dumps(nodes,ensure_ascii=False)
        return self.schema_template.replace("${nodes}", json.dumps(nodes,ensure_ascii=False)).replace("${edges}", json.dumps(edges,ensure_ascii=False))

    def invoke(self, record: Dict[str, str]) -> str:
        query = record.get("input")
        dsl_result = query_transfer_to_dsl(query, self.schema, self.nl2dsl_client)
        return dsl_result

if __name__ == '__main__':
    query = "周杰伦成立的公司"
    nl2dsl = NL2DSL(params={"namespace": "Demo", "project_id": 2})
    record = {"input": query}
    print(nl2dsl.invoke(record))
