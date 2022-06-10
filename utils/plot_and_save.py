from scipy.interpolate import make_interp_spline
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import os
import qt5_applications
dirname = os.path.dirname(qt5_applications.__file__)
plugin_path = os.path.join(dirname, 'Qt', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


def getRGB(dWave: float, maxPix=1, gamma=1):
    """根据波长绘制颜色

    Args:
        dWave (float): 波长
        maxPix (int, optional): 最大值. Defaults to 1.
        gamma (int, optional): 调教参数. Defaults to 1.

    Returns:
        _type_: 波长对应颜色的rgb值
    """
    waveArea = [380, 440, 490, 510, 580, 645, 780]
    minusWave = [0, 440, 440, 510, 510, 645, 780]
    deltWave = [1, 60, 50, 20, 70, 65, 35]
    for p in range(len(waveArea)):
        if dWave < waveArea[p]:
            break

    pVar = abs(minusWave[p]-dWave)/deltWave[p]
    rgbs = [[0, 0, 0], [pVar, 0, 1], [0, pVar, 1], [0, 1, pVar],
            [pVar, 1, 0], [1, pVar, 0], [1, 0, 0], [0, 0, 0]]

    # 在光谱边缘处颜色变暗
    if (dWave >= 380) & (dWave < 420):
        alpha = 0.3+0.7*(dWave-380)/(420-380)
    elif (dWave >= 420) & (dWave < 701):
        alpha = 1.0
    elif (dWave >= 701) & (dWave < 780):
        alpha = 0.3+0.7*(780-dWave)/(780-700)
    else:
        alpha = 0  # 非可见区

    return [maxPix*(c*alpha)**gamma for c in rgbs[p]]  # 返回0-1浮点数范围的rgb值列表


def drawSpec():
    pic = np.zeros([100, 360, 3])
    rgb = [getRGB(d) for d in range(400, 760)]
    pic = pic + rgb
    plt.imshow(pic)
    plt.yticks(range(0, 100, 10), [str(0 + 10 * i) for i in range(10)])
    plt.xticks(range(0, 360, 50), [str(400 + 50 * i)
               for i in range(int((760-400)/50)+1)])
    plt.savefig('Spec from 400 to 760')
    plt.show()


def smooth_xy(lx: np.ndarray, ly: np.ndarray):
    """数据平滑处理

    Args:
        lx (np.ndarray): x轴数据
        ly (np.ndarray): y轴数据
    """

    x_smooth = np.linspace(lx.min(), ly.min(), 400)
    y_smooth = make_interp_spline(lx, ly)(x_smooth)

    return (x_smooth, y_smooth)



def save_image(lx: np.ndarray, ly: np.ndarray, path, cal_i, cal_lambda):
    """画图并保存

    Args:
        lx (_type_): 横轴数据 已经转换为λ了 但不是按照大小顺序
        ly (_type_): 纵轴数据
        path (_type_): 保存路径 xxx.png
        cal_i (_type_): 校准的激光的i 方便多次实验比较
        cal_lambda (_type_): 校准激光的λ
    """
    plt.figure()
    
    lth = lx.argsort() # 返回横轴坐标中从小到大的索引值
    
    for i in range(len(lth)-1):
        rgbs = getRGB((lx[lth[i]]+lx[lth[i+1]])/2)
        plt.plot(np.array([lx[lth[i]], lx[lth[i+1]]]), np.array([ly[lth[i]], ly[lth[i+1]]]), color=rgbs)
        
    plt.xlabel('lambda')
    plt.ylabel('relative intensity')
    # 在图片标题处显示校准所用的激光的信息
    plt.title(f"cal_i_1{cal_i[0]}-cal_lambda_1{cal_lambda[1]}-cal_i_2{cal_i[1]}-cal_lambda_2{cal_lambda[1]}")
    
    
    
    plt.savefig(path)
    plt.show()


if __name__ == '__main__':
    # drawSpec()
    lx = np.array([405.0 + i * 0.5 for i in range(800)])
    ly = np.random.rand(1000)
    plt.figure()
    for i in range(len(lx)-1):
        rgb = getRGB((lx[i]+lx[i+1])/2)
        plt.plot(lx[i:i+2], ly[i:i+2], color=rgb, label='test')
    
    plt.show()