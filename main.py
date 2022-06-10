import sys
import os
import serial
import time
import numpy as np

import qt5_applications
dirname = os.path.dirname(qt5_applications.__file__)
plugin_path = os.path.join(dirname, 'Qt', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
import pyqtgraph as pg
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui import spectrographGUI as sgui

from utils.serialutils import sendorder, readlinedata, AngletoLambda
from utils.MapItoLambda import Calibrate
from utils.plot_and_save import save_image

import matplotlib
matplotlib.use('agg')

class ThreadPlot(QThread):
    """画图线程"""
    _signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # 数据初始化
        self.data = np.zeros([4097, ]) # 读取到的光谱数据，也是需要绘制的数据
        self.tmpdata = (0, 0) 
        # 临时数据，用于临时存储每次读到的数据，方便判断下位机状态，因为有时候会错误的读取到停止信号，其实并没有停止，因此需要和上一轮的信号对比
        
        # 画图窗口部分
        self.plot = pg.PlotWidget(enableAutoRange=True)
        self.plot.setYRange(-2, 1024) # 固定显示的Y轴范围
        self.curve = self.plot.plot(self.data) # 初始化显示
        
        # 控制部分
        self.flag = 0 # 0为默认状态，1为准备停止状态
        self.plotinterval = 0 # 如果每个循环都画4096个数据点会卡死，因此设置画图间隔，最小值还有待测试
        
        
    def run(self):
        
        while self.tmpdata != (-2, -2):
            
            if self.flag == 1: # 说明已经接收到了停止信号
                self.flag = 0
                break
            
            self.tmpdata = readlinedata(ser)
            print(self.tmpdata)
            self.data[min(4096, max(0, self.tmpdata[0]))] = self.tmpdata[1] # 不知道为什么有时候会读取到超出预设的DACSignal，所以限制一下
            
            # 更新画图
            self.plotinterval = (self.plotinterval + 1) % 20
            if self.plotinterval == 0:
                self.updateplot()
                
        while True:
            if readlinedata(ser) == (-1, -1) or readlinedata(ser) == (-2, -2):
                sendorder(ser, 0)
                if readlinedata(ser) == (-2, -2):
                    ui.printf("扫描已暂停")
                    break
                
        print("check flag")
        print(self.flag)
        print("###\n")
                
        if self.flag == 2: # 单次扫描的画图程序
        
            ui.printf("尝试绘制光谱图")
            start_time = time.ctime().replace(' ', '_').replace(':', '_')
            ly = threadPlot.data
            cal_i = np.array([1480, 2846])
            # cal_i = np.array([np.argmax(ly)])
            print("######", cal_i)
            '''if cal_i.size > 1:
                cal_i = np.array(cal_i[int(cal_i.size/2)])'''
            # cal_lambda = np.array([445.0*1e-9])
            cal_lambda = np.array([520.0*1e-9, 445*1e-9])
            map_fun = Calibrate(cal_i, cal_lambda)
            if map_fun is None:
                print("map_fun is None")
                return 
            lx_lambda = np.empty_like(ly)
            for i in range(lx_lambda.size):
                lx_lambda[i] = map_fun(i)
            save_path = f'results/spec_{start_time}.png'
            
            plot_start = time.time()
            save_image(lx_lambda, ly, save_path, cal_i, cal_lambda)
            plot_end = time.time()
            print(plot_end - plot_start)
            
            ui.printf(f"图片保存成功，名称为{save_path}")
        
        self.tmpdata = (0, 0)
                
        self._signal.emit()
                
    
    def updateplot(self):
        self.curve.setData(self.data)
        pg.QtWidgets.QApplication.processEvents()  
  
        
class ThreadCycleScan(QThread):
    """发送循环扫描指令的线程"""
    _signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        while readlinedata(ser) == (-2, -2):
            sendorder(ser, 2)
            
        ui.printf("开始循环扫描！")
        self._signal.emit()
        

class ThreadSingleScan(QThread):
    """发送单次扫描指令的线程"""
    _signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        if readlinedata(ser) != (-2, -2):
            ui.printf("仍在扫描中，尝试先暂停当前扫描")
            threadPlot.flag = 1
            time.sleep(0.5)
        cnt = sendorder(ser, 3)
        if cnt:
            ui.printf("单次扫描命令发送成功")
        
        threadPlot.flag = 2
        click_Plot()
        threadPlot.flag = 2
        
        print("单次扫描结束")
        
        # 待添加保存图片的功能
        
        self._signal.emit()
        
        
class ThreadStopScan(QThread):
    """发送暂停指令的线程"""
    _signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        ui.printf("尝试发送暂停指令")
        threadPlot.flag = 1 # 见ThreadPlot中的run()
        sendorder(ser, 0)
        sendorder(ser, 0)
        self._signal.emit()


class ThreadCalibrate(QThread):
    """发送校准指令的线程"""
    _signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        ui.printf("发送校准指令, 注意：此指令只在暂停状态下生效")
        while readlinedata(ser) != (-2, -2):
            threadPlot.flag = 1
            time.sleep(0.1)
        sendorder(ser, 1)
        
        self._signal.emit()
        

        
if __name__ == '__main__':
    
    # QWidget: Must construct a QApplication before a QWidget
    app = QApplication(sys.argv)
    
    # 进程实例化
    threadPlot = ThreadPlot()
    threadCycleScan = ThreadCycleScan()
    threadSingleScan = ThreadSingleScan()
    threadStopScan = ThreadStopScan()
    threadCalibrate = ThreadCalibrate()
    
    # GUI 
    MainWindow = QMainWindow()
    ui = sgui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    # 定义按钮对应的函数
    
    def click_Plot(): # 画图按钮
        def setButton():
            ui.PlotButton.setEnabled(True)
        ui.PlotButton.setEnabled(False)
        threadPlot._signal.connect(setButton)
        threadPlot.start()
    
    def click_CycleScan(): # 循环扫描按钮
        def setButton():
            ui.BeginScanButton.setEnabled(True)
        ui.BeginScanButton.setEnabled(False)
        threadCycleScan._signal.connect(setButton)
        threadCycleScan.start()
        
    def click_SingleScan(): # 单次扫描按钮
        def setButton():
            ui.SingleScanButton.setEnabled(True)
        ui.SingleScanButton.setEnabled(False)
        threadSingleScan._signal.connect(setButton)
        threadSingleScan.start()
        
    def click_StopScan(): # 暂停按钮
        def setButton():
            ui.StopScanButton.setEnabled(True)
        ui.StopScanButton.setEnabled(False)
        threadStopScan._signal.connect(setButton)
        threadStopScan.start()
        
    def click_Calibrate(): # 校准按钮
        def setButton():
            ui.CalibrateButton.setEnabled(True)
        ui.CalibrateButton.setEnabled(False)
        threadCalibrate._signal.connect(setButton)
        threadCalibrate.start()
    
    def click_KillApp(): # 关闭程序按钮
        app = QApplication.instance() # 获取当前在运行的实例
        app.quit()
    
    
    # 绑定按钮函数以及画图窗口
    ui.Spectrograph_Window.addWidget(threadPlot.plot)
    ui.PlotButton.clicked.connect(click_Plot)
    ui.BeginScanButton.clicked.connect(click_CycleScan)
    ui.SingleScanButton.clicked.connect(click_SingleScan)
    ui.CalibrateButton.clicked.connect(click_Calibrate)
    ui.StopScanButton.clicked.connect(click_StopScan)
    ui.KillButton.clicked.connect(click_KillApp)
    
    # 串口通信
    serialPort = "COM8"
    baudRate = 115200
    ser = serial.Serial(serialPort, baudRate, timeout=0.5)
    
    while ser.is_open is False:
        # 判断串口是否已经打开
        time.sleep(0.1)
        
    ui.printf("serial open success")
    ui.printf("serial={}, baudRate={}".format(serialPort, baudRate))
    
    
    sys.exit(app.exec_())


