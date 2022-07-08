from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from guicapture import *
import os
import platform as pf
from pathlib import Path
import sys
import cv2
import time as tm
import numpy as np
from datetime import datetime
from threading import Thread as th

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
PATH_SDK = os.path.join(ROOT, r'Camera')
PATH_DATASET = os.path.join(ROOT, r'Dataset')

if str(PATH_SDK) not in sys.path:
    sys.path.append(str(PATH_SDK))

if str(PATH_DATASET) not in sys.path:
    sys.path.append(str(PATH_DATASET))

from Camera import mvsdk as sdk

class MyGUI(Ui_MainWindow):
    def __init__(self) -> None:
        super().setupUi(MainWindow)
        MainWindow.setWindowTitle('Capture Image By: Anurak Ch. [ ELECTRONICS ENG. ] ( Ctrl+Q for Exit )')
        MainWindow.setWindowIcon(QtGui.QIcon(r'Images-icon.png'))
        # MainWindow.setFixedWidth(1114)
        # MainWindow.setFixedHeight(820)
        # MainWindow.showFullScreen()
        # MainWindow.showMaximized()
        self.tmtx1 = QtCore.QTimer()
        self.tmtx1.timeout.connect(self.ShowPreview)
        self.tmtx1.setInterval(0.5)

        self.Dir = ''
        self.button()
        self.value_exposure = 30
        self.Exposure.setValue(self.value_exposure)
        self.SearchCamera()
        self.x_left_border = 80
        self.y_left_border = 950
        self.x_right_border = 2495 
        self.y_right_border = 1700

    def button(self):
        self.capture.clicked.connect  (self.captureimage)
        self.capture.setShortcut('Spacebar')
        self.selectdir.clicked.connect(self.GetDirectory)
        self.actionExit_Program.setShortcut('Ctrl+q')
        self.actionExit_Program.triggered.connect(self.closeProgram)
        self.stopCam.clicked.connect(self.stopPreview)
        self.X_left.editingFinished.connect(self.SetXleftBorder)
        self.Y_left.editingFinished.connect(self.SetYleftBorder)
        self.X_right.editingFinished.connect(self.SetXrightBorder)
        self.Y_right.editingFinished.connect(self.SetYrightBorder)
        self.Exposure.sliderReleased.connect(self.SetExposure)
        self.Exposure.actionTriggered.connect(self.SetExposure)

    def SetExposure(self):
        self.value_exposure = int(self.Exposure.value())
        sdk.CameraSetExposureTime(self.h_camera_index0, self.value_exposure * 1000)
        
    def SetXleftBorder(self):
        self.x_left_border = self.X_left.text()
        if self.x_left_border.isnumeric():
            self.x_left_border = int(self.x_left_border)
        else:
            self.X_left.clear()
            self.error_type()
        print(f'X left border: {self.x_left_border}')

    def SetYleftBorder(self):
        self.y_left_border = self.Y_left.text()
        if self.y_left_border.isnumeric():
            self.y_left_border = int(self.y_left_border)
        else:
            self.Y_left.clear()
            self.error_type()
        print(f'Y left border: {self.y_left_border}')

    def SetXrightBorder(self):
        self.x_right_border = self.X_right.text()
        if self.x_right_border.isnumeric():
            self.x_right_border = int(self.x_right_border)
        else:
            self.X_right.clear()
            self.error_type()
        print(f'X right border: {self.x_right_border}')
    
    def SetYrightBorder(self):
        self.y_right_border = self.Y_right.text()
        if self.y_right_border.isnumeric():
            self.y_right_border = int(self.y_right_border)
        else:
            self.Y_right.clear()
            self.error_type()
        print(f'X right border: {self.y_right_border}')

    def startComboBox(self):
        self.CameraIndex.currentIndexChanged.connect(self.setcamera)

    def error_type(self):
        msg = QMessageBox()
        msg.setWindowTitle('Type error!')
        msg.setText('Please enter integer only!')
        exit_msgbox = msg.exec_()

    def stopPreview(self):
        self.tmtx1.stop()
        self.Preview.clear()
        self.Preview.setText("Selected camera . . .")
        sdk.CameraUnInit(self.h_camera_index0)
        sdk.CameraAlignFree(self.pFrame0)

    def setcamera(self):
        self.SelectedCamera = self.CameraIndex.currentIndex()
        self.InitCamera()

    def closeProgram(self):
        try:
            sdk.CameraUnInit(self.h_camera_index0)
            sdk.CameraAlignFree(self.pFrame0)
            MainWindow.close()
        except:
            MainWindow.close()

    def GetDirectory(self):
        # Path for save Image
        self.Dir = QFileDialog.getExistingDirectory(caption = 'Select folder for save Image')
        self.showDir.setText(f'Directory: {self.Dir}')
    
    def captureimage(self):
        try:
            if self.Dir == '':
                # self.filename_cam0 = f'{ROOT}\Cam-' + str(datetime.now().strftime('%d-%m-%Y_%H-%M-%S')) + '.jpg'
                # cv2.imwrite(self.filename_cam0, self.frame_capture0)
                print(f'Capture success: {ROOT}\Cam-' + str(datetime.now().strftime('%d-%m-%Y_%H-%M-%S')) + '.jpg')
                
                # Save crop image
                self.cropimage(self.frame_capture0)
                self.filename_cropimage = f'{ROOT}\Cam_crop-' + str(datetime.now().strftime('%d-%m-%Y_%H-%M-%S')) + '.jpg'
                cv2.imwrite(self.filename_cropimage, self.cropppedimage)
                # cv2.imwrite(self.filename_cropimage, cv2.cvtColor(self.cropppedimage, cv2.COLOR_BGR2GRAY))
            else: 
                # self.filename_cam0 = f'{self.Dir}\Cam-' + str(datetime.now().strftime('%d-%m-%Y_%H-%M-%S')) + '.jpg'
                # cv2.imwrite(self.filename_cam0, self.frame_capture0)
                print(f'Capture success: {self.Dir}\Cam-' + str(datetime.now().strftime('%d-%m-%Y_%H-%M-%S')) + '.jpg')

                # Save crop image
                self.cropimage(self.frame_capture0)
                self.filename_cropimage = f'{self.Dir}\Cam_crop-' + str(datetime.now().strftime('%d-%m-%Y_%H-%M-%S')) + '.jpg'
                cv2.imwrite(self.filename_cropimage, self.cropppedimage)
                # cv2.imwrite(self.filename_cropimage, cv2.cvtColor(self.cropppedimage, cv2.COLOR_BGR2GRAY))
        except:
            print('Capture error')

    def ShowPreview(self):
        self.key_stream0 = cv2.waitKey(1)
        if self.key_stream0 == 27:
            self.tmtx1.stop()
        try:
            self.pRawData0, self.FrameHead0 = sdk.CameraGetImageBuffer(self.h_camera_index0, 200)
            sdk.CameraImageProcess(self.h_camera_index0, self.pRawData0, self.pFrame0, self.FrameHead0)
            sdk.CameraReleaseImageBuffer(self.h_camera_index0, self.pRawData0)
            
            if pf.system() == 'windows':
                sdk.CameraFlipFrameBuffer(self.pFrame0, self.FrameHead0, 1)

            self.frame_data0 = (sdk.c_ubyte * self.FrameHead0.uBytes).from_address(self.pFrame0)
            self.frame0 = np.frombuffer(self.frame_data0, dtype = np.uint8)
            self.frame0 = self.frame0.reshape((self.FrameHead0.iHeight, self.FrameHead0.iWidth, 1 if self.FrameHead0.uiMediaType == sdk.CAMERA_MEDIA_TYPE_MONO8 else 3))
            # # define frame_capture0 for use in detection process
            # self.frame_capture0 = cv2.flip(self.frame0, 0)
            self.frame_capture0 = cv2.flip(self.frame0, 1)
            # self.frame_capture0 = cv2.cvtColor(self.frame_capture0, cv2.COLOR_BGR2GRAY)
            self.height0, self.width0, self.channel0 = self.frame0.shape
            self.frame0 = cv2.flip(self.frame0, 1)
            # Boundging box in image from camera
            # .shape() is return (row, column, channel [3 is RGB image, 2 is gray scale])
            # Syntax cv2.rectangle(image, (x_lefttop, y_lefttop), (x_rightbottom, y_rightbottom), (color mode: rgb value), thickness)
            try:
                self.frame0 = cv2.rectangle(self.frame0, (self.x_left_border, self.y_left_border), (self.x_right_border, self.y_right_border), (0, 0, 255), 2)
            except:
                pass
            # Resized video stream
            self.frame0 = cv2.resize(self.frame0, (int(self.width0 * 42 / 100), int(self.height0 * 42 / 100)), interpolation = cv2.INTER_AREA)
            # # vertical flip
            # self.frame0 = cv2.flip(self.frame0, 0)
            # change color of image
            self.frame0 = cv2.cvtColor(self.frame0, cv2.COLOR_BGR2RGB)
            # self.frame0 = cv2.rotate(self.frame0, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.height0, self.width0, self.channel0 = self.frame0.shape
            self.step0 = self.channel0 * self.width0
            self.qImg0 = QImage(self.frame0.data, self.width0, self.height0, self.step0, QImage.Format_RGB888)
            # show image in img_label
            self.Preview.setPixmap(QPixmap.fromImage(self.qImg0))
        except sdk.CameraException as e:
            if sdk.CameraException != sdk.CAMERA_STATUS_TIME_OUT:
                print("CameraGetImageBuffer failed({}): {}" .format(e.error_code, e.message))
            pass

    def cropimage(self, img_original):
        # syntax for crop image: img[start_row : end_row, start_column : end_column]
        self.cropppedimage = img_original[self.y_left_border : self.y_right_border, self.x_left_border : self.x_right_border]
        
        filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        self.cropppedimage = cv2.GaussianBlur(self.cropppedimage, (3, 3), 0)
        self.cropppedimage = cv2.filter2D(self.cropppedimage, -1, filter)
        self.cropppedimage = cv2.blur(self.cropppedimage, (1, 1))
        
        print(f'Image size stream = {self.frame0.shape}')
        print(f'Image size original = {self.frame_capture0.shape}')
        print(f'Image size for crop = {self.cropppedimage.shape}')
        
    def SearchCamera(self):
        self.DevListCamera = sdk.CameraEnumerateDevice()
        self.DevListFound = len(self.DevListCamera)
        if self.DevListFound < 1:
            print('Can\'t find camera!')
            self.error_popup()
            sys.exit()
        else:
            print(f"Found: {self.DevListFound} device{'s' * (self.DevListFound > 1)}")
            self.startComboBox()
        for i, DevInfo in enumerate(self.DevListCamera):
            # Add item of found camera to combo box
            self.CameraIndex.addItem(f'{i}: {DevInfo.GetProductName()}')

    def error_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle('Camera Error!')
        msg.setText('Pleas check camera connection!')
        exit_msgbox = msg.exec_()
        # if exit_msgbox:
        #     sys.exit()

    def InitCamera(self):
        self.h_camera_index0 = 0
        try:
            self.h_camera_index0 = sdk.CameraInit(self.DevListCamera[self.SelectedCamera])
            print(f'Camera {self.SelectedCamera}: Success Initial')
        except sdk.CameraException:
            print(f'Camera {self.SelectedCamera}: Init Failed({sdk.CameraException.error_code}):{sdk.CameraException.message}')
        # Call method for Setup camera0
        self.SetUpCamera()
    
    def SetUpCamera(self):
        self.cap_0 = sdk.CameraGetCapability(self.h_camera_index0)
        self.monoCamera_0 = (self.cap_0.sIspCapacity.bMonoSensor != 0)
        if self.monoCamera_0:
            sdk.CameraSetIspOutFormat(self.h_camera_index0, sdk.CAMERA_MEDIA_TYPE_MONO8)
        else:
            sdk.CameraSetIspOutFormat(self.h_camera_index0, sdk.CAMERA_MEDIA_TYPE_BGR8)

        sdk.CameraSetTriggerMode(self.h_camera_index0, 0)

        sdk.CameraSetAeState(self.h_camera_index0, 0)
        sdk.CameraSetExposureTime(self.h_camera_index0, self.value_exposure * 1000)

        sdk.CameraPlay(self.h_camera_index0)
        
        self.FrameBufferSize0 = self.cap_0.sResolutionRange.iWidthMax * self.cap_0.sResolutionRange.iHeightMax * (1 if self.monoCamera_0 else 3)

        self.pFrame0 = sdk.CameraAlignMalloc(self.FrameBufferSize0, 16)
        print(f'Camera {self.SelectedCamera}: Setup Complete!')
        self.tmtx1.start()


obj = MyGUI()

if __name__ == '__main__':
    MainWindow.show()
    sys.exit(app.exec_())