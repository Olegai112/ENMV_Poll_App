def calculate_timeouts_rtu(baudrate):
    """Расчет таймаутов для Modbus RTU"""
    # Время передачи одного символа (старт+8+стоп=11 бит)
    char_time = 11 / baudrate  # в секундах

    return {
        'inter_char_timeout': char_time * 1.5,  # 1.5 символа
        'frame_timeout': char_time * 3.5  # 3.5 символа (пауза между сообщениями)
    }

# Пример для разных скоростей:
# 9600 бод:  inter_char = 0.0017 сек (1.7 мс)
# 19200 бод: inter_char = 0.00086 сек (0.86 мс)
# 115200 бод: inter_char = 0.00014 сек (0.14 мс)

res = calculate_timeouts(115200)
print(res['inter_char_timeout'])


# как работают модули в пайтон