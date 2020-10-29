import os
import numpy as np
from sys import argv as SYS_argv
from sys import exit as SYS_exit
from re import search as RE_search
from time import sleep as TIME_sleep
from threading import Thread as THREADING_Thread
from copy import deepcopy as COPY_deepcopy
from UI import Ui_MainWindow
from PIL import Image,ImageQt
from PyQt5.Qt import QPoint
from PyQt5.QtGui import QPixmap,QIntValidator
from PyQt5.QtCore import Qt,QTimer,pyqtSignal
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QMessageBox

CLEAN_LIMITE = 20
ZOOM_LIMITE = 80
BACKUP_LIMITE = 200

class Functional_Arithmetic:
    def __init__(self):
        pass
        pass

    def Cutout_image(self,x0,y0,mode):
        #0:由鼠标唤起
        #1~4:由半自动唤起
        #5~8:由全自动唤起
        if mode == 0:
            self.System_busy()
        elif mode == 1:
            x0 = 0
            y0 = 0
        elif mode == 2:
            x0 = 0
            y0 = self.current_image_image.size[1] - 1
        elif mode == 3:
            x0 = self.current_image_image.size[0] - 1
            y0 = 0
        elif mode == 4:
            x0 = self.current_image_image.size[0] - 1
            y0 = self.current_image_image.size[1] - 1
        elif mode == 5:
            x0 = 0
            y0 = 0
        elif mode == 6:
            x0 = 0
            y0 = self.current_image_image.size[1] - 1
        elif mode == 7:
            x0 = self.current_image_image.size[0] - 1
            y0 = 0
        elif mode == 8:
            x0 = self.current_image_image.size[0] - 1
            y0 = self.current_image_image.size[1] - 1

        self.cruuent_image_edited = True
        color = np.array(self.color)
        tolerance = self.tolerance
        transparent = np.array([0,0,0,0])
        stack = list()
        stack.append((x0,y0))
        count = 0
        while True:
            if len(stack) == 0:
                break

            x,y = stack.pop()
            self.current_image_array[y,x] = transparent
            
            if count == 0:
                if self.tomede:
                    self.On_revoke_button_clicked()
                    self.System_free()
                    return
                else:
                    self.current_image_image = Image.fromarray(self.current_image_array)
                    self.Draw_image_lable()
                count = 1
                    
            if x + 1 < self.current_image_image.size[0] and \
            all(abs(self.current_image_array[y,x + 1] - color) <= tolerance) and \
            self.current_image_array[y,x + 1][3] != 0:
                stack.append((x + 1,y))
                count = count + 1 if count < 10000 else 0
                
            if x - 1 >= 0 and \
            all(abs(self.current_image_array[y,x - 1] - color) <= tolerance) and \
            self.current_image_array[y,x - 1][3] != 0:
                stack.append((x - 1,y))
                count = count + 1 if count < 10000 else 0
                
            if y + 1 < self.current_image_image.size[1] and \
            all(abs(self.current_image_array[y + 1,x] - color) <= tolerance) and \
            self.current_image_array[y + 1,x][3] != 0:
                stack.append((x,y + 1))
                count = count + 1 if count < 10000 else 0

            if y - 1 >= 0 and \
            all(abs(self.current_image_array[y - 1,x] - color) <= tolerance) and \
            self.current_image_array[y - 1,x][3] != 0:
                stack.append((x,y - 1))
                count = count + 1 if count < 10000 else 0

        self.current_image_image = Image.fromarray(self.current_image_array)

        if mode == 0:
            self.Insert_backup()
            self.Draw_image_lable()
            self.System_free()
        elif mode == 1:
            t = THREADING_Thread(target=self.Cutout_image,args=(x0,y0,2,))
            t.start()
        elif mode == 2:
            t = THREADING_Thread(target=self.Cutout_image,args=(x0,y0,3,))
            t.start()
        elif mode == 3:
            t = THREADING_Thread(target=self.Cutout_image,args=(x0,y0,4,))
            t.start()
        elif mode == 4:          
            self.Insert_backup()
            self.Draw_image_lable()
            self.System_free()
        elif mode == 5:
            t = THREADING_Thread(target=self.Cutout_image,args=(x0,y0,6,))
            t.start()
        elif mode == 6:
            t = THREADING_Thread(target=self.Cutout_image,args=(x0,y0,7,))
            t.start()
        elif mode == 7:
            t = THREADING_Thread(target=self.Cutout_image,args=(x0,y0,8,))
            t.start()
        elif mode == 8:
            self.Draw_image_lable() 

            if self.image_index == len(self.images) - 1:
                self.Save_image()
                self.System_free()
            else:
                self.On_next_button_clicked()
                TIME_sleep(0.01)
                t = THREADING_Thread(target=self.Auto_pick_color,args=(5,))
                t.start()

    def Filling_image(self,x0,y0):
        #这玩意只能由鼠标唤起
        self.System_busy()

        self.cruuent_image_edited = True
        initial_color = self.current_image_array[y0,x0].copy()
        tolerance = self.tolerance
        color = np.array(self.color)
        stack = list()
        stack.append((x0,y0))
        count = 1
        while True:
            if len(stack) == 0:
                break

            x,y = stack.pop()
            self.current_image_array[y,x] = color

            if count == 0:
                if self.tomede:
                    self.On_revoke_button_clicked()
                    self.System_free()
                    return
                else:
                    self.current_image_image = Image.fromarray(self.current_image_array)
                    self.Draw_image_lable()
                count = 1
            
            if x + 1 < self.current_image_image.size[0] and \
            all(abs(self.current_image_array[y,x + 1] - initial_color) <= tolerance) and \
            any(self.current_image_array[y,x + 1] != color):
                stack.append((x + 1,y))
                count = count + 1 if count < 10000 else 0
                
            if x - 1 >= 0 and \
            all(abs(self.current_image_array[y,x - 1] - initial_color) <= tolerance) and \
            any(self.current_image_array[y,x - 1] != color):
                stack.append((x - 1,y))
                count = count + 1 if count < 10000 else 0
                
            if y + 1 < self.current_image_image.size[1] and \
            all(abs(self.current_image_array[y + 1,x] - initial_color) <= tolerance) and \
            any(self.current_image_array[y + 1,x] != color):
                stack.append((x,y + 1))
                count = count + 1 if count < 10000 else 0

            if y - 1 >= 0 and \
            all(abs(self.current_image_array[y - 1,x] - initial_color) <= tolerance) and \
            any(self.current_image_array[y - 1,x] != color):
                stack.append((x,y - 1)) 
                count = count + 1 if count < 10000 else 0
 
        self.current_image_image = Image.fromarray(self.current_image_array)
        self.Insert_backup()
        self.Draw_image_lable()
        self.System_free()

    def Clean_image(self):
        self.System_busy()
        
        self.cruuent_image_edited = True
        transparent = np.array([0,0,0,0])
        all_pixels = [(x,y) for x in range(self.current_image_image.size[0])\
                            for y in range(self.current_image_image.size[1])\
                            if self.current_image_array[y,x][3] != 0]
        stack = list()
        count = 1
        visited = [[0] * self.current_image_image.size[0] for i in range(self.current_image_image.size[1])]

        while len(all_pixels) != 0:
            pixel = all_pixels[0]
            stack.append(pixel)
            visited[pixel[1]][pixel[0]] = 1
            block = [pixel]
            all_pixels.remove(pixel)

            while True:
                if len(stack) == 0:
                    break

                x,y = stack.pop()

                if count == 0:
                    if self.tomede:
                        self.cruuent_image_edited = False
                        self.On_revoke_button_clicked()
                        self.System_free()
                        return
                    else:
                        self.current_image_image = Image.fromarray(self.current_image_array)
                        self.Draw_image_lable()
                    count = 1
       
                if x + 1 < self.current_image_image.size[0] and \
                visited[y][x + 1] == 0 and \
                self.current_image_array[y,x + 1][3] != 0:
                    stack.append((x + 1,y))
                    visited[y][x + 1] = 1
                    block.append((x + 1,y))
                    all_pixels.remove((x + 1,y))
                    count = count + 1 if count < 10000 else 0
                
                if x - 1 >= 0 and \
                visited[y][x - 1] == 0 and \
                self.current_image_array[y,x - 1][3] != 0:
                    stack.append((x - 1,y))
                    visited[y][x - 1] = 1
                    block.append((x - 1,y))
                    all_pixels.remove((x - 1,y))
                    count = count + 1 if count < 10000 else 0
                
                if y + 1 < self.current_image_image.size[1] and \
                visited[y + 1][x] == 0 and \
                self.current_image_array[y + 1,x][3] != 0:
                    stack.append((x,y + 1))
                    visited[y + 1][x] = 1
                    block.append((x,y + 1))
                    all_pixels.remove((x,y + 1))
                    count = count + 1 if count < 10000 else 0

                if y - 1 >= 0 and \
                visited[y - 1][x] == 0 and \
                self.current_image_array[y - 1,x][3] != 0:
                    stack.append((x,y - 1))
                    visited[y - 1][x] = 1
                    block.append((x,y - 1))
                    all_pixels.remove((x,y - 1))
                    count = count + 1 if count < 10000 else 0
        
            if len(block) < CLEAN_LIMITE:
                for pixel in block:
                    self.current_image_array[pixel[1],pixel[0]] = transparent

        self.current_image_image = Image.fromarray(self.current_image_array)
        self.Draw_image_lable()
        
        self.System_free()

    def Crop_image(self,mode):
        #0:由鼠标唤起
        #1~4:由半自动唤起
        #5~8:由全自动唤起
        if mode == 0:
            self.System_busy()

        self.cruuent_image_edited = True
        tolerance = self.tolerance
        color = np.array(self.color)
        left,upper,right,lower = 0,0,0,0

        flag = 0
        for x in range(self.current_image_image.size[0]):
            for y in range(self.current_image_image.size[1]):
                if not all(abs(self.current_image_array[y,x] - color) <= tolerance):
                    left = x
                    flag = 1
                    break
            if flag == 1 :
                break

        if self.tomede:
            self.On_revoke_button_clicked()
            self.System_free()
            return

        flag = 0
        for y in range(self.current_image_image.size[1]):
            for x in range(self.current_image_image.size[0]):
                if not all(abs(self.current_image_array[y,x] - color) <= tolerance):
                    upper = y
                    flag = 1
                    break
            if flag == 1 :
                break

        if self.tomede:
            self.On_revoke_button_clicked()
            self.System_free()
            return

        flag = 0
        for x in range(self.current_image_image.size[0] - 1,-1,-1):
           for y in range(self.current_image_image.size[1]):
               if not all(abs(self.current_image_array[y,x] - color) <= tolerance):
                   right = x
                   flag = 1
                   break
           if flag == 1 :
               break

        if self.tomede:
            self.On_revoke_button_clicked()
            self.System_free()
            return

        flag = 0
        for y in range(self.current_image_image.size[1] - 1,-1,-1):
            for x in range(self.current_image_image.size[0]):
                if not all(abs(self.current_image_array[y,x] - color) <= tolerance):
                    lower = y
                    flag = 1
                    break
            if flag == 1 :
                break

        if self.tomede:
            self.On_revoke_button_clicked()
            self.System_free()
            return

        self.current_image_image = self.current_image_image.crop((left,upper,right + 1,lower + 1))
        self.current_image_array = np.array(self.current_image_image)

        self.Image_H_Scrollbar.blockSignals(True)
        self.Image_V_Scrollbar.blockSignals(True)
        self.scrollbar_offset = [0,0]
        self.Image_H_Scrollbar.setValue(0)
        self.Image_V_Scrollbar.setValue(0)
        self.Set_scrollbar()
        self.Image_H_Scrollbar.blockSignals(False)
        self.Image_V_Scrollbar.blockSignals(False)

        if mode == 0:
            self.Insert_backup()
            self.Draw_image_lable()
            self.System_free()
        if mode == 1:
            self.Draw_image_lable()
            t = THREADING_Thread(target=self.Cutout_image,args=(0,0,1,))
            t.start()
        elif mode == 5:
            self.Draw_image_lable()
            t = THREADING_Thread(target=self.Cutout_image,args=(0,0,5,))
            t.start()

    def Auto_pick_color(self,mode):
        #0:由系统唤起
        #1~4:由半自动唤起
        #5~8:由全自动唤起
        colors = {}

        y1 = 0
        y2 = self.current_image_image.size[1] - 1
        for x in range(self.current_image_image.size[0]): 
            if tuple(self.current_image_array[y1,x]) in colors:
                colors[tuple(self.current_image_array[y1,x])] += 1
            else:
                colors[tuple(self.current_image_array[y1,x])] = 1
            if tuple(self.current_image_array[y2,x]) in colors:
                colors[tuple(self.current_image_array[y2,x])] += 1
            else:
                colors[tuple(self.current_image_array[y2,x])] = 1

        x1 = 0
        x2 = self.current_image_image.size[0] - 1
        for y in range(self.current_image_image.size[1]): 
            if tuple(self.current_image_array[y,x1]) in colors:
                colors[tuple(self.current_image_array[y,x1])] += 1
            else:
                colors[tuple(self.current_image_array[y,x1])] = 1
            if tuple(self.current_image_array[y,x2]) in colors:
                colors[tuple(self.current_image_array[y,x2])] += 1
            else:
                colors[tuple(self.current_image_array[y,x2])] = 1

        result = max(colors.values())
        color = [k for k,v in colors.items() if v == result]
        color = list(color[0])

        self.R_Value.setText(str(color[0]))
        self.G_Value.setText(str(color[1]))
        self.B_Value.setText(str(color[2]))
        self.A_Value.setText(str(color[3]))

        if mode == 1:
            t = THREADING_Thread(target=self.Crop_image,args=(1,))
            t.start()
        elif mode == 5:
            t = THREADING_Thread(target=self.Crop_image,args=(5,))
            t.start()

    def Save_image(self):
        if self.image_loaded:
            if not os.path.isdir("done"):
                os.makedirs("done")

            self.images[self.image_index] = self.current_image_image.copy()
            index = len(self.file_names[self.image_index]) - self.file_names[self.image_index][::-1].find('.')
            self.current_image_image.save('done/' + self.file_names[self.image_index][:index] + 'png')

    def Import_path(self,path):
        if self.cruuent_image_edited:
            self.Save_image()

        image_backup = COPY_deepcopy(self.images)
        image_index_backup = self.image_index

        self.cruuent_image_edited = False
        self.image_index = 0
        self.zoom = 1
        self.images = ['']
        self.file_names = ['']

        self.scrollbar_offset = [0,0]
        self.Image_H_Scrollbar.blockSignals(True)
        self.Image_V_Scrollbar.blockSignals(True)
        self.Image_H_Scrollbar.setValue(0)
        self.Image_V_Scrollbar.setValue(0)
        self.Image_H_Scrollbar.blockSignals(False)
        self.Image_V_Scrollbar.blockSignals(False)

        for root,dir,filelist in os.walk(path):
            for file in filelist:
                if RE_search('(jpg|jpeg|png|webp|bmp|tif|tga|JPG|JPEG|PNG|WEBP|BMP|TIF|TGA)$',file):
                    self.images.append(Image.open(root + '/' + file))
                    self.file_names.append(file)
            break

        if len(self.images) <= 1:
            QMessageBox.question(self,'这个目录里没有图片','小老弟你怎么回事？',QMessageBox.Yes)
            self.images = COPY_deepcopy(image_backup)
            self.image_index = image_index_backup
            return

        self.image_index = 1
        self.current_image_image = self.images[self.image_index].copy().convert('RGBA')
        self.current_image_array = np.array(self.current_image_image)

        self.backup_pin = 0
        self.backup = [self.current_image_image.copy()]

        self.Set_scrollbar()
        self.Set_image_background()
        self.Draw_image_lable()
        self.image_loaded = True

    def Import_image(self,path_list):
        if self.cruuent_image_edited:
            self.Save_image()

        image_backup = COPY_deepcopy(self.images)
        image_index_backup = self.image_index

        self.cruuent_image_edited = False
        self.image_index = 0
        self.zoom = 1
        self.images = ['']
        self.file_names = ['']

        self.scrollbar_offset = [0,0]
        self.Image_H_Scrollbar.blockSignals(True)
        self.Image_V_Scrollbar.blockSignals(True)
        self.Image_H_Scrollbar.setValue(0)
        self.Image_V_Scrollbar.setValue(0)
        self.Image_H_Scrollbar.blockSignals(False)
        self.Image_V_Scrollbar.blockSignals(False)

        for path in path_list:
            self.images.append(Image.open(path))
            self.file_names.append(path[(len(path) - path[::-1].find('/')):])
            
        self.image_index = 1
        self.current_image_image = self.images[self.image_index].copy().convert('RGBA')
        self.current_image_array = np.array(self.current_image_image)

        self.backup_pin = 0
        self.backup = [self.current_image_image.copy()]

        self.Set_scrollbar()
        self.Set_image_background()
        self.Draw_image_lable()
        self.image_loaded = True


