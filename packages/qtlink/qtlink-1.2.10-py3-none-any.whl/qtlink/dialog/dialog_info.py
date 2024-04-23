from typing import Optional, Callable, Iterable

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class DialogInfo(QDialog):
    """显示文本消息和简单交互按钮的对话框类"""

    def __init__(self, text: str,
                 title: str = '提示',
                 set_buttons: Optional[Iterable[tuple[str, Optional[Callable]]]] = None,
                 parent=None):
        """
        :param text: 对话框的文本消息
        :param set_buttons: 设置按钮参数，str指按钮文本，callable指点击按钮后调用的函数。如[('确定', None), ('取消', None)]
        :param parent: 对话框所属的ui父类
        """
        super().__init__(parent=parent)

        self.set_buttons = set_buttons
        self.setWindowTitle(title)

        vLayout = QVBoxLayout()
        label = QLabel(text, self)
        label.setWordWrap(True)
        vLayout.addWidget(label)

        if self.set_buttons:
            h_layout = QHBoxLayout()
            for btn in self.set_buttons:
                button = QPushButton(btn[0], self)
                button.clicked.connect(self.create_button_slot(btn[1]))
                h_layout.addWidget(button)
            vLayout.addLayout(h_layout)

        self.setLayout(vLayout)

    def create_button_slot(self, func):
        def button_slot():
            if func:
                func()
            self.close()
        return button_slot
