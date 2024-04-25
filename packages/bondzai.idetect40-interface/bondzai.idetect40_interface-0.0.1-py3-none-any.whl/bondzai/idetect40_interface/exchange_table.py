
from enum import Enum
import struct
from typing import Any
import numpy as np

class ComProtocolType(Enum):
    DIRECT = "direct"
    MODBUS = "modbus"
    S7_NET = "s7_net"

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

class ExchangeTableConverter():
    """Class to convert bytearray message to an exchange table as dict
    """
    def __init__(self, descriptor: dict = None) -> None:
        self.descriptor = descriptor
    
    def _get_byte_len(self, bit_len: int) -> (int, int):
        """Internal method to get the size of an attribute whose size is given in bit

        Args:
            int (_type_): size of attribute in bit

        Returns:
            int: size in bytes
            int: size in words
        """
        byte_len = int(np.ceil(bit_len / 8))
        word_byte_len = byte_len + (byte_len % 2)
        return byte_len, word_byte_len
    
    def get_output_table_size(self) -> int:
        """Get size of the output table (I40 table)

        Returns:
            int: size of the table in bytes
        """
        input_table = self.get_input_table_size()
        result_size = 6
        output_size = input_table + result_size
        return output_size

    def get_input_table_size(self) -> int:
        """Get size of the input table (automate table)

        Returns:
            int: size of the table in bytes
        """
        nb_agent = self.descriptor["agents"]["nb_agents"]
        system_size = 2
        agent_size = nb_agent * 2
        attribute_size = sum([self._get_byte_len(att_dict["size"])[1] for att_dict in self.descriptor["attributes"]])
        output_size = system_size + agent_size + attribute_size
        return output_size

    
    def msg_to_table(self, binary: bytearray) -> dict:
        """Convert bytes message to table

        Args:
            binary (bytearray): message as array of bytes

        Returns:
            dict: table as dict
        """
        table = {"system": {}, "agents": {}, "attributes": {}}
        nb_agent = self.descriptor["agents"]["nb_agents"]
        nb_sources = self.descriptor["agents"]["nb_sources"]
        byte_offset = 0
        system_bin_data = int.from_bytes(binary[byte_offset:byte_offset + 1], byteorder="little")
        bin_len = len(binary)
        expected_output_size = self.get_output_table_size()
        is_output_table = bin_len == expected_output_size
        if is_output_table:
            system_key_list = ["running", "process_ongoing", "heart_beat", "exception_occured"]
        else:
            system_key_list = ["running", "process_ongoing", "heart_beat", "ack_result", "ack_exception"]
        table["system"] = {key: bool(system_bin_data & 2**idx) for idx, key in enumerate(system_key_list)}
        byte_offset += 1
        if is_output_table:
            table["system"]["exception"] = int.from_bytes(binary[byte_offset:byte_offset + 1], byteorder="little")
        byte_offset += 1
        agent_bin_table = binary[byte_offset:byte_offset + 2*nb_agent]
        for index in range(0, len(agent_bin_table), 2):
            agent_bin_data = int.from_bytes(agent_bin_table[index: index + 2], byteorder="little")
            source_dict = {_nb: bool(agent_bin_data & (2**_nb)) for _nb in range(1, nb_sources + 1)}
            table["agents"][index // 2 + 1] = {"active": bool(agent_bin_data & 1), "sources": source_dict}
            byte_offset += 2
        if is_output_table:
            table["result"] = {}
            result_key_list = ["agent_id", "source_id", "key_id", "value_id", "category_id"]
            for idx, key in enumerate(result_key_list):
                table["result"][key] = int.from_bytes(binary[byte_offset :byte_offset + 1], byteorder="little")
                byte_offset += 1 
            byte_offset += 1  
        attr_bin_table = binary[byte_offset:]
        idx = 0
        for attribute_desc in self.descriptor["attributes"]:
            size = attribute_desc["size"]
            byte_len, word_byte_len = self._get_byte_len(size)
            value_array = attr_bin_table[idx: idx + byte_len]
            idx += word_byte_len
            attr_type = AttributeDataType(attribute_desc["type"])
            if attr_type == AttributeDataType.STRING:
                value = str(value_array.decode("utf8")).rstrip("\x00")
            elif attr_type == AttributeDataType.INT:
                value = int.from_bytes(value_array, byteorder="little")
            elif attr_type == AttributeDataType.FLOAT:
                value = struct.unpack('f',value_array)[0]
            elif attr_type == AttributeDataType.BOOL:
                value = struct.unpack("?", value_array)[0] # TODO : Check if other value next to it
            table["attributes"][attribute_desc["name"]] = value
        return table
    
    def table_to_msg(self, table: dict) -> bytearray:
        """Convert bytes message to table
        Args:
            table (dict): table as dict

        Returns:
            bytearray: message as array of bytes
        """
        nb_sources = self.descriptor["agents"]["nb_sources"]
        byte_array = bytearray()
        system_integer = 0
        is_output_table = table.get("result", None) is not None
        if is_output_table:
            system_key_list = ["running", "process_ongoing", "heart_beat", "exception_occured"]
        else:
            system_key_list = ["running", "process_ongoing", "heart_beat", "ack_result", "ack_exception"]
        for index, key in enumerate(system_key_list):
            system_integer += int(table["system"][key]) * 2 ** (index)
        byte_array += bytearray([system_integer, table["system"].get("exception", 0)])
        for agent_index in range(1, self.descriptor["agents"]["nb_agents"] + 1):
            agent_desc = table["agents"][agent_index]
            agent_integer = int(agent_desc["active"])
            for source_nb in range(1, nb_sources + 1):
                agent_integer+= int(agent_desc["sources"].get(source_nb, False)) * 2 ** (source_nb)
            byte_array += agent_integer.to_bytes(2, "little")
        if is_output_table:
            result_desc = table["result"]
            byte_array.append(result_desc["agent_id"])
            byte_array.append(result_desc["source_id"])
            byte_array.append(result_desc["key_id"])
            byte_array.append(result_desc["value_id"])
            byte_array.append(result_desc["category_id"])
            byte_array.append(0)
        for attribute_desc in self.descriptor["attributes"]:
            attr_name = attribute_desc["name"]
            size = attribute_desc["size"]
            value = table["attributes"][attr_name]
            byte_nb = int(np.ceil(size / 16)) * 2
            attr_type = AttributeDataType(attribute_desc["type"])
            if attr_type == AttributeDataType.STRING:
                value_array = value.encode("utf8")
            elif attr_type ==  AttributeDataType.INT:
                value_array = value.to_bytes(int(size / 8), byteorder="little")
            elif attr_type ==  AttributeDataType.FLOAT:
                value_array = struct.pack('f',value)
            elif attr_type ==  AttributeDataType.BOOL:
                value_array = struct.pack("?", value)
            byte_array += bytearray(value_array) + int(0).to_bytes(byte_nb - len(value_array), byteorder="little")
        return byte_array
    
