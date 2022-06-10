import numpy as np
from matplotlib import pyplot as plt
import sympy
from sympy import solve, sin, cos, Symbol, re, acos


D = 1 / 1200 * 1e-3  # 光栅常数 1/1200 mm
DELTA_THETA = (12.5 / 4096) * sympy.pi / 180  # 指的是i每+1，对应的角度变化 单位是弧度


def CirctoRad(theta_circ): return theta_circ / 180.0 * sympy.pi


def Calibrate(cal_i: np.ndarray, cal_lambda: np.ndarray):
    print("!!!")
    print(cal_i.shape)
    if cal_i.shape == (1, ):
        print("???")
        """
        只有一个校准点，此时如果要正常工作，需要调节面镜初始角度使得在旋转的一侧极限处，接收到校准信号，因此理论上 cal_i 会接近0 或者接近4095
        关于面镜旋转方向，可能要在后续固定镜子后确定镜子旋转方向后再进行确定
        """
        # lambda = 2 * d * sin(theta + 7/72*pi) * cos(phi - 7/72 * pi)
        x = Symbol('x')  # phi_0 - 7/72*pi
        # 由于返回解的范围是0-2pi，因此必定会有两个解 theta 已经包含了 - 7/72*pi
        print("cal_lambda: {}\nD: {}\ncal_i: {}".format(cal_lambda, D, cal_i))
        cos_theta = solve(
            cal_lambda[0] - 2 * D * x * sin((4096 - cal_i[0]) * DELTA_THETA + 7/72*sympy.pi))

        print(cos_theta)

        def map_fun(i):
            # 这里实现的是默认 cal_i 非常接近0
            # print(DELTA_THETA*(i-cal_i[0]))
            if len(cos_theta) > 1:
                return 2 * D * max(*cos_theta) * sin((4096 - i) * DELTA_THETA + 7/72*sympy.pi)
            else:
                return 2 * D * cos_theta[0] * sin((4096 - i) * DELTA_THETA + 7/72*sympy.pi)

        return map_fun

    elif cal_i.shape == (2, ):
        """
        有两个校准点 此时增加一个修正常数C 即 phi = i*DELTA_THETA + C
        """
        x = Symbol('x') # theta_0
        y = Symbol('y') # C, phi = 12.5/4096*i + C

        C = solve(acos((cal_lambda[1]-cal_lambda[0])/(2*D*sin(((cal_i[1]-cal_i[0])*DELTA_THETA)/2)))-(cal_i[1]+cal_i[0])*DELTA_THETA/2-y)

        theta_0 = solve(cal_lambda[0] - D*(sin(x)-sin(cal_i[0]*DELTA_THETA+C[0])))

        def map_fun(i):
            return D * (sin(theta_0[0]) - sin(DELTA_THETA*i + C[0]))

        return map_fun


if __name__ == '__main__':

    print("\n\n\n### 一个校准点 ###")

    cal_i1 = np.array([0, ])
    cal_lambda1 = np.array([423.0*1e-9, ])
    f1 = Calibrate(cal_i1, cal_lambda1)

    print(f1(0).evalf()*1e9, '     ', f1(4095).evalf()*1e9,
          '     ', f1(4095).evalf()*1e9-f1(0).evalf()*1e9)
    '''for i in range(0, 4000, 300):
        print(f"{i}: lambda: {f1(i).evalf()*1e9} nm")'''

    print("### 两个校准点 ###\n\n\n")

    cal_i2 = np.array([0, 30])
    cal_lambda2 = np.array([1105.0*1e-9, 1434.0*1e-9])
    f2 = Calibrate(cal_i2, cal_lambda2)
    print(f2(0).evalf()*1e9, '     ', f2(4095).evalf()*1e9,
          '     ', f2(4095).evalf()*1e9-f2(0).evalf()*1e9)
    '''for i in range(0, 4000, 100):
        print(f"{i}: lambda: {f2(i).evalf() * 1e9} nm")'''

    print("success?")