class Color_Lable:
    def __init__(self):
        self.color = [255,255,255,255]
        self.color_preview_background = Image.open('res/Transparent_Lable.png').convert('RGBA')

    def Draw_color_preview_lable(self):
        color_preview_image = Image.new('RGBA', (120,120), (self.color[0],self.color[1],self.color[2],self.color[3]))
        color_preview_background = self.color_preview_background.resize((120,120)).copy()
        color_preview_background.alpha_composite(color_preview_image)
        
        self.Color_Preview_Lable.setPixmap(ImageQt.toqpixmap(color_preview_background))

    def On_R_value_textChanged(self):
        text = self.R_Value.text()

        if len(text) == 0:
            text = '0'
        elif text[0] == '0' and len(text) > 1:
            for i in range(len(text)):
                if text[0] == '0':
                   text = text.replace('0','',1)
                else:
                    break

            if len(text) == 0:
                text = '0'

        self.R_Scrollbar.setValue(eval(text))
        self.color[0] = eval(text)

        self.Draw_color_preview_lable()

    def On_G_value_textChanged(self):
        text = self.G_Value.text()

        if len(text) == 0:
            text = '0'
        elif text[0] == '0' and len(text) > 1:
            for i in range(len(text)):
                if text[0] == '0':
                   text = text.replace('0','',1)
                else:
                    break

            if len(text) == 0:
                text = '0'

        self.G_Scrollbar.setValue(eval(text))
        self.color[1] = eval(text)

        self.Draw_color_preview_lable()

    def On_B_value_textChanged(self):
        text = self.B_Value.text()

        if len(text) == 0:
            text = '0'
        elif text[0] == '0' and len(text) > 1:
            for i in range(len(text)):
                if text[0] == '0':
                   text = text.replace('0','',1)
                else:
                    break

            if len(text) == 0:
                text = '0'

        self.B_Scrollbar.setValue(eval(text))
        self.color[2] = eval(text)

        self.Draw_color_preview_lable()

    def On_A_value_textChanged(self):
        text = self.A_Value.text()

        if len(text) == 0:
            text = '0'
        elif text[0] == '0' and len(text) > 1:
            for i in range(len(text)):
                if text[0] == '0':
                   text = text.replace('0','',1)
                else:
                    break

            if len(text) == 0:
                text = '0'

        self.A_Scrollbar.setValue(eval(text))
        self.color[3] = eval(text)

        self.Draw_color_preview_lable()

    def On_R_scrollbar_valueChanged(self):
        self.R_Value.setText(str(self.R_Scrollbar.value()))
        pass

    def On_G_scrollbar_valueChanged(self):
        self.G_Value.setText(str(self.G_Scrollbar.value()))
        pass

    def On_B_scrollbar_valueChanged(self):
        self.B_Value.setText(str(self.B_Scrollbar.value()))
        pass

    def On_A_scrollbar_valueChanged(self):
        self.A_Value.setText(str(self.A_Scrollbar.value()))
        pass


