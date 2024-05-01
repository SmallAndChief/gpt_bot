import logging
import math
from config import LOGS, MAX_USERS, MAX_USER_GPT_TOKENS, MAX_USER_STT_BLOCKS, MAX_USER_TTS_SYMBOLS
from database import count_users, count_all_limits
from gpt import count_gpt_tokens

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=LOGS,
    filemode='a',
)


def check_number_of_users(user_id):
    count = count_users(user_id)
    if count is None:
        return None, "������ ��� ������ � ��"
    if count > MAX_USERS:
        return None, "��������� ������������ ���������� �������������"
    return True, ""


def is_gpt_token_limit(messages, total_spent_tokens):
    all_tokens = count_gpt_tokens(messages) + total_spent_tokens
    if all_tokens > MAX_USER_GPT_TOKENS:
        return None, f"�������� ����� ����� GPT-������� {MAX_USER_GPT_TOKENS}"
    return all_tokens, ""


def is_stt_block_limit(message, duration):
    user_id = message.from_user.id
    audio_blocks = math.ceil(duration / 15)
    all_blocks = count_all_limits(user_id, "stt_blocks") + audio_blocks
    if duration >= 30:
        msg = "SpeechKit STT �������� � ���������� ����������� ������ 30 ������"
        return 0, msg
    if all_blocks >= MAX_USER_STT_BLOCKS:
        msg = (f"�������� ����� ����� SpeechKit STT {MAX_USER_STT_BLOCKS}. ������������ {all_blocks} "
               f"������. ��������: {MAX_USER_STT_BLOCKS - all_blocks}")
        return 0, msg
    return audio_blocks, ''


def is_tts_symbol_limit(message, text):
    user_id = message.from_user.id
    text_symbols = len(text)
    all_symbols = count_all_limits(user_id, "tts_symbols") + text_symbols
    if all_symbols >= MAX_USER_TTS_SYMBOLS:
        msg = (f"�������� ����� ����� SpeechKit TTS {MAX_USER_TTS_SYMBOLS}. ������������: {all_symbols} "
               f"��������. ��������: {MAX_USER_TTS_SYMBOLS - all_symbols}")
        return 0, msg
    return len(text), ''
