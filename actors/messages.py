from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
import uuid
from enum import Enum


# Базовые типы сообщений
class MessageType(str, Enum):
    """Типы сообщений в системе акторов"""
    PING = 'ping'
    PONG = 'pong'
    ERROR = 'error'
    SHUTDOWN = 'shutdown'
    DLQ_QUEUED = 'dlq_queued'
    DLQ_PROCESSED = 'dlq_processed'
    DLQ_CLEANUP = 'dlq_cleanup'
    USER_MESSAGE = 'user_message'
    GENERATE_RESPONSE = 'generate_response'
    BOT_RESPONSE = 'bot_response'
    STREAMING_CHUNK = 'streaming_chunk'
    SESSION_CREATED = 'session_created'
    SESSION_UPDATED = 'session_updated'
    CACHE_HIT_METRIC = 'cache_hit_metric'
    PROMPT_INCLUSION = 'prompt_inclusion'
    JSON_MODE_FAILURE = 'json_mode_failure'
    TELEGRAM_MESSAGE_RECEIVED = 'telegram_message_received'
    PROCESS_USER_MESSAGE = 'process_user_message'
    SEND_TELEGRAM_RESPONSE = 'send_telegram_response'
    JSON_VALIDATION_FAILED = 'json_validation_failed'
    STRUCTURED_RESPONSE_GENERATED = 'structured_response_generated'
    MODE_DETECTED = 'mode_detected'
    MODE_FALLBACK = 'mode_fallback'
    GENERATION_PARAMETERS_USED = 'generation_parameters_used'
    PYDANTIC_VALIDATION_SUCCESS = 'pydantic_validation_success'
    PATTERN_DEBUG = 'pattern_debug'


# Для обратной совместимости
MESSAGE_TYPES = {
    'PING': MessageType.PING,
    'PONG': MessageType.PONG,
    'ERROR': MessageType.ERROR,
    'SHUTDOWN': MessageType.SHUTDOWN,
    'DLQ_QUEUED': MessageType.DLQ_QUEUED,
    'DLQ_PROCESSED': MessageType.DLQ_PROCESSED,
    'DLQ_CLEANUP': MessageType.DLQ_CLEANUP,
    'USER_MESSAGE': MessageType.USER_MESSAGE,
    'GENERATE_RESPONSE': MessageType.GENERATE_RESPONSE,
    'BOT_RESPONSE': MessageType.BOT_RESPONSE,
    'STREAMING_CHUNK': MessageType.STREAMING_CHUNK,
    'SESSION_CREATED': MessageType.SESSION_CREATED,
    'SESSION_UPDATED': MessageType.SESSION_UPDATED,
    'CACHE_HIT_METRIC': MessageType.CACHE_HIT_METRIC,
    'PROMPT_INCLUSION': MessageType.PROMPT_INCLUSION,
    'JSON_MODE_FAILURE': MessageType.JSON_MODE_FAILURE,
    'TELEGRAM_MESSAGE_RECEIVED': MessageType.TELEGRAM_MESSAGE_RECEIVED,
    'PROCESS_USER_MESSAGE': MessageType.PROCESS_USER_MESSAGE,
    'SEND_TELEGRAM_RESPONSE': MessageType.SEND_TELEGRAM_RESPONSE,
    'JSON_VALIDATION_FAILED': MessageType.JSON_VALIDATION_FAILED,
    'STRUCTURED_RESPONSE_GENERATED': MessageType.STRUCTURED_RESPONSE_GENERATED,
    'MODE_DETECTED': MessageType.MODE_DETECTED,
    'MODE_FALLBACK': MessageType.MODE_FALLBACK,
    'GENERATION_PARAMETERS_USED': MessageType.GENERATION_PARAMETERS_USED,
    'PYDANTIC_VALIDATION_SUCCESS': MessageType.PYDANTIC_VALIDATION_SUCCESS,
    'PATTERN_DEBUG': MessageType.PATTERN_DEBUG,
}


class ActorMessage(BaseModel):
    """Базовый класс для всех сообщений между акторами"""
    model_config = ConfigDict(
        # Разрешаем произвольные типы (для datetime)
        arbitrary_types_allowed=True,
        # Для обратной совместимости с существующим кодом
        populate_by_name=True,
        # Валидация при присваивании
        validate_assignment=True
    )
    
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: Optional[str] = None
    message_type: str = ''
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)
    
    @classmethod
    def create(cls, 
               sender_id: Optional[str] = None,
               message_type: str = '',
               payload: Optional[Dict[str, Any]] = None) -> 'ActorMessage':
        """Фабричный метод для удобного создания сообщений"""
        return cls(
            sender_id=sender_id,
            message_type=message_type,
            payload=payload or {}
        )
    
    # Для обратной совместимости с кодом, который может использовать как dict
    def __getitem__(self, key):
        """Обеспечить доступ как к словарю для обратной совместимости"""
        return getattr(self, key)