import sys
import random
import math
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QFrame)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QLinearGradient


class SimpleAnimatedGauge(QWidget):
    """Простой круговой индикатор с гарантированной анимацией"""

    def __init__(self, title="CPU", color="#00ff88"):
        super().__init__()
        self.title = title
        self.color = QColor(color)
        self._value = 0
        self.target_value = 0

        # ВАЖНО: Настраиваем анимацию прямо здесь
        self.animation = QPropertyAnimation(self, b"value")
        self.animation.setDuration(1000)  # 1 секунда
        self.animation.setEasingCurve(QEasingCurve.OutBounce)  # Заметная анимация!

        self.setMinimumSize(200, 230)

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value
        self.update()  # Перерисовываем

    value = property(get_value, set_value)

    def set_target(self, value):
        """Запускает анимацию к целевому значению"""
        self.animation.setStartValue(self._value)
        self.animation.setEndValue(value)
        self.animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # Центр
        cx = w // 2
        cy = h // 2 - 10
        r = min(w, h) // 2 - 30

        # Рисуем фон
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(40, 40, 50))
        painter.drawEllipse(cx - r, cy - r, r * 2, r * 2)

        # Рисуем прогресс
        painter.setPen(QPen(self.color, 10, Qt.SolidLine, Qt.RoundCap))

        # Рисуем дугу от 0 до текущего значения
        angle = int(360 * (self._value / 100))  # 0-360 градусов

        # Рисуем дугу (немного сложно, но работает)
        if angle > 0:
            start_angle = 90 * 16  # Начинаем сверху
            span_angle = -angle * 16  # Идем против часовой стрелки

            # Рисуем дугу
            painter.drawArc(cx - r + 5, cy - r + 5, (r - 5) * 2, (r - 5) * 2, start_angle, span_angle)

        # Центральный круг
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(30, 30, 40))
        painter.drawEllipse(cx - r // 2, cy - r // 2, r, r)

        # Значение
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 20, QFont.Bold)
        painter.setFont(font)
        text = f"{self._value:.0f}%"
        painter.drawText(cx - 30, cy + 10, text)

        # Заголовок
        painter.setPen(QColor(180, 180, 200))
        font = QFont("Arial", 12)
        painter.setFont(font)
        painter.drawText(cx - 20, cy - r // 2 - 10, self.title)


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎯 Тест анимаций")
        self.setGeometry(300, 300, 500, 400)

        # Центральный виджет
        central = QWidget()
        central.setStyleSheet("background-color: #1a1a2e;")
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(20)

        # Заголовок
        title = QLabel("ПРОВЕРКА АНИМАЦИЙ")
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold; padding: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Индикатор
        self.gauge = SimpleAnimatedGauge("Загрузка", "#ff3366")
        layout.addWidget(self.gauge)

        # Кнопки
        btn_layout = QHBoxLayout()

        # Кнопка с фиксированным значением
        btn1 = QPushButton("🚀 100% (Bounce)")
        btn1.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        btn1.clicked.connect(lambda: self.gauge.set_target(100))

        # Кнопка со случайным значением
        btn2 = QPushButton("🎲 Случайно")
        btn2.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #1e88e5; }
        """)
        btn2.clicked.connect(self.random_value)

        # Кнопка сброса
        btn3 = QPushButton("🔄 0%")
        btn3.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #e53935; }
        """)
        btn3.clicked.connect(lambda: self.gauge.set_target(0))

        btn_layout.addWidget(btn1)
        btn_layout.addWidget(btn2)
        btn_layout.addWidget(btn3)

        layout.addLayout(btn_layout)

        # Статус
        self.status = QLabel("Нажми кнопку, чтобы увидеть анимацию!")
        self.status.setStyleSheet("color: #888; font-size: 12px; padding: 10px;")
        self.status.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status)

        # Таймер для автоматической смены значений
        self.timer = QTimer()
        self.timer.timeout.connect(self.random_value)

        # Кнопка авто-режима
        self.auto_btn = QPushButton("▶ Авто-режим")
        self.auto_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #fb8c00; }
        """)
        self.auto_btn.clicked.connect(self.toggle_auto)
        layout.addWidget(self.auto_btn)

    def random_value(self):
        value = random.randint(0, 100)
        self.gauge.set_target(value)
        self.status.setText(f"🎯 Установлено значение: {value}%")

    def toggle_auto(self):
        if self.timer.isActive():
            self.timer.stop()
            self.auto_btn.setText("▶ Авто-режим")
        else:
            self.timer.start(1500)  # Каждые 1.5 секунды
            self.auto_btn.setText("⏸ Стоп")
            self.random_value()  # Сразу запускаем


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Темная тема
    app.setStyle("Fusion")

    window = TestWindow()
    window.show()

    sys.exit(app.exec())