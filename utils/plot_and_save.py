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

    dWave = dWave * 1e9

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


def save_image(lx: np.ndarray, ly: np.ndarray, path, cal_i=None, cal_lambda=None):
    """画图并保存

    Args:
        lx (_type_): 横轴数据 已经转换为λ了 但不是按照大小顺序
        ly (_type_): 纵轴数据
        path (_type_): 保存路径 xxx.png
        cal_i (_type_): 校准的激光的i 方便多次实验比较
        cal_lambda (_type_): 校准激光的λ
    """

    # PD响应曲线
    def PD_eff(wave):
        if 400.0 <= wave and wave < 500:
            return 0.3 - 0.0012 * (500-wave)
        elif wave < 600:
            return 0.41 - 0.0011 * (600-wave)
        elif wave < 700:
            return 0.48 - 0.0007 * (700-wave)
        else:
            raise NotImplementedError('目前设计的波长范围肯定不会超过700nm 不会低于400nm')

    # 光栅效率参数
    efficiency_x = []  # 波长 单位为nm
    efficiency_y = []  # 效率 单位为100% 使用的时候需要除100

    with open('utils\gatecoe.txt', 'r') as f:
        Data = f.readlines()
        for data in Data:
            wave = float(data.strip('\n').split(',')[0])
            efficiency = float(data.strip('\n').split(',')[1])
            efficiency_x.append(wave)
            efficiency_y.append(efficiency)

    # gate_eff = {k:v for k, v in zip(efficiency_x, efficiency_y)}
    # 转换成ndarray在查找的时候会快一些
    efficiency_x = np.array(efficiency_x)
    efficiency_y = np.array(efficiency_y)

    def Gate_eff(wave):
        idx1 = np.where(efficiency_x > wave)[0][0]

        e1, e2 = efficiency_y[idx1], efficiency_y[idx1-1]
        return (e1+e2) / 2 / 100

    lth = lx.argsort()  # 返回横轴坐标中从小到大的索引值

    x_lth = np.empty_like(lx)
    y_lth = np.empty_like(ly)
    # 将读取到的光谱数据按照波长从小到大进行排序 便于之后的求平均值处理
    for i in range(len(x_lth)):
        x_lth[i] = lx[lth[i]] * 1e9  # 单位nm
        y_lth[i] = ly[lth[i]]
        y_lth[i] = y_lth[i] / PD_eff(x_lth[i]) / \
            Gate_eff(x_lth[i]) / 1024*5.0  # 单位V

    '''但这种做法并不能很好解决我们的数据是上下波动的情况
    # 平滑降噪操作 使用Savitzky-Golay方法
    from scipy.signal import savgol_filter
    y_lth = savgol_filter(y_lth, 11, 2)
    '''

    # 尝试实现一个一维卷积 实现每十个数据求平均值
    def np_move_avg(arr, N=25, mode='same'):
        return (np.convolve(arr, np.ones((N,))/N, mode=mode))


    y_lth = np_move_avg(y_lth)
    
    ### 尝试在平均降噪之后，在通过savitzky-golay进行一次平滑操作
    from scipy.signal import savgol_filter
    y_lth = savgol_filter(y_lth, 11, 2)

    plt.figure(figsize=(18.0, 15))

    for i in range(len(lth)-1):
        rgbs = getRGB((x_lth[i]+x_lth[i+1])/2*1e-9)
        plt.plot(np.array([x_lth[i], x_lth[i+1]]),
                 np.array([y_lth[i], y_lth[i+1]]), color=rgbs)

    plt.xlabel(
        'wavelength: {:.1f}-{:.1f}nm'.format(np.min(x_lth), np.max(x_lth)))
    plt.ylabel('relative intensity/V')
    # 在图片标题处显示校准所用的激光的信息
    if cal_i and cal_lambda:
        plt.title(
            f"cal_i_1{cal_i[0]}-cal_lambda_1{cal_lambda[1]}-cal_i_2{cal_i[1]}-cal_lambda_2{cal_lambda[1]}")

    plt.savefig(path)
    plt.show()


if __name__ == '__main__':

    data = np.loadtxt(r'D:\pbl2\results\NFC芒果汁.txt')
    save_image(data[0, :], data[1, :], os.path.abspath('./test_NFC芒果_补偿_平均25_savgol'))
