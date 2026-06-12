import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QScrollArea, QFrame, QLabel, QPushButton, QLineEdit,
    QComboBox, QDialog, QStackedWidget, QSizePolicy
)
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer, pyqtSignal
)
from PyQt6.QtGui import (
    QColor, QLinearGradient, QPainter, QBrush, QPen, QFont, QPixmap
)
import random

# ============================================================
# COSTANTI E STILI
# ============================================================
COLORS = {
    'primary': '#6366f1', 'primary_dark': '#4f46e5',
    'secondary': '#ec4899', 'accent': '#06b6d4',
    'dark': '#0f172a', 'dark_light': '#1e293b',
    'card': '#1e293b', 'text': '#f8fafc',
    'text_muted': '#94a3b8', 'success': '#22c55e',
    'warning': '#f59e0b', 'danger': '#ef4444',
    'border': '#334155'
}

DEVICE_ICONS = {
    'light': '💡', 'climate': '❄️', 'appliance': '🔌',
    'entertainment': '📺', 'security': '🔒'
}

STYLE = f"""
QMainWindow {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['dark']}, stop:0.5 #1a1a2e, stop:1 {COLORS['dark_light']});
}}
QFrame#card {{
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    border-radius: 20px;
}}
QFrame#card:hover {{
    border: 2px solid {COLORS['primary']};
}}
QLineEdit {{
    background-color: {COLORS['dark_light']};
    border: 2px solid {COLORS['border']};
    border-radius: 16px;
    padding: 14px 16px;
    color: {COLORS['text']};
    font-size: 14px;
    font-family: 'Segoe UI';
}}
QLineEdit:focus {{
    border: 2px solid {COLORS['primary']};
}}
QComboBox {{
    background-color: {COLORS['dark_light']};
    border: 2px solid {COLORS['border']};
    border-radius: 16px;
    padding: 12px 16px;
    color: {COLORS['text']};
    font-size: 14px;
    min-width: 200px;
}}
QComboBox::drop-down {{ border: none; width: 30px; }}
QComboBox QAbstractItemView {{
    background-color: {COLORS['dark_light']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    selection-background-color: {COLORS['primary']};
    border-radius: 12px;
}}
QScrollArea {{ border: none; background: transparent; }}
QScrollBar:vertical {{
    background: transparent; width: 6px; margin: 0px;
}}
QScrollBar::handle:vertical {{
    background: {COLORS['border']}; border-radius: 3px; min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{ background: {COLORS['primary']}; }}
QDialog {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['dark']}, stop:1 {COLORS['dark_light']});
    border-radius: 24px;
}}
"""

# ============================================================
# WIDGET PERSONALIZZATI
# ============================================================

class ModernButton(QPushButton):
    def __init__(self, text, icon='', color='primary', parent=None):
        super().__init__(parent)
        self.setText(f"{{icon}}  {{text}}".format(icon=icon, text=text) if icon else text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(50)

        if color == 'primary':
            bg = f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {COLORS['primary']}, stop:1 {COLORS['primary_dark']})"
            tc = 'white'
        elif color == 'danger':
            bg, tc = COLORS['danger'], 'white'
        elif color == 'warning':
            bg, tc = COLORS['warning'], 'white'
        elif color == 'ghost':
            bg, tc = 'transparent', COLORS['text_muted']
        else:
            bg, tc = COLORS['dark'], COLORS['text']

        self.setStyleSheet(f"""
            QPushButton {{
                background: {bg};
                color: {tc};
                border: {{'2px solid #334155' if color == 'ghost' else 'none'}};
                border-radius: 16px;
                padding: 14px 24px;
                font-size: 15px; font-weight: 600; font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: {'#4f46e5' if color=='primary' else '#dc2626' if color=='danger' else '#d97706' if color=='warning' else '#334155'};
            }}
            QPushButton:pressed {{
                background: {'#4338ca' if color=='primary' else '#b91c1c' if color=='danger' else '#b45309'};
            }}
        """)


class ToggleSwitch(QFrame):
    toggled = pyqtSignal(bool)

    def __init__(self, checked=False, parent=None):
        super().__init__(parent)
        self._checked = checked
        self.setFixedSize(52, 30)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_style()

        self.circle = QFrame(self)
        self.circle.setFixedSize(24, 24)
        self.circle.setStyleSheet("QFrame { background: white; border-radius: 12px; }")
        self.circle.move(26 if checked else 4, 3)

        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 2)
        self.circle.setGraphicsEffect(shadow)

    def update_style(self):
        bg = f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {COLORS['primary']}, stop:1 {COLORS['secondary']})" if self._checked else COLORS['border']
        self.setStyleSheet(f"QFrame {{ background: {bg}; border-radius: 15px; }}")

    def mousePressEvent(self, event):
        self._checked = not self._checked
        self.update_style()
        anim = QPropertyAnimation(self.circle, b"pos")
        anim.setDuration(200)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anim.setEndValue(QPoint(26 if self._checked else 4, 3))
        anim.start()
        self.toggled.emit(self._checked)

    def isChecked(self): return self._checked
    def setChecked(self, checked):
        if self._checked != checked:
            self._checked = checked
            self.update_style()
            self.circle.move(26 if checked else 4, 3)


class StatCard(QFrame):
    def __init__(self, icon, value, label, color, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setMinimumWidth(110)
        self.setMaximumWidth(140)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        il = QLabel(icon)
        il.setStyleSheet("font-size: 28px;")
        il.setAlignment(Qt.AlignmentFlag.AlignCenter)

        vl = QLabel(value)
        vl.setStyleSheet(f"color: {color}; font-size: 22px; font-weight: 700; font-family: 'Segoe UI';")
        vl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ll = QLabel(label)
        ll.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 11px; font-family: 'Segoe UI';")
        ll.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(il)
        layout.addWidget(vl)
        layout.addWidget(ll)

        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)


