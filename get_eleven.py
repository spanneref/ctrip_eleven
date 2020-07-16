# coding:utf-8
import execjs
import time
import requests
from ws4py.client.threadedclient import WebSocketClient
import Queue
import threading
# import redis




class CTRIP_WSClient(WebSocketClient):
	"""定义一个类负责连接websocket，发送oceanball.js代码给websocket服务器，
	服务器再转发到页面的tampermonkey"""

	instance = None

	def __new__(cls, *args):
		if cls.instance is None:
			obj = super(CTRIP_WSClient, cls).__new__(cls, *args)

			obj.result_queue = Queue.Queue()
			# obj.redis = StrictRedis(host='localhost', port=6379)

			cls.instance = obj

		return cls.instance


	def opened(self):
		"""连接时触发的函数"""
		self.send('Python')

	def closed(self, code, reason=None):
		"""关闭时触发"""
		print("Closed down:", code, reason)

	def received_message(self, resp):
		"""接收到数据时触发"""
		# print("resp", resp.data)
		self.result_queue.put(resp.data)
		# self.close()

	def generate_cas(self, num):
		"""生成CAS混淆参数"""
		ctx_cas = execjs.compile("""function generateMixed(e) {
		    for (var t = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"], o = "CAS", n = 0; n < e; n++) {
		        var i = Math.ceil(51 * Math.random());
		        o += t[i]
		    }
		    return o
		}""")
		cas = ctx_cas.call('generateMixed', num)
		# print cas
		return cas

	def get_oceanball(self):

		oceanball = 'http://hotels.ctrip.com/domestic/cas/oceanball?callback={}&_={}'
		# 生成时间戳
		current_time = str(int(time.time()*1000))  # 生成13位的时间戳字符串
		# 生成cas 这里默认传入的num为15
		cas = self.generate_cas(15)
		print(cas)
		# format格式化得到完整的url
		oceanball = oceanball.format(cas, current_time)

		# return (oceanball, cas)
		headers = {
			"user-agent": "Mozilla/5.0 (darwin) AppleWebKit/537.36 (KHTML, like Gecko) jsdom/16.2.2",
			"referer": "https://hotels.ctrip.com/hotel/shanghai2",
			}

		response = requests.get(url=oceanball, headers=headers)

		code = (
		    """
		    window["%s"] = function (e) {
		    var f = e();
		    console.log(f);
		    ws.send(f);
		};;
		"""
		    % cas
		    + response.text
		)

		# print(code)
		self.send(code)

	def generate_eleven(self):
		"""得到eleven参数"""
		print('start geneleven')
		while True:
			self.get_oceanball()
			time.sleep(5)  # 换成以后的触发条件


	def get_elevn(self):
		print('start geteleven')
		while True:
			res = self.result_queue.get()
			print(res)
			# return res

	def run_forever(self):

		thread_list = list()
		# 生成CAS并请求得到oceanball.js后发送到到websocket获得eleven
		generate_eleven_thread = threading.Thread(target=self.generate_eleven)
		thread_list.append(generate_eleven_thread)
		# 从队列里取出eleven参数
		get_eleven_thread = threading.Thread(target=self.get_elevn)
		thread_list.append(get_eleven_thread)

		for t in thread_list:
			t.setDaemon(True)
			t.start()
		generate_eleven_thread.join()
		get_eleven_thread.join()


if __name__ == '__main__':
	try:
		ws = CTRIP_WSClient("ws://127.0.0.1:8014/")
		ws.connect()
		ws.run_forever()

	except KeyboardInterrupt:
		ws.close()
	except Exception as e:
		print(e)
