
from enum import Enum
import struct
from typing import Any

import numpy as np

class ComProtocolType(Enum):
    DIRECT = "direct"
    MODBUS = "modbus"
    S7_NET = "s7_net"

def get_byte_len(bit_len: int) -> (int, int):
    """get the size of an attribute whose size is given in bit

    Args:
        int (_type_): size of attribute in bit

    Returns:
        int: size in bytes
        int: size in words
    """
    byte_len = int(np.ceil(bit_len / 8))
    word_byte_len = byte_len + (byte_len % 2)
    return byte_len, word_byte_len
    
def int_to_bool_list(n):
    return [bool(n & (1 << i)) for i in range(0, 8)]

def bool_list_to_int(bool_list) -> int:
    byte_value = 0
    for i, bit in enumerate(bool_list):
        if bit:
            byte_value |= 1 << i
    return byte_value

class AttributeDataType(Enum):
    BOOL = "BOOL"
    INT = "INT"
    STRING = "STRING"
    FLOAT = "FLOAT" # TODO : check if necessary

    def to_type(self) -> type:
        """Get associated python type

        Returns:
            type: python type
        """
        if self == AttributeDataType.BOOL:
            data_type = bool
        elif self == AttributeDataType.INT:
            data_type = int
        elif self == AttributeDataType.STRING:
            data_type = str
        elif self == AttributeDataType.FLOAT:
            data_type = float
        return data_type
    
    def get_null(self) -> Any:
        """Get associated null value

        Returns:
            Any: null value of correct type
        """
        if self == AttributeDataType.BOOL:
            null_value = False
        elif self == AttributeDataType.INT:
            null_value = 0
        elif self == AttributeDataType.STRING:
            null_value = "\0"
        elif self == AttributeDataType.FLOAT:
            null_value = 0.0
        return null_value
    
    def __str__(self) -> str:
        return self.value

class Attribute():
    def __init__(self, name: str, attr_type: AttributeDataType, size: int) -> None:
        self.name = name
        self.type = attr_type
        self.value = attr_type.get_null()
        self.size = size
    
    def __eq__(self, other) -> bool:
        eq = self.name == other.name and self.type == other.type and self.value == other.value and self.size == other.size
        return eq
    
class Agent():
    def __init__(self, agent_id: int, source_nb: int):
        self.active = False
        self.agent_id = agent_id
        self.source_dict = {src_id: False for src_id in range(1, source_nb + 1)}
    
    def set_active(self, active: bool):
        self.active = active
    
    def get_state(self):
        return self.active
    
    def set_source_active(self, source_id: int, active: bool):
        self.source_dict[source_id] = active
    
    def get_source_state(self, source_id: int):
        return self.source_dict[source_id]
    
    def __eq__(self, other) -> bool:
        eq = self.active == other.active and self.agent_id == other.agent_id
        for source_id, active in self.source_dict.items():
            eq = eq and other.source_dict[source_id] == active
        return eq


