from typing import Tuple
import serial

def sendorder(ser: serial.Serial, order: int) -> int:
    """给下位机发送指令

    Args:
        ser (serial.Serial): 串口
        order (int): 0-停止 1-校准 2-循环扫描 3-单次扫描

    Returns:
        int: 返回成功发送的字节数
    """
    return ser.write(order.to_bytes(length=1, byteorder='little'))

def readlinedata(ser: serial.Serial) -> Tuple:
    """读取Arduino发送的一行数据 形式为 i' 'pdout

    Args:
        ser (serial.Serial): 串口

    Returns:
        Tuple: 返回(DACSignal: int, pdout: int) 如果是(-2, -2)表示没有读取到数据，
        如果是(-1, -1)则是Arduino扫描一次后发出的间隔信号 
    """
    
    line = ser.readline().split() # line = [DACSingle, pdout]
    
    if line:
        return (int(line[0]), int(line[1])) # (DACSignal: 0-4095, pdout: 0-1023)
    else:
        return (-2, -2) # 说明没有读取到数据，可能存在通信问题或者下位机处于暂停状态
    
def AngletoLambda(DACSigal: int) -> float:
    """将下位机发送的DACSignal转化为对应的测量波长

    Args:
        DACSigal (int): 下位机发送的DACSignal

    Returns:
        float: 对应的测量波长，0.5nm精度
    """
    # 待完成
    pass
    