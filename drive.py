"""
GPIO drive
"""
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)


def delay_microsecond(delay_time):  # 微秒级延时函数
    start, end = 0, 0  # 声明变量
    start = time.time()  # 记录开始时间
    delay_time = (delay_time - 3) / 1000000  # 将输入t的单位转换为秒，-3是时间补偿
    while end - start < delay_time:  # 循环至时间差值大于或等于设定值时
        end = time.time()


class ConnectError(Exception):
    def __init__(self, info):
        print(info)


class DHT22:
    def __init__(self):
        self.data = []
        self.channel = 22

    def start(self):
        GPIO.setup(self.channel, GPIO.OUT)
        GPIO.output(self.channel, GPIO.LOW)
        delay_microsecond(1 * 1000)  # 延时20毫秒
        GPIO.output(self.channel, GPIO.HIGH)  # 设置GPIO输出高电平
        delay_microsecond(30)
        GPIO.setup(self.channel, GPIO.IN)
        delay_microsecond(40)
        if GPIO.input(self.channel):
            raise ConnectError('answer is wrong')
        delay_microsecond(80)
        if not GPIO.input(self.channel):
            raise ConnectError('answer is wrong')
        delay_microsecond(40)
        return True

    def get(self):
        tmp = []
        for i in range(40):  # 循环40次，接收温湿度数据
            a = time.time()
            while GPIO.input(self.channel) == 0:  # 一直循环至输入为高电平
                b = time.time()
                if (b - a) > 0.1:
                    break

            delay_microsecond(28)  # 延时28微秒

            if GPIO.input(self.channel):  # 超过28微秒后判断是否还处于高电平
                tmp.append(1)  # 记录接收到的bit为1

                a = time.time()
                while GPIO.input(self.channel):  # 一直循环至输入为低电平
                    b = time.time()
                    if (b - a) > 0.1:
                        break
            else:
                tmp.append(0)  # 记录接收到的bit为0
        return tmp

    def response(self):
        pass

    def check(self):
        pass
