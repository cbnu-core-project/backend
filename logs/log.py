import logging

# 로거 세팅
logger = logging.getLogger("postprocessor")
logger.setLevel(logging.DEBUG)

# 일반 핸들러, 포매터 세팅
formatter = logging.Formatter("%(asctime)s %(levelname)s:%(message)s")
handler = logging.FileHandler("logs/info_logs.log")
handler.setFormatter(formatter)


# 에러 핸들러
formatter_error = logging.Formatter("!!%(asctime)s %(levelname)s:%(message)s!!")
handler_error = logging.FileHandler("logs/error_logs.log")
handler_error.setLevel(logging.ERROR)
handler_error.setFormatter(formatter_error)


# 크리티컬 이벤트에 대한 핸들러, 포매터 세팅
formatter_critical = logging.Formatter("!!!!!!!!!!!!%(asctime)s %(levelname)s:%(message)s!!!!!!!!!!!!")
handler_critical = logging.FileHandler("logs/critical_logs.log")
handler_critical.setLevel(logging.CRITICAL)
handler_critical.setFormatter(formatter_critical)


# 각 핸들러를 로거에 추가
logger.addHandler(handler)
logger.addHandler(handler_error)
logger.addHandler(handler_critical)

