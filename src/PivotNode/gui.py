#!/usr/bin/python3

import numpy as np
import new_era
import cv2
import time
import rospy
import serial
import PIL

from utils import *
from PySide2 import QtCore
from cv_bridge import CvBridge, CvBridgeError
from tkdnn_ros.msg import batchBbox
from sensor_msgs.msg import Image

from PySide2.QtCore import QSize, QThread, Signal, QTimer
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QImage, QPixmap

import torch
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


matplotlib.use("Qt5Agg")

serial_port = '/dev/ttyUSB1'

syringes = {'0.1 ml Hamilton': '1.47',
            '0.25 ml Hamilton': '2.30',
            '1 ml Hamilton': '4.61',
            '5 ml Hamilton': '10.30',
            '10 ml Hamilton': '14.60'}

maxRates = {
    '1.470': 1000,
    '2.300': 2500,
    '4.610': 10000,
    '10.30': 50000,
    '14.60': 100000
}

Xs = np.load("Xs.npy")[::8]

############# Start Configuring LeNet ############


use_cuda = torch.cuda.is_available()                   # check if GPU exists
device = torch.device("cuda:1" if use_cuda else "cpu")   # use CPU or GPU

transform = transforms.Compose([transforms.Resize([224, 224]),
                                transforms.ToTensor(),
                                transforms.Normalize(mean=[0.0943, 0.0428, 0.1029], std=[0.4348, 0.3602, 0.1520])])

lenet = torch.load("Lenet_last_model.pth")


def infer(model, x):
    model.eval()
    s = model(x)
    return s
################### End Configuring LeNet ####################


class UpdateCamThread(QThread):
    signal = Signal(np.ndarray)

    def __init__(self, parent=None):
        super(UpdateCamThread, self).__init__()
        self.fps = 60
        self.size = (512, 288)
        self.addCrossHair()

    def callback(self, image):
        bridge = CvBridge()
        img = bridge.imgmsg_to_cv2(image)
        frame = img.copy()
        frame = cv2.resize(
            frame, self.size, interpolation=cv2.INTER_CUBIC)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.frame = cv2.addWeighted(frame, 1, self.crossHair, 0.5, 0)
        self.signal.emit(self.frame)

    def addCrossHair(self):
        crossHair = cv2.imread("crossHair.png")
        crossHair = cv2.cvtColor(crossHair, cv2.COLOR_BGR2RGB)
        crossHair = cv2.resize(crossHair, self.size,
                               interpolation=cv2.INTER_CUBIC)
        self.crossHair = crossHair

    def run(self):
        while True:
            frame = cv2.imread("droplet.jpg")
            frame = cv2.resize(frame, self.size, interpolation=cv2.INTER_CUBIC)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self.frame = cv2.addWeighted(frame, 1, self.crossHair, 0.5, 0)
            self.signal.emit(self.frame)
            time.sleep(1)


class UpdateDetectionThread(QThread):
    """
    Take care of the detection box and send the img
    to the ML model.
    """
    signal_spec = Signal(np.ndarray, float, float)

    def __init__(self, parent=None):
        super(UpdateDetectionThread, self).__init__()
        self.fps = 60
        self.size = (100, 100)
        self.frame = np.zeros((self.size[1], self.size[0], 3))
        self.Xs = np.load("Xs.npy")[::8]

    def callback(self, batchBbox):
        bridge = CvBridge()
        img = bridge.imgmsg_to_cv2(batchBbox.img_processed)
        if len(batchBbox.batchBbox) != 0:
            bbox = batchBbox.batchBbox[-1]
            if bbox.x0 > 720 and bbox.x1 < 1200 and bbox.y0 > 200 and bbox.y1 < 800:
                # first convert BGR to RGB so that cv2 image
                # could be correctly converted to PIL
                bbox = cv2.cvtColor(
                    img[bbox.y0:bbox.y1, bbox.x0:bbox.x1], cv2.COLOR_BGR2RGB)

                # convert cv2 array to PIL images (to be made available for torch.transform)
                bbox = PIL.Image.fromarray(bbox)
                x = transform(bbox).view(1, 3, 224, 224)
                s = infer(lenet, x).data.cpu().numpy()

                peak, fwhm = getSpecInfo(s)

                self.signal_spec.emit(s, peak, fwhm)

    def run(self):
        while True:
            specs = np.load("20210716_spec_128pts.npy")
            s = specs[363]
            peak,fwhm = getSpecInfo(self.Xs, s)
            self.signal_spec.emit(s, peak, fwhm)


