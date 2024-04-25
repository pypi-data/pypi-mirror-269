from bondzai.idetect40_interface.exchange_table import ExchangeTable, I40Table, PLCTable


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

def table_from_dict(descriptor: dict, d: dict) -> ExchangeTable:
    if "result" in d:
        table = I40Table(descriptor)
        table.set_exception_occured(d["system"]["exception_occured"])
        table.set_exception(d["system"]["exception"])
        table.set_result(d["result"]["agent_id"], d["result"]["source_id"], d["result"]["key_id"], 
                         d["result"]["value_id"], d["result"]["category_id"])
    else:
        table = PLCTable(descriptor)
        table.set_ack_result(d["system"]["ack_result"])
        table.set_ack_exception(d["system"]["ack_exception"])
    table.set_system_running(d["system"]["running"])
    table.set_process_ongoing(d["system"]["process_ongoing"])
    table.set_heart_beat(d["system"]["heart_beat"])
    for agent_id, agent_dict in d["agents"].items():
        table.activate_agent(agent_id, agent_dict["active"])
        for source_id, scr_active in agent_dict["sources"].items():
            table.activate_source(agent_id, source_id, scr_active)
    for attribute_name, value in d["attributes"].items():
        table.set_attribute_value(attribute_name, value)
    return table
    


class Test_ExchangeTable():
    is_connected = False
    error_code = 7
    input_table_dict = {
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
    input_table = table_from_dict(TEST_DESCRIPTOR, input_table_dict)
    input_bin_table = bytearray([25, 0, 11, 0, 9, 0, 14, 0, 26, 0, 12, 0, 97, 98, 99, 0, 205, 204, 66, 66, 0, 0])
    output_table_dict = {
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
    output_table = table_from_dict(TEST_DESCRIPTOR, output_table_dict)
    output_bin_table = bytearray([9, error_code, 11, 0, 9, 0, 14, 0, 26, 0, 1, 3, 1, 6, 4, 0, 12, 0, 97, 98, 0, 0, 205, 
                                  204, 66, 66, 0, 0])
           
    def test_msg_to_table(self):
        table_from_msg = PLCTable(TEST_DESCRIPTOR, self.input_bin_table)
        assert self.input_table == table_from_msg
        table_from_msg = I40Table(TEST_DESCRIPTOR, self.output_bin_table)
        assert self.output_table == table_from_msg

    def test_table_to_msg(self):
        result = self.input_table.to_msg()
        assert result == self.input_bin_table
        result = self.output_table.to_msg()
        assert result == self.output_bin_table
    
    def test_get_input_table_size(self):
        input_size = len(self.input_table)
        assert input_size == len(self.input_bin_table)
    
    def test_get_output_table_size(self):
        output_size = len(self.output_table)
        assert output_size == len(self.output_bin_table)
