import os
import qt5_applications
dirname = os.path.dirname(qt5_applications.__file__)
plugin_path = os.path.join(dirname, 'Qt', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline


def getRGB(dWave: float, maxPix=1, gamma=1):
    """根据波长绘制颜色

    Args:
        dWave (float): 波长
        maxPix (int, optional): 最大值. Defaults to 1.
        gamma (int, optional): 调教参数. Defaults to 1.

    Returns:
        _type_: 波长对应颜色的rgb值
    """
    waveArea = [380,440,490,510,580,645,780]
    minusWave = [0,440,440,510,510,645,780]
    deltWave = [1,60,50,20,70,65,35]
    for p in range(len(waveArea)):
        if dWave<waveArea[p]:
            break

    pVar = abs(minusWave[p]-dWave)/deltWave[p]
    rgbs = [[0,0,0],[pVar,0,1],[0,pVar,1],[0,1,pVar],
            [pVar,1,0],[1,pVar,0],[1,0,0],[0,0,0]]
    
    #在光谱边缘处颜色变暗
    if (dWave>=380) & (dWave<420):
        alpha = 0.3+0.7*(dWave-380)/(420-380)
    elif (dWave>=420) & (dWave<701):
        alpha = 1.0
    elif (dWave>=701) & (dWave<780):
        alpha = 0.3+0.7*(780-dWave)/(780-700)
    else:
        alpha = 0       #非可见区

    return [maxPix*(c*alpha)**gamma for c in rgbs[p]] # 返回0-1浮点数范围的rgb值列表


def drawSpec():
    pic = np.zeros([100, 360, 3])
    rgb = [getRGB(d) for d in range(400, 760)]
    pic = pic + rgb
    plt.imshow(pic)
    plt.yticks(range(0, 100, 10), [str(0 + 10 * i) for i in range(10)])
    plt.xticks(range(0, 360, 50), [str(400+ 50 * i) for i in range(int((760-400)/50)+1)])
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


def line_chart(lx: np.ndarray, ly: np.ndarray):
    """折线图

    Args:
        lx (np.ndarray): x轴数据
        ly (np.ndarray): y轴数据
    """
    fig, ax = plt.subplots()
    ax.plot()


def save_image(lx, ly, path):
    plt.figure()
    plt.plot(lx, ly, label='spec data')
    plt.legend() # 使图例生效
    plt.xlabel('lambda')
    plt.ylabel('relative intensity')
    plt.savefig(path)
    plt.show()


if __name__ == '__main__':
    # drawSpec()
    print(getRGB(532.8))