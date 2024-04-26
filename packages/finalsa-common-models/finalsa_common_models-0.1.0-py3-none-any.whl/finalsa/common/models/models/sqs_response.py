from datetime import datetime, timezone
from typing import Dict, Optional, Union
from uuid import UUID, uuid4
from pydantic import BaseModel
from json import loads
from .sqs_message import SqsMessage
from .functions import parse_message_attributes


class SqsReponse(BaseModel):
    message_id: str
    receipt_handle: str
    md5_of_body: str
    body: str
    attributes: Optional[Dict] = {}
    topic: Optional[str] = ""
    md5_of_message_attributes: Optional[str] = ""
    message_attributes: Optional[Dict] = {}

    def get_payload(self) -> Dict:
        return loads(self.body)

    @staticmethod
    def correlation_id_from_attributes(attributes: Dict) -> Optional[str]:
        correlation_id = attributes.get('correlation_id', None)
        if not correlation_id:
            return None
        if isinstance(correlation_id, str):
            return correlation_id
        if isinstance(correlation_id, dict) and 'Type' in correlation_id and 'Value' in correlation_id:
            return correlation_id["Value"]
        return None

    def get_correlation_id(self) -> Union[str, UUID]:
        correlation_id = self.correlation_id_from_attributes(self.message_attributes)
        if correlation_id:
            return correlation_id
        correlation_id = self.correlation_id_from_attributes(self.attributes)
        if correlation_id:
            return correlation_id
        try:
            s = self.get_payload()['correlation_id']
            return s
        except Exception:
            return str(uuid4())

    def parse_from_sns(self) -> Optional[Dict]:
        payload = self.get_payload()
        if 'Type' not in payload or payload['Type'] != 'Notification':
            return None
        self.topic = str(payload['TopicArn'].split(':')[-1]).lower()
        self.body = payload['Message']
        self.message_attributes = parse_message_attributes(
            payload.get('MessageAttributes', {}))
        return self.get_payload()

    def parse(self) -> Optional[Dict]:
        sns_response = self.parse_from_sns()
        if sns_response is not None:
            return sns_response
        return self.get_payload()

    def get_sqs_message(self) -> SqsMessage:
        sns_payload = self.parse_from_sns()
        if sns_payload:
            if 'correlation_id' not in sns_payload:
                sns_payload['correlation_id'] = str(self.get_correlation_id())
            if 'timestamp' not in sns_payload:
                sns_payload['timestamp'] = datetime.now(timezone.utc).isoformat()
            return SqsMessage(
                id=UUID(sns_payload['id']),
                topic=sns_payload['topic'],
                payload=sns_payload['payload'],
                correlation_id=sns_payload['correlation_id'],
                timestamp=sns_payload['timestamp']
            )
        payload = self.get_payload()
        if 'correlation_id' not in payload:
            payload['correlation_id'] = str(self.get_correlation_id())
        return SqsMessage(
            id=UUID(payload['id']),
            topic=payload['topic'],
            payload=payload['payload'],
            correlation_id=payload['correlation_id'],
            timestamp=payload['timestamp']
        )

    @classmethod
    def from_boto_response(cls, response: Dict):
        return cls(
            message_id=response['MessageId'],
            receipt_handle=response['ReceiptHandle'],
            md5_of_body=response.get('MD5OfBody', ""),
            body=response['Body'],
            attributes=response['Attributes'],
            md5_of_message_attributes=response.get(
                'MD5OfMessageAttributes', ''),
            message_attributes=parse_message_attributes(
                response.get('MessageAttributes', {}))
        )
