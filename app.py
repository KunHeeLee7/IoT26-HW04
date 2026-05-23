'''

Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson

Modified by Rui Santos
Complete project details: https://randomnerdtutorials.com

Updated for Raspberry Pi OS Bookworm using gpiozero by Gemini (2026)

'''

from flask import Flask, render_template, request
from gpiozero import LED

app = Flask(__name__)

# gpiozero의 LED 객체를 사용해 핀을 제어합니다. (출력용 핀은 LED 객체로 매핑하면 편리합니다)
# 처음 생성할 때 기본값으로 핀은 꺼진 상태(Low)가 됩니다.
pins = {
   23 : {'name' : 'GPIO 23', 'device' : LED(23)},
   24 : {'name' : 'GPIO 24', 'device' : LED(24)}
}

@app.route("/")
def main():
   # 각 핀의 현재 상태(켜짐: 1, 꺼짐: 0)를 템플릿에 보낼 구조로 가공합니다.
   template_pins = {}
   for pin_num, pin_info in pins.items():
      template_pins[pin_num] = {
         'name': pin_info['name'],
         'state': pin_info['device'].value  # .value는 켜져 있으면 1, 꺼져 있으면 0을 반환합니다.
      }
      
   templateData = {
      'pins' : template_pins
   }
   return render_template('main.html', **templateData)

@app.route("/<changePin>/<action>")
def action(changePin, action):
   changePin = int(changePin)
   deviceName = pins[changePin]['name']
   device = pins[changePin]['device']
   
   # action 값에 따라 온/오프 제어
   if action == "on":
      device.on()  # 핀 HIGH
      message = "Turned " + deviceName + " on."
   elif action == "off":
      device.off() # 핀 LOW
      message = "Turned " + deviceName + " off."

   # 변경된 상태를 다시 읽어서 템플릿용 딕셔너리 생성
   template_pins = {}
   for pin_num, pin_info in pins.items():
      template_pins[pin_num] = {
         'name': pin_info['name'],
         'state': pin_info['device'].value
      }

   templateData = {
      'pins' : template_pins
   }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
   # 포트 80은 권한이 필요하므로 실행 시 그대로 sudo python app.py 로 실행하시면 됩니다.
   app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)
