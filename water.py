import RPi.GPIO as GPIO
import time

# 設定GPIO模式
GPIO.setmode(GPIO.BCM)

# 繼電器引腳
water_pin = 17
sensor_pin = 10  # 水流量傳感器連接的GPIO腳位（BCM模式下的GPIO 10）
flow_frequency = 0  # 計數水流量傳感器的脈衝頻率
flow_rate = 0  # 以升/小時為單位的流速

# 設置引腳為輸出模式
GPIO.setup(water_pin, GPIO.OUT)

# 設定GPIO
GPIO.setmode(GPIO.BCM)  # 設置GPIO編號模式為BCM
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 設置sensor_pin為輸入模式，並啟用上拉電阻

# 添加中斷檢測
GPIO.add_event_detect(sensor_pin, GPIO.RISING, callback=flow_callback)  # 當檢測到上升沿時調用flow_callback函數

# 初始化時間變數
current_time = time.time()  # 當前時間
loop_time = current_time  # 上一次循環的時間

# 中斷處理函數
def flow_callback(channel):
    global flow_frequency
    flow_frequency += 1  # 每次檢測到上升沿時增加計數
    
# 打開繼電器
def water_on():
    GPIO.output(water_pin, GPIO.LOW)  # 取決於繼電器模組，某些模組可能需要設置為HIGH

# 關閉繼電器
def water_off():
    GPIO.output(water_pin, GPIO.HIGH)  # 取決於繼電器模組，某些模組可能需要設置為LOW

try:
    while True:
        current_time = time.time()  # 獲取當前時間
        if current_time >= (loop_time + 1):
            loop_time = current_time  # 更新循環時間
            # 脈衝頻率 (Hz) = 4.8Q，Q 是以 L/min 為單位的流速
            flow_rate = (flow_frequency * 60 / 4.8)  # (脈衝頻率 x 60 分鐘) / 4.8Q = 流速（以 L/hour 為單位）
            flow_frequency = 0  # 重置計數器
            print(f"{flow_rate:.2f} L/hour")  # 打印升/小時
        time.sleep(0.1)  # 每0.1秒休眠一次，減少CPU佔用
        print("噴水")
        water_on()
        time.sleep(5)  # 繼電器保持打開5秒
        if flow_rate >= 50:
            print("停水")
            water_off()

except KeyboardInterrupt:
    print("程式終止")

finally:
    GPIO.cleanup()  # 清理GPIO設置