class RoomCard(QFrame):
    clicked = pyqtSignal(int)
    edit_clicked = pyqtSignal(int)
    delete_clicked = pyqtSignal(int)

    def __init__(self, room_id, name, icon, devices, color, parent=None):
        super().__init__(parent)
        self.room_id = room_id
        self.setObjectName("card")
        self.setFixedSize(160, 190)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 16)
        layout.setSpacing(8)

        ic = QFrame()
        ic.setFixedSize(48, 48)
        ic.setStyleSheet(f"QFrame {{ background: {color}33; border-radius: 16px; }}")
        icl = QVBoxLayout(ic)
        icl.setContentsMargins(0, 0, 0, 0)
        icl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        il = QLabel(icon)
        il.setStyleSheet("font-size: 24px;")
        icl.addWidget(il)

        nl = QLabel(name)
        nl.setStyleSheet("color: #f8fafc; font-size: 15px; font-weight: 600; font-family: 'Segoe UI';")

        cl = QLabel(f"{devices} dispositivi")
        cl.setStyleSheet("color: #94a3b8; font-size: 12px; font-family: 'Segoe UI';")

        bl = QHBoxLayout()
        bl.setSpacing(6)

        eb = QPushButton("✏️")
        eb.setFixedSize(32, 32)
        eb.setStyleSheet(f"QPushButton {{ background: {COLORS['warning']}; border-radius: 10px; border: none; font-size: 14px; }} QPushButton:hover {{ background: #d97706; }}")
        eb.setCursor(Qt.CursorShape.PointingHandCursor)
        eb.clicked.connect(lambda: self.edit_clicked.emit(self.room_id))

        db = QPushButton("🗑️")
        db.setFixedSize(32, 32)
        db.setStyleSheet(f"QPushButton {{ background: {COLORS['danger']}; border-radius: 10px; border: none; font-size: 14px; }} QPushButton:hover {{ background: #dc2626; }}")
        db.setCursor(Qt.CursorShape.PointingHandCursor)
        db.clicked.connect(lambda: self.delete_clicked.emit(self.room_id))

        bl.addWidget(eb)
        bl.addWidget(db)

        layout.addWidget(ic, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(nl)
        layout.addWidget(cl)
        layout.addLayout(bl)
        layout.addStretch()

        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.room_id)


class DeviceCard(QFrame):
    toggle_changed = pyqtSignal(int, bool)
    edit_clicked = pyqtSignal(int)
    delete_clicked = pyqtSignal(int)

    def __init__(self, device_id, name, room_name, icon, power, is_on, parent=None):
        super().__init__(parent)
        self.device_id = device_id
        self.power = power
        self.setObjectName("card")
        self.setMinimumHeight(170)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 14)
        layout.setSpacing(10)

        header = QHBoxLayout()

        ic = QFrame()
        ic.setFixedSize(44, 44)
        ic.setStyleSheet(f"QFrame {{ background: {'#6366f1' if is_on else '#0f172a'}; border-radius: 14px; }}")
        icl = QVBoxLayout(ic)
        icl.setContentsMargins(0, 0, 0, 0)
        icl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        il = QLabel(icon)
        il.setStyleSheet("font-size: 20px;")
        icl.addWidget(il)

        self.toggle = ToggleSwitch(is_on)
        self.toggle.toggled.connect(lambda c: self.toggle_changed.emit(self.device_id, c))

        header.addWidget(ic)
        header.addStretch()
        header.addWidget(self.toggle)

        info = QVBoxLayout()
        info.setSpacing(2)
        nl = QLabel(name)
        nl.setStyleSheet("color: #f8fafc; font-size: 15px; font-weight: 600; font-family: 'Segoe UI';")
        rl = QLabel(room_name)
        rl.setStyleSheet("color: #94a3b8; font-size: 12px; font-family: 'Segoe UI';")
        info.addWidget(nl)
        info.addWidget(rl)

        pl = QHBoxLayout()
        pl.setSpacing(6)
        pi = QLabel("⚡")
        pi.setStyleSheet("font-size: 14px;")
        self.power_lbl = QLabel(f"{power if is_on else 0} W")
        self.power_lbl.setStyleSheet("color: #94a3b8; font-size: 12px; font-family: 'Segoe UI';")
        pl.addWidget(pi)
        pl.addWidget(self.power_lbl)
        pl.addStretch()

        btn_l = QHBoxLayout()
        btn_l.setSpacing(6)

        eb = QPushButton("✏️ Modifica")
        eb.setStyleSheet(f"""
            QPushButton {{ background: transparent; border: 1px solid {COLORS['border']}; border-radius: 10px; padding: 8px; color: #f8fafc; font-size: 11px; font-family: 'Segoe UI'; }}
            QPushButton:hover {{ background: {COLORS['primary']}; border-color: {COLORS['primary']}; }}
        """)
        eb.setCursor(Qt.CursorShape.PointingHandCursor)
        eb.clicked.connect(lambda: self.edit_clicked.emit(self.device_id))

        db = QPushButton("🗑️ Elimina")
        db.setStyleSheet(f"""
            QPushButton {{ background: transparent; border: 1px solid {COLORS['border']}; border-radius: 10px; padding: 8px; color: #f8fafc; font-size: 11px; font-family: 'Segoe UI'; }}
            QPushButton:hover {{ background: {COLORS['danger']}; border-color: {COLORS['danger']}; }}
        """)
        db.setCursor(Qt.CursorShape.PointingHandCursor)
        db.clicked.connect(lambda: self.delete_clicked.emit(self.device_id))

        btn_l.addWidget(eb)
        btn_l.addWidget(db)

        layout.addLayout(header)
        layout.addLayout(info)
        layout.addLayout(pl)
        layout.addLayout(btn_l)

        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)

    def update_power(self, is_on):
        self.power_lbl.setText(f"{self.power if is_on else 0} W")


