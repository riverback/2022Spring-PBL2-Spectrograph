import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import fsolve


def CirctoRad(theta_circ): return theta_circ / 180.0 * np.pi


D = 1 / 1200  # 光栅常数 1/1200 mm
DELTA_THETA = 12.5 / 4096


def ItoLambda_1(cal_lambda: np.ndarray, array_I: np.ndarray) -> function:
    # 只有一个校准点的时候 此时不存在校准功能 只是通过已知的波长 将i映射到lambda上

    assert cal_lambda.shape == (
        1, ), f"calibrate node expext 1, but got: {cal_lambda.shape}"

    # 由于镜子转动的方向只有在实验时才能知道 因此这里先假定i变大镜子转动的角度theta也变大

    # d(lambda)/d(theta) = D * ( cos(theta + 17.5*2) - cos(theta) )

    def lambda_func(cal_lambda) -> function:
        # lambda = d(sin(theta+17.5*2+C)-sin(theta+C)) C是修正的参数，暂时不考虑
        # cal_theta 是角度值

        def fun(cal_theta) -> float:
            x = D * (np.sin(CirctoRad(cal_theta+17.5*2)) -
                     np.sin(CirctoRad(cal_theta))) - cal_lambda
            return x

        return fun

    # 返回函数的零点估计值 即解出当前lambda对应的理论角度
    cal_theta = fsolve(lambda_func(cal_lambda), 0.)

    def ImapLambda(i): return D * (np.sin(CirctoRad((i-array_I[0])*DELTA_THETA + 17.5*2) + cal_theta[0]) - np.sin(
        CirctoRad((i-array_I[0])*DELTA_THETA)) + cal_theta[0])
    
    return ImapLambda


def ItoLambda_2(cal_lambda: np.ndarray, array_I: np.ndarray) -> function:

    # 会有两个 cal_lambda时使用此函数 因此会求出 lambda(theta(i)) = lambda(ai)

    assert cal_lambda.shape == (
        2,), f"calibrate node expect 2, but got: {cal_lambda.shape}"

    def lambda_func(cal_lambda) -> function:
        # lambda = d(sin(theta+17.5*2+C)-sin(theta+C)) C是修正的参数，暂时不考虑
        # cal_theta 是角度值

        def fun(cal_theta) -> float:
            x = D * (np.sin(CirctoRad(cal_theta+17.5*2)) -
                     np.sin(CirctoRad(cal_theta))) - cal_lambda
            return x

        return fun

    cal_theta = fsolve(lambda_func(cal_lambda), 0.)  # 返回函数的零点估计值

    k = cal_theta[0] / array_I[0]

    def ItoTheta(i): return k * i

    # 用第二组 (i, lambda) 对函数进行校准

    theta_2 = ItoTheta(array_I[1])

    # lambda = d * (sin(theta+17.5*2+C) - sin(theta+C))
    C = cal_theta[1] - theta_2

    def ImapLambda(i): return D * (np.sin(CirctoRad(ItoTheta(i) + 17.5 * 2) +
                                          C) - np.sin(np.sin(CirctoRad(ItoTheta(i) + 17.5 * 2))))

    return ImapLambda
