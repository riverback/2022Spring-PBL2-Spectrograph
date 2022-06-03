import numpy as np
from matplotlib import pyplot as plt
from sympy import solve, sin, cos, Symbol, re



D = 1 / 1200 * 1e-3  # 光栅常数 1/1200 mm
DELTA_THETA = 12.5 / 4096  # 单位为° 指的是i每+1，对应的角度变化


def CirctoRad(theta_circ): return theta_circ / 180.0 * np.pi


def Calibrate(cal_i: np.ndarray, cal_lambda: np.ndarray):
    if cal_i.shape == (1, ):
        """
        只有一个校准点，此时如果要正常工作，需要调节面镜初始角度使得在旋转的一侧极限处，接收到校准信号，因此理论上 cal_i 会接近0 或者接近4095
        关于面镜旋转方向，可能要在后续固定镜子后确定镜子旋转方向后再进行确定
        """
        # lambda = 2 * d * sin(pi/2) * cos(phi - 7/72 * pi)
        x = Symbol('x') # phi_0 - 7/72*pi
        phi_0 = solve(cal_lambda - 2 * D * cos(x))  # 由于返回解的范围是0-2pi，因此必定会有两个解 phi_0 已经包含了 - 7/72*pi
        print(phi_0)
        print(phi_0[0])
        print(phi_0[0][x])
        def map_fun(i):
            # 这里实现的是默认 cal_i 非常接近0
            return 2 * D * cos(CirctoRad(DELTA_THETA*(i-cal_i[0]))+re(phi_0[1][x]))
        
        return map_fun
    elif cal_i.shape == (2, ):
        """
        有两个校准点，此时可以直接通过方程求解给出映射公式，但是仍需要根据镜子具体的旋转方向(即i变大时phi是变大还是变小)
        """
        x = Symbol('x') # phi_1 - 7/72*pi
        y = Symbol('y') # phi_2 - 7/72*pi
        z = Symbol('z') # sin(theta + 7/72 * pi)
        roots = solve([cal_lambda[0] - 2*D*z*cos(x), cal_lambda[1] - 2*D*z*cos(y), y-x-CirctoRad((cal_i[1]-cal_i[0])*DELTA_THETA)], [x,y,z])
        # 由于第三个方程是通过i的差值给出两次phi的插值，因此最终给出映射的时候就只使用phi_1了
        print(f"roots:{roots}")
        def map_fun(i):
            return 2 * D * cos(CirctoRad(DELTA_THETA*(i-cal_i[0])+roots[x][0]))


if __name__ == '__main__':
    cal_i1 = np.array([0, ])
    cal_lambda1 = np.array([1228.0, ])
    f1 = Calibrate(cal_i1, cal_lambda1)
    print("hello")
    print(f1(0))
    for i in range(0, 4000, 300):
        print(f"{i}: lambda: {f1(i)*1e9}nm")
    '''
    cal_i2 = np.array([0, 30])
    cal_lambda2 = np.array([1105.0*1e-9, 1434.0*1e-9])
    f2 = Calibrate(cal_i2, cal_lambda2)
    for i in range(0, 100, 10):
        print(f"{i}: lambda{f2(i)}")
    '''
    print("success?")