class ChartWidget(QFrame):
    def __init__(self, title, chart_type='line', parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.chart_type = chart_type
        self.title = title
        self.data = []
        self.labels = []
        self.colors = []
        self.setMinimumHeight(220)
        self.setMaximumHeight(260)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)

        header = QHBoxLayout()
        tl = QLabel(title)
        tl.setStyleSheet("color: #f8fafc; font-size: 15px; font-weight: 600; font-family: 'Segoe UI';")

        badge_text = "LIVE" if chart_type == 'line' else "SETTIMANALE" if chart_type == 'bar' else "MENSILE"
        badge_color = COLORS['success'] if chart_type == 'line' else COLORS['warning']
        bl = QLabel(badge_text)
        bl.setStyleSheet(f"background: {badge_color}33; color: {badge_color}; border-radius: 12px; padding: 4px 12px; font-size: 11px; font-weight: 600;")

        header.addWidget(tl)
        header.addStretch()
        header.addWidget(bl)

        self.chart_area = QFrame()
        self.chart_area.setMinimumHeight(160)
        layout.addLayout(header)
        layout.addWidget(self.chart_area)

        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)

    def set_data(self, labels, data, colors=None):
        self.labels = labels
        self.data = data
        self.colors = colors or [COLORS['primary']] * len(data)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.data:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        cr = self.chart_area.geometry()
        margin = 20
        w = cr.width() - 2 * margin
        h = cr.height() - 2 * margin
        x = cr.x() + margin
        y = cr.y() + margin

        if self.chart_type == 'line':
            self._draw_line(painter, x, y, w, h)
        elif self.chart_type == 'bar':
            self._draw_bar(painter, x, y, w, h)
        elif self.chart_type == 'pie':
            self._draw_pie(painter, x, y, w, h)

    def _draw_line(self, p, x, y, w, h):
        max_val = max(self.data) * 1.2
        pen = QPen(QColor(COLORS['border']))
        pen.setWidth(1)
        p.setPen(pen)
        for i in range(5):
            gy = y + h * i / 4
            p.drawLine(x, int(gy), x + w, int(gy))

        points = []
        for i, val in enumerate(self.data):
            px = x + w * i / (len(self.data) - 1)
            py = y + h - val / max_val * h
            points.append((px, py))

        if len(points) > 1:
            grad = QLinearGradient(x, y, x, y + h)
            grad.setColorAt(0, QColor(COLORS['primary'] + '40'))
            grad.setColorAt(1, QColor(COLORS['primary'] + '00'))
            p.setBrush(QBrush(grad))
            p.setPen(Qt.PenStyle.NoPen)
            poly = []
            poly.append(QPoint(int(points[0][0]), int(y + h)))
            for px, py in points:
                poly.append(QPoint(int(px), int(py)))
            poly.append(QPoint(int(points[-1][0]), int(y + h)))
            p.drawPolygon(poly)

        pen = QPen(QColor(COLORS['primary']))
        pen.setWidth(3)
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        for i in range(len(points) - 1):
            p.drawLine(QPoint(int(points[i][0]), int(points[i][1])), QPoint(int(points[i+1][0]), int(points[i+1][1])))

        for px, py in points:
            p.setBrush(QColor(COLORS['primary']))
            p.drawEllipse(QPoint(int(px), int(py)), 4, 4)

    def _draw_bar(self, p, x, y, w, h):
        max_val = max(self.data) * 1.2
        bw = w / len(self.data) * 0.6
        sp = w / len(self.data)
        for i, (label, val, color) in enumerate(zip(self.labels, self.data, self.colors)):
            bh = (val / max_val) * h
            bx = x + i * sp + (sp - bw) / 2
            by = y + h - bh
            grad = QLinearGradient(bx, by, bx, by + bh)
            grad.setColorAt(0, QColor(color))
            grad.setColorAt(1, QColor(color + '80'))
            p.setBrush(QBrush(grad))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(int(bx), int(by), int(bw), int(bh), 8, 8)
            p.setPen(QColor(COLORS['text_muted']))
            p.drawText(int(bx), int(y + h + 5), int(bw), 20, Qt.AlignmentFlag.AlignCenter, label)

    def _draw_pie(self, p, x, y, w, h):
        total = sum(self.data)
        if total == 0:
            return
        cx = x + w / 2
        cy = y + h / 2
        r = min(w, h) / 2 - 10
        ir = r * 0.6
        start = 0
        for val, color in zip(self.data, self.colors):
            angle = (val / total) * 360 * 16
            p.setBrush(QColor(color))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawPie(int(cx - r), int(cy - r), int(r * 2), int(r * 2), int(start), int(angle))
            start += angle
        p.setBrush(QColor(COLORS['card']))
        p.drawEllipse(QPoint(int(cx), int(cy)), int(ir), int(ir))


class ToastWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setStyleSheet(f"QFrame {{ background: #1e293b; border: 1px solid {COLORS['primary']}; border-radius: 16px; }}")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)

        self.icon_lbl = QLabel("✅")
        self.icon_lbl.setStyleSheet("font-size: 18px;")
        self.msg_lbl = QLabel("")
        self.msg_lbl.setStyleSheet("color: #f8fafc; font-size: 13px; font-family: 'Segoe UI';")

        layout.addWidget(self.icon_lbl)
        layout.addWidget(self.msg_lbl)
        layout.addStretch()
        self.hide()

        if parent:
            self.move((parent.width() - 300) // 2, -60)
            self.setFixedWidth(300)

    def show_message(self, message, icon="✅"):
        self.msg_lbl.setText(message)
        self.icon_lbl.setText(icon)
        self.show()
        anim = QPropertyAnimation(self, b"pos")
        anim.setDuration(300)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.setStartValue(QPoint((self.parent().width() - 300) // 2, -60))
        anim.setEndValue(QPoint((self.parent().width() - 300) // 2, 20))
        anim.start()
        QTimer.singleShot(3000, self._hide)

    def _hide(self):
        anim = QPropertyAnimation(self, b"pos")
        anim.setDuration(300)
        anim.setEasingCurve(QEasingCurve.Type.InCubic)
        anim.setStartValue(self.pos())
        anim.setEndValue(QPoint((self.parent().width() - 300) // 2, -60))
        anim.finished.connect(self.hide)
        anim.start()


class RoomDialog(QDialog):
    def __init__(self, room=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stanze")
        self.setFixedWidth(360)
        self.room = room

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        title = QLabel("Modifica Stanza" if room else "Nuova Stanza")
        title.setStyleSheet("color: #f8fafc; font-size: 20px; font-weight: 700; font-family: 'Segoe UI';")
        layout.addWidget(title)

        nl = QLabel("Nome Stanza")
        nl.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: 600;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Es. Soggiorno")
        if room:
            self.name_input.setText(room['name'])
        layout.addWidget(nl)
        layout.addWidget(self.name_input)

        il = QLabel("Icona")
        il.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: 600;")
        layout.addWidget(il)

        ig = QGridLayout()
        ig.setSpacing(8)
        self.icon_btns = []
        icons = ['🛋️', '🛏️', '🍳', '🚿', '💻', '🚗', '🌳', '🔧', '📚', '🏋️']
        for i, icon in enumerate(icons):
            btn = QPushButton(icon)
            btn.setFixedSize(50, 50)
            btn.setStyleSheet("""
                QPushButton { background: #0f172a; border: 2px solid #334155; border-radius: 14px; font-size: 22px; }
                QPushButton:hover { border-color: #6366f1; }
                QPushButton:checked { border-color: #6366f1; background: rgba(99,102,241,0.2); }
            """)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, b=btn: self.select_icon(b))
            ig.addWidget(btn, i // 5, i % 5)
            self.icon_btns.append(btn)

        if room:
            for btn in self.icon_btns:
                if btn.text() == room.get('icon', '🛋️'):
                    btn.setChecked(True)
                    break
        else:
            self.icon_btns[0].setChecked(True)

        layout.addLayout(ig)

        bl = QHBoxLayout()
        bl.setSpacing(12)
        cb = ModernButton("Annulla", color='ghost')
        cb.clicked.connect(self.reject)
        sb = ModernButton("Salva", icon='💾', color='primary')
        sb.clicked.connect(self.accept)
        bl.addWidget(cb)
        bl.addWidget(sb)
        layout.addLayout(bl)

    def select_icon(self, selected):
        for btn in self.icon_btns:
            if btn != selected:
                btn.setChecked(False)

    def get_data(self):
        icon = '🛋️'
        for btn in self.icon_btns:
            if btn.isChecked():
                icon = btn.text()
                break
        return {'name': self.name_input.text().strip(), 'icon': icon}


class DeviceDialog(QDialog):
    def __init__(self, rooms, device=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dispositivi")
        self.setFixedWidth(360)
        self.device = device

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Modifica Dispositivo" if device else "Nuovo Dispositivo")
        title.setStyleSheet("color: #f8fafc; font-size: 20px; font-weight: 700; font-family: 'Segoe UI';")
        layout.addWidget(title)

        nl = QLabel("Nome Dispositivo")
        nl.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: 600;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Es. Lampada LED")
        if device:
            self.name_input.setText(device['name'])
        layout.addWidget(nl)
        layout.addWidget(self.name_input)

        rl = QLabel("Stanza")
        rl.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: 600;")
        self.room_combo = QComboBox()
        for room in rooms:
            self.room_combo.addItem(f"{room['icon']} {room['name']}", room['id'])
        if device:
            idx = self.room_combo.findData(device['roomId'])
            if idx >= 0:
                self.room_combo.setCurrentIndex(idx)
        layout.addWidget(rl)
        layout.addWidget(self.room_combo)

        tl = QLabel("Tipo")
        tl.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: 600;")
        self.type_combo = QComboBox()
        types = [('💡 Illuminazione', 'light'), ('❄️ Climatizzazione', 'climate'),
                 ('🔌 Elettrodomestico', 'appliance'), ('📺 Intrattenimento', 'entertainment'),
                 ('🔒 Sicurezza', 'security')]
        for label, val in types:
            self.type_combo.addItem(label, val)
        if device:
            idx = self.type_combo.findData(device['type'])
            if idx >= 0:
                self.type_combo.setCurrentIndex(idx)
        layout.addWidget(tl)
        layout.addWidget(self.type_combo)

        pl = QLabel("Consumo (Watt)")
        pl.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: 600;")
        self.power_input = QLineEdit()
        self.power_input.setPlaceholderText("Es. 60")
        self.power_input.setText(str(device['power']) if device else "60")
        layout.addWidget(pl)
        layout.addWidget(self.power_input)

        bl = QHBoxLayout()
        bl.setSpacing(12)
        cb = ModernButton("Annulla", color='ghost')
        cb.clicked.connect(self.reject)
        sb = ModernButton("Salva", icon='💾', color='primary')
        sb.clicked.connect(self.accept)
        bl.addWidget(cb)
        bl.addWidget(sb)
        layout.addLayout(bl)

    def get_data(self):
        return {
            'name': self.name_input.text().strip(),
            'roomId': self.room_combo.currentData(),
            'type': self.type_combo.currentData(),
            'power': int(self.power_input.text() or 0)
        }


# ============================================================
# SCHERMATE PRINCIPALI
# ============================================================

class LoginScreen(QWidget):
    login_success = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        logo = QLabel("🏠")
        logo.setStyleSheet("font-size: 72px;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("SmartHome")
        title.setStyleSheet(f"color: {COLORS['primary']}; font-size: 32px; font-weight: 700; font-family: 'Segoe UI';")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("La tua casa intelligente")
        subtitle.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 14px; font-family: 'Segoe UI';")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("📧  Email")
        self.email_input.setText("utente@smarthome.it")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("🔒  Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setText("password123")

        login_btn = ModernButton("Accedi", icon='🔑', color='primary')
        login_btn.clicked.connect(self.do_login)

        guest_btn = ModernButton("Accedi come Ospite", icon='👤', color='ghost')
        guest_btn.clicked.connect(self.do_guest)

        layout.addStretch()
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(30)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addSpacing(10)
        layout.addWidget(login_btn)
        layout.addWidget(guest_btn)
        layout.addStretch()

    def do_login(self):
        email = self.email_input.text()
        if not email:
            return
        self.login_success.emit({'name': email.split('@')[0], 'email': email})

    def do_guest(self):
        self.login_success.emit({'name': 'Ospite', 'email': 'ospite@smarthome.it'})


class HomeScreen(QWidget):
    room_add = pyqtSignal()
    room_edit = pyqtSignal(int)
    room_delete = pyqtSignal(int)
    room_filter = pyqtSignal(int)
    device_add = pyqtSignal()
    device_edit = pyqtSignal(int)
    device_delete = pyqtSignal(int)
    device_toggle = pyqtSignal(int, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(20)

        # Header
        header = QHBoxLayout()
        user_l = QHBoxLayout()
        self.avatar = QLabel("U")
        self.avatar.setFixedSize(44, 44)
        self.avatar.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS['primary']}, stop:1 {COLORS['secondary']});
            border-radius: 14px; color: white; font-size: 18px; font-weight: 700;
        """)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        gl = QVBoxLayout()
        self.greeting = QLabel("Ciao!")
        self.greeting.setStyleSheet("color: #f8fafc; font-size: 20px; font-weight: 700; font-family: 'Segoe UI';")
        welcome = QLabel("Benvenuto nella tua casa")
        welcome.setStyleSheet("color: #94a3b8; font-size: 13px; font-family: 'Segoe UI';")
        gl.addWidget(self.greeting)
        gl.addWidget(welcome)

        user_l.addWidget(self.avatar)
        user_l.addLayout(gl)
        header.addLayout(user_l)
        header.addStretch()

        # Stats
        stats = QHBoxLayout()
        stats.setSpacing(12)
        self.stat_power = StatCard("⚡", "2.4", "kW Attuali", COLORS['warning'])
        self.stat_temp = StatCard("🌡️", "22°", "Temperatura", COLORS['accent'])
        self.stat_hum = StatCard("💧", "45%", "Umidità", COLORS['primary'])
        stats.addWidget(self.stat_power)
        stats.addWidget(self.stat_temp)
        stats.addWidget(self.stat_hum)

        # Rooms header
        rh = QHBoxLayout()
        rt = QLabel("Le tue Stanze")
        rt.setStyleSheet("color: #f8fafc; font-size: 18px; font-weight: 700; font-family: 'Segoe UI';")
        arb = QPushButton("➕")
        arb.setFixedSize(36, 36)
        arb.setStyleSheet(f"QPushButton {{ background: {COLORS['primary']}; border-radius: 12px; border: none; font-size: 16px; }} QPushButton:hover {{ background: {COLORS['primary_dark']}; }}")
        arb.setCursor(Qt.CursorShape.PointingHandCursor)
        arb.clicked.connect(lambda: self.room_add.emit())
        rh.addWidget(rt)
        rh.addStretch()
        rh.addWidget(arb)

        # Rooms scroll
        rs = QScrollArea()
        rs.setWidgetResizable(True)
        rs.setFixedHeight(200)
        rs.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        rs.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        rs.setStyleSheet("background: transparent; border: none;")

        self.rooms_widget = QWidget()
        self.rooms_layout = QHBoxLayout(self.rooms_widget)
        self.rooms_layout.setSpacing(14)
        self.rooms_layout.setContentsMargins(0, 0, 0, 0)
        self.rooms_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        rs.setWidget(self.rooms_widget)

        # Devices header
        dh = QHBoxLayout()
        dt = QLabel("Dispositivi")
        dt.setStyleSheet("color: #f8fafc; font-size: 18px; font-weight: 700; font-family: 'Segoe UI';")
        adb = QPushButton("➕")
        adb.setFixedSize(36, 36)
        adb.setStyleSheet(f"QPushButton {{ background: {COLORS['primary']}; border-radius: 12px; border: none; font-size: 16px; }} QPushButton:hover {{ background: {COLORS['primary_dark']}; }}")
        adb.setCursor(Qt.CursorShape.PointingHandCursor)
        adb.clicked.connect(lambda: self.device_add.emit())
        dh.addWidget(dt)
        dh.addStretch()
        dh.addWidget(adb)

        self.devices_grid = QGridLayout()
        self.devices_grid.setSpacing(14)

        cl.addLayout(header)
        cl.addLayout(stats)
        cl.addLayout(rh)
        cl.addWidget(rs)
        cl.addLayout(dh)
        cl.addLayout(self.devices_grid)
        cl.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll)

    def set_user(self, user):
        self.greeting.setText(f"Ciao, {user['name']}!")
        self.avatar.setText(user['name'][0].upper())

    def update_rooms(self, rooms):
        while self.rooms_layout.count():
            item = self.rooms_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for room in rooms:
            card = RoomCard(room['id'], room['name'], room['icon'], room['devices'], room['color'])
            card.clicked.connect(self.room_filter.emit)
            card.edit_clicked.connect(self.room_edit.emit)
            card.delete_clicked.connect(self.room_delete.emit)
            self.rooms_layout.addWidget(card)
        self.rooms_layout.addStretch()

    def update_devices(self, devices, rooms):
        while self.devices_grid.count():
            item = self.devices_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        row, col = 0, 0
        for device in devices:
            room = next((r for r in rooms if r['id'] == device['roomId']), None)
            rn = room['name'] if room else 'Sconosciuto'
            icon = DEVICE_ICONS.get(device['type'], '🔌')
            card = DeviceCard(device['id'], device['name'], rn, icon, device['power'], device['on'])
            card.toggle_changed.connect(self.device_toggle.emit)
            card.edit_clicked.connect(self.device_edit.emit)
            card.delete_clicked.connect(self.device_delete.emit)
            self.devices_grid.addWidget(card, row, col)
            col += 1
            if col >= 2:
                col = 0
                row += 1

    def update_power(self, total_watts):
        for child in self.stat_power.findChildren(QLabel):
            if child.text() and any(c.isdigit() for c in child.text()):
                child.setText(f"{(total_watts / 1000):.1f}")
                break


class ConsumptionScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(16)

        title = QLabel("⚡ Consumo Energetico")
        title.setStyleSheet("color: #f8fafc; font-size: 20px; font-weight: 700; font-family: 'Segoe UI';")
        cl.addWidget(title)

        summary = QHBoxLayout()
        summary.setSpacing(12)
        summary.addWidget(self._create_summary("Consumo Oggi", "12.4", "kWh", COLORS['warning'], "↓ 8% vs ieri", True))
        summary.addWidget(self._create_summary("Stima Mese", "340", "kWh", COLORS['accent'], "↑ 3% vs mese scorso", False))
        cl.addLayout(summary)

        self.hourly_chart = ChartWidget("📈 Consumo Orario", 'line')
        hours = [f"{i}:00" for i in range(24)]
        hourly_data = [1.5 + 1.2 * (0.5 + 0.5 * ((i - 6) % 24 / 12)) + random.uniform(-0.3, 0.3) for i in range(24)]
        self.hourly_chart.set_data(hours, hourly_data)

        self.room_chart = ChartWidget("📊 Consumo per Stanza", 'bar')
        self.device_chart = ChartWidget("🥧 Distribuzione Dispositivi", 'pie')

        cl.addWidget(self.hourly_chart)
        cl.addWidget(self.room_chart)
        cl.addWidget(self.device_chart)
        cl.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll)

    def _create_summary(self, label, value, unit, color, change, is_down):
        card = QFrame()
        card.setObjectName("card")
        card.setMinimumHeight(100)

        l = QVBoxLayout(card)
        l.setContentsMargins(18, 18, 18, 18)
        l.setSpacing(4)

        lbl = QLabel(label)
        lbl.setStyleSheet("color: #94a3b8; font-size: 12px; font-family: 'Segoe UI';")

        val = QLabel(f'<span style="color: {color}; font-size: 26px; font-weight: 700;">{value}</span> <span style="color: #94a3b8; font-size: 14px;">{unit}</span>')
        val.setTextFormat(Qt.TextFormat.RichText)
        val.setStyleSheet("font-family: 'Segoe UI';")

        chg = QLabel(f"{'🟢' if is_down else '🔴'} {change}")
        chg.setStyleSheet(f"color: {'#22c55e' if is_down else '#ef4444'}; font-size: 12px; font-family: 'Segoe UI';")

        l.addWidget(lbl)
        l.addWidget(val)
        l.addWidget(chg)

        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 8)
        card.setGraphicsEffect(shadow)

        return card

    def update_charts(self, rooms):
        rn = [r['name'] for r in rooms]
        rd = [random.uniform(10, 60) for _ in rooms]
        rc = [r['color'] for r in rooms]
        self.room_chart.set_data(rn, rd, rc)

        dl = ['Illuminazione', 'Climatizzazione', 'Elettrodomestici', 'Intrattenimento', 'Sicurezza']
        dd = [15, 35, 25, 15, 10]
        dc = [COLORS['primary'], COLORS['secondary'], COLORS['warning'], COLORS['accent'], COLORS['success']]
        self.device_chart.set_data(dl, dd, dc)


class SettingsScreen(QWidget):
    logout_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title = QLabel("⚙️ Impostazioni")
        title.setStyleSheet("color: #f8fafc; font-size: 20px; font-weight: 700; font-family: 'Segoe UI';")
        layout.addWidget(title)

        sc = QFrame()
        sc.setObjectName("card")
        sl = QVBoxLayout(sc)
        sl.setContentsMargins(0, 8, 0, 8)
        sl.setSpacing(0)

        settings = [
            ("🌙", "Tema Scuro", "Attualmente attivo", True, COLORS['primary']),
            ("🔔", "Notifiche", "Avvisi consumo elevato", True, COLORS['success']),
            ("📶", "Connessione Auto", "Riconnetti dispositivi", True, COLORS['warning']),
            ("🛡️", "Sicurezza", "Modalità assente", False, COLORS['danger'])
        ]

        for i, (icon, name, desc, checked, color) in enumerate(settings):
            row = QHBoxLayout()
            row.setContentsMargins(16, 12, 16, 12)

            left = QHBoxLayout()
            il = QLabel(icon)
            il.setFixedSize(40, 40)
            il.setStyleSheet(f"background: {color}; border-radius: 12px; font-size: 18px;")
            il.setAlignment(Qt.AlignmentFlag.AlignCenter)

            info = QVBoxLayout()
            info.setSpacing(2)
            nl = QLabel(name)
            nl.setStyleSheet("color: #f8fafc; font-size: 15px; font-weight: 600; font-family: 'Segoe UI';")
            dl = QLabel(desc)
            dl.setStyleSheet("color: #94a3b8; font-size: 12px; font-family: 'Segoe UI';")
            info.addWidget(nl)
            info.addWidget(dl)

            left.addWidget(il)
            left.addLayout(info)
            left.addStretch()

            toggle = ToggleSwitch(checked)

            row.addLayout(left)
            row.addStretch()
            row.addWidget(toggle)

            sl.addLayout(row)

            if i < len(settings) - 1:
                line = QFrame()
                line.setFixedHeight(1)
                line.setStyleSheet("background: #334155;")
                sl.addWidget(line)

        layout.addWidget(sc)

        ac = QFrame()
        ac.setObjectName("card")
        al = QVBoxLayout(ac)
        al.setContentsMargins(20, 20, 20, 20)
        al.setSpacing(16)

        at = QLabel("👤 Informazioni Account")
        at.setStyleSheet("color: #f8fafc; font-size: 16px; font-weight: 600; font-family: 'Segoe UI';")
        al.addWidget(at)

        ur = QHBoxLayout()
        self.settings_avatar = QLabel("U")
        self.settings_avatar.setFixedSize(60, 60)
        self.settings_avatar.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS['primary']}, stop:1 {COLORS['secondary']});
            border-radius: 20px; color: white; font-size: 24px; font-weight: 700;
        """)
        self.settings_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ui = QVBoxLayout()
        self.settings_name = QLabel("Utente")
        self.settings_name.setStyleSheet("color: #f8fafc; font-size: 18px; font-weight: 700; font-family: 'Segoe UI';")
        self.settings_email = QLabel("utente@smarthome.it")
        self.settings_email.setStyleSheet("color: #94a3b8; font-size: 14px; font-family: 'Segoe UI';")
        ui.addWidget(self.settings_name)
        ui.addWidget(self.settings_email)

        ur.addWidget(self.settings_avatar)
        ur.addLayout(ui)
        ur.addStretch()

        al.addLayout(ur)

        logout_btn = ModernButton("Disconnetti", icon='🚪', color='danger')
        logout_btn.clicked.connect(self.logout_clicked.emit)
        al.addWidget(logout_btn)

        layout.addWidget(ac)
        layout.addStretch()

    def set_user(self, user):
        self.settings_name.setText(user['name'])
        self.settings_email.setText(user['email'])
        self.settings_avatar.setText(user['name'][0].upper())


class BottomNav(QFrame):
    tab_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(70)
        self.setStyleSheet("QFrame { background: rgba(15, 23, 42, 0.95); border-top: 1px solid #334155; }")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 12)
        layout.setSpacing(0)

        self.tabs = [("🏠", "Home", 0), ("📊", "Consumi", 1), ("⚙️", "Impostazioni", 2)]
        self.tab_buttons = []

        for icon, label, idx in self.tabs:
            btn = QPushButton(f"{icon}\n{label}")
            btn.setStyleSheet("""
                QPushButton { background: transparent; border: none; color: #94a3b8; font-size: 11px; font-family: 'Segoe UI'; padding: 4px 20px; }
                QPushButton:hover { color: #6366f1; }
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, i=idx: self.set_tab(i))
            layout.addWidget(btn)
            self.tab_buttons.append(btn)

        self.set_tab(0)

    def set_tab(self, index):
        for i, btn in enumerate(self.tab_buttons):
            if i == index:
                btn.setStyleSheet("""
                    QPushButton { background: transparent; border: none; color: #6366f1; font-size: 11px; font-family: 'Segoe UI'; padding: 4px 20px; font-weight: 600; }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton { background: transparent; border: none; color: #94a3b8; font-size: 11px; font-family: 'Segoe UI'; padding: 4px 20px; }
                    QPushButton:hover { color: #6366f1; }
                """)
        self.tab_changed.emit(index)


# ============================================================
# MAIN WINDOW
# ============================================================

class SmartHomeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartHome")
        self.setMinimumSize(400, 700)
        self.setMaximumSize(500, 900)

        self.rooms = [
            {'id': 1, 'name': 'Soggiorno', 'icon': '🛋️', 'devices': 5, 'color': '#6366f1'},
            {'id': 2, 'name': 'Camera', 'icon': '🛏️', 'devices': 3, 'color': '#ec4899'},
            {'id': 3, 'name': 'Cucina', 'icon': '🍳', 'devices': 4, 'color': '#f59e0b'},
            {'id': 4, 'name': 'Bagno', 'icon': '🚿', 'devices': 2, 'color': '#06b6d4'}
        ]

        self.devices = [
            {'id': 1, 'name': 'Lampada Principale', 'roomId': 1, 'type': 'light', 'power': 60, 'on': True},
            {'id': 2, 'name': 'Smart TV', 'roomId': 1, 'type': 'entertainment', 'power': 120, 'on': False},
            {'id': 3, 'name': 'Condizionatore', 'roomId': 1, 'type': 'climate', 'power': 800, 'on': True},
            {'id': 4, 'name': 'Lampada Comodino', 'roomId': 2, 'type': 'light', 'power': 40, 'on': False},
            {'id': 5, 'name': 'Termostato', 'roomId': 2, 'type': 'climate', 'power': 0, 'on': True},
            {'id': 6, 'name': 'Frigorifero', 'roomId': 3, 'type': 'appliance', 'power': 150, 'on': True},
            {'id': 7, 'name': 'Lavatrice', 'roomId': 3, 'type': 'appliance', 'power': 500, 'on': False},
            {'id': 8, 'name': 'Luce Bagno', 'roomId': 4, 'type': 'light', 'power': 50, 'on': False}
        ]

        self.current_user = None
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.stack = QStackedWidget()

        # Login
        self.login_screen = LoginScreen()
        self.login_screen.login_success.connect(self.on_login)
        self.stack.addWidget(self.login_screen)

        # Main container
        self.main_container = QWidget()
        ml = QVBoxLayout(self.main_container)
        ml.setContentsMargins(0, 0, 0, 0)
        ml.setSpacing(0)

        # Screens
        self.home_screen = HomeScreen()
        self.home_screen.room_add.connect(self.add_room)
        self.home_screen.room_edit.connect(self.edit_room)
        self.home_screen.room_delete.connect(self.delete_room)
        self.home_screen.room_filter.connect(self.filter_devices)
        self.home_screen.device_add.connect(self.add_device)
        self.home_screen.device_edit.connect(self.edit_device)
        self.home_screen.device_delete.connect(self.delete_device)
        self.home_screen.device_toggle.connect(self.toggle_device)

        self.consumption_screen = ConsumptionScreen()

        self.settings_screen = SettingsScreen()
        self.settings_screen.logout_clicked.connect(self.logout)

        self.content_stack = QStackedWidget()
        self.content_stack.addWidget(self.home_screen)
        self.content_stack.addWidget(self.consumption_screen)
        self.content_stack.addWidget(self.settings_screen)

        self.bottom_nav = BottomNav()
        self.bottom_nav.tab_changed.connect(self.switch_tab)

        ml.addWidget(self.content_stack)
        ml.addWidget(self.bottom_nav)

        self.stack.addWidget(self.main_container)
        layout.addWidget(self.stack)

        # Toast
        self.toast = ToastWidget(self)

        self.setStyleSheet(STYLE)

    def on_login(self, user):
        self.current_user = user
        self.home_screen.set_user(user)
        self.settings_screen.set_user(user)
        self.stack.setCurrentIndex(1)
        self.refresh_data()
        self.show_toast("Benvenuto nella tua SmartHome!")

    def logout(self):
        self.current_user = None
        self.stack.setCurrentIndex(0)
        self.switch_tab(0)

    def switch_tab(self, index):
        self.content_stack.setCurrentIndex(index)
        if index == 1:
            self.consumption_screen.update_charts(self.rooms)

    def refresh_data(self):
        self.update_room_counts()
        self.home_screen.update_rooms(self.rooms)
        self.home_screen.update_devices(self.devices, self.rooms)
        self.update_power()

    def update_room_counts(self):
        for room in self.rooms:
            room['devices'] = len([d for d in self.devices if d['roomId'] == room['id']])

    def update_power(self):
        total = sum(d['power'] for d in self.devices if d['on'])
        self.home_screen.update_power(total)

    def show_toast(self, msg, icon="✅"):
        self.toast.show_message(msg, icon)

    # CRUD Rooms
    def add_room(self):
        dlg = RoomDialog(parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            if not data['name']:
                self.show_toast("Inserisci un nome", "❌")
                return
            colors = ['#6366f1', '#ec4899', '#f59e0b', '#06b6d4', '#22c55e', '#8b5cf6']
            self.rooms.append({
                'id': max([r['id'] for r in self.rooms], default=0) + 1,
                'name': data['name'],
                'icon': data['icon'],
                'devices': 0,
                'color': colors[len(self.rooms) % len(colors)]
            })
            self.refresh_data()
            self.show_toast("Stanza aggiunta")

    def edit_room(self, room_id):
        room = next((r for r in self.rooms if r['id'] == room_id), None)
        if not room:
            return
        dlg = RoomDialog(room, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            room['name'] = data['name']
            room['icon'] = data['icon']
            self.refresh_data()
            self.show_toast("Stanza aggiornata")

    def delete_room(self, room_id):
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(self, "Conferma", "Eliminare questa stanza? I dispositivi associati verranno rimossi.")
        if reply == QMessageBox.StandardButton.Yes:
            self.rooms = [r for r in self.rooms if r['id'] != room_id]
            self.devices = [d for d in self.devices if d['roomId'] != room_id]
            self.refresh_data()
            self.show_toast("Stanza eliminata")

    def filter_devices(self, room_id):
        room = next((r for r in self.rooms if r['id'] == room_id), None)
        filtered = [d for d in self.devices if d['roomId'] == room_id]
        self.home_screen.update_devices(filtered, self.rooms)
        self.show_toast(f"Filtrato per {room['name'] if room else 'Sconosciuto'}")

    # CRUD Devices
    def add_device(self):
        dlg = DeviceDialog(self.rooms, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            if not data['name'] or not data['roomId']:
                self.show_toast("Compila tutti i campi", "❌")
                return
            self.devices.append({
                'id': max([d['id'] for d in self.devices], default=0) + 1,
                'name': data['name'],
                'roomId': data['roomId'],
                'type': data['type'],
                'power': data['power'],
                'on': False
            })
            self.refresh_data()
            self.show_toast("Dispositivo aggiunto")

    def edit_device(self, device_id):
        device = next((d for d in self.devices if d['id'] == device_id), None)
        if not device:
            return
        dlg = DeviceDialog(self.rooms, device, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            device['name'] = data['name']
            device['roomId'] = data['roomId']
            device['type'] = data['type']
            device['power'] = data['power']
            self.refresh_data()
            self.show_toast("Dispositivo aggiornato")

    def delete_device(self, device_id):
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(self, "Conferma", "Eliminare questo dispositivo?")
        if reply == QMessageBox.StandardButton.Yes:
            self.devices = [d for d in self.devices if d['id'] != device_id]
            self.refresh_data()
            self.show_toast("Dispositivo eliminato")

    def toggle_device(self, device_id, is_on):
        device = next((d for d in self.devices if d['id'] == device_id), None)
        if device:
            device['on'] = is_on
            self.refresh_data()
            self.show_toast(f"{device['name']} {'acceso' if is_on else 'spento'}")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = SmartHomeApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
