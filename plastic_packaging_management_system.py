import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QStackedWidget, QWidget, QVBoxLayout, QLabel, QHBoxLayout,QStyledItemDelegate,QStyle,QListWidgetItem
from PySide6.QtGui import QPainter, QColor, QFont,QPolygon,QPalette
from PySide6.QtCore import Qt,QSize,QPoint,QEvent


class FactoryRecordManagement(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("出厂记录管理"))
        self.setLayout(layout)

class CirculationTrackingManagement(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("流通追踪管理"))
        self.setLayout(layout)

class LogManager(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("日志管理"))
        self.setLayout(layout)

class OrderManagement(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("订单管理"))
        self.setLayout(layout)

class RecyclingManagement(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("回收管理"))
        self.setLayout(layout)

class DiscardManagement(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("丢弃管理"))
        self.setLayout(layout)

class QualityInspectorManagement(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("质检员管理"))
        self.setLayout(layout)

class CustomDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option, index):
        # 检查是否为特殊的空白项
        if index.data(Qt.UserRole) == "blank":
            # 这里使用与QListWidget背景相同的颜色，以保持一致的外观
            # 直接使用默认背景色进行填充
            painter.fillRect(option.rect, option.palette.color(QPalette.Window))
            return
        
        # 绘制默认矩形
        rect = option.rect
        # 检查项是否被选中
        if option.state & QStyle.State_Selected:
            painter.fillRect(rect, QColor("#f0f0f0"))  # 选中时的背景色，使用调整后的矩形
            painter.setPen(QColor("black"))  # 选中时的文本颜色
        else:
            painter.setPen(QColor(50, 50, 50))  # 未选中时的文本颜色
        
        # 设置画笔颜色和字体
        painter.setFont(QFont("Arial", 12, QFont.Bold))  # 字体样式
        
        # 绘制文本，保持文本在调整后的矩形中居中
        painter.drawText(rect, Qt.AlignCenter, index.data())

        # 绘制右上角三角形
        topTriangle = QPolygon([
            rect.topRight(),  # 右上角
            rect.topRight() - QPoint(30 , 0),  # 向左移动30单位
            rect.topRight() - QPoint(0, 30)  # 向上移动30单位
        ])
        painter.drawPolygon(topTriangle)

        # 绘制右下角三角形，关于上三角x轴对称
        bottomTriangle = QPolygon([
            rect.bottomRight(),   # 右下角
            rect.bottomRight() - QPoint(30 , 0),  # 向左移动30单位
            rect.bottomRight() - QPoint(0, -30)  # 向下移动30单位
        ])
        painter.drawPolygon(bottomTriangle)

    def sizeHint(self, option, index):
        originalSize = super().sizeHint(option, index)
        extraSpace = 30  # 为三角形预留的额外空间

        # 中间的项不需要额外的空间
        newSize = originalSize + QSize(0, extraSpace)

        # 确保至少有40px的高度，再加上外部间距
        return newSize.expandedTo(QSize(0, 40 ))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("塑料包装管理和监测平台")
        self.setGeometry(100, 100, 900, 600) 
        # 初始化标志为False，表示当前没有重写光标形状
        self.cursorOverridden = False

        # 主布局和控件
        self.mainWidget = QWidget()
        self.mainLayout = QHBoxLayout()
        self.leftMenu = QListWidget()  # 使用自定义列表组件
        self.stack = QStackedWidget()

        self.setupUI()
        self.apply_styles()

    def eventFilter(self, watched, event):#更改鼠标形状的事件过滤器  
        if watched == self.leftMenu.viewport():  
            if event.type() == QEvent.MouseMove:  
                pos = event.position().toPoint()  
                item = self.leftMenu.itemAt(pos)  
                if item and item.data(Qt.UserRole) != "blank":  
                    self.leftMenu.viewport().setCursor(Qt.PointingHandCursor)  
                else:  
                    self.leftMenu.viewport().unsetCursor()  
        return super().eventFilter(watched, event)

    def setupUI(self):
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setLayout(self.mainLayout)

        # 设置左侧菜单容器及布局
        leftMenuContainer = QWidget()
        leftMenuLayout = QVBoxLayout()
        leftMenuContainer.setLayout(leftMenuLayout)

        # 添加弹性空间和左侧菜单
        leftMenuLayout.addWidget(self.leftMenu)  # 添加QListWidget

        # 设置左侧菜单
        self.leftMenu.setViewMode(QListWidget.ListMode)
        self.leftMenu.setItemDelegate(CustomDelegate())  # 应用自定义委托
        # 确保 leftMenu 有设置鼠标追踪，以便接收到 Hover 事件  
        self.leftMenu.setMouseTracking(True)  # 鼠标追踪
        self.leftMenu.viewport().installEventFilter(self)  # 应用事件过滤器，更改鼠标悬浮时的鼠标形状

        # 添加一个空白项作为列表的第一个项
        blankItem = QListWidgetItem()
        blankItem.setSizeHint(QSize(-1, 30))  # 设置空白项的高度为30像素
        self.leftMenu.addItem(blankItem)

        # 确保空白项不可选择和不可交互
        blankItem.setFlags(Qt.NoItemFlags)

        # 设置一个自定义角色数据标记这是一个空白项
        blankItem.setData(Qt.UserRole, "blank")

        self.leftMenu.addItem("出厂记录管理")
        self.leftMenu.addItem("流通追踪管理")
        self.leftMenu.addItem("订单管理")
        self.leftMenu.addItem("回收管理")
        self.leftMenu.addItem("丢弃管理")
        self.leftMenu.addItem("日志管理")
        self.leftMenu.addItem("质检员管理")

        # 调整 QListWidget 的大小,设置宽度为150px，高度为450px
        self.leftMenu.setFixedSize(150, 450) 


        # 设置模块
        self.stack.addWidget(FactoryRecordManagement())
        self.stack.addWidget(CirculationTrackingManagement())
        self.stack.addWidget(LogManager())
        self.stack.addWidget(OrderManagement())
        self.stack.addWidget(RecyclingManagement())
        self.stack.addWidget(DiscardManagement())
        self.stack.addWidget(QualityInspectorManagement())

        # 布局设置
        self.mainLayout.addWidget(leftMenuContainer)  # 修改这里
        self.mainLayout.addWidget(self.stack)

        # 连接信号
        self.leftMenu.currentRowChanged.connect(self.display)

    def display(self, index):
        self.stack.setCurrentIndex(index)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QListWidget {
                border: none;
                background: #e0e0e0;
                /*padding-top: 50px;*/
            }
            QLabel {
                font-size: 16px;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())