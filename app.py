import sys
import random
import os
from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QPoint, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import math

class CharacterWidget(QLabel):
    def __init__(self):
        super().__init__()
        # لود کردن سه تصویر
        self.pixmap_right = QPixmap("assets/img/cat-right.png")
        self.pixmap_left = QPixmap("assets/img/cat-left.png")
        self.pixmap_stop = QPixmap("assets/img/cat-stop.png")
        
        # تنظیم تصویر اولیه و اندازه
        self.set_pixmap_and_resize(self.pixmap_right)
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # تنظیمات صفحه
        screen_geometry = QDesktopWidget().screenGeometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()
        start_x = random.randint(0, self.screen_width - self.width())
        start_y = random.randint(0, self.screen_height - self.height())
        self.move(start_x, start_y)

        # متغیرهای اولیه
        self.angle = random.uniform(0, 360)
        self.base_speed = random.uniform(0.5, 1)
        self.dx = 0
        self.dy = 0
        self.state = "moving"  # حالت اولیه: در حال حرکت

        # تنظیمات پخش صدا
        self.media_player = QMediaPlayer()

        # تایمر حرکت
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_character)
        self.move_timer.start(16)

        # تایمر تغییر جهت
        self.change_timer = QTimer(self)
        self.change_timer.timeout.connect(self.change_movement)
        self.update_change_timer()

        # تایمر تغییر حالت (حرکت/توقف)
        self.state_timer = QTimer(self)
        self.state_timer.timeout.connect(self.change_state)
        move_duration = random.randint(2000, 5000)  # مدت حرکت اولیه
        self.state_timer.start(move_duration)

    def set_pixmap_and_resize(self, pixmap):
        """تابع کمکی برای تنظیم تصویر و تغییر اندازه ویجیت"""
        self.setPixmap(pixmap)
        self.setFixedSize(pixmap.size())

    def update_change_timer(self):
        self.change_timer.stop()
        random_interval = random.randint(1000, 3000)
        self.change_timer.start(random_interval)

    def move_character(self):
        if self.state == "moving":
            current_pos = self.pos()
            rad = math.radians(self.angle)
            self.dx = math.cos(rad) * self.base_speed
            self.dy = math.sin(rad) * self.base_speed

            # تنظیم تصویر و اندازه بر اساس جهت
            if self.dx > 0:
                self.set_pixmap_and_resize(self.pixmap_right)
            else:
                self.set_pixmap_and_resize(self.pixmap_left)

            new_x = current_pos.x() + self.dx
            new_y = current_pos.y() + self.dy

            # برخورد با لبه‌ها
            if new_x < 0 or new_x + self.width() > self.screen_width:
                self.angle = 180 - self.angle
                new_x = max(0, min(new_x, self.screen_width - self.width()))
            if new_y < 0 or new_y + self.height() > self.screen_height:
                self.angle = -self.angle
                new_y = max(0, min(new_y, self.screen_height - self.height()))

            self.move(int(new_x), int(new_y))

    def change_movement(self):
        angle_change = random.uniform(-45, 45)
        self.angle = (self.angle + angle_change) % 360
        self.base_speed = random.uniform(0, 3)
        self.update_change_timer()

    def change_state(self):
        self.state_timer.stop()
        if self.state == "moving":
            self.state = "stopped"
            self.change_timer.stop()  # توقف تغییر جهت
            if random.random() < 0.5:  # 50% شانس نمایش تصویر توقف
                self.set_pixmap_and_resize(self.pixmap_stop)
            stop_duration = random.randint(1000, 3000)  # مدت توقف
            self.state_timer.setInterval(stop_duration)
        else:  # حالت "stopped"
            self.state = "moving"
            self.change_movement()  # تنظیم جهت و سرعت جدید و شروع تایمر تغییر جهت
            move_duration = random.randint(2000, 5000)  # مدت حرکت
            self.state_timer.setInterval(move_duration)
        self.state_timer.start()

    def mousePressEvent(self, event):
        """مدیریت رویداد کلیک ماوس"""
        sound_number = random.randint(1, 8)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sound_path = os.path.join(
            current_dir,
            "assets",
            "wav",
            f"cat-meow ({sound_number}).mp3"
        )
        
        if os.path.exists(sound_path):
            url = QUrl.fromLocalFile(sound_path)
            content = QMediaContent(url)
            self.media_player.setMedia(content)
            self.media_player.play()
        else:
            print(f"فایل صوتی یافت نشد: {sound_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    character = CharacterWidget()
    character.show()
    sys.exit(app.exec_())