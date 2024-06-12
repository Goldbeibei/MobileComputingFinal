import RPi.GPIO as GPIO
import time
# 设置 GPIO 模式为 BCM
GPIO.setmode(GPIO.BCM)

# 设置 GPIO 数据引脚
data_pin = 7 # 对应 BCM 模式下的 GPIO 4 (物理引脚 7)

# 设置 GPIO 引脚为输入模式
GPIO.setup(data_pin, GPIO.IN)

def read_soil_moisture():
    # 读取 GPIO 引脚的输入值
    value = GPIO.input(data_pin)
    
    # 将输入值转换为湿度等级
    if value == GPIO.LOW:
        return "湿润"
    else:
        return "干燥"
try:
    while True:
        # 读取土壤湿度
        soil_moisture = read_soil_moisture()
        print(f"土壤湿度: {soil_moisture}")
        # 每隔1秒读取一次
        time.sleep(1)
except KeyboardInterrupt:
    print("程序终止")
finally:
    # 清理 GPIO 设置
    GPIO.cleanup()
