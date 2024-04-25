from bondzai.idetect40_interface.dict import check_dict_equity
from bondzai.idetect40_interface.exchange_table import ExchangeTableConverter


TEST_DESCRIPTOR = {
    "agents": {
        "nb_sources": 4,
        "nb_agents": 4
    },
    "attributes": [
        {
            "name": "serial number",
            "type": "INT",
            "size": 16
        },
        {
            "name": "vehicule type",
            "type": "STRING",
            "size": 24
        },
        {
            "name": "temperature",
            "type": "FLOAT",
            "size": 32
        },
        {
            "name": "over pressure",
            "type": "BOOL",
            "size": 1
        }
    ]
}

class Test_ExchangeTableConverter():
    exchange_table_converter = ExchangeTableConverter(TEST_DESCRIPTOR)
    is_connected = False
    error_code = 7
    input_table = {
        "system": {"running": True, "process_ongoing": False, "heart_beat": False, 
                   "ack_result": True, "ack_exception": True},
        "agents": {
            1: {"active": True, "sources": {1: True, 2: False, 3: True, 4: False}},
            2: {"active": True, "sources": {1: False, 2: False, 3: True, 4: False}},
            3: {"active": False, "sources": {1: True, 2: True, 3: True, 4: False}},
            4: {"active": False, "sources": {1: True, 2: False, 3: True, 4: True}}
        },
        "attributes": {"serial number": 12, "vehicule type": "abc", "temperature": 48.70000076293945, 
                       "over pressure": False}
        }
    input_bin_table = bytearray([25, 0, 11, 0, 9, 0, 14, 0, 26, 0, 12, 0, 97, 98, 99, 0, 205, 204, 66, 66, 0, 0])
    output_table = {
        "system": {"running": True, "process_ongoing": False, "heart_beat": False, "exception_occured": True, 
                "exception": error_code},
        "agents": {
        1: {"active": True, "sources": {1: True, 2: False, 3: True, 4: False}},
        2: {"active": True, "sources": {1: False, 2: False, 3: True, 4: False}},
        3: {"active": False, "sources": {1: True, 2: True, 3: True, 4: False}},
        4: {"active": False, "sources": {1: True, 2: False, 3: True, 4: True}}
        },
        "result": {"agent_id": 1, "source_id": 3, "key_id": 1, "value_id": 6, "category_id": 4},
        "attributes": {"serial number": 12, "vehicule type": "ab", "temperature": 48.70000076293945, 
                       "over pressure": False}
        } 
    output_bin_table = bytearray([9, error_code, 11, 0, 9, 0, 14, 0, 26, 0, 1, 3, 1, 6, 4, 0, 12, 0, 97, 98, 0, 0, 205, 
                                  204, 66, 66, 0, 0])
           
    def test_msg_to_table(self):
        result = self.exchange_table_converter.msg_to_table(self.input_bin_table) 
        assert check_dict_equity(result, self.input_table)
        result = self.exchange_table_converter.msg_to_table(self.output_bin_table) 
        assert check_dict_equity(result, self.output_table)

    def test_table_to_msg(self):
        result = self.exchange_table_converter.table_to_msg(self.input_table) 
        assert result == self.input_bin_table
        result = self.exchange_table_converter.table_to_msg(self.output_table) 
        assert result == self.output_bin_table
    
    def test_get_input_table_size(self):
        input_size = self.exchange_table_converter.get_input_table_size()
        assert input_size == len(self.input_bin_table)
    
    def test_get_output_table_size(self):
        output_size = self.exchange_table_converter.get_output_table_size()
        assert output_size == len(self.output_bin_table)
