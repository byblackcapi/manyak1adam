import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QListWidget, QMessageBox, QAction
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QProcess

class CapiBotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖 Capi Bot v1")
        self.setGeometry(100, 100, 800, 700)
        self.process = None

        # Tema stilleri
        self.themes = {
            "🌙 Karanlık": "background-color: #2e2e2e; color: white;",
            "🌞 Açık": "background-color: white; color: black;",
            "🔷 Mavi": "background-color: #add8e6; color: #000;",
            "🌈 Renkli": "background-color: #f0e68c; color: #333;"
        }

        self._build_ui()
        self._build_menu()
        # Varsayılan tema
        self.change_theme("🌞 Açık")

    def _build_ui(self):
        central = QWidget()
        layout = QVBoxLayout()

        # Başlık
        title = QLabel("🎮 Capi ART Analiz Bot GUI v1")
        title.setFont(QFont("Arial", 20))
        layout.addWidget(title)

        # Hızlı Erişim Butonları
        btn_layout = QHBoxLayout()
        btn_games = QPushButton("📂 Oyun Listesi")
        btn_games.clicked.connect(self.load_games)
        btn_layout.addWidget(btn_games)

        btn_images = QPushButton("🖼️ Resim Listesi")
        btn_images.clicked.connect(self.load_images)
        btn_layout.addWidget(btn_images)

        btn_install = QPushButton("📦 Yüklemeleri Yap")
        btn_install.clicked.connect(self.install_requirements)
        btn_layout.addWidget(btn_install)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Oyun listesi
        self.game_list = QTextEdit()
        self.game_list.setReadOnly(True)
        layout.addWidget(self.game_list)

        # Resim listesi
        self.img_list = QListWidget()
        layout.addWidget(self.img_list)

        # Bot kontrol butonları
        ctrl_layout = QHBoxLayout()
        self.run_btn = QPushButton("▶️ Botu Başlat")
        self.run_btn.clicked.connect(self.run_bot)
        ctrl_layout.addWidget(self.run_btn)

        self.stop_btn = QPushButton("⛔ Durdur")
        self.stop_btn.clicked.connect(self.stop_bot)
        ctrl_layout.addWidget(self.stop_btn)

        self.restart_btn = QPushButton("🔁 Yeniden Başlat")
        self.restart_btn.clicked.connect(self.restart_bot)
        ctrl_layout.addWidget(self.restart_btn)

        ctrl_layout.addStretch()
        layout.addLayout(ctrl_layout)

        # Konsol Çıktısı
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        layout.addWidget(self.console_output)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def _build_menu(self):
        mb = self.menuBar()

        # Dosya Menü
        file_menu = mb.addMenu("📁 Dosya")
        exit_act = QAction("Çıkış", self)
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)

        # Araçlar Menü
        tools_menu = mb.addMenu("🛠️ Araçlar")
        tools_menu.addAction("Oyunları Listele", self.load_games)
        tools_menu.addAction("Resimleri Listele", self.load_images)
        tools_menu.addAction("Yüklemeleri Yap", self.install_requirements)

        # Bot Menü
        bot_menu = mb.addMenu("🚀 Bot")
        bot_menu.addAction("Başlat", self.run_bot)
        bot_menu.addAction("Durdur", self.stop_bot)
        bot_menu.addAction("Yeniden Başlat", self.restart_bot)

        # Tema Menü
        theme_menu = mb.addMenu("🎨 Tema")
        for name in self.themes:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, n=name: self.change_theme(n))
            theme_menu.addAction(action)

        # Yardım Menü
        help_menu = mb.addMenu("❓ Yardım")
        about_act = QAction("Hakkında", self)
        about_act.triggered.connect(lambda: QMessageBox.information(
            self, "Hakkında", "Capi Bot v1 - PyQt5 GUI"
        ))
        help_menu.addAction(about_act)

    def load_games(self):
        self.game_list.clear()
        try:
            with open("game.json", "r", encoding="utf-8") as f:
                games = json.load(f).get("games", [])
                for g in games:
                    self.game_list.append(f"• {g}")
        except Exception as e:
            self.game_list.append(f"❌ Hata: {e}")

    def load_images(self):
        self.img_list.clear()
        try:
            for fn in os.listdir("images"):
                if fn.lower().endswith((".png", ".jpg", ".jpeg")):
                    self.img_list.addItem(fn)
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Resim klasörü hatası:\n{e}")

    def install_requirements(self):
        self.append_log("📦 Kütüphaneler yükleniyor...")
        proc = QProcess(self)
        proc.start("pip", ["install", "-r", "requirements.txt"])
        proc.waitForFinished()
        out = proc.readAllStandardOutput().data().decode().strip()
        self.append_log(out)

    def run_bot(self):
        if self.process and self.process.state() != QProcess.NotRunning:
            self.append_log("⚠️ Bot zaten çalışıyor.")
            return
        self.append_log("🚀 Bot başlatılıyor...")
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(
            lambda: self.append_log(self.process.readAllStandardOutput().data().decode().strip())
        )
        self.process.readyReadStandardError.connect(
            lambda: self.append_log(self.process.readAllStandardError().data().decode().strip())
        )
        self.process.start("python", ["index.py"])

    def stop_bot(self):
        if self.process and self.process.state() != QProcess.NotRunning:
            self.process.kill()
            self.append_log("⛔ Bot durduruldu.")
        else:
            self.append_log("⚠️ Durdurulan bot yok.")

    def restart_bot(self):
        self.append_log("🔁 Yeniden başlatılıyor...")
        self.stop_bot()
        self.run_bot()

    def append_log(self, text):
        self.console_output.append(text)

    def change_theme(self, name):
        self.setStyleSheet(self.themes.get(name, ""))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('images/bot_icon.png'))
    win = CapiBotGUI()
    win.show()
    sys.exit(app.exec_())
