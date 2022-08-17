Code for 2022Spring PBL2 Group2 Spectrograph Project

Arduino code by ywh
    email: 2000011029@stu.pku.edu.cn
    
Python code by hhz 
    email: hhz_pku@163.com

More details about our prototype can be found in ![report](https://riverback.github.io/FileStorage/Spectrograph.pdf)

[Usage]

运行(Run)：

```bash
python main.py
```

![MainGUI](https://github.com/riverback/2022Spring-PBL2-Spectrograph/blob/main/images/MainGUI.png)

右下角显示 `serial open success`后可以正常使用

![start_scan](https://github.com/riverback/2022Spring-PBL2-Spectrograph/blob/main/images/start_scan.png)

循环扫描+画图：在点击**循环扫描**后，可在右下角观察到`开始循环扫描`，然后点击**画图**，便可以实时显示光电二极管的输出数据。

![Circular scan](https://github.com/riverback/2022Spring-PBL2-Spectrograph/blob/main/images/cycle_scan.png)

此时点击**暂停扫描**，便可以停止扫描，面镜旋转到最大或者最小位置，当右下角显示`扫描已暂停`，可以进行后续操作。



单次扫描：

只扫描一次，并根据之前的激光校准数据`cal_i,cal_lambda`进行波长的映射，最终保存光谱数据，命名规则为当前的系统时间。



校准：

根据Arduino程序`pbl2\arduino\main.ino`中预设好的`CORRECTING_VAL`进行校准（0对应DAC模块的0V，4096对应DAC模块的5V），注意校准命令只在暂停状态下生效

效果展示：
![Sample](https://github.com/riverback/2022Spring-PBL2-Spectrograph/blob/main/images/sample.png)