class Gui:
    def __init__(self):
        self.ui = QUiLoader().load("practice.ui")
        self.t_updateCam = UpdateCamThread()
        self.t_updateCam.signal.connect(self.displayStream)
        self.t_updateDetection = UpdateDetectionThread()
        self.t_updateDetection.signal_spec.connect(self.displaySpectrum)
        self.initUI()

    def initUI(self):
        self.ui.startStreamButton.clicked.connect(self.startStream)
        self.ser = serial.Serial(serial_port, 19200, timeout=.1)

        # add spectrum widget in specLayout
        dynamic_canvas = FigureCanvas(
            Figure(figsize=(1.6, 1.2), tight_layout={"rect": (0, 0, 0.9, 1)}))
        self.ui.specLayout.addWidget(dynamic_canvas)
        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._dynamic_ax.set_xlabel("Wavelength (nm)")
        self._dynamic_ax.set_ylabel("Reflectance (a. u.)")
        self.Xs = np.load("Xs.npy")[::8]
        self._line,  = self._dynamic_ax.plot(
            Xs, np.zeros((128,)), color="tab:orange")

        # grouped widgets
        self.syringeCombos = [self.ui.syringeCombo1,
                              self.ui.syringeCombo2, self.ui.syringeCombo3]
        self.pumpSliders = [self.ui.pumpSlider1,
                            self.ui.pumpSlider2, self.ui.pumpSlider3]
        self.minRateLabels = [self.ui.minRateLabel1,
                              self.ui.minRateLabel2, self.ui.minRateLabel3]
        self.maxRateLabels = [self.ui.maxRateLabel1,
                              self.ui.maxRateLabel2, self.ui.maxRateLabel3]
        self.setRateBoxes = [self.ui.setRateBox1,
                             self.ui.setRateBox2, self.ui.setRateBox3]
        self.currRateLabels = [self.ui.currRateLabel1,
                               self.ui.currRateLabel2, self.ui.currRateLabel3]
        for syringeCombo in self.syringeCombos:
            [syringeCombo.addItem(s) for s in syringes]

        # set mapper & pump attributes
        self.mapper = QtCore.QSignalMapper(self.ui)
        self.sliderMapper = QtCore.QSignalMapper(self.ui)
        self.currflow = dict()
        self.curr_state = "Stopped"
        self.pumps = [1, 2, 3]
        for i in range(len(self.pumps)):
            self.mapper.setMapping(self.syringeCombos[i], self.pumps[i])
            self.sliderMapper.setMapping(self.pumpSliders[i], self.pumps[i])

            self.syringeCombos[i].activated.connect(self.mapper.map)
            self.pumpSliders[i].sliderReleased.connect(self.sliderMapper.map)

        self.mapper.mapped.connect(self.updateSyringe)
        self.sliderMapper.mapped.connect(self.updateRate)
        self.ui.runPumpButton.clicked.connect(self.runUpdate)
        self.ui.stopPumpButton.clicked.connect(self.stop_all)

    def _update_canvas(self):
        t = np.linspace(0, 10, 101)
        # shift the sinusoid as a function of time
        self._line.set_data(t, np.sin(t + time.time()))
        self._line.figure.canvas.draw()

    def startStream(self):
        self.t_updateCam.start()
        self.t_updateDetection.start()

    def displayStream(self, frame):
        image = QImage(
            frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.ui.camStreamLabel.setPixmap(QPixmap.fromImage(image))

    def displaySpectrum(self, s, peak, fwhm):
        self._dynamic_ax.cla()
        self._line,  = self._dynamic_ax.plot(self.Xs, s, color="tab:orange")
        self._dynamic_ax.set_xlabel("Wavelength (nm)")
        self._dynamic_ax.set_ylabel("Reflectance (a. u.)")
        self._line.figure.canvas.draw()

        self.ui.peakPosLabel_val.setText("%.2f nm" % peak)
        self.ui.fwhmLabel_val.setText("%.2f nm" % fwhm)


    def updateSyringe(self, pump):
        if self.curr_state == 'Stopped':
            dia = syringes[str(self.mapper.mapping(pump).currentText())]
            new_era.set_diameter(self.ser, pump, dia)
            dia = new_era.get_diameter(self.ser, pump)
            self.ui.commandBarLabel.setText('Last command: pump %i set to %s (%s mm)' % (
                pump, self.mapper.mapping(pump).currentText(), dia))
            # set the max and min values of the slider bar
            i = self.pumps.index(pump)
            self.pumpSliders[i].setMinimum(0)
            self.pumpSliders[i].setMaximum(maxRates[str(dia)])
            self.minRateLabels[i].setText("0")
            self.maxRateLabels[i].setText("%dk" % (maxRates[str(dia)]/1000))

        else:
            self.ui.commandBarLabel.setText(
                "Can't change syringe while running")

    def updateRate(self, pump):
        i = self.pumps.index(pump)
        rate = self.pumpSliders[i].value()
        self.setRateBoxes[i].setText("%d" % rate)

    def runUpdate(self):
        # check if the flow rates are legit numbers, if not set to zero
        self.ui.runPumpButton.setChecked(1)
        self.ui.stopPumpButton.setChecked(0)
        rates = {}
        for pump in self.pumps:
            i = self.pumps.index(pump)
            if str(self.setRateBoxes[i].text()).strip()[1:].isdigit():
                rates[pump] = str(self.setRateBoxes[i].text()).strip()
            else:
                rates[pump] = '0'
                self.setRateBoxes[i].setText('0')

        if self.curr_state == 'Running':
            new_era.stop_all(self.ser)
            new_era.set_rates(self.ser, rates)
            new_era.run_all(self.ser)
            actual_rates = new_era.get_rates(self.ser, rates.keys())
            self.ui.commandBarLabel.setText(
                'Last command: update '+', '.join(['p%i=%s' % (p, actual_rates[p]) for p in actual_rates]))
            [self.currRateLabels[i].setText(
                actual_rates[pump]+' ul/hr') for i, pump in enumerate(self.pumps)]
            [self.pumpSliders[i].setValue(
                int(actual_rates[pump])) for i, pump in enumerate(self.pumps)]

        if self.curr_state == 'Stopped':
            new_era.set_rates(self.ser, rates)
            new_era.run_all(self.ser)
            self.curr_state = 'Running'
            actual_rates = new_era.get_rates(self.ser, rates.keys())
            self.ui.commandBarLabel.setText(
                'Last command: run '+', '.join(['p%i=%s' % (p, actual_rates[p]) for p in actual_rates]))
            [self.currRateLabels[i].setText(
                actual_rates[pump]+' ul/hr') for i, pump in enumerate(self.pumps)]
            [self.pumpSliders[i].setValue(
                int(actual_rates[pump])) for i, pump in enumerate(self.pumps)]

    def stop_all(self):
        self.ui.runPumpButton.setChecked(0)
        self.ui.stopPumpButton.setChecked(1)
        new_era.stop_all(self.ser)
        self.curr_state = 'Stopped'
        self.ui.commandBarLabel.setText('Last command: stop all pumps')
        [self.currRateLabels[i].setText(
            '0 ul/hr') for i, pump in enumerate(self.pumps)]


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    gui = Gui()
    gui.ui.show()
    app.exec_()