class Image_Lable:
    def __init__(self):
        self.zoom = 1
        self.scrollbar_offset = [0,0]
        self.current_image_image = Image.new('RGBA',(100,100))
        self.current_image_array = np.array(self.current_image_image)
        self.image_lable_background = Image.open('res/TransparentBg-W.png').convert('RGBA')

    def Draw_image_lable(self):
        drwan_image_rect = [0,0,0,0]
        drwan_image_rect[0] = self.scrollbar_offset[0]\
                              if self.current_image_image.size[0] * self.zoom > self.Image_Lable.width()\
                              else 0
        drwan_image_rect[1] = self.scrollbar_offset[1]\
                              if self.current_image_image.size[1] * self.zoom > self.Image_Lable.height() \
                              else 0
        drwan_image_rect[2] = self.Image_Lable.width() + self.scrollbar_offset[0]\
                              if self.current_image_image.size[0] * self.zoom > self.Image_Lable.width()\
                              else self.current_image_image.size[0] * self.zoom
        drwan_image_rect[3] = self.Image_Lable.height() + self.scrollbar_offset[1]\
                              if self.current_image_image.size[1] * self.zoom > self.Image_Lable.height() \
                              else self.current_image_image.size[1] * self.zoom

        drwan_lable_rect = [0,0,0,0]
        drwan_lable_rect[0] = 0\
                              if self.current_image_image.size[0] * self.zoom > self.Image_Lable.width()\
                              else (self.Image_Lable.width() - self.current_image_image.size[0] * self.zoom) // 2
        drwan_lable_rect[1] = 0\
                              if self.current_image_image.size[1] * self.zoom > self.Image_Lable.height() \
                              else (self.Image_Lable.height() - self.current_image_image.size[1] * self.zoom) // 2
        drwan_lable_rect[2] = self.Image_Lable.width()\
                              if self.current_image_image.size[0] * self.zoom > self.Image_Lable.width()\
                              else drwan_lable_rect[0] + self.current_image_image.size[0] * self.zoom
        drwan_lable_rect[3] = self.Image_Lable.height()\
                              if self.current_image_image.size[1] * self.zoom > self.Image_Lable.height() \
                              else drwan_lable_rect[1] + self.current_image_image.size[1] * self.zoom

        temp_image = self.current_image_image.resize((drwan_image_rect[2] - drwan_image_rect[0],drwan_image_rect[3] - drwan_image_rect[1]),\
                                                      Image.NEAREST,\
                                                     (drwan_image_rect[0] // self.zoom, drwan_image_rect[1] // self.zoom, drwan_image_rect[2] // self.zoom, drwan_image_rect[3] // self.zoom))
        drawn_image_image = self.image_lable_background.resize((self.Image_Lable.width(),self.Image_Lable.height()))
        drawn_image_image.alpha_composite(temp_image,((drwan_lable_rect[0],drwan_lable_rect[1])))
        self.Image_Lable.setPixmap(ImageQt.toqpixmap(drawn_image_image))

    def Set_scrollbar(self):
        if self.current_image_image.size[0] * self.zoom > self.Image_Lable.width():
            self.Image_H_Scrollbar.setEnabled(True)
            self.Image_H_Scrollbar.setRange(0,self.current_image_image.size[0] * self.zoom - self.Image_Lable.width())
            self.Image_H_Scrollbar.setPageStep((self.current_image_image.size[0] * self.zoom - self.Image_Lable.width()) // 10)
        else:
            self.Image_H_Scrollbar.setDisabled(True)

        if self.current_image_image.size[1] * self.zoom > self.Image_Lable.height():
            self.Image_V_Scrollbar.setEnabled(True)
            self.Image_V_Scrollbar.setRange(0,self.current_image_image.size[1] * self.zoom - self.Image_Lable.height())
            self.Image_V_Scrollbar.setPageStep((self.current_image_image.size[1] * self.zoom - self.Image_Lable.height()) // 10)
        else:
            self.Image_V_Scrollbar.setDisabled(True)

    def On_image_H_scrollbar_valueChanged(self):
        self.scrollbar_offset[0] = self.Image_H_Scrollbar.value()
        self.Draw_image_lable()
       
    def On_image_V_scrollbar_valueChanged(self):
        self.scrollbar_offset[1] = self.Image_V_Scrollbar.value()
        self.Draw_image_lable()

    def wheelEvent(self,event):
        if self.image_loaded:
            if event.angleDelta().y() > 0 :
                if self.zoom < ZOOM_LIMITE:
                    self.zoom += 1

                    self.Image_H_Scrollbar.blockSignals(True)
                    self.Image_V_Scrollbar.blockSignals(True)
                    self.Set_scrollbar()

                    if self.Image_H_Scrollbar.isEnabled():
                        self.Image_H_Scrollbar.setValue(self.scrollbar_offset[0] + (self.scrollbar_offset[0] + self.Image_Lable.width() // 2) // (self.zoom - 1))
                        self.scrollbar_offset[0] = self.Image_H_Scrollbar.value()
                    else:
                        self.Image_H_Scrollbar.setValue(0)
                        self.scrollbar_offset[0] = self.Image_H_Scrollbar.value()

                    if self.Image_V_Scrollbar.isEnabled():
                        self.Image_V_Scrollbar.setValue(self.scrollbar_offset[1] + (self.scrollbar_offset[1] + self.Image_Lable.height() // 2) // (self.zoom - 1))
                        self.scrollbar_offset[1] = self.Image_V_Scrollbar.value()
                    else:
                        self.Image_V_Scrollbar.setValue(0)
                        self.scrollbar_offset[1] = self.Image_V_Scrollbar.value()

                    self.Image_H_Scrollbar.blockSignals(False)
                    self.Image_V_Scrollbar.blockSignals(False)

                    self.Draw_image_lable()

            elif event.angleDelta().y() < 0 :
                if self.zoom > 1:
                    self.zoom -= 1

                    self.Image_H_Scrollbar.blockSignals(True)
                    self.Image_V_Scrollbar.blockSignals(True)
                    self.Set_scrollbar()

                    if self.Image_H_Scrollbar.isEnabled():
                        if self.scrollbar_offset[0] - (self.scrollbar_offset[0] + self.Image_Lable.width() // 2) // (self.zoom + 1) < self.Image_H_Scrollbar.maximum():
                            self.Image_H_Scrollbar.setValue(self.scrollbar_offset[0] - (self.scrollbar_offset[0] + self.Image_Lable.width() // 2) // (self.zoom + 1))
                        else:
                            self.Image_H_Scrollbar.setValue(self.Image_H_Scrollbar.maximum())
                        self.scrollbar_offset[0] = self.Image_H_Scrollbar.value()
                    else:
                        self.Image_H_Scrollbar.setValue(0)
                        self.scrollbar_offset[0] = self.Image_H_Scrollbar.value()

                    if self.Image_V_Scrollbar.isEnabled():
                        if self.scrollbar_offset[1] - (self.scrollbar_offset[1] + self.Image_Lable.height() // 2) // (self.zoom + 1) < self.Image_V_Scrollbar.maximum():
                            self.Image_V_Scrollbar.setValue(self.scrollbar_offset[1] - (self.scrollbar_offset[1] + self.Image_Lable.height() // 2) // (self.zoom + 1))
                        else:
                            self.Image_V_Scrollbar.setValue(self.Image_V_Scrollbar.maximum())
                        self.scrollbar_offset[1] = self.Image_V_Scrollbar.value()
                    else:
                        self.Image_V_Scrollbar.setValue(0)
                        self.scrollbar_offset[1] = self.Image_V_Scrollbar.value()

                    self.Image_H_Scrollbar.blockSignals(False)
                    self.Image_V_Scrollbar.blockSignals(False)

                    self.Draw_image_lable()

    def resizeEvent(self,event):
        if not self.UIloaded:
            self.UIloaded = True
            return
        self.Set_scrollbar()
        self.Draw_image_lable()
        self.Draw_color_preview_lable()

    def Set_image_background(self):
        self.Auto_pick_color(0)
        if int(self.color[0]) + int(self.color[1]) + int(self.color[2]) < 382 or self.color[3] == 0:
            self.image_lable_background = Image.open('res/TransparentBg-W.png').convert('RGBA')
        else:
            self.image_lable_background = Image.open('res/TransparentBg-B.png').convert('RGBA')

        self.R_Value.setText(str(255))
        self.G_Value.setText(str(255))
        self.B_Value.setText(str(255))
        self.A_Value.setText(str(255))


class Mouse_And_Key_Events:
    def __init__(self):
        self.draging = False
        self.drag_first_point = QPoint()
        self.drag_second_point = QPoint()

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            click_point = [0,0]
            click_point[0] = (event.pos().x() - self.Image_Lable.geometry().x() + self.scrollbar_offset[0]) // self.zoom\
                             if self.Image_H_Scrollbar.isEnabled()\
                             else ((event.pos().x() - self.Image_Lable.geometry().x()) - \
                                   (self.Image_Lable.width() - self.current_image_image.size[0] * self.zoom) // 2) // self.zoom
            click_point[1] = (event.pos().y() - self.Image_Lable.geometry().y() + self.scrollbar_offset[1]) // self.zoom\
                             if self.Image_V_Scrollbar.isEnabled()\
                             else ((event.pos().y() - self.Image_Lable.geometry().y()) - \
                                   (self.Image_Lable.height() - self.current_image_image.size[1] * self.zoom) // 2) // self.zoom
              
            if self.draging and self.image_loaded and self.Image_Lable.geometry().x() <= event.pos().x() and event.pos().x() <= self.Image_Lable.geometry().x() + self.Image_Lable.geometry().width() and self.Image_Lable.geometry().y() <= event.pos().y() and event.pos().y() <= self.Image_Lable.geometry().y() + self.Image_Lable.geometry().height():
                self.drag_first_point = event.pos()
                self.setCursor(Qt.ClosedHandCursor)

            elif self.Cutout_RadioB.isChecked() and self.image_loaded and not self.system_busy and self.Image_Lable.geometry().x() <= event.pos().x() and event.pos().x() <= self.Image_Lable.geometry().x() + self.Image_Lable.geometry().width() and self.Image_Lable.geometry().y() <= event.pos().y() and event.pos().y() <= self.Image_Lable.geometry().y() + self.Image_Lable.geometry().height():
                if self.current_image_array[click_point[1],click_point[0]][3] != 0:
                    t = THREADING_Thread(target=self.Cutout_image,args=(click_point[0],click_point[1],0,))
                    t.start()

            elif self.PickColor_RadioB.isChecked() and self.image_loaded and self.Image_Lable.geometry().x() <= event.pos().x() and event.pos().x() <= self.Image_Lable.geometry().x() + self.Image_Lable.geometry().width() and self.Image_Lable.geometry().y() <= event.pos().y() and event.pos().y() <= self.Image_Lable.geometry().y() + self.Image_Lable.geometry().height():
                self.color = list(self.current_image_array[click_point[1],click_point[0]])
                self.R_Value.setText(str(self.color[0]))
                self.G_Value.setText(str(self.color[1]))
                self.B_Value.setText(str(self.color[2]))
                self.A_Value.setText(str(self.color[3]))

            elif self.Coloring_RadioB.isChecked() and self.image_loaded and not self.system_busy and self.Image_Lable.geometry().x() <= event.pos().x() and event.pos().x() <= self.Image_Lable.geometry().x() + self.Image_Lable.geometry().width() and self.Image_Lable.geometry().y() <= event.pos().y() and event.pos().y() <= self.Image_Lable.geometry().y() + self.Image_Lable.geometry().height():
                self.cruuent_image_edited = True

                coloring_area = [(i,j) for i in range(click_point[0] - self.brush_size // 2,click_point[0] - self.brush_size // 2 + self.brush_size + 1)\
                                       for j in range(click_point[1] - self.brush_size // 2,click_point[1] - self.brush_size // 2 + self.brush_size + 1)]
                exclude = list()
                for point in coloring_area:
                    if abs((point[0] - click_point[0])) ** 2 + abs((point[1] - click_point[1])) ** 2 > \
                    (self.brush_size // 2) ** 2 or point[0] < 0 or point[1] < 0 or point[0] > self.current_image_image.size[0] - 1 or point[1] > self.current_image_image.size[1] - 1:
                        exclude.append(point)
                coloring_area = [point for point in coloring_area if point not in exclude]

                for point in coloring_area:
                    self.current_image_array[point[1],point[0]] = np.array(self.color)

                self.current_image_image = Image.fromarray(self.current_image_array)
                self.Draw_image_lable()

            elif self.Filling_RadioB.isChecked() and self.image_loaded and not self.system_busy and self.Image_Lable.geometry().x() <= event.pos().x() and event.pos().x() <= self.Image_Lable.geometry().x() + self.Image_Lable.geometry().width() and self.Image_Lable.geometry().y() <= event.pos().y() and event.pos().y() <= self.Image_Lable.geometry().y() + self.Image_Lable.geometry().height():
                t = THREADING_Thread(target=self.Filling_image,args=(click_point[0],click_point[1],))
                t.start()

        elif event.button() == Qt.RightButton and self.Cutout_RadioB.isChecked() and self.image_loaded and not self.system_busy and self.Image_Lable.geometry().x() <= event.pos().x() and event.pos().x() <= self.Image_Lable.geometry().x() + self.Image_Lable.geometry().width() and self.Image_Lable.geometry().y() <= event.pos().y() and event.pos().y() <= self.Image_Lable.geometry().y() + self.Image_Lable.geometry().height():
            click_point = [0,0]
            click_point[0] = (event.pos().x() - self.Image_Lable.geometry().x() + self.scrollbar_offset[0]) // self.zoom\
                             if self.Image_H_Scrollbar.isEnabled()\
                             else ((event.pos().x() - self.Image_Lable.geometry().x()) - \
                                   (self.Image_Lable.width() - self.current_image_image.size[0] * self.zoom) // 2) // self.zoom
            click_point[1] = (event.pos().y() - self.Image_Lable.geometry().y() + self.scrollbar_offset[1]) // self.zoom\
                             if self.Image_V_Scrollbar.isEnabled()\
                             else ((event.pos().y() - self.Image_Lable.geometry().y()) - \
                                   (self.Image_Lable.height() - self.current_image_image.size[1] * self.zoom) // 2) // self.zoom
            if self.current_image_array[click_point[1],click_point[0]][3] != 0:
                self.color = list(self.current_image_array[click_point[1],click_point[0]])
                self.R_Value.setText(str(self.color[0]))
                self.G_Value.setText(str(self.color[1]))
                self.B_Value.setText(str(self.color[2]))
                self.A_Value.setText(str(self.color[3]))

                t = THREADING_Thread(target=self.Cutout_image,args=(click_point[0],click_point[1],0,))
                t.start()
  
    def mouseMoveEvent(self,event):
        if event.buttons() == Qt.LeftButton:
            click_point = [0,0]
            click_point[0] = (event.pos().x() - self.Image_Lable.geometry().x() + self.scrollbar_offset[0]) // self.zoom\
                             if self.Image_H_Scrollbar.isEnabled()\
                             else ((event.pos().x() - self.Image_Lable.geometry().x()) - \
                                   (self.Image_Lable.width() - self.current_image_image.size[0] * self.zoom) // 2) // self.zoom
            click_point[1] = (event.pos().y() - self.Image_Lable.geometry().y() + self.scrollbar_offset[1]) // self.zoom\
                             if self.Image_V_Scrollbar.isEnabled()\
                             else ((event.pos().y() - self.Image_Lable.geometry().y()) - \
                                   (self.Image_Lable.height() - self.current_image_image.size[1] * self.zoom) // 2) // self.zoom

            if self.draging and self.image_loaded :
                self.drag_second_point = event.pos()

                if self.Image_H_Scrollbar.isEnabled():
                    self.scrollbar_offset[0] += self.drag_first_point.x() - self.drag_second_point.x()
                    if self.scrollbar_offset[0] < 0:
                        self.scrollbar_offset[0] = 0
                    if self.scrollbar_offset[0] > self.current_image_image.size[0] * self.zoom - self.Image_Lable.width():
                        self.scrollbar_offset[0] = self.current_image_image.size[0] * self.zoom - self.Image_Lable.width()
                    self.Image_H_Scrollbar.blockSignals(True)
                    self.Image_H_Scrollbar.setValue(self.scrollbar_offset[0])
                    self.Image_H_Scrollbar.blockSignals(False)
                if self.Image_V_Scrollbar.isEnabled():       
                    self.scrollbar_offset[1] += self.drag_first_point.y() - self.drag_second_point.y()
                    if self.scrollbar_offset[1] < 0:
                        self.scrollbar_offset[1] = 0
                    if self.scrollbar_offset[1] > self.current_image_image.size[1] * self.zoom - self.Image_Lable.height():
                        self.scrollbar_offset[1] = self.current_image_image.size[1] * self.zoom - self.Image_Lable.height()
                    self.Image_V_Scrollbar.blockSignals(True)
                    self.Image_V_Scrollbar.setValue(self.scrollbar_offset[1])
                    self.Image_V_Scrollbar.blockSignals(False)
                                            
                self.Draw_image_lable()

                self.drag_first_point = self.drag_second_point

            elif self.Cutout_RadioB.isChecked() and self.image_loaded and not self.system_busy and self.Image_Lable.geometry().x() <= event.pos().x() and event.pos().x() <= self.Image_Lable.geometry().x() + self.Image_Lable.geometry().width() and self.Image_Lable.geometry().y() <= event.pos().y() and event.pos().y() <= self.Image_Lable.geometry().y() + self.Image_Lable.geometry().height():
                if self.current_image_array[click_point[1],click_point[0]][3] != 0:
                    t = THREADING_Thread(target=self.Cutout_image,args=(click_point[0],click_point[1],0,))
                    t.start()

            elif self.PickColor_RadioB.isChecked() and self.image_loaded and self.Image_Lable.geometry().x() <= event.pos().x() and event.pos().x() <= self.Image_Lable.geometry().x() + self.Image_Lable.geometry().width() and self.Image_Lable.geometry().y() <= event.pos().y() and event.pos().y() <= self.Image_Lable.geometry().y() + self.Image_Lable.geometry().height():
                self.color = list(self.current_image_array[click_point[1],click_point[0]])
                self.R_Value.setText(str(self.color[0]))
                self.G_Value.setText(str(self.color[1]))
                self.B_Value.setText(str(self.color[2]))
                self.A_Value.setText(str(self.color[3]))

            elif self.Coloring_RadioB.isChecked() and self.image_loaded and not self.system_busy and self.Image_Lable.geometry().x() <= event.pos().x() and event.pos().x() <= self.Image_Lable.geometry().x() + self.Image_Lable.geometry().width() and self.Image_Lable.geometry().y() <= event.pos().y() and event.pos().y() <= self.Image_Lable.geometry().y() + self.Image_Lable.geometry().height():
                self.cruuent_image_edited = True

                coloring_area = [(i,j) for i in range(click_point[0] - self.brush_size // 2,click_point[0] - self.brush_size // 2 + self.brush_size + 1)\
                                       for j in range(click_point[1] - self.brush_size // 2,click_point[1] - self.brush_size // 2 + self.brush_size + 1)]
                exclude = list()
                for point in coloring_area:
                    if abs((point[0] - click_point[0])) ** 2 + abs((point[1] - click_point[1])) ** 2 > \
                    (self.brush_size // 2) ** 2 or point[0] < 0 or point[1] < 0 or point[0] > self.current_image_image.size[0] - 1 or point[1] > self.current_image_image.size[1] - 1:
                        exclude.append(point)
                coloring_area = [point for point in coloring_area if point not in exclude]

                for point in coloring_area:
                    self.current_image_array[point[1],point[0]] = np.array(self.color)

                self.current_image_image = Image.fromarray(self.current_image_array)
                self.Draw_image_lable()

            elif self.Filling_RadioB.isChecked() and self.image_loaded and not self.system_busy and self.Image_Lable.geometry().x() <= event.pos().x() and event.pos().x() <= self.Image_Lable.geometry().x() + self.Image_Lable.geometry().width() and self.Image_Lable.geometry().y() <= event.pos().y() and event.pos().y() <= self.Image_Lable.geometry().y() + self.Image_Lable.geometry().height():
                t = THREADING_Thread(target=self.Filling_image,args=(click_point[0],click_point[1],))
                t.start()

        elif event.buttons() == Qt.RightButton and self.Cutout_RadioB.isChecked() and self.image_loaded and not self.system_busy and self.Image_Lable.geometry().x() <= event.pos().x() and event.pos().x() <= self.Image_Lable.geometry().x() + self.Image_Lable.geometry().width() and self.Image_Lable.geometry().y() <= event.pos().y() and event.pos().y() <= self.Image_Lable.geometry().y() + self.Image_Lable.geometry().height():
            click_point = [0,0]
            click_point[0] = (event.pos().x() - self.Image_Lable.geometry().x() + self.scrollbar_offset[0]) // self.zoom\
                             if self.Image_H_Scrollbar.isEnabled()\
                             else ((event.pos().x() - self.Image_Lable.geometry().x()) - \
                                   (self.Image_Lable.width() - self.current_image_image.size[0] * self.zoom) // 2) // self.zoom
            click_point[1] = (event.pos().y() - self.Image_Lable.geometry().y() + self.scrollbar_offset[1]) // self.zoom\
                             if self.Image_V_Scrollbar.isEnabled()\
                             else ((event.pos().y() - self.Image_Lable.geometry().y()) - \
                                   (self.Image_Lable.height() - self.current_image_image.size[1] * self.zoom) // 2) // self.zoom
            if self.current_image_array[click_point[1],click_point[0]][3] != 0:
                self.color = list(self.current_image_array[click_point[1],click_point[0]])
                self.R_Value.setText(str(self.color[0]))
                self.G_Value.setText(str(self.color[1]))
                self.B_Value.setText(str(self.color[2]))
                self.A_Value.setText(str(self.color[3]))

                t = THREADING_Thread(target=self.Cutout_image,args=(click_point[0],click_point[1],0,))
                t.start()

    def mouseReleaseEvent(self,event):
        self.setCursor(Qt.ArrowCursor)
        if self.Coloring_RadioB.isChecked() and self.image_loaded and not self.system_busy and self.Image_Lable.geometry().x() <= event.pos().x() and event.pos().x() <= self.Image_Lable.geometry().x() + self.Image_Lable.geometry().width() and self.Image_Lable.geometry().y() <= event.pos().y() and event.pos().y() <= self.Image_Lable.geometry().y() + self.Image_Lable.geometry().height():
            self.Insert_backup()
              
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Space:
            self.draging = True

    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Space:
            self.draging = False


class System_State():
    def __init__(self):
        self.tomede = False
        self.UIloaded = False
        self.system_busy = False
        self.image_loaded = False
        self.cruuent_image_edited = False

        self.images = []
        self.file_names = []
        self.image_index = 0

        self.working_status_pin = 0
        self.working_status_text = ['少女祈祷中','少女祈祷中.','少女祈祷中..','少女祈祷中...']

        self.timer = QTimer()
        self.start_timer.connect(self.Start_timer)
        self.end_timer.connect(self.End_timer)
        self.timer.timeout.connect(self.Update_working_status)

    def System_busy(self):
        self.tomede = False
        self.system_busy = True
        self.Update_working_status()
        self.start_timer.emit()
        
        if self.Cutout_RadioB.isChecked():
            self.radio_button_state = 1
        elif self.PickColor_RadioB.isChecked():
            self.radio_button_state = 2
        elif self.Coloring_RadioB.isChecked():
            self.radio_button_state = 3
        elif self.Filling_RadioB.isChecked():
            self.radio_button_state = 4

        self.Cutout_RadioB.setCheckable(False)
        self.PickColor_RadioB.setCheckable(False)
        self.Coloring_RadioB.setCheckable(False)
        self.Filling_RadioB.setCheckable(False)

        self.Full_Automatic_Button.setText('团长！团长停下来啊！')

        self.WorkDir_Button.setDisabled(True)
        self.Change_Background_Button.setDisabled(True)
        self.Previous_Button.setDisabled(True)
        self.Next_Button.setDisabled(True)
        self.Semi_Automatic_Button.setDisabled(True)
        self.Crop_Button.setDisabled(True)
        self.Revoke_Button.setDisabled(True)
        self.Redo_Button.setDisabled(True)
        self.Save_Botton.setDisabled(True)

    def System_free(self):
        self.tomede = False
        self.system_busy = False
        self.end_timer.emit()
     
        self.Cutout_RadioB.setCheckable(True)
        self.PickColor_RadioB.setCheckable(True)
        self.Coloring_RadioB.setCheckable(True)
        self.Filling_RadioB.setCheckable(True)

        if self.radio_button_state == 1:
            self.Cutout_RadioB.setChecked(True)
        elif self.radio_button_state == 2:
            self.PickColor_RadioB.setChecked(True)
        elif self.radio_button_state == 3:
            self.Coloring_RadioB.setChecked(True)
        elif self.radio_button_state == 4:
            self.Filling_RadioB.setChecked(True)

        self.Full_Automatic_Button.setText('全自动')

        self.WorkDir_Button.setEnabled(True)
        self.Change_Background_Button.setEnabled(True)
        self.Previous_Button.setEnabled(True)
        self.Next_Button.setEnabled(True)
        self.Semi_Automatic_Button.setEnabled(True)
        self.Crop_Button.setEnabled(True)
        self.Revoke_Button.setEnabled(True)
        self.Redo_Button.setEnabled(True)
        self.Save_Botton.setEnabled(True)
     
    def Update_working_status(self):
        self.Working_Status_Label.setText(self.working_status_text[self.working_status_pin])
        self.working_status_pin = self.working_status_pin + 1 if self.working_status_pin < 3 else 0

    def Start_timer(self):
        self.timer.start(900)
        pass

    def End_timer(self):
        self.timer.stop()
        self.Working_Status_Label.setText('')


class All_Bottons:
    def __init__(self):
        self.tolerance = 0
        self.brush_size = 1
        self.radio_button_state = 1

        self.WorkDir_Button.clicked.connect(self.On_workDir_button_clicked)
        self.Change_Background_Button.clicked.connect(self.On_change_background_button_clicked)
        self.Previous_Button.clicked.connect(self.On_previous_button_clicked)
        self.Next_Button.clicked.connect(self.On_next_button_clicked)
        self.Full_Automatic_Button.clicked.connect(self.On_full_automatic_button_clicked)
        self.Semi_Automatic_Button.clicked.connect(self.On_semi_automatic_button_clicked)
        self.Crop_Button.clicked.connect(self.On_crop_button_clicked)
        self.Revoke_Button.clicked.connect(self.On_revoke_button_clicked)
        self.Redo_Button.clicked.connect(self.On_redo_button_clicked)
        self.Save_Botton.clicked.connect(self.On_save_button_clicked)

        self.Image_H_Scrollbar.valueChanged.connect(self.On_image_H_scrollbar_valueChanged)
        self.Image_V_Scrollbar.valueChanged.connect(self.On_image_V_scrollbar_valueChanged)
        self.R_Scrollbar.valueChanged.connect(self.On_R_scrollbar_valueChanged)
        self.G_Scrollbar.valueChanged.connect(self.On_G_scrollbar_valueChanged)
        self.B_Scrollbar.valueChanged.connect(self.On_B_scrollbar_valueChanged)
        self.A_Scrollbar.valueChanged.connect(self.On_A_scrollbar_valueChanged)
        self.T_Scrollbar.valueChanged.connect(self.On_T_scrollbar_valueChanged)
        self.S_Scrollbar.valueChanged.connect(self.On_S_scrollbar_valueChanged)
        self.R_Value.textChanged.connect(self.On_R_value_textChanged)
        self.G_Value.textChanged.connect(self.On_G_value_textChanged)
        self.B_Value.textChanged.connect(self.On_B_value_textChanged)
        self.A_Value.textChanged.connect(self.On_A_value_textChanged)
        self.T_Value.textChanged.connect(self.On_T_value_textChanged)
        self.S_Value.textChanged.connect(self.On_S_value_textChanged)

    def On_T_scrollbar_valueChanged(self):
        self.T_Value.setText(str(self.T_Scrollbar.value()))
        pass

    def On_S_scrollbar_valueChanged(self):
        self.S_Value.setText(str(self.S_Scrollbar.value()))
        pass

    def On_T_value_textChanged(self):
        text = self.T_Value.text()

        if len(text) == 0:
            text = '0'
        elif text[0] == '0' and len(text) > 1:
            for i in range(len(text)):
                if text[0] == '0':
                   text = text.replace('0','',1)
                else:
                    break

            if len(text) == 0:
                text = '0'

        self.T_Scrollbar.setValue(eval(text))
        self.tolerance = eval(text)

    def On_S_value_textChanged(self):
        text = self.S_Value.text()

        if len(text) == 0:
            text = '0'
        elif text[0] == '0' and len(text) > 1:
            for i in range(len(text)):
                if text[0] == '0':
                   text = text.replace('0','',1)
                else:
                    break

            if len(text) == 0:
                text = '0'

        self.S_Scrollbar.setValue(eval(text))
        self.brush_size = eval(text)

    def On_workDir_button_clicked(self):
        workroot = QFileDialog.getExistingDirectory(self,'文件目录')
        if workroot == '':
            return

        self.Import_path(workroot)
        
    def On_change_background_button_clicked(self):
        if self.image_lable_background.size[0] == 700:
            self.image_lable_background = Image.open('res/TransparentBg-B.png').convert('RGBA')
        else:
            self.image_lable_background = Image.open('res/TransparentBg-W.png').convert('RGBA')

        self.Draw_image_lable()

    def On_previous_button_clicked(self):
        if self.image_loaded and self.image_index > 1: 
            if self.cruuent_image_edited:
                self.Save_image()

            self.image_index -= 1
            self.zoom = 1
            self.cruuent_image_edited = False

            self.scrollbar_offset = [0,0]
            self.Image_H_Scrollbar.blockSignals(True)
            self.Image_V_Scrollbar.blockSignals(True)
            self.Image_H_Scrollbar.setValue(0)
            self.Image_V_Scrollbar.setValue(0)
            self.Image_H_Scrollbar.blockSignals(False)
            self.Image_V_Scrollbar.blockSignals(False)

            self.current_image_image = self.images[self.image_index].copy().convert('RGBA')
            self.current_image_array = np.array(self.current_image_image)

            self.backup = [self.current_image_image.copy()]
            self.backup_pin = 0

            self.Set_scrollbar()
            self.Set_image_background()
            self.Draw_image_lable()

    def On_next_button_clicked(self):
        if self.image_loaded and self.image_index < len(self.images) - 1: 
            if self.cruuent_image_edited:
                self.Save_image()

            self.image_index += 1
            self.zoom = 1
            self.cruuent_image_edited = False

            self.scrollbar_offset = [0,0]
            self.Image_H_Scrollbar.blockSignals(True)
            self.Image_V_Scrollbar.blockSignals(True)
            self.Image_H_Scrollbar.setValue(0)
            self.Image_V_Scrollbar.setValue(0)
            self.Image_H_Scrollbar.blockSignals(False)
            self.Image_V_Scrollbar.blockSignals(False)

            self.current_image_image = self.images[self.image_index].copy().convert('RGBA')
            self.current_image_array = np.array(self.current_image_image)

            self.backup = [self.current_image_image.copy()]
            self.backup_pin = 0

            self.Set_scrollbar()
            self.Set_image_background()
            self.Draw_image_lable()

    def On_full_automatic_button_clicked(self):
        if self.image_loaded:
            if not self.system_busy:
                self.System_busy()
                self.Auto_pick_color(5) 
            else:
                self.tomede = True

    def On_semi_automatic_button_clicked(self):
        if self.image_loaded:
            self.System_busy()
            self.Auto_pick_color(1) 

    def On_crop_button_clicked(self):
        if self.image_loaded:
            t = THREADING_Thread(target=self.Crop_image,args=(0,))
            t.start()

    def On_revoke_button_clicked(self):
        self.Revoke_backup()
        pass
            
    def On_redo_button_clicked(self):
        self.Redo_backup()
        pass

    def On_save_button_clicked(self):
        self.Save_image()
        pass


class Backup_Arithmetic:
    def __init__(self):
        self.backup_pin = 0
        pass

    def Insert_backup(self):
        self.Working_Status_Label.setText('')
        if not self.backup_pin == len(self.backup) - 1:
            for i in range(self.backup_pin + 1,len(self.backup)):
                self.backup.pop()
            self.backup.append(self.current_image_image.copy())
            self.backup_pin += 1
        else:
            if len(self.backup) < BACKUP_LIMITE:
                self.backup.append(self.current_image_image.copy())
                self.backup_pin += 1
            else:
                self.backup.pop(0)
                self.backup.append(self.current_image_image.copy())

    def Revoke_backup(self):
        if self.image_loaded:
            if self.tomede:
                self.Working_Status_Label.setText('')
                self.current_image_image = self.backup[self.backup_pin].copy()
                self.current_image_array = np.array(self.current_image_image)
                self.Draw_image_lable()
            elif self.backup_pin >= 1:
                self.Working_Status_Label.setText('')
                self.current_image_image = self.backup[self.backup_pin - 1].copy()
                self.current_image_array = np.array(self.current_image_image)
                self.backup_pin -= 1
                self.Draw_image_lable()
            elif self.backup_pin == 0:
                self.Working_Status_Label.setText('已经没有备份了')

    def Redo_backup(self):
        if self.image_loaded:
            if not self.backup_pin == len(self.backup) - 1:
                self.Working_Status_Label.setText('')
                self.current_image_image = self.backup[self.backup_pin + 1].copy()
                self.current_image_array = np.array(self.current_image_image)
                self.backup_pin += 1
                self.Draw_image_lable()
            else:
                self.Working_Status_Label.setText('已经没有备份了')


class MainWindow(QMainWindow,Ui_MainWindow,Functional_Arithmetic,Color_Lable,Image_Lable,Mouse_And_Key_Events,System_State,All_Bottons,Backup_Arithmetic):
    start_timer = pyqtSignal()
    end_timer = pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)

        if not os.path.isfile('res/Icon.ico'):
            QMessageBox.question(self,'阿勒勒？','Icon.ico没了？？？',QMessageBox.Yes)
            SYS_exit()
        if not os.path.isfile('res/Transparent_Lable.png'):
            QMessageBox.question(self,'阿勒勒？','Transparent_Lable.png没了？？？',QMessageBox.Yes)
            SYS_exit()
        if not os.path.isfile('res/TransparentBg-B.png'):
            QMessageBox.question(self,'阿勒勒？','TransparentBg-B.png没了？？？',QMessageBox.Yes)
            SYS_exit()
        if not os.path.isfile('res/TransparentBg-W.png'):
            QMessageBox.question(self,'阿勒勒？','TransparentBg-W.png没了？？？',QMessageBox.Yes)
            SYS_exit()
        self.setupUi(self)

        Functional_Arithmetic.__init__(self)
        Color_Lable.__init__(self)
        Image_Lable.__init__(self)
        Mouse_And_Key_Events.__init__(self)
        System_State.__init__(self)
        All_Bottons.__init__(self)
        Backup_Arithmetic.__init__(self)

        intValidator = QIntValidator(self)
        intValidator.setRange(0,255)
        self.R_Value.setValidator(intValidator)
        self.G_Value.setValidator(intValidator)
        self.B_Value.setValidator(intValidator)
        self.A_Value.setValidator(intValidator)
        self.T_Value.setValidator(intValidator)
        intValidator.setRange(1,255)
        self.S_Value.setValidator(intValidator)

        self.Draw_color_preview_lable()

        self.Image_Lable.mainWindow = self


if __name__ == '__main__':
    app = QApplication(SYS_argv)
    mainWindow = MainWindow()
    mainWindow.show()
    SYS_exit(app.exec_())