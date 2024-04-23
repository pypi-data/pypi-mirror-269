from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen, QGuiApplication
from PySide6.QtWidgets import QWidget, QGridLayout, QSlider, QLabel, QLineEdit, QPushButton, QCheckBox

from frontengine.show.text.draw_text import TextWidget
from frontengine.utils.logging.loggin_instance import front_engine_logger
from frontengine.utils.multi_language.language_wrapper import language_wrapper


class TextSettingUI(QWidget):

    def __init__(self):
        super().__init__()
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        # Init variable
        self.text_widget_list = list()
        self.show_all_screen = False
        # Opacity setting
        self.opacity_slider = QSlider()
        self.opacity_slider.setOrientation(Qt.Orientation.Horizontal)
        self.opacity_label = QLabel(
            language_wrapper.language_word_dict.get("Opacity")
        )
        self.opacity_slider.setMinimum(1)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(20)
        self.opacity_slider.setTickInterval(1)
        self.opacity_slider_value_label = QLabel(str(self.opacity_slider.value()))
        self.opacity_slider.actionTriggered.connect(self.opacity_trick)
        # Font size setting
        self.font_size_slider = QSlider()
        self.font_size_slider.setOrientation(Qt.Orientation.Horizontal)
        self.font_size_label = QLabel(
            language_wrapper.language_word_dict.get("Font size")
        )
        self.font_size_slider.setMinimum(1)
        self.font_size_slider.setMaximum(300)
        self.font_size_slider.setValue(100)
        self.font_size_slider.setTickInterval(1)
        self.font_size_slider_value_label = QLabel(str(self.font_size_slider.value()))
        self.font_size_slider.actionTriggered.connect(self.font_size_trick)
        # Font input button
        self.line_edit = QLineEdit()
        # Start Button
        self.start_button = QPushButton(
            language_wrapper.language_word_dict.get("text_setting_start_draw")
        )
        self.start_button.clicked.connect(self.start_draw_text_on_screen)
        # Show on all screen
        self.show_on_all_screen_checkbox = QCheckBox(
            language_wrapper.language_word_dict.get("Show on all screen")
        )
        self.show_on_all_screen_checkbox.clicked.connect(self.set_show_all_screen)
        # Show on bottom
        self.show_on_bottom_checkbox = QCheckBox(
            language_wrapper.language_word_dict.get("Show on bottom")
        )
        # Add to layout
        self.grid_layout.addWidget(self.opacity_label, 0, 0)
        self.grid_layout.addWidget(self.opacity_slider_value_label, 0, 1)
        self.grid_layout.addWidget(self.opacity_slider, 0, 2)
        self.grid_layout.addWidget(self.font_size_label, 1, 0)
        self.grid_layout.addWidget(self.font_size_slider_value_label, 1, 1)
        self.grid_layout.addWidget(self.font_size_slider, 1, 2)
        self.grid_layout.addWidget(self.show_on_all_screen_checkbox, 2, 0)
        self.grid_layout.addWidget(self.show_on_bottom_checkbox, 2, 1)
        self.grid_layout.addWidget(self.start_button, 3, 0)
        self.grid_layout.addWidget(self.line_edit, 3, 2)
        self.setLayout(self.grid_layout)

    def set_show_all_screen(self) -> None:
        self.show_all_screen = self.show_on_all_screen_checkbox.isChecked()

    def _create_text_widget(self) -> TextWidget:
        text_widget = TextWidget(self.line_edit.text())
        text_widget.set_font_variable(self.font_size_slider.value())
        text_widget.set_ui_variable(float(self.opacity_slider.value()) / 100)
        text_widget.set_ui_window_flag(self.show_on_bottom_checkbox.isChecked())
        self.text_widget_list.append(text_widget)
        return text_widget

    def opacity_trick(self) -> None:
        self.opacity_slider_value_label.setText(str(self.opacity_slider.value()))

    def font_size_trick(self) -> None:
        self.font_size_slider_value_label.setText(str(self.font_size_slider.value()))

    def start_draw_text_on_screen(self) -> None:
        front_engine_logger.info("start_draw_text_on_screen")
        if not self.show_all_screen:
            text_widget = self._create_text_widget()
            text_widget.showFullScreen()
        else:
            monitors = QGuiApplication.screens()
            for monitor in monitors:
                text_widget = self._create_text_widget()
                text_widget.setScreen(monitor)
                text_widget.move(monitor.availableGeometry().topLeft())
                text_widget.showFullScreen()