class ExchangeTable:
    def __init__(self, descriptor: dict, msg: bytearray = None):
        self.system_running = False
        self.process_ongoing = False
        self.heartbeat = False
        self.nb_sources = descriptor["agents"]["nb_sources"]
        self.agents = {agent_id: Agent(agent_id, self.nb_sources) 
                       for agent_id in range(1, descriptor["agents"]["nb_agents"] + 1)}
        self.attributes = [Attribute(attr["name"], AttributeDataType(attr["type"]), attr["size"]) 
                           for attr in descriptor["attributes"]]
        if msg is not None:
            self.init_from_msg(msg)
    
    def init_from_msg(self, msg: bytearray):
        """Convert bytes message to table

        Args:
            binary (bytearray): message as array of bytes

        Returns:
            dict: table as dict
        """
        byte_offset = 0
        msg_int_list = [int(byte) for byte in msg]
        self.set_system_word(int_to_bool_list(msg_int_list[0]) + int_to_bool_list(msg_int_list[1]))
        byte_offset += 2
        agent_bin_table = msg_int_list[byte_offset:byte_offset + 2 * len(self.agents)]
        for index in range(0, len(agent_bin_table), 2):
            agent_bin_data = int_to_bool_list(agent_bin_table[index]) + int_to_bool_list(agent_bin_table[index + 1])
            agent_id = index // 2 + 1
            self.activate_agent(agent_id, agent_bin_data[0])
            for source_id in range(1, self.nb_sources + 1):
                self.activate_source(agent_id, source_id, agent_bin_data[source_id])
            byte_offset += 2
        byte_offset += self.set_result_word(msg_int_list[byte_offset: byte_offset + 6])
        attr_bin_table = msg[byte_offset:]
        idx = 0
        for attribute in self.attributes:
            byte_len, word_byte_len = get_byte_len(attribute.size)
            value_array = attr_bin_table[idx: idx + byte_len]
            idx += word_byte_len
            if attribute.type == AttributeDataType.STRING:
                value = str(value_array.decode("utf8")).rstrip("\x00")
            elif attribute.type == AttributeDataType.INT:
                value = int.from_bytes(value_array, byteorder="little")
            elif attribute.type == AttributeDataType.FLOAT:
                value = struct.unpack('f',value_array)[0]
            elif attribute.type == AttributeDataType.BOOL:
                value = struct.unpack("?", value_array)[0] # TODO : Check if other value next to it
            attribute.value = value
    
    def __len__(self) -> int:
        """Get size of the table

        Returns:
            int: size of the table in bytes
        """
        nb_agent = len(self.agents)
        system_size = 2
        agent_size = nb_agent * 2
        attribute_size = sum([get_byte_len(attr.size)[1] for attr in self.attributes])
        output_size = system_size + agent_size + attribute_size
        return output_size
    
    def set_system_running(self, running: bool):
        self.system_running = running
    
    def get_system_running(self):
        return self.system_running
    
    def set_process_ongoing(self, ongoing: bool):
        self.process_ongoing = ongoing
    
    def get_process_ongoing(self):
        return self.process_ongoing
    
    def set_heart_beat(self, heartbeat: bool):
        self.heartbeat = heartbeat
    
    def get_heart_beat(self):
        return self.heartbeat
    
    def get_system_word(self):
        return [self.get_system_running(), self.get_process_ongoing(), self.get_heart_beat()] + [False] * 13
    
    def set_system_word(self, word: list[bool]):
        self.set_system_running(word[0])
        self.set_process_ongoing(word[1])
        self.set_heart_beat(word[2])
        
    def get_result_word(self):
        return []
    
    def set_result_word(self, word: list[int]):
        return 0
    
    def activate_agent(self, agent_id: int, active: bool):
        self.agents[agent_id].set_active(active)
    
    def get_agent_state(self, agent_id: int):
        return self.agents[agent_id].get_state()
    
    def activate_source(self, agent_id: int, source_id: int, active: bool):
        self.agents[agent_id].set_source_active(source_id, active)

    def get_source_state(self, agent_id: int, source_id: int):
        return self.agents[agent_id].get_source_state(source_id)
    
    def _get_attribute_by_name(self, attribute_name: str) -> Attribute:
        attribute = None
        for _attribute in self.attributes:
            if _attribute.name == attribute_name:
                attribute = _attribute
                break
        return attribute
    
    def get_attribute_value(self, attribute_name: str) -> Any:
        return self._get_attribute_by_name(attribute_name).value
    
    def set_attribute_value(self, attribute_name: str, value: Any):
        self._get_attribute_by_name(attribute_name).value = value
    
    def to_msg(self) -> bytearray:
        """Convert table to a bytearray
        Returns:
            bytearray: message as array of bytes
        """
        byte_array = bytearray()
        system_word = self.get_system_word()
        byte_array.extend([bool_list_to_int(system_word[:7]), bool_list_to_int(system_word[7:])])
        for agent_id in range(1, len(self.agents) + 1):
            agent_integer = int(self.get_agent_state(agent_id))
            for source_id in range(1, self.nb_sources + 1):
                agent_integer += int(self.get_source_state(agent_id, source_id)) * 2 ** (source_id)
            byte_array += agent_integer.to_bytes(2, "little")
        byte_array.extend(self.get_result_word())
        for attribute in self.attributes:
            byte_nb = int(np.ceil(attribute.size / 16)) * 2
            value = attribute.value
            if attribute.type == AttributeDataType.STRING:
                value_array = attribute.value.encode("utf8")
            elif attribute.type ==  AttributeDataType.INT:
                value_array = attribute.value.to_bytes(int(attribute.size / 8), byteorder="little")
            elif attribute.type ==  AttributeDataType.FLOAT:
                value_array = struct.pack('f',value)
            elif attribute.type ==  AttributeDataType.BOOL:
                value_array = struct.pack("?", value)
            byte_array += bytearray(value_array) + int(0).to_bytes(byte_nb - len(value_array), byteorder="little")
        return byte_array
    
    # def to_dict(self) -> dict:
    #     input_table = {
    #     "system": {"running": True, "process_ongoing": False, "heart_beat": False, 
    #                "ack_result": True, "ack_exception": True},
    #     "agents": {
    #         1: {"active": True, "sources": {1: True, 2: False, 3: True, 4: False}},
    #         2: {"active": True, "sources": {1: False, 2: False, 3: True, 4: False}},
    #         3: {"active": False, "sources": {1: True, 2: True, 3: True, 4: False}},
    #         4: {"active": False, "sources": {1: True, 2: False, 3: True, 4: True}}
    #     },
    #     "attributes": {"serial number": 12, "vehicule type": "abc", "temperature": 48.70000076293945, 
    #                    "over pressure": False}
    #     }
    
    def __eq__(self, other):
        eq = self.system_running == other.system_running
        eq = eq and self.process_ongoing == other.process_ongoing
        eq = eq and self.heartbeat == other.heartbeat
        for agent_id, agent in self.agents.items():
            eq = eq and other.agents[agent_id] == agent
        for idx, attribute in enumerate(self.attributes):
            eq = eq and other.attributes[idx] == attribute
        return eq


