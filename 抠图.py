from os import walk
from PIL import Image
import numpy as np

#抠图方法，以最左上角为背景色，把背景抠掉
def cut(root,filename):
    img = Image.open(root + '\\' + filename)
    img = img.convert("RGBA")
    #把图片转化成数组，加快速度
    pixdata = np.array(img)

    #透明的RGBA通道数值
    transparent = np.array([0,0,0,0])

    
    #当最左上角的像素是透明，是已经抠过一次，有死角没扣到，手动修正一下又来抠，就要手动指定颜色
    if all(pixdata[0,0] == transparent):
        r,g,b = list(map(eval,input("以RGB值指定背景颜色，用空格间隔\n").split()))
        color = np.array([r,g,b,255])
    else:
    #否则以最左上角为背景色，把背景抠掉
        color = pixdata[0,0]
    

    #先把外面一圈的纯色像素扣掉，既是为了抠出图片的主体，也是为了减小复杂度，上下左右指要留下区域的上下左右边界
    left,upper,right,lower = 10,0,0,0
    #从上下左右四个方向四次遍历图片，确定上下左右边界
    flag = 0
    for x in range(img.size[0]):
        for y in range(img.size[1]):
                #如果某个像素和背景色的差值大于容差，就要留下不抠，第一个这样的像素就是边界的位置
            if  any(abs(pixdata[y,x] - color) > tolerance):
                left = x
                flag = 1
                break
        if flag == 1 :
            break

    flag = 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if any(abs(pixdata[y,x] - color) > tolerance):
                upper = y
                flag = 1
                break
        if flag == 1 :
            break

    flag = 0
    for x in range(img.size[0] - 1,-1,-1):
        for y in range(img.size[1]):
            if any(abs(pixdata[y,x] - color) > tolerance):
                right = x
                flag = 1
                break
        if flag == 1 :
            break

    flag = 0
    for y in range(img.size[1] - 1,-1,-1):
        for x in range(img.size[0]):
            if any(abs(pixdata[y,x] - color) > tolerance):
                lower = y
                flag = 1
                break
        if flag == 1 :
            break

    #边界确定了，抠出来，再刷新一下pixdata
    img = img.crop((left,upper,right + 1,lower + 1))
    pixdata = np.array(img)
    print("第",i,"张图片，当前阶段1/3")


    #预处理，先从左到右，从右到左，从上到下，从下到上各遍历一遍，遇到需要抠掉的像素就抠，遇到要留下的像素就跳到下一行或下一列，
    #这样子一般能把大部分要抠掉的像素都抠掉，没抠到的才交给广度优先遍历，减小复杂度
    #有没有预处理整个抠图过程中访问的像素数量是一样的，但预处理中访问每个像素的时间比广度优先更短，
    #加入预处理相当于把一部分像素交给速度快的预处理，只有少量死角才由速度慢当不留死角的广度优先处理
    #我的例子测试下来有预处理比没有快了1/6到1/7
    for x in range(img.size[0]):
        for y in range(img.size[1]):
                #如果某个像素四个通道数值和背景差值小于容差，就要抠掉
            if all(abs(pixdata[y,x] - color) < tolerance):
                pixdata[y,x] = transparent
                #其他情况就只有遇到了应该留下的像素，跳到下一行或下一列
            else:
                break

    for x in range(img.size[0]):
        for y in range(img.size[1] - 1,-1,-1):
            if all(abs(pixdata[y,x] - color) < tolerance):
                pixdata[y,x] = transparent
            else:
                break

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if all(abs(pixdata[y,x] - color) < tolerance):
                pixdata[y,x] = transparent
            else:
                break

    for y in range(img.size[1]):
        for x in range(img.size[0] - 1,-1,-1):
            if all(abs(pixdata[y,x] - color) < tolerance):
                pixdata[y,x] = transparent
            else:
                break
    print("第",i,"张图片，当前阶段2/3")


    #广度优先遍历的起点
    starting_point = list()
    #扫描所有像素
    for y in range(1,img.size[1]-1):
        for x in range(1,img.size[0]-1):
               #这个像素不透明                      这个像素和背景差值小于容差                    这个像素的上下左右至少有一个是透明的（已经被抠掉了）
            if all(pixdata[y,x] != transparent) and all(abs(pixdata[y,x] - color) < tolerance) and (pixdata[y,x - 1][3] == 0 or pixdata[y,x + 1][3] == 0 or pixdata[y - 1,x][3] == 0 or pixdata[y + 1,x][3] == 0):
                #那这个像素是死角的边界
                starting_point.append((x,y))


    #遍历用的栈
    stack = list()
    #剩余的遍历入口数量
    length = len(starting_point)
    for point in starting_point:
        stack.append(point)
        length -= 1
        #广度优先的细节懒得写了，反正来看代码的肯定知道广度优先是啥
        while True:
            if len(stack) == 0:
                break

            x,y = stack.pop()

            print("第",i,"张图片，当前阶段3/3,剩余待处理的区块：",length, "当前区块剩余像素数量：",len(stack))

            #把当前访问的像素抠掉
            pixdata[y,x] = transparent
            

            #如果上下左右的像素需要被抠掉就压栈            
            if all(abs(pixdata[y,x + 1] - color) < tolerance) and all(pixdata[y,x + 1] != transparent):
                stack.append((x + 1,y))
                
            if all(abs(pixdata[y,x - 1] - color) < tolerance) and all(pixdata[y,x - 1] != transparent):
                stack.append((x - 1,y))
                
            if all(abs(pixdata[y - 1,x] - color) < tolerance) and all(pixdata[y - 1,x] != transparent):
                stack.append((x,y - 1))
                
            if all(abs(pixdata[y + 1,x] - color) < tolerance) and all(pixdata[y + 1,x] != transparent):
                stack.append((x,y + 1))
                

    img = Image.fromarray(np.uint8(pixdata))
    img.save('done\\' + filename)
    



#抠图容差，有些图背景可能是254，253之类的，当某个像素三个通道颜色都和背景之差都小于容差时会被抠掉
tolerance = eval(input("指定抠图颜色容差\n"))
#正在处理第i张图片
i = 0
for root,dir,file in walk("source"):
    for filename in file:
        i += 1
        #抠source文件夹里的所有图片，抠完了放在done文件夹里
        cut(root,filename)
        print("第",i,"张图片抠图完成")

print("都抠完了")

#最后就是这个算法实现了边缘检测，但只能检测到算法认为的边缘，比如一条丝带围了一圈，在人看来中间一圈白的是要抠掉的，但是算法认不出来
#这种可以手动用PS什么的点一个透明像素在里面，再跑一遍算法
#还有一种情况就是比如一张纸，边缘是黑的，中间是白的，这张纸超出了图片的边界，在人看来是不应该抠掉的，但是算法就会把纸中间的白色像素抠掉
#这种因为抠掉的都是纯色，可以用PS手动填充一下，不怎么麻烦
#这两种边界检测的算法是想不出来了，目测要用机器学习弄，菜鸡表示......
