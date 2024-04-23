from typing import Dict, List

from knext.builder.operator.spg_record import SPGRecord
from knext.schema.model.base import BaseSpgType, ConstraintTypeEnum, SpgTypeEnum


class Node(object):
    id: str
    name: str
    label: str
    properties: Dict[str, str]
    hash_map: Dict[int, str] = dict()

    def __init__(self, _id: str, name: str, label: str, properties: Dict[str, str]):
        self.name = name
        self.label = label
        self.properties = properties
        self.id = _id

    @classmethod
    def from_spg_record(cls, idx, spg_record: SPGRecord):
        return cls(
            _id=idx,
            name=spg_record.get_property("name"),
            label=spg_record.spg_type_name,
            properties=spg_record.properties,
        )

    @staticmethod
    def unique_key(spg_record):
        return spg_record.spg_type_name + '_' + spg_record.get_property("name", "")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "label": self.label,
            "properties": self.properties,
        }


class Edge(object):
    id: str
    from_id: str
    from_type: str
    to_id: str
    to_type: str
    label: str
    properties: Dict[str, str]

    def __init__(
            self, _id: str, from_node: Node, to_node: Node, label: str, properties: Dict[str, str]
    ):
        self.from_id = from_node.id
        self.from_type = from_node.label
        self.to_id = to_node.id
        self.to_type = to_node.label
        self.label = label
        self.properties = properties
        if not _id:
            _id = id(self)
        self.id = _id

    @classmethod
    def from_spg_record(
            cls, s_idx, subject_record: SPGRecord, o_idx, object_record: SPGRecord, label: str
    ):
        from_node = Node.from_spg_record(s_idx, subject_record)
        to_node = Node.from_spg_record(o_idx, object_record)

        return cls(_id="", from_node=from_node, to_node=to_node, label=label, properties={})

    def to_dict(self):
        return {
            "id": self.id,
            "from": self.from_id,
            "to": self.to_id,
            "fromType": self.from_type,
            "toType": self.to_type,
            "label": self.label,
            "properties": self.properties,
        }


class SubGraph(object):
    nodes: List[Node] = list()
    edges: List[Edge] = list()

    def __init__(self, nodes: List[Node], edges: List[Edge]):
        self.nodes = nodes
        self.edges = edges

    def to_dict(self):
        return {
            "resultNodes": [n.to_dict() for n in self.nodes],
            "resultEdges": [e.to_dict() for e in self.edges],
        }

    @staticmethod
    def filter_record(spg_record: SPGRecord, spg_type: BaseSpgType):

        filtered_properties, filtered_relations = {}, {}
        for prop_name, prop_value in spg_record.properties.items():
            if prop_value != 'NAN':
                filtered_properties[prop_name] = prop_value
        for rel_name, rel_value in spg_record.relations.items():
            if rel_value != 'NAN':
                filtered_relations[rel_name] = rel_value
        spg_record.properties = filtered_properties
        spg_record.relations = filtered_relations

        # if len(spg_record.properties) == 1 and spg_record.get_property("name"):
        #     print("filtered_entity: ")
        #     print(spg_record)
        #     return None
        if spg_type.spg_type_enum == SpgTypeEnum.Event and \
                (spg_type.properties.get('subject') and not spg_record.properties.get('subject')) and \
                (spg_type.properties.get('object') and not spg_record.properties.get('object')) and \
                (spg_type.properties.get('eventTime') and not spg_record.properties.get('eventTime')):
            print("filtered_event: ")
            print(spg_record)
            return None
        else:
            return spg_record

    @staticmethod
    def filter_node(nodes: List[Node], edges: List[Edge]):
        ids = []
        filtered_nodes = []
        for edge in edges:
            ids.extend([edge.from_id, edge.to_id])
        for node in nodes:
            if len(node.properties) == 1 and node.properties.get("name"):
                if node.id not in ids:
                    print("filtered_node: ")
                    print(node)
                    continue
            filtered_nodes.append(node)
        return filtered_nodes


    @classmethod
    def from_spg_record(
            cls, spg_types: Dict[str, BaseSpgType], spg_records: List[SPGRecord]
    ):
        nodes, edges = set(), set()
        filtered_records = []
        for subject_record in spg_records:
            spg_type_name = subject_record.spg_type_name
            spg_type = spg_types.get(spg_type_name)
            filtered_record = cls.filter_record(subject_record, spg_type)
            if filtered_record:
                filtered_records.append(filtered_record)
        for idx, subject_record in enumerate(filtered_records):
            from_node = Node.from_spg_record(idx, subject_record)
            spg_type_name = subject_record.spg_type_name
            spg_type = spg_types.get(spg_type_name)
            removed_props = []
            for prop_name, prop_value in subject_record.properties.items():
                prop = spg_type.properties.get(prop_name)
                object_type_name = prop.object_type_name
                if prop.constraint.get(ConstraintTypeEnum.MultiValue):
                    prop_value_list = prop_value.split(",")
                else:
                    prop_value_list = [prop_value]
                removed_values = []
                for value in prop_value_list:
                    for o_idx, object_record in enumerate(filtered_records):
                        if (
                                object_record.spg_type_name == object_type_name
                                and (object_record.get_property("name") == value or value in object_record.get_property("alias", "").split(','))
                        ):
                            removed_values.append(value)
                            edge = Edge.from_spg_record(
                                idx, subject_record, o_idx, object_record, prop_name
                            )
                            edges.add(edge)
                if removed_values == prop_value_list:
                    removed_props.append(prop_name)
            for prop in removed_props:
                from_node.properties.pop(prop)
            nodes.add(from_node)

        nodes = cls.filter_node(list(nodes), list(edges))

        return cls(nodes=list(nodes), edges=list(edges)).to_dict()
