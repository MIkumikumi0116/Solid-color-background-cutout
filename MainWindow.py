import numpy as np
from PIL import Image,ImageQt
from os import path as OS_path
from os import walk as OS_walk
from os import makedirs as OS_makedirs
from sys import argv as SYS_argv
from sys import exit as SYS_exit
from re import search as RE_search
from copy import deepcopy as COPY_deepcopy
from threading import Thread as THREADING_Thread
from UI import Ui_MainWindow
from PyQt5.Qt import QPoint
from PyQt5.QtGui import QPixmap,QIntValidator
from PyQt5.QtCore import Qt,QTimer,pyqtSignal,QObject
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QMessageBox,QWidget



ZOOM_LIMITE = 80
CLEAN_LIMITE = 200
BACKUP_LIMITE = 200
DRAW_INTERAL = 5000
DRAW_INTERAL_CLEAN = 20



class Functional_Arithmetic:
    def __init__(self,mainWindow):
        self.mainWindow = mainWindow
        pass

    def Cutout_image(self,x0,y0,mode):
        #0:由鼠标唤起
        #1~4:由半自动唤起
        #5~8:由全自动唤起
        if mode == 0:
            pass
        elif mode == 1:
            x0 = 0
            y0 = 0
        elif mode == 2:
            x0 = 0
            y0 = self.image_lable.current_image_image.size[1] - 1
        elif mode == 3:
            x0 = self.image_lable.current_image_image.size[0] - 1
            y0 = 0
        elif mode == 4:
            x0 = self.image_lable.current_image_image.size[0] - 1
            y0 = self.image_lable.current_image_image.size[1] - 1
        elif mode == 5:
            x0 = 0
            y0 = 0
        elif mode == 6:
            x0 = 0
            y0 = self.image_lable.current_image_image.size[1] - 1
        elif mode == 7:
            x0 = self.image_lable.current_image_image.size[0] - 1
            y0 = 0
        elif mode == 8:
            x0 = self.image_lable.current_image_image.size[0] - 1
            y0 = self.image_lable.current_image_image.size[1] - 1

        self.system_state.cruuent_image_edited = True
        color = np.array(self.color_lable.color)
        tolerance = self.all_bottons.tolerance
        transparent = np.array([0,0,0,0])

        if self.image_lable.current_image_array[y0,x0][3] != 0:
            stack = list()
            stack.append((x0,y0))
            self.image_lable.current_image_array[y0,x0] = transparent

            count = 0
            while True:
                if len(stack) == 0:
                    break

                x,y = stack.pop()
            
                if count == 0:
                    if self.system_state.tomede:
                        self.backup_mod.Revoke_backup()
                        self.system_state.System_free()
                        return
                    else:
                        self.image_lable.current_image_image = Image.fromarray(self.image_lable.current_image_array)
                        self.image_lable.Draw_image_lable()
                    count = 1
                    
                if  x + 1 < self.image_lable.current_image_image.size[0] and \
                all(abs(self.image_lable.current_image_array[y,x + 1] - color) <= tolerance) and \
                self.image_lable.current_image_array[y,x + 1][3] != 0:
                    stack.append((x + 1,y))
                    self.image_lable.current_image_array[y,x + 1] = transparent
                    count = count + 1 if count < DRAW_INTERAL else 0
                
                if x - 1 >= 0 and \
                all(abs(self.image_lable.current_image_array[y,x - 1] - color) <= tolerance) and \
                self.image_lable.current_image_array[y,x - 1][3] != 0:
                    stack.append((x - 1,y))
                    self.image_lable.current_image_array[y,x - 1] = transparent
                    count = count + 1 if count < DRAW_INTERAL else 0
                
                if y + 1 < self.image_lable.current_image_image.size[1] and \
                all(abs(self.image_lable.current_image_array[y + 1,x] - color) <= tolerance) and \
                self.image_lable.current_image_array[y + 1,x][3] != 0:
                    stack.append((x,y + 1))
                    self.image_lable.current_image_array[y + 1,x] = transparent
                    count = count + 1 if count < DRAW_INTERAL else 0

                if y - 1 >= 0 and \
                all(abs(self.image_lable.current_image_array[y - 1,x] - color) <= tolerance) and \
                self.image_lable.current_image_array[y - 1,x][3] != 0:
                    stack.append((x,y - 1))
                    self.image_lable.current_image_array[y - 1,x] = transparent
                    count = count + 1 if count < DRAW_INTERAL else 0

            self.image_lable.current_image_image = Image.fromarray(self.image_lable.current_image_array)
            self.image_lable.Draw_image_lable()

        if mode == 0:
            self.backup_mod.Insert_backup()
            self.system_state.System_free()

        elif mode == 1:
            t = THREADING_Thread(target=self.functional_arithmetic.Cutout_image,args=(0,0,2,))
            t.start()
        elif mode == 2:
            t = THREADING_Thread(target=self.functional_arithmetic.Cutout_image,args=(0,0,3,))
            t.start()
        elif mode == 3:
            t = THREADING_Thread(target=self.functional_arithmetic.Cutout_image,args=(0,0,4,))
            t.start()
        elif mode == 4:
            t = THREADING_Thread(target=self.functional_arithmetic.Clean_image,args=(4,))
            t.start()

        elif mode == 5:
            t = THREADING_Thread(target=self.functional_arithmetic.Cutout_image,args=(0,0,6,))
            t.start()
        elif mode == 6:
            t = THREADING_Thread(target=self.functional_arithmetic.Cutout_image,args=(0,0,7,))
            t.start()
        elif mode == 7:
            t = THREADING_Thread(target=self.functional_arithmetic.Cutout_image,args=(0,0,8,))
            t.start()
        elif mode == 8:
            t = THREADING_Thread(target=self.functional_arithmetic.Clean_image,args=(8,))
            t.start()

    def Pick_color(self,x0,y0):
        self.color_lable.color = list(self.image_lable.current_image_array[y0,x0])
        self.mainWindow.R_Value.setText(str(self.color_lable.color[0]))
        self.mainWindow.G_Value.setText(str(self.color_lable.color[1]))
        self.mainWindow.B_Value.setText(str(self.color_lable.color[2]))
        self.mainWindow.A_Value.setText(str(self.color_lable.color[3]))

    def Coloring_image(self,x0,y0):
        self.system_state.cruuent_image_edited = True

        coloring_area = [(i,j) for i in range(x0 - self.all_bottons.brush_size // 2,x0 + self.all_bottons.brush_size // 2 + 1)\
                               for j in range(y0 - self.all_bottons.brush_size // 2,y0 + self.all_bottons.brush_size // 2 + 1)\
                               if abs((i - x0)) ** 2 + abs((j - y0)) ** 2 <= (self.all_bottons.brush_size // 2) ** 2 \
                               and 0 <= x0 and x0 < self.image_lable.current_image_image.size[0] and 0 <= y0 and y0 <= self.image_lable.current_image_image.size[1]]

        for point in coloring_area:
            self.image_lable.current_image_array[point[1],point[0]] = np.array(self.color_lable.color)

        self.image_lable.current_image_image = Image.fromarray(self.image_lable.current_image_array)
        self.image_lable.Draw_image_lable()

    def Filling_image(self,x0,y0):
        self.system_state.cruuent_image_edited = True
        initial_color = self.image_lable.current_image_array[y0,x0].copy()
        tolerance = self.all_bottons.tolerance

        color = np.array(self.color_lable.color)
        stack = list()
        stack.append((x0,y0))
        self.image_lable.current_image_array[y0,x0] = color

        count = 1
        while True:
            if len(stack) == 0:
                break

            x,y = stack.pop()

            if count == 0:
                if self.system_state.tomede:
                    self.backup_mod.Revoke_backup()
                    self.system_state.System_free()
                    return
                else:
                    self.image_lable.current_image_image = Image.fromarray(self.image_lable.current_image_array)
                    self.image_lable.Draw_image_lable()
                count = 1
            
            if x + 1 < self.image_lable.current_image_image.size[0] and \
            all(abs(self.image_lable.current_image_array[y,x + 1] - initial_color) <= tolerance) and \
            any(self.image_lable.current_image_array[y,x + 1] != color):
                stack.append((x + 1,y))
                self.image_lable.current_image_array[y,x + 1] = color
                count = count + 1 if count < DRAW_INTERAL else 0
                
            if x - 1 >= 0 and \
            all(abs(self.image_lable.current_image_array[y,x - 1] - initial_color) <= tolerance) and \
            any(self.image_lable.current_image_array[y,x - 1] != color):
                stack.append((x - 1,y))
                self.image_lable.current_image_array[y,x - 1] = color
                count = count + 1 if count < DRAW_INTERAL else 0
                
            if  y + 1 < self.image_lable.current_image_image.size[1] and \
            all(abs(self.image_lable.current_image_array[y + 1,x] - initial_color) <= tolerance) and \
            any(self.image_lable.current_image_array[y + 1,x] != color):
                stack.append((x,y + 1))
                self.image_lable.current_image_array[y + 1,x] = color
                count = count + 1 if count < DRAW_INTERAL else 0

            if y - 1 >= 0 and \
            all(abs(self.image_lable.current_image_array[y - 1,x] - initial_color) <= tolerance) and \
            any(self.image_lable.current_image_array[y - 1,x] != color):
                stack.append((x,y - 1)) 
                self.image_lable.current_image_array[y - 1,x] = color
                count = count + 1 if count < DRAW_INTERAL else 0
 
        self.image_lable.current_image_image = Image.fromarray(self.image_lable.current_image_array)
        self.image_lable.Draw_image_lable()
        self.backup_mod.Insert_backup()
        self.system_state.System_free()

    def Crop_image(self,mode):
        #0:由按钮唤起
        #1~4:由半自动唤起
        #5~8:由全自动唤起
        #9:clean_image唤起

        self.system_state.cruuent_image_edited = True
        tolerance = self.all_bottons.tolerance
        color = np.array(self.color_lable.color)
        left,upper,right,lower = 0,0,0,0

        flag = 0
        for x in range(self.image_lable.current_image_image.size[0]):
            for y in range(self.image_lable.current_image_image.size[1]):
                if not all(abs(self.image_lable.current_image_array[y,x] - color) <= tolerance):
                    left = x
                    flag = 1
                    break
            if flag == 1 :
                break

        flag = 0
        for y in range(self.image_lable.current_image_image.size[1]):
            for x in range(self.image_lable.current_image_image.size[0]):
                if not all(abs(self.image_lable.current_image_array[y,x] - color) <= tolerance):
                    upper = y
                    flag = 1
                    break
            if flag == 1 :
                break

        if self.system_state.tomede:
            self.backup_mod.Revoke_backup()
            self.system_state.System_free()
            return

        flag = 0
        for x in range(self.image_lable.current_image_image.size[0] - 1,-1,-1):
           for y in range(self.image_lable.current_image_image.size[1]):
               if not all(abs(self.image_lable.current_image_array[y,x] - color) <= tolerance):
                   right = x
                   flag = 1
                   break
           if flag == 1 :
               break

        flag = 0
        for y in range(self.image_lable.current_image_image.size[1] - 1,-1,-1):
            for x in range(self.image_lable.current_image_image.size[0]):
                if not all(abs(self.image_lable.current_image_array[y,x] - color) <= tolerance):
                    lower = y
                    flag = 1
                    break
            if flag == 1 :
                break

        if self.system_state.tomede:
            self.backup_mod.Revoke_backup()
            self.system_state.System_free()
            return

        self.image_lable.current_image_image = self.image_lable.current_image_image.crop((left,upper,right + 1,lower + 1))
        self.image_lable.current_image_array = np.array(self.image_lable.current_image_image)

        self.image_lable.Set_scrollbar_value(0,0)
        self.image_lable.Draw_image_lable()

        if mode == 0:
            self.backup_mod.Insert_backup()
            self.system_state.System_free()

        elif mode == 1:
            t = THREADING_Thread(target=self.functional_arithmetic.Cutout_image,args=(0,0,1,))
            t.start()

        elif mode == 5:
            t = THREADING_Thread(target=self.functional_arithmetic.Cutout_image,args=(0,0,5,))
            t.start()

        elif mode == 9:
            return

    def Clean_image(self,mode):
        #0:由按钮唤起
        #1~4:由半自动唤起
        #5~8:由全自动唤起

        self.system_state.cruuent_image_edited = True
        transparent = np.array([0,0,0,0])
        pixels_transparency = self.image_lable.current_image_array[:,:,3:].copy()
        
        stack = list()
        block_list = list()
        
        flag = 0
        for j in range(self.image_lable.current_image_image.size[1]):
            for i in range(self.image_lable.current_image_image.size[0]):
                if pixels_transparency[j,i] != 0:
                    x,y = i,j
                    flag = 1
                    break
            if flag == 1:
                break

        count = 1
        array0 = np.array([0])
        while not np.all(pixels_transparency == array0):
            if count == 0:
                if self.system_state.tomede:
                    self.backup_mod.Revoke_backup()
                    self.system_state.System_free()
                    return
                else:
                    self.image_lable.current_image_image = Image.fromarray(self.image_lable.current_image_array)
                    self.image_lable.Draw_image_lable()
                count = 1

            stack = [(x,y)]
            block_list = [(x,y)]
            current_point_backup = (x,y)
            pixels_transparency[y,x] = 0

            while True:
                if len(stack) == 0:
                    break

                if self.system_state.tomede:
                    self.backup_mod.Revoke_backup()
                    self.system_state.System_free()
                    return

                x,y = stack.pop()
                    
                if x + 1 < self.image_lable.current_image_image.size[0] and \
                pixels_transparency[y,x + 1] != 0:
                    stack.append((x + 1,y))
                    pixels_transparency[y,x + 1] = 0
                    block_list.append((x + 1,y))
                
                if x - 1 >= 0 and \
                pixels_transparency[y,x - 1] != 0:
                    stack.append((x - 1,y))
                    pixels_transparency[y,x - 1] = 0
                    block_list.append((x - 1,y))
                    
                if y + 1 < self.image_lable.current_image_image.size[1] and \
                pixels_transparency[y + 1,x] != 0:
                    stack.append((x,y + 1))
                    pixels_transparency[y + 1,x] = 0
                    block_list.append((x,y + 1))
                    
                if y - 1 >= 0 and \
                pixels_transparency[y - 1,x] != 0:
                    stack.append((x,y - 1))
                    pixels_transparency[y - 1,x] = 0
                    block_list.append((x,y - 1))

            if len(block_list) <= CLEAN_LIMITE:
                for x,y in block_list:
                    self.image_lable.current_image_array[y,x] = transparent

            for x,y in block_list:
                pixels_transparency[y,x] == 0

            x,y = current_point_backup
            flag = 0
            while y < self.image_lable.current_image_image.size[1]:
                if self.system_state.tomede:
                    self.backup_mod.Revoke_backup()
                    self.system_state.System_free()
                    return

                while x < self.image_lable.current_image_image.size[0]:
                    if pixels_transparency[y,x] != 0:
                        flag = 1
                        break
                    elif x < self.image_lable.current_image_image.size[0] - 1:
                        x += 1
                    elif x == self.image_lable.current_image_image.size[0] - 1:
                        x = 0
                        y += 1
                        if y == self.image_lable.current_image_image.size[1]:
                            break
                        
                if flag == 1:
                    break

            count = count + 1 if count < DRAW_INTERAL_CLEAN else 0

        self.image_lable.current_image_image = Image.fromarray(self.image_lable.current_image_array)
        self.image_lable.Draw_image_lable()
        
        if mode == 0:
            self.backup_mod.Insert_backup()
            self.system_state.System_free()

        elif mode == 4:          
            color_backup = self.color_lable.color.copy()
            self.color_lable.color = transparent

            t = THREADING_Thread(target=self.functional_arithmetic.Crop_image,args=(1,))
            t.start()
            t.join

            self.color_lable.color = color_backup

            self.backup_mod.Insert_backup()
            self.system_state.System_free()

        elif mode == 8:
            if self.system_state.image_index == len(self.system_state.images) - 1:
                self.functional_arithmetic.Save_image()
                self.system_state.System_free()
            else:
                color_backup = self.color_lable.color.copy()
                self.color_lable.color = transparent

                t = THREADING_Thread(target=self.functional_arithmetic.Crop_image,args=(9,))
                t.start()
                t.join

                self.color_lable.color = color_backup

                self.all_bottons.On_next_button_clicked()
                t = THREADING_Thread(target=self.functional_arithmetic.Auto_pick_color,args=(5,))
                t.start()

    def Auto_pick_color(self,mode):
        #0:由系统唤起
        #1~4:由半自动唤起
        #5~8:由全自动唤起
        colors = {}

        y1 = 0
        y2 = self.image_lable.current_image_image.size[1] - 1
        for x in range(self.image_lable.current_image_image.size[0]): 
            if tuple(self.image_lable.current_image_array[y1,x]) in colors:
                colors[tuple(self.image_lable.current_image_array[y1,x])] += 1
            else:
                colors[tuple(self.image_lable.current_image_array[y1,x])] = 1
            if tuple(self.image_lable.current_image_array[y2,x]) in colors:
                colors[tuple(self.image_lable.current_image_array[y2,x])] += 1
            else:
                colors[tuple(self.image_lable.current_image_array[y2,x])] = 1

        x1 = 0
        x2 = self.image_lable.current_image_image.size[0] - 1
        for y in range(1,self.image_lable.current_image_image.size[1] - 1): 
            if tuple(self.image_lable.current_image_array[y,x1]) in colors:
                colors[tuple(self.image_lable.current_image_array[y,x1])] += 1
            else:
                colors[tuple(self.image_lable.current_image_array[y,x1])] = 1
            if tuple(self.image_lable.current_image_array[y,x2]) in colors:
                colors[tuple(self.image_lable.current_image_array[y,x2])] += 1
            else:
                colors[tuple(self.image_lable.current_image_array[y,x2])] = 1

        max_count = max(colors.values())
        for k,v in colors.items():
            if v == max_count:
                color = k
                break

        self.mainWindow.R_Value.setText(str(color[0]))
        self.mainWindow.G_Value.setText(str(color[1]))
        self.mainWindow.B_Value.setText(str(color[2]))
        self.mainWindow.A_Value.setText(str(color[3]))

        if mode == 1:
            self.system_state.System_busy()
            t = THREADING_Thread(target=self.functional_arithmetic.Crop_image,args=(1,))
            t.start()

        elif mode == 5:
            self.system_state.System_busy()
            t = THREADING_Thread(target=self.functional_arithmetic.Crop_image,args=(5,))
            t.start()

    def Save_image(self):
        if self.system_state.image_loaded:
            if not OS_path.isdir("done"):
                OS_makedirs("done")

            self.system_state.images[self.system_state.image_index] = self.image_lable.current_image_image.copy()
            file_name_index = len(self.system_state.file_names[self.system_state.image_index]) - self.system_state.file_names[self.system_state.image_index][::-1].find('.')
            self.image_lable.current_image_image.save('done/' + self.system_state.file_names[self.system_state.image_index][:file_name_index] + 'png')

    def Import_path(self,path):
        if self.system_state.cruuent_image_edited:
            self.functional_arithmetic.Save_image()

        images_backup = COPY_deepcopy(self.system_state.images)
        image_index_backup = self.system_state.image_index
        file_names_backup = COPY_deepcopy(self.system_state.file_names)

        self.system_state.images = ['']
        self.system_state.image_index = 1
        self.system_state.file_names = ['']
        
        for root,dir,filelist in OS_walk(path):
            for file in filelist:
                if RE_search('(jpg|jpeg|png|webp|bmp|tif|tga|JPG|JPEG|PNG|WEBP|BMP|TIF|TGA)$',file):
                    self.system_state.images.append(Image.open(root + '/' + file))
                    self.system_state.file_names.append(file)
            break

        if len(self.system_state.images) <= 1:
            QMessageBox.question(self.mainWindow,'这个目录里没有图片','小老弟你怎么回事？',QMessageBox.Yes)
            self.system_state.images = images_backup
            self.system_state.image_index = image_index_backup
            self.system_state.file_names = file_names_backup
            return

        self.image_lable.current_image_image = self.system_state.images[self.system_state.image_index].convert('RGBA')
        self.image_lable.current_image_array = np.array(self.image_lable.current_image_image)
        
        self.image_lable.zoom = 1
        self.system_state.image_loaded = True
        self.system_state.cruuent_image_edited = False

        self.image_lable.Set_scrollbar_value(0,0)
        self.image_lable.Set_scrollbar_display()

        self.backup_mod.backup_pin = 0
        self.backup_mod.backups = [self.image_lable.current_image_image.copy()]

        self.image_lable.Set_image_background()
        self.image_lable.Draw_image_lable()

    def Import_image(self,path_list):
        if self.system_state.cruuent_image_edited:
            self.functional_arithmetic.Save_image()

        self.system_state.images = ['']
        self.system_state.image_index = 1
        self.system_state.file_names = ['']

        for path in path_list:
            self.system_state.images.append(Image.open(path))
            self.system_state.file_names.append(path[(len(path) - path[::-1].find('/')):])
            
        self.image_lable.current_image_image = self.system_state.images[self.system_state.image_index].convert('RGBA')
        self.image_lable.current_image_array = np.array(self.image_lable.current_image_image)
        
        self.image_lable.zoom = 1
        self.system_state.image_loaded = True
        self.system_state.cruuent_image_edited = False

        self.image_lable.Set_scrollbar_value(0,0)
        self.image_lable.Set_scrollbar_display()

        self.backup_mod.backup_pin = 0
        self.backup_mod.backups = [self.image_lable.current_image_image.copy()]

        self.image_lable.Set_image_background()
        self.image_lable.Draw_image_lable()

class Backup_Mod:
    def __init__(self,mainWindow):
        self.mainWindow = mainWindow

        self.backups = []
        self.backup_pin = 0
        
    def Insert_backup(self):
        self.mainWindow.Working_Status_Label.setText('')
        if not self.backup_mod.backup_pin == len(self.backups) - 1:
            for i in range(self.backup_mod.backup_pin + 1,len(self.backups)):
                self.backups.pop()
            self.backups.append(self.image_lable.current_image_image.copy())
            self.backup_mod.backup_pin += 1

        else:
            if len(self.backups) < BACKUP_LIMITE:
                self.backups.append(self.image_lable.current_image_image.copy())
                self.backup_mod.backup_pin += 1
            else:
                self.backups.pop(0)
                self.backups.append(self.image_lable.current_image_image.copy())

    def Revoke_backup(self):
        if self.system_state.image_loaded:
            if self.system_state.tomede:
                self.mainWindow.Working_Status_Label.setText('')
                self.image_lable.current_image_image = self.backups[self.backup_mod.backup_pin].copy()
                self.image_lable.current_image_array = np.array(self.image_lable.current_image_image)
                self.image_lable.Draw_image_lable()

            elif self.backup_mod.backup_pin > 0:
                self.mainWindow.Working_Status_Label.setText('')
                self.image_lable.current_image_image = self.backups[self.backup_mod.backup_pin - 1].copy()
                self.image_lable.current_image_array = np.array(self.image_lable.current_image_image)
                self.backup_mod.backup_pin -= 1
                self.image_lable.Draw_image_lable()

            elif self.backup_mod.backup_pin == 0:
                self.mainWindow.Working_Status_Label.setText('已经没有备份了')

    def Redo_backup(self):
        if self.system_state.image_loaded:
            if not self.backup_mod.backup_pin == len(self.backups) - 1:
                self.mainWindow.Working_Status_Label.setText('')
                self.image_lable.current_image_image = self.backups[self.backup_mod.backup_pin + 1].copy()
                self.image_lable.current_image_array = np.array(self.image_lable.current_image_image)
                self.backup_mod.backup_pin += 1
                self.image_lable.Draw_image_lable()

            else:
                self.mainWindow.Working_Status_Label.setText('已经没有备份了')

class System_State(QObject):
    start_timer = pyqtSignal()
    end_timer = pyqtSignal()

    def __init__(self,mainWindow):
        self.mainWindow = mainWindow
        QObject.__init__(self)

        self.tomede = False
        self.UIloaded = False
        self.system_busy = False
        self.image_loaded = False
        self.cruuent_image_edited = False
        self.images = ['']
        self.file_names = ['']
        self.image_index = 1
        self.working_status_pin = 0
        self.working_status_text = ['少女祈祷中','少女祈祷中.','少女祈祷中..','少女祈祷中...']

        self.timer = QTimer()
        self.timer.timeout.connect(self.Update_working_status)
        self.start_timer.connect(self.Start_timer)
        self.end_timer.connect(self.End_timer)

    def System_busy(self):
        self.system_state.tomede = False
        self.system_state.system_busy = True
        self.system_state.Update_working_status()
        self.system_state.start_timer.emit()
        
        if self.mainWindow.Cutout_RadioB.isChecked():
            self.all_bottons.radio_button_state = 1
        elif self.mainWindow.PickColor_RadioB.isChecked():
            self.all_bottons.radio_button_state = 2
        elif self.mainWindow.Coloring_RadioB.isChecked():
            self.all_bottons.radio_button_state = 3
        elif self.mainWindow.Filling_RadioB.isChecked():
            self.all_bottons.radio_button_state = 4

        self.mainWindow.Cutout_RadioB.setCheckable(False)
        self.mainWindow.PickColor_RadioB.setCheckable(False)
        self.mainWindow.Coloring_RadioB.setCheckable(False)
        self.mainWindow.Filling_RadioB.setCheckable(False)

        self.mainWindow.Full_Automatic_Button.setText('团长！团长停下来啊！')

        self.mainWindow.WorkDir_Button.setDisabled(True)
        self.mainWindow.Change_Background_Button.setDisabled(True)
        self.mainWindow.Previous_Button.setDisabled(True)
        self.mainWindow.Next_Button.setDisabled(True)
        self.mainWindow.Semi_Automatic_Button.setDisabled(True)
        self.mainWindow.Crop_Button.setDisabled(True)
        self.mainWindow.Clean_Button.setDisabled(True)
        self.mainWindow.Revoke_Button.setDisabled(True)
        self.mainWindow.Redo_Button.setDisabled(True)
        self.mainWindow.Save_Botton.setDisabled(True)

    def System_free(self):
        self.system_state.tomede = False
        self.system_state.system_busy = False
        self.system_state.end_timer.emit()
     
        self.mainWindow.Cutout_RadioB.setCheckable(True)
        self.mainWindow.PickColor_RadioB.setCheckable(True)
        self.mainWindow.Coloring_RadioB.setCheckable(True)
        self.mainWindow.Filling_RadioB.setCheckable(True)

        if self.all_bottons.radio_button_state == 1:
            self.mainWindow.Cutout_RadioB.setChecked(True)
        elif self.all_bottons.radio_button_state == 2:
            self.mainWindow.PickColor_RadioB.setChecked(True)
        elif self.all_bottons.radio_button_state == 3:
            self.mainWindow.Coloring_RadioB.setChecked(True)
        elif self.all_bottons.radio_button_state == 4:
            self.mainWindow.Filling_RadioB.setChecked(True)

        self.mainWindow.Full_Automatic_Button.setText('全自动')

        self.mainWindow.WorkDir_Button.setEnabled(True)
        self.mainWindow.Change_Background_Button.setEnabled(True)
        self.mainWindow.Previous_Button.setEnabled(True)
        self.mainWindow.Next_Button.setEnabled(True)
        self.mainWindow.Semi_Automatic_Button.setEnabled(True)
        self.mainWindow.Crop_Button.setEnabled(True)
        self.mainWindow.Clean_Button.setEnabled(True)
        self.mainWindow.Revoke_Button.setEnabled(True)
        self.mainWindow.Redo_Button.setEnabled(True)
        self.mainWindow.Save_Botton.setEnabled(True)

    def Update_working_status(self):
        self.mainWindow.Working_Status_Label.setText(self.system_state.working_status_text[self.system_state.working_status_pin])
        self.system_state.working_status_pin = self.system_state.working_status_pin + 1 if self.system_state.working_status_pin < 3 else 0

    def Start_timer(self):
        self.system_state.timer.start(900)
        pass

    def End_timer(self):
        self.system_state.timer.stop()
        self.mainWindow.Working_Status_Label.setText('')

    def closeEvent(self,event):
        if self.system_state.image_loaded and self.system_state.cruuent_image_edited:
            self.functional_arithmetic.Save_image()

class All_Bottons(QMainWindow):
    def __init__(self,mainWindow):
        self.mainWindow = mainWindow

        QMainWindow.__init__(self)
        intValidator = QIntValidator(self)
        intValidator.setRange(0,255)
        self.mainWindow.T_Value.setValidator(intValidator)
        intValidator.setRange(1,255)
        self.mainWindow.S_Value.setValidator(intValidator)

        self.tolerance = 0
        self.brush_size = 1
        self.radio_button_state = 1

        self.mainWindow.T_Scrollbar.valueChanged.connect(self.On_T_scrollbar_valueChanged)
        self.mainWindow.S_Scrollbar.valueChanged.connect(self.On_S_scrollbar_valueChanged)
        self.mainWindow.T_Value.textChanged.connect(self.On_T_value_textChanged)
        self.mainWindow.S_Value.textChanged.connect(self.On_S_value_textChanged)

        self.mainWindow.WorkDir_Button.clicked.connect(self.On_workDir_button_clicked)
        self.mainWindow.Change_Background_Button.clicked.connect(self.On_change_background_button_clicked)
        self.mainWindow.Previous_Button.clicked.connect(self.On_previous_button_clicked)
        self.mainWindow.Next_Button.clicked.connect(self.On_next_button_clicked)
        self.mainWindow.Full_Automatic_Button.clicked.connect(self.On_full_automatic_button_clicked)
        self.mainWindow.Semi_Automatic_Button.clicked.connect(self.On_semi_automatic_button_clicked)
        self.mainWindow.Crop_Button.clicked.connect(self.On_crop_button_clicked)
        self.mainWindow.Clean_Button.clicked.connect(self.On_clean_button_clicked)
        self.mainWindow.Revoke_Button.clicked.connect(self.On_revoke_button_clicked)
        self.mainWindow.Redo_Button.clicked.connect(self.On_redo_button_clicked)
        self.mainWindow.Save_Botton.clicked.connect(self.On_save_button_clicked)
       
    def On_T_scrollbar_valueChanged(self):
        self.mainWindow.T_Value.setText(str(self.mainWindow.T_Scrollbar.value()))
        pass

    def On_S_scrollbar_valueChanged(self):
        self.mainWindow.S_Value.setText(str(self.mainWindow.S_Scrollbar.value()))
        pass

    def On_T_value_textChanged(self):
        text = self.mainWindow.T_Value.text()

        if len(text) == 0:
            text = '0'
            self.mainWindow.T_Value.setText(text)
        elif text[0] == '0' and len(text) > 1:
            for i in range(len(text)):
                if text[0] == '0':
                   text = text.replace('0','',1)
                else:
                    break

            if len(text) == 0:
                text = '0'

        self.mainWindow.T_Scrollbar.setValue(eval(text))
        self.all_bottons.tolerance = eval(text)

    def On_S_value_textChanged(self):
        text = self.mainWindow.S_Value.text()

        if len(text) == 0:
            text = '1'
            self.mainWindow.S_Value.setText(text)
        elif text[0] == '0' and len(text) > 1:
            for i in range(len(text)):
                if text[0] == '0':
                   text = text.replace('0','',1)
                else:
                    break

            if len(text) == 0:
                text = '0'

        self.mainWindow.S_Scrollbar.setValue(eval(text))
        self.all_bottons.brush_size = eval(text)

    def On_workDir_button_clicked(self):
        workroot = QFileDialog.getExistingDirectory(self.mainWindow,'文件目录')
        if workroot == '':
            return

        self.mainWindow.Working_Status_Label.setText('')
        self.functional_arithmetic.Import_path(workroot)

    def On_change_background_button_clicked(self):
        if self.image_lable.image_lable_background.size[0] == 700:
            self.image_lable.image_lable_background = self.image_lable.image_lable_background_B
        else:
            self.image_lable.image_lable_background = self.image_lable.image_lable_background_W

        self.mainWindow.Working_Status_Label.setText('')
        self.image_lable.Draw_image_lable() 

    def On_previous_button_clicked(self):
        if self.system_state.image_loaded and self.system_state.image_index > 1: 
            if self.system_state.cruuent_image_edited:
                self.functional_arithmetic.Save_image()

            self.system_state.image_index -= 1
            self.image_lable.current_image_image = self.system_state.images[self.system_state.image_index].copy().convert('RGBA')
            self.image_lable.current_image_array = np.array(self.image_lable.current_image_image)

            self.backup_mod.backups = [self.image_lable.current_image_image.copy()]
            self.backup_mod.backup_pin = 0

            self.image_lable.zoom = 1
            self.image_lable.Set_scrollbar_value(0,0)
            self.image_lable.Set_scrollbar_display()
            self.system_state.cruuent_image_edited = False
            self.mainWindow.Working_Status_Label.setText('')

            self.image_lable.Set_image_background()
            self.image_lable.Draw_image_lable()
            
        elif self.system_state.image_index == 1:
            self.mainWindow.Working_Status_Label.setText('这是第一张了')

    def On_next_button_clicked(self):
        if self.system_state.image_loaded and self.system_state.image_index < len(self.system_state.images) - 1: 
            if self.system_state.cruuent_image_edited:
                self.functional_arithmetic.Save_image()

            self.system_state.image_index += 1
            self.image_lable.current_image_image = self.system_state.images[self.system_state.image_index].copy().convert('RGBA')
            self.image_lable.current_image_array = np.array(self.image_lable.current_image_image)

            self.backup_mod.backups = [self.image_lable.current_image_image.copy()]
            self.backup_mod.backup_pin = 0

            self.image_lable.zoom = 1
            self.image_lable.Set_scrollbar_value(0,0)
            self.image_lable.Set_scrollbar_display()
            self.system_state.cruuent_image_edited = False
            self.mainWindow.Working_Status_Label.setText('')

            self.image_lable.Set_image_background()
            self.image_lable.Draw_image_lable()

        elif self.system_state.image_index == len(self.system_state.images) - 1:
            self.mainWindow.Working_Status_Label.setText('这是最后一张了')

    def On_full_automatic_button_clicked(self):
        if self.system_state.image_loaded:
            if not self.system_state.system_busy:
                self.functional_arithmetic.Auto_pick_color(5) 
            else:
                self.system_state.tomede = True

    def On_semi_automatic_button_clicked(self):
        if self.system_state.image_loaded:
            self.functional_arithmetic.Auto_pick_color(1) 

    def On_crop_button_clicked(self):
        if self.system_state.image_loaded:
            self.system_state.System_busy()
            t = THREADING_Thread(target=self.functional_arithmetic.Crop_image,args=(0,))
            t.start()

    def On_clean_button_clicked(self):
        if self.system_state.image_loaded:
            self.system_state.System_busy()
            t = THREADING_Thread(target=self.functional_arithmetic.Clean_image,args=(0,))
            t.start()

    def On_revoke_button_clicked(self):
        self.backup_mod.Revoke_backup()
        pass  

    def On_redo_button_clicked(self):
        self.backup_mod.Redo_backup()
        pass

    def On_save_button_clicked(self):
        self.mainWindow.Working_Status_Label.setText('')
        self.functional_arithmetic.Save_image()

class Color_Lable(QMainWindow):
    def __init__(self,mainWindow):
        self.mainWindow = mainWindow

        QMainWindow.__init__(self)
        intValidator = QIntValidator(self)
        intValidator.setRange(0,255)
        self.mainWindow.R_Value.setValidator(intValidator)
        self.mainWindow.G_Value.setValidator(intValidator)
        self.mainWindow.B_Value.setValidator(intValidator)
        self.mainWindow.A_Value.setValidator(intValidator)

        self.mainWindow.R_Scrollbar.valueChanged.connect(self.On_R_scrollbar_valueChanged)
        self.mainWindow.G_Scrollbar.valueChanged.connect(self.On_G_scrollbar_valueChanged)
        self.mainWindow.B_Scrollbar.valueChanged.connect(self.On_B_scrollbar_valueChanged)
        self.mainWindow.A_Scrollbar.valueChanged.connect(self.On_A_scrollbar_valueChanged)

        self.mainWindow.R_Value.textChanged.connect(self.On_R_value_textChanged)
        self.mainWindow.G_Value.textChanged.connect(self.On_G_value_textChanged)
        self.mainWindow.B_Value.textChanged.connect(self.On_B_value_textChanged)
        self.mainWindow.A_Value.textChanged.connect(self.On_A_value_textChanged)

        self.color = [255,255,255,255]
        self.color_preview_background = Image.open('res/Transparent_Lable.png').convert('RGBA')

    def Draw_color_preview_lable(self):
        color_preview_image = Image.new('RGBA', (120,120), tuple(self.color))
        color_preview_background = self.color_lable.color_preview_background.resize((120,120))
        color_preview_background.alpha_composite(color_preview_image)
        
        self.mainWindow.Color_Preview_Lable.setPixmap(ImageQt.toqpixmap(color_preview_background))

    def On_R_scrollbar_valueChanged(self):
        self.mainWindow.R_Value.setText(str(self.mainWindow.R_Scrollbar.value()))
        pass

    def On_G_scrollbar_valueChanged(self):
        self.mainWindow.G_Value.setText(str(self.mainWindow.G_Scrollbar.value()))
        pass

    def On_B_scrollbar_valueChanged(self):
        self.mainWindow.B_Value.setText(str(self.mainWindow.B_Scrollbar.value()))
        pass

    def On_A_scrollbar_valueChanged(self):
        self.mainWindow.A_Value.setText(str(self.mainWindow.A_Scrollbar.value()))
        pass

    def On_R_value_textChanged(self):
        text = self.mainWindow.R_Value.text()

        if len(text) == 0:
            text = '0'
            self.mainWindow.R_Value.setText(text)
        elif text[0] == '0' and len(text) > 1:
            for i in range(len(text)):
                if text[0] == '0':
                   text = text.replace('0','',1)
                else:
                    break

            if len(text) == 0:
                text = '0'

        self.mainWindow.R_Scrollbar.setValue(eval(text))
        self.color_lable.color[0] = eval(text)

        self.color_lable.Draw_color_preview_lable()

    def On_G_value_textChanged(self):
        text = self.mainWindow.G_Value.text()

        if len(text) == 0:
            text = '0'
            self.mainWindow.G_Value.setText(text)
        elif text[0] == '0' and len(text) > 1:
            for i in range(len(text)):
                if text[0] == '0':
                   text = text.replace('0','',1)
                else:
                    break

            if len(text) == 0:
                text = '0'

        self.mainWindow.G_Scrollbar.setValue(eval(text))
        self.color_lable.color[1] = eval(text)

        self.color_lable.Draw_color_preview_lable()

    def On_B_value_textChanged(self):
        text = self.mainWindow.B_Value.text()

        if len(text) == 0:
            text = '0'
            self.mainWindow.B_Value.setText(text)
        elif text[0] == '0' and len(text) > 1:
            for i in range(len(text)):
                if text[0] == '0':
                   text = text.replace('0','',1)
                else:
                    break

            if len(text) == 0:
                text = '0'

        self.mainWindow.B_Scrollbar.setValue(eval(text))
        self.color_lable.color[2] = eval(text)

        self.color_lable.Draw_color_preview_lable()

    def On_A_value_textChanged(self):
        text = self.mainWindow.A_Value.text()

        if len(text) == 0:
            text = '0'
            self.mainWindow.A_Value.setText(text)
        elif text[0] == '0' and len(text) > 1:
            for i in range(len(text)):
                if text[0] == '0':
                   text = text.replace('0','',1)
                else:
                    break

            if len(text) == 0:
                text = '0'

        self.mainWindow.A_Scrollbar.setValue(eval(text))
        self.color_lable.color[3] = eval(text)

        self.color_lable.Draw_color_preview_lable()

class Image_Lable:
    def __init__(self,mainWindow):
        self.mainWindow = mainWindow

        self.zoom = 1
        self.scrollbar_offset = [0,0]
        self.current_image_image = Image.new('RGBA',(100,100))
        self.current_image_array = np.array(self.current_image_image)
        self.image_lable_background_W = Image.open('res/TransparentBg-W.png').convert('RGBA')
        self.image_lable_background_B = Image.open('res/TransparentBg-B.png').convert('RGBA')
        self.image_lable_background = self.image_lable_background_W

        self.mainWindow.Image_H_Scrollbar.valueChanged.connect(self.On_image_H_scrollbar_valueChanged)
        self.mainWindow.Image_V_Scrollbar.valueChanged.connect(self.On_image_V_scrollbar_valueChanged)

    def Draw_image_lable(self):
        drwan_image_rect = [0,0,0,0]
        drwan_image_rect[0] = self.image_lable.scrollbar_offset[0]\
                              if self.image_lable.current_image_image.size[0] * self.image_lable.zoom > self.mainWindow.Image_Lable.width()\
                              else 0
        drwan_image_rect[1] = self.image_lable.scrollbar_offset[1]\
                              if self.image_lable.current_image_image.size[1] * self.image_lable.zoom > self.mainWindow.Image_Lable.height() \
                              else 0
        drwan_image_rect[2] = self.image_lable.scrollbar_offset[0] + self.mainWindow.Image_Lable.width()\
                              if self.image_lable.current_image_image.size[0] * self.image_lable.zoom > self.mainWindow.Image_Lable.width()\
                              else self.image_lable.current_image_image.size[0] * self.image_lable.zoom
        drwan_image_rect[3] = self.image_lable.scrollbar_offset[1] + self.mainWindow.Image_Lable.height()\
                              if self.image_lable.current_image_image.size[1] * self.image_lable.zoom > self.mainWindow.Image_Lable.height() \
                              else self.image_lable.current_image_image.size[1] * self.image_lable.zoom
        
        drwan_lable_rect = [0,0,0,0]
        drwan_lable_rect[0] = 0\
                              if self.image_lable.current_image_image.size[0] * self.image_lable.zoom > self.mainWindow.Image_Lable.width()\
                              else (self.mainWindow.Image_Lable.width() - self.image_lable.current_image_image.size[0] * self.image_lable.zoom) // 2
        drwan_lable_rect[1] = 0\
                              if self.image_lable.current_image_image.size[1] * self.image_lable.zoom > self.mainWindow.Image_Lable.height() \
                              else (self.mainWindow.Image_Lable.height() - self.image_lable.current_image_image.size[1] * self.image_lable.zoom) // 2
        drwan_lable_rect[2] = self.mainWindow.Image_Lable.width()\
                              if self.image_lable.current_image_image.size[0] * self.image_lable.zoom > self.mainWindow.Image_Lable.width()\
                              else drwan_lable_rect[0] + self.image_lable.current_image_image.size[0] * self.image_lable.zoom
        drwan_lable_rect[3] = self.mainWindow.Image_Lable.height()\
                              if self.image_lable.current_image_image.size[1] * self.image_lable.zoom > self.mainWindow.Image_Lable.height() \
                              else drwan_lable_rect[1] + self.image_lable.current_image_image.size[1] * self.image_lable.zoom
        
        temp_image = self.image_lable.current_image_image.resize((drwan_image_rect[2] - drwan_image_rect[0],drwan_image_rect[3] - drwan_image_rect[1]),\
                     Image.NEAREST,\
                    (drwan_image_rect[0] // self.image_lable.zoom, drwan_image_rect[1] // self.image_lable.zoom, drwan_image_rect[2] // self.image_lable.zoom, drwan_image_rect[3] // self.image_lable.zoom))
        drawn_image_image = self.image_lable.image_lable_background.resize((self.mainWindow.Image_Lable.width(),self.mainWindow.Image_Lable.height()))
        drawn_image_image.alpha_composite(temp_image,((drwan_lable_rect[0],drwan_lable_rect[1])))
        self.mainWindow.Image_Lable.setPixmap(ImageQt.toqpixmap(drawn_image_image))

    def Set_scrollbar_display(self):
        if self.image_lable.current_image_image.size[0] * self.image_lable.zoom > self.mainWindow.Image_Lable.width():
            self.mainWindow.Image_H_Scrollbar.setEnabled(True)
            self.mainWindow.Image_H_Scrollbar.setRange(0,self.image_lable.current_image_image.size[0] * self.image_lable.zoom - self.mainWindow.Image_Lable.width())
            self.mainWindow.Image_H_Scrollbar.setPageStep((self.image_lable.current_image_image.size[0] * self.image_lable.zoom - self.mainWindow.Image_Lable.width()) // 10)
        else:
            self.mainWindow.Image_H_Scrollbar.setDisabled(True)

        if self.image_lable.current_image_image.size[1] * self.image_lable.zoom > self.mainWindow.Image_Lable.height():
            self.mainWindow.Image_V_Scrollbar.setEnabled(True)
            self.mainWindow.Image_V_Scrollbar.setRange(0,self.image_lable.current_image_image.size[1] * self.image_lable.zoom - self.mainWindow.Image_Lable.height())
            self.mainWindow.Image_V_Scrollbar.setPageStep((self.image_lable.current_image_image.size[1] * self.image_lable.zoom - self.mainWindow.Image_Lable.height()) // 10)
        else:
            self.mainWindow.Image_V_Scrollbar.setDisabled(True)

    def Set_scrollbar_value(self,x,y):
        self.image_lable.scrollbar_offset = [x,y]

        self.mainWindow.Image_H_Scrollbar.blockSignals(True)
        self.mainWindow.Image_V_Scrollbar.blockSignals(True)
        self.mainWindow.Image_H_Scrollbar.setValue(x)
        self.mainWindow.Image_V_Scrollbar.setValue(y)
        self.mainWindow.Image_H_Scrollbar.blockSignals(False)
        self.mainWindow.Image_V_Scrollbar.blockSignals(False)

    def On_image_H_scrollbar_valueChanged(self):
        self.image_lable.scrollbar_offset[0] = self.mainWindow.Image_H_Scrollbar.value()
        self.image_lable.Draw_image_lable()

    def On_image_V_scrollbar_valueChanged(self):
        self.image_lable.scrollbar_offset[1] = self.mainWindow.Image_V_Scrollbar.value()
        self.image_lable.Draw_image_lable()

    def wheelEvent(self,event):
        if self.system_state.image_loaded:
            if event.angleDelta().y() > 0 :
                if self.image_lable.zoom < ZOOM_LIMITE:
                    self.image_lable.zoom += 1

                    self.mainWindow.Image_H_Scrollbar.blockSignals(True)
                    self.mainWindow.Image_V_Scrollbar.blockSignals(True)
                    self.image_lable.Set_scrollbar_display()

                    if self.mainWindow.Image_H_Scrollbar.isEnabled():
                        self.mainWindow.Image_H_Scrollbar.setValue(self.image_lable.scrollbar_offset[0] + (self.image_lable.scrollbar_offset[0] + self.mainWindow.Image_Lable.width() // 2) // (self.image_lable.zoom - 1))
                        self.image_lable.scrollbar_offset[0] = self.mainWindow.Image_H_Scrollbar.value()
                    else:
                        self.mainWindow.Image_H_Scrollbar.setValue(0)
                        self.image_lable.scrollbar_offset[0] = self.mainWindow.Image_H_Scrollbar.value()

                    if self.mainWindow.Image_V_Scrollbar.isEnabled():
                        self.mainWindow.Image_V_Scrollbar.setValue(self.image_lable.scrollbar_offset[1] + (self.image_lable.scrollbar_offset[1] + self.mainWindow.Image_Lable.height() // 2) // (self.image_lable.zoom - 1))
                        self.image_lable.scrollbar_offset[1] = self.mainWindow.Image_V_Scrollbar.value()
                    else:
                        self.mainWindow.Image_V_Scrollbar.setValue(0)
                        self.image_lable.scrollbar_offset[1] = self.mainWindow.Image_V_Scrollbar.value()

                    self.mainWindow.Image_H_Scrollbar.blockSignals(False)
                    self.mainWindow.Image_V_Scrollbar.blockSignals(False)

                    self.image_lable.Draw_image_lable()

            elif event.angleDelta().y() < 0 :
                if self.image_lable.zoom > 1:
                    self.image_lable.zoom -= 1

                    self.mainWindow.Image_H_Scrollbar.blockSignals(True)
                    self.mainWindow.Image_V_Scrollbar.blockSignals(True)
                    self.image_lable.Set_scrollbar_display()

                    if self.mainWindow.Image_H_Scrollbar.isEnabled():
                        if self.image_lable.scrollbar_offset[0] - (self.image_lable.scrollbar_offset[0] + self.mainWindow.Image_Lable.width() // 2) // (self.image_lable.zoom + 1) < self.mainWindow.Image_H_Scrollbar.maximum():
                            self.mainWindow.Image_H_Scrollbar.setValue(self.image_lable.scrollbar_offset[0] - (self.image_lable.scrollbar_offset[0] + self.mainWindow.Image_Lable.width() // 2) // (self.image_lable.zoom + 1))
                        else:
                            self.mainWindow.Image_H_Scrollbar.setValue(self.mainWindow.Image_H_Scrollbar.maximum())
                        self.image_lable.scrollbar_offset[0] = self.mainWindow.Image_H_Scrollbar.value()
                    else:
                        self.mainWindow.Image_H_Scrollbar.setValue(0)
                        self.image_lable.scrollbar_offset[0] = self.mainWindow.Image_H_Scrollbar.value()

                    if self.mainWindow.Image_V_Scrollbar.isEnabled():
                        if self.image_lable.scrollbar_offset[1] - (self.image_lable.scrollbar_offset[1] + self.mainWindow.Image_Lable.height() // 2) // (self.image_lable.zoom + 1) < self.mainWindow.Image_V_Scrollbar.maximum():
                            self.mainWindow.Image_V_Scrollbar.setValue(self.image_lable.scrollbar_offset[1] - (self.image_lable.scrollbar_offset[1] + self.mainWindow.Image_Lable.height() // 2) // (self.image_lable.zoom + 1))
                        else:
                            self.mainWindow.Image_V_Scrollbar.setValue(self.mainWindow.Image_V_Scrollbar.maximum())
                        self.image_lable.scrollbar_offset[1] = self.mainWindow.Image_V_Scrollbar.value()
                    else:
                        self.mainWindow.Image_V_Scrollbar.setValue(0)
                        self.image_lable.scrollbar_offset[1] = self.mainWindow.Image_V_Scrollbar.value()

                    self.mainWindow.Image_H_Scrollbar.blockSignals(False)
                    self.mainWindow.Image_V_Scrollbar.blockSignals(False)

                    self.image_lable.Draw_image_lable()

    def resizeEvent(self,event):
        if not self.system_state.UIloaded:
            self.system_state.UIloaded = True
            return

        self.image_lable.Set_scrollbar_display()
        self.color_lable.Draw_color_preview_lable()
        self.image_lable.Draw_image_lable()

    def Set_image_background(self):
        color_backup = self.color_lable.color.copy()

        self.functional_arithmetic.Auto_pick_color(0)
        if int(self.color_lable.color[0]) + int(self.color_lable.color[1]) + int(self.color_lable.color[2]) < 382 or self.color_lable.color[3] == 0:
            self.image_lable.image_lable_background = self.image_lable_background_W
        else:
            self.image_lable.image_lable_background = self.image_lable_background_B

        self.mainWindow.R_Value.setText(str(255))
        self.mainWindow.G_Value.setText(str(255))
        self.mainWindow.B_Value.setText(str(255))
        self.mainWindow.A_Value.setText(str(255))

        self.color_lable.color = color_backup

        self.image_lable.Draw_image_lable()

class Mouse_And_Key_Events(QWidget):
    def __init__(self,mainWindow):
        self.mainWindow = mainWindow
        QWidget.__init__(self)

        self.draging = False
        self.drag_first_point = QPoint()
        self.drag_second_point = QPoint()

    def mousePressEvent(self,event):
        if self.mainWindow.Image_Lable.geometry().x() <= event.pos().x() and event.pos().x() <= self.mainWindow.Image_Lable.geometry().x() + self.mainWindow.Image_Lable.geometry().width()\
           and self.mainWindow.Image_Lable.geometry().y() <= event.pos().y() and event.pos().y() <= self.mainWindow.Image_Lable.geometry().y() + self.mainWindow.Image_Lable.geometry().height()\
           and self.system_state.image_loaded:
            click_point = [0,0]
            click_point[0] = (event.pos().x() - self.mainWindow.Image_Lable.geometry().x() + self.image_lable.scrollbar_offset[0]) // self.image_lable.zoom\
                             if self.mainWindow.Image_H_Scrollbar.isEnabled()\
                             else ((event.pos().x() - self.mainWindow.Image_Lable.geometry().x())\
                                  - (self.mainWindow.Image_Lable.width() - self.image_lable.current_image_image.size[0] * self.image_lable.zoom) // 2) \
                                  // self.image_lable.zoom
            click_point[1] = (event.pos().y() - self.mainWindow.Image_Lable.geometry().y() + self.image_lable.scrollbar_offset[1]) // self.image_lable.zoom\
                             if self.mainWindow.Image_V_Scrollbar.isEnabled()\
                             else ((event.pos().y() - self.mainWindow.Image_Lable.geometry().y())\
                                  - (self.mainWindow.Image_Lable.height() - self.image_lable.current_image_image.size[1] * self.image_lable.zoom) // 2) \
                                  // self.image_lable.zoom
             
            if event.button() == Qt.LeftButton:
                if self.mouse_and_key_events.draging:
                    self.mouse_and_key_events.drag_first_point = event.pos()
                    self.setCursor(Qt.ClosedHandCursor)

                elif self.mainWindow.Cutout_RadioB.isChecked() and not self.system_state.system_busy:
                    self.system_state.System_busy()
                    t = THREADING_Thread(target=self.functional_arithmetic.Cutout_image,args=(click_point[0],click_point[1],0,))
                    t.start()

                elif self.mainWindow.PickColor_RadioB.isChecked():
                    self.functional_arithmetic.Pick_color(click_point[0],click_point[1])

                elif self.mainWindow.Coloring_RadioB.isChecked() and not self.system_state.system_busy:
                    self.functional_arithmetic.Coloring_image(click_point[0],click_point[1])

                elif self.mainWindow.Filling_RadioB.isChecked() and not self.system_state.system_busy:
                    self.system_state.System_busy()
                    t = THREADING_Thread(target=self.functional_arithmetic.Filling_image,args=(click_point[0],click_point[1],))
                    t.start()

            elif event.button() == Qt.RightButton and self.mainWindow.Cutout_RadioB.isChecked() and not self.system_state.system_busy:
                self.functional_arithmetic.Pick_color(click_point[0],click_point[1])

                self.system_state.System_busy()
                t = THREADING_Thread(target=self.functional_arithmetic.Cutout_image,args=(click_point[0],click_point[1],0,))
                t.start()

    def mouseMoveEvent(self,event):
        if self.mainWindow.Image_Lable.geometry().x() <= event.pos().x() and event.pos().x() <= self.mainWindow.Image_Lable.geometry().x() + self.mainWindow.Image_Lable.geometry().width()\
           and self.mainWindow.Image_Lable.geometry().y() <= event.pos().y() and event.pos().y() <= self.mainWindow.Image_Lable.geometry().y() + self.mainWindow.Image_Lable.geometry().height()\
           and self.system_state.image_loaded:
            click_point = [0,0]
            click_point[0] = (event.pos().x() - self.mainWindow.Image_Lable.geometry().x() + self.image_lable.scrollbar_offset[0]) // self.image_lable.zoom\
                             if self.mainWindow.Image_H_Scrollbar.isEnabled()\
                             else ((event.pos().x() - self.mainWindow.Image_Lable.geometry().x())\
                                  - (self.mainWindow.Image_Lable.width() - self.image_lable.current_image_image.size[0] * self.image_lable.zoom) // 2) \
                                  // self.image_lable.zoom
            click_point[1] = (event.pos().y() - self.mainWindow.Image_Lable.geometry().y() + self.image_lable.scrollbar_offset[1]) // self.image_lable.zoom\
                             if self.mainWindow.Image_V_Scrollbar.isEnabled()\
                             else ((event.pos().y() - self.mainWindow.Image_Lable.geometry().y())\
                                  - (self.mainWindow.Image_Lable.height() - self.image_lable.current_image_image.size[1] * self.image_lable.zoom) // 2) \
                                  // self.image_lable.zoom
            
            if event.buttons() == Qt.LeftButton:
                if self.mouse_and_key_events.draging:
                    self.mouse_and_key_events.drag_second_point = event.pos()

                    if self.mainWindow.Image_H_Scrollbar.isEnabled():
                        self.image_lable.scrollbar_offset[0] += self.mouse_and_key_events.drag_first_point.x() - self.mouse_and_key_events.drag_second_point.x()
                        if self.image_lable.scrollbar_offset[0] < 0:
                            self.image_lable.scrollbar_offset[0] = 0
                        if self.image_lable.scrollbar_offset[0] > self.image_lable.current_image_image.size[0] * self.image_lable.zoom - self.mainWindow.Image_Lable.width():
                            self.image_lable.scrollbar_offset[0] = self.image_lable.current_image_image.size[0] * self.image_lable.zoom - self.mainWindow.Image_Lable.width()

                        self.mainWindow.Image_H_Scrollbar.blockSignals(True)
                        self.mainWindow.Image_H_Scrollbar.setValue(self.image_lable.scrollbar_offset[0])
                        self.mainWindow.Image_H_Scrollbar.blockSignals(False)

                    if self.mainWindow.Image_V_Scrollbar.isEnabled():       
                        self.image_lable.scrollbar_offset[1] += self.mouse_and_key_events.drag_first_point.y() - self.mouse_and_key_events.drag_second_point.y()
                        if self.image_lable.scrollbar_offset[1] < 0:
                            self.image_lable.scrollbar_offset[1] = 0
                        if self.image_lable.scrollbar_offset[1] > self.image_lable.current_image_image.size[1] * self.image_lable.zoom - self.mainWindow.Image_Lable.height():
                            self.image_lable.scrollbar_offset[1] = self.image_lable.current_image_image.size[1] * self.image_lable.zoom - self.mainWindow.Image_Lable.height()

                        self.mainWindow.Image_V_Scrollbar.blockSignals(True)
                        self.mainWindow.Image_V_Scrollbar.setValue(self.image_lable.scrollbar_offset[1])
                        self.mainWindow.Image_V_Scrollbar.blockSignals(False)
                                            
                    self.image_lable.Draw_image_lable()

                    self.mouse_and_key_events.drag_first_point = self.mouse_and_key_events.drag_second_point

                elif self.mainWindow.Cutout_RadioB.isChecked() and not self.system_state.system_busy:
                    self.system_state.System_busy()
                    t = THREADING_Thread(target=self.functional_arithmetic.Cutout_image,args=(click_point[0],click_point[1],0,))
                    t.start()

                elif self.mainWindow.PickColor_RadioB.isChecked():
                    self.functional_arithmetic.Pick_color(click_point[0],click_point[1])

                elif self.mainWindow.Coloring_RadioB.isChecked() and not self.system_state.system_busy:
                    self.functional_arithmetic.Coloring_image(click_point[0],click_point[1])

                elif self.mainWindow.Filling_RadioB.isChecked() and not self.system_state.system_busy:
                    self.system_state.System_busy()
                    t = THREADING_Thread(target=self.functional_arithmetic.Filling_image,args=(click_point[0],click_point[1],))
                    t.start()

            elif event.buttons() == Qt.RightButton and self.mainWindow.Cutout_RadioB.isChecked() and not self.system_state.system_busy:
                self.functional_arithmetic.Pick_color(click_point[0],click_point[1])

                self.system_state.System_busy()
                t = THREADING_Thread(target=self.functional_arithmetic.Cutout_image,args=(click_point[0],click_point[1],0,))
                t.start()

    def mouseReleaseEvent(self,event):
        self.setCursor(Qt.ArrowCursor)

        if self.mainWindow.Coloring_RadioB.isChecked() and self.system_state.image_loaded and not self.system_state.system_busy \
        and self.mainWindow.Image_Lable.geometry().x() <= event.pos().x() and event.pos().x() <= self.mainWindow.Image_Lable.geometry().x() + self.mainWindow.Image_Lable.geometry().width() \
        and self.mainWindow.Image_Lable.geometry().y() <= event.pos().y() and event.pos().y() <= self.mainWindow.Image_Lable.geometry().y() + self.mainWindow.Image_Lable.geometry().height():
            self.backup_mod.Insert_backup()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.mouse_and_key_events.draging = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.mouse_and_key_events.draging = False

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        if not OS_path.isfile('res/Icon.ico'):
            QMessageBox.question(self,'阿勒勒？','Icon.ico没了？？？',QMessageBox.Yes)
            SYS_exit()
        if not OS_path.isfile('res/Transparent_Lable.png'):
            QMessageBox.question(self,'阿勒勒？','Transparent_Lable.png没了？？？',QMessageBox.Yes)
            SYS_exit()
        if not OS_path.isfile('res/TransparentBg-B.png'):
            QMessageBox.question(self,'阿勒勒？','TransparentBg-B.png没了？？？',QMessageBox.Yes)
            SYS_exit()
        if not OS_path.isfile('res/TransparentBg-W.png'):
            QMessageBox.question(self,'阿勒勒？','TransparentBg-W.png没了？？？',QMessageBox.Yes)
            SYS_exit()

        self.setupUi(self)

        self.mainWindow = self

        self.functional_arithmetic = Functional_Arithmetic(self.mainWindow)
        self.backup_mod = Backup_Mod(self.mainWindow)
        self.system_state = System_State(self.mainWindow)
        self.all_bottons = All_Bottons(self.mainWindow)
        self.color_lable = Color_Lable(self.mainWindow)
        self.image_lable = Image_Lable(self.mainWindow)
        self.mouse_and_key_events = Mouse_And_Key_Events(self.mainWindow)

        self.Set_functional_arithmetic()
        self.Set_backup_mod()
        self.Set_system_state()
        self.Set_all_bottons()
        self.Set_color_lable()
        self.Set_image_lable()
        self.Set_mouse_and_key_events()
        self.Set_QLable_file_dragable()

        self.wheelEvent = self.image_lable.wheelEvent
        self.resizeEvent = self.image_lable.resizeEvent
        self.mousePressEvent = self.mouse_and_key_events.mousePressEvent
        self.mouseMoveEvent = self.mouse_and_key_events.mouseMoveEvent
        self.mouseReleaseEvent = self.mouse_and_key_events.mouseReleaseEvent
        self.keyPressEvent = self.mouse_and_key_events.keyPressEvent
        self.keyReleaseEvent = self.mouse_and_key_events.keyReleaseEvent
        self.closeEvent = self.system_state.closeEvent

        self.color_lable.Draw_color_preview_lable()
        self.Image_Lable.setPixmap(ImageQt.toqpixmap(self.image_lable.image_lable_background))

    def Set_functional_arithmetic(self):
        self.functional_arithmetic.functional_arithmetic = self.functional_arithmetic
        self.functional_arithmetic.color_lable = self.color_lable
        self.functional_arithmetic.image_lable = self.image_lable
        self.functional_arithmetic.mouse_and_key_events = self.mouse_and_key_events
        self.functional_arithmetic.system_state = self.system_state
        self.functional_arithmetic.all_bottons = self.all_bottons
        self.functional_arithmetic.backup_mod = self.backup_mod

    def Set_backup_mod(self):
        self.backup_mod.functional_arithmetic = self.functional_arithmetic
        self.backup_mod.color_lable = self.color_lable
        self.backup_mod.image_lable = self.image_lable
        self.backup_mod.mouse_and_key_events = self.mouse_and_key_events
        self.backup_mod.system_state = self.system_state
        self.backup_mod.all_bottons = self.all_bottons
        self.backup_mod.backup_mod = self.backup_mod

    def Set_system_state(self):
        self.system_state.functional_arithmetic = self.functional_arithmetic
        self.system_state.color_lable = self.color_lable
        self.system_state.image_lable = self.image_lable
        self.system_state.mouse_and_key_events = self.mouse_and_key_events
        self.system_state.system_state = self.system_state
        self.system_state.all_bottons = self.all_bottons
        self.system_state.backup_mod = self.backup_mod

    def Set_all_bottons(self):
        self.all_bottons.functional_arithmetic = self.functional_arithmetic
        self.all_bottons.color_lable = self.color_lable
        self.all_bottons.image_lable = self.image_lable
        self.all_bottons.mouse_and_key_events = self.mouse_and_key_events
        self.all_bottons.system_state = self.system_state
        self.all_bottons.all_bottons = self.all_bottons
        self.all_bottons.backup_mod = self.backup_mod

    def Set_color_lable(self):
        self.color_lable.functional_arithmetic = self.functional_arithmetic
        self.color_lable.color_lable = self.color_lable
        self.color_lable.image_lable = self.image_lable
        self.color_lable.mouse_and_key_events = self.mouse_and_key_events
        self.color_lable.system_state = self.system_state
        self.color_lable.all_bottons = self.all_bottons
        self.color_lable.backup_mod = self.backup_mod

    def Set_image_lable(self):
        self.image_lable.functional_arithmetic = self.functional_arithmetic
        self.image_lable.color_lable = self.color_lable
        self.image_lable.image_lable = self.image_lable
        self.image_lable.mouse_and_key_events = self.mouse_and_key_events
        self.image_lable.system_state = self.system_state
        self.image_lable.all_bottons = self.all_bottons
        self.image_lable.backup_mod = self.backup_mod

    def Set_mouse_and_key_events(self):
        self.mouse_and_key_events.functional_arithmetic = self.functional_arithmetic
        self.mouse_and_key_events.color_lable = self.color_lable
        self.mouse_and_key_events.image_lable = self.image_lable
        self.mouse_and_key_events.mouse_and_key_events = self.mouse_and_key_events
        self.mouse_and_key_events.system_state = self.system_state
        self.mouse_and_key_events.all_bottons = self.all_bottons
        self.mouse_and_key_events.backup_mod = self.backup_mod

    def Set_QLable_file_dragable(self):
        self.Image_Lable.mainWindow = self.mainWindow

        self.Image_Lable.functional_arithmetic = self.functional_arithmetic
        self.Image_Lable.color_lable = self.color_lable
        self.Image_Lable.image_lable = self.image_lable
        self.Image_Lable.mouse_and_key_events = self.mouse_and_key_events
        self.Image_Lable.system_state = self.system_state
        self.Image_Lable.all_bottons = self.all_bottons
        self.Image_Lable.backup_mod = self.backup_mod

    

if __name__ == '__main__':
    app = QApplication(SYS_argv)
    mainWindow = MainWindow()
    mainWindow.show()
    SYS_exit(app.exec_())
