from typing import Dict
from datetime import datetime
from decimal import Decimal
from uuid import UUID


def parse_message_attributes(attributes: Dict) -> Dict:
    message_attributes = {}
    if not attributes:
        return message_attributes
    for key, value in attributes.items():
        if value['Type'] == 'String':
            message_attributes[key] = value['Value']
        elif value['Type'] == 'Number':
            message_attributes[key] = int(value['Value'])
        elif value['Type'] == 'Binary':
            message_attributes[key] = bytes(value['Value'], 'utf-8')
    return message_attributes


def to_message_attributes(attributes: Dict) -> Dict:
    att_dict = {}
    for key, value in attributes.items():
        if isinstance(value, str):
            att_dict[key] = {
                'DataType': 'String', 'StringValue': value}
        elif isinstance(value, Decimal):
            att_dict[key] = {
                'DataType': 'Number', 'StringValue': str(value)}
        elif isinstance(value, UUID):
            att_dict[key] = {
                'DataType': 'String', 'StringValue': str(value)}
        elif isinstance(value, datetime):
            att_dict[key] = {
                'DataType': 'String', 'StringValue': value.isoformat()}
        elif isinstance(value, int):
            att_dict[key] = {
                'DataType': 'Number', 'StringValue': str(value)}
        elif isinstance(value, bytes):
            att_dict[key] = {
                'DataType': 'Binary', 'BinaryValue': value}
    return att_dict