class PLCTable(ExchangeTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ack_result = False
        self.ack_exception = False
    
    def set_ack_result(self, ack: bool):
        self.ack_result = ack
    
    def get_ack_result(self):
        return self.ack_result
    
    def set_ack_exception(self, ack: bool):
        self.ack_exception = ack
    
    def get_ack_exception(self):
        return self.ack_exception
    
    def get_system_word(self):
        system_word = super().get_system_word()
        system_word[3]= self.get_ack_result()
        system_word[4] = self.get_ack_exception()
        return system_word
    
    def set_system_word(self, word: list[bool]):
        super().set_system_word(word)
        self.set_ack_result(word[3])
        self.set_ack_exception(word[4])

class I40Table(ExchangeTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exception_occured = False
        self.exception_code = 0
        self.result = {"agent_id": 0, "source_id": 0, "key_id": 0, "value_id": 0, "category_id": 0}
    
    def __len__(self) -> int:
        result_size = 6
        return super().__len__() + result_size

    def set_exception_occured(self, is_exception: bool):
        self.exception_occured = is_exception
    
    def get_exception_occured(self):
        return self.exception_occured
    
    def set_exception(self, exception_code: bool):
        self.exception_code = exception_code
    
    def get_exception(self):
        return self.exception_code
    
    def get_system_word(self):
        system_word = super().get_system_word()
        system_word[3]= self.get_exception_occured()
        system_word[7:] = int_to_bool_list(self.get_exception())
        return system_word
    
    def set_system_word(self, word: list[bool]):
        super().set_system_word(word)
        self.set_exception_occured(word[3])
        self.set_exception(bool_list_to_int(word[7:]))
    
    def get_result_word(self):
        return [self.result["agent_id"], self.result["source_id"], 
                self.result["key_id"], self.result["value_id"], self.result["category_id"], 0]
    
    def set_result_word(self, word: list[int]):
        self.set_result(word[0], word[1], word[2], word[3], word[4])
        return 6
    
    def set_result(self, agent_id: int, source_id: int, key_id: int, value_id: int, category_id: int):
        self.result = {"agent_id": agent_id, "source_id": source_id, "key_id": key_id, 
                       "value_id": value_id, "category_id": category_id}
    
    def get_result(self):
        return self.result  
