# -*- coding: utf-8 -*-

#from _typeshed import Self

from .pypack.fylo.controlserver import Controlserver, ConnectType

class UserApi:
	def __init__(self):
		self._control_server = Controlserver()

#=============================================System Config======================================================================#

	def connect(self, server_ip = None):
		'''
			描述:
			上位机作为服务器,
			参数:
			选填:server_ip: 无人机IPv4地址 不填自动获取
			返回值:
			True:成功 False:失败
		'''
		return self._control_server.connect(server_ip)

	# scratch
	def single_fly_takeoff(self):
		'''
			描述:
			实时控制无人机起飞
     	'''
		return	self._control_server.single_fly_takeoff()
	
	def single_fly_touchdown(self):
		'''
			描述:
			实时控制无人机降落
		'''
		return self._control_server.single_fly_touchdown()
	
	def single_fly_forward(self, distance):
		'''
			描述:
			实时控制无人机向前飞
			参数:
			distance:飞行距离（厘米）
		'''
		self._control_server.single_fly_forward(distance)
	
	def single_fly_back(self, distance):
		'''
			描述:
			实时控制无人机向后飞
			参数:
			distance:飞行距离（厘米）
		'''
		self._control_server.single_fly_back( distance)
	
	def single_fly_left(self,  distance):
		'''
			描述:
			实时控制无人机向左飞
			参数:
			distance:飞行距离（厘米）
		'''
		self._control_server.single_fly_left( distance)
	
	def single_fly_right(self, distance):
		'''
			描述:
			实时控制无人机向右飞
			参数:
			distance:飞行距离（厘米）
		'''
		self._control_server.single_fly_right( distance)

	def single_fly_up(self,  height):
		'''
			描述:
			实时控制无人机向上飞
			参数:
			distance:飞行高度（厘米）
		'''
		self._control_server.single_fly_up(height)
		
	def single_fly_down(self, height):
		'''
			描述:
			实时控制无人机向下飞
			参数:
			distance:飞行高度（厘米）
		'''
		self._control_server.single_fly_down( height)
		
	def single_fly_turnleft(self, angle):
		'''
			描述:
			实时控制无人机向左转
			参数:
			distance:旋转角度（度）
		'''
		self._control_server.single_fly_turnleft( angle)
		
	def single_fly_turnright(self,  angle):
		'''
			描述:
			实时控制无人机向右转
			参数:
			distance:旋转角度（度）
		'''
		self._control_server.single_fly_turnright(-angle)

	def single_fly_bounce(self, frequency, height):
		'''
			描述:
			实时控制无人机跳起
			参数:
			frequency:弹跳次数
			distance:弹跳距离（厘米）
		'''
		self._control_server.single_fly_bounce(frequency, height)

	def single_fly_straight_flight(self, x, y, z):
		'''
			描述:
			直线飞行(x,y,z)
			参数:
			x:坐标x（厘米）
			y:坐标y（厘米）
			z:坐标z（厘米）
		'''
		self._control_server.single_fly_straight_flight( x, y, z)

	def single_fly_radius_around(self, radius):
		'''
			描述:
			半径环绕飞行
			参数:
			radius：环绕半径(厘米，正：逆时针 负：顺时针)
		'''
		return self._control_server.single_fly_radius_around(radius)
	def single_fly_autogyration360(self,num):
		'''
			描述:
			顺时针、逆时针自转一定圈数
			参数:
			num:(正：逆时针 负：顺时针)
		'''
		return self._control_server.single_fly_autogyration360(num)
	def	single_fly_somersault(self, direction):
		'''
			描述:
			无人机原地向上下前后左右翻滚
			参数:
			   DIRECTION_FORWARD=0, /* forward. | */
                DIRECTION_BACK=1, /* back. | */
                DIRECTION_LEFT=2, /* left. | */
                DIRECTION_RIGHT=3, /* right. | */
                DIRECTION_DOWN=4, /* down. | */
                DIRECTION_UP=5, /* up. | */
		'''
		return self._control_server.single_fly_somersault(direction)
	def single_fly_curvilinearFlight(self, x, y, z):
		'''
			描述:
			曲线飞行(x,y,z)
			参数:
			x：x轴坐标（厘米）（机体左右，右为正）
			y：y轴坐标（厘米）（机体前后，前为正）
			z：z轴坐标（厘米）（机体上下，上为正）
		'''
		return self._control_server.single_fly_curvilinearFlight(x, y, z)
	
	def single_fly_hover_flight(self, time):
		'''
			描述:
			无人机悬停
			参数:
			time:悬停时间（秒）
		'''
		return self._control_server.single_fly_hover_flight(time)
	
	def single_fly_barrier_aircraft(self, mode ):
		'''
			描述:
			开启避障
			参数:
			mode:True:开启 False:关闭
		'''
		return self._control_server.single_fly_barrier_aircraft(mode)
	
	def single_fly_Line_walking(self,fun_id, dist, tv, way_color):
		'''
			描述:
			巡线检测
			参数:
			fun_id  = 0  //0:向前巡线，无视路口；1：向前巡线，遇到路口结束巡线；2：在路口悬停；3：在轨道上悬停； 10：退出巡线； 现在只有向前巡线
			dist          //距离，单位cm
			tv            //巡线时间，单位s
			way_color   //巡线颜色色域，0-黑色 255-白色
			返回:
			return result = 1; //指令执行的结果：0-失败，1-成功 2-成功遇到路口

		'''	
		return self._control_server.single_fly_Line_walking(fun_id, dist, tv, way_color)
	def single_fly_AiIdentifies(self,mode):
		'''
			描述:
			识别标签
			参数:
			mode:0-9识别0-9的数字标签，10识别左箭头，11识别右箭头，12识别上箭头，13识别下箭头，20结束任务，65-90大写字母A-Z；触发识别后识别过程持续300ms，如果识别成功就立马结束
			返回:
			float x;标签卡与无人机的X坐标
			floag y;标卡与无人机的Y坐标
			float z;标卡与无人机的Z坐标
			float angle;标卡与无人机的角度
			result；//0 识别失败， 1识别成功

		'''
		return self._control_server.single_fly_AiIdentifies(mode)
	

	def single_fly_Qrcode_align(self, mode, qr_id):
		'''
			描述:
			光流、前摄对齐二维码
			参数:
			qr_id; 到二维码id[0-9]，
	        mode:  mode = 0 光流对齐二维码，mode = 1 前摄对齐二维码 
			返回:
			result；//False 识别失败， True识别成功

		'''
		if mode == 0:
			return self._control_server.single_fly_Qrcode_align(1, 5, 0, qr_id)
		return self._control_server.single_fly_Qrcode_tracking(qr_id, 3, 0)
	
	
	def single_fly_recognition_Qrcode(self, mode, qr_id):
		'''
			描述:
			光流、前摄识别二维码
			参数:
            qr_id; 到二维码id[0-9]，
	        mode:  mode = 0 光流识别二维码，mode = 1 前摄识别二维码 
			返回:
			{
			result；//False 识别失败， True识别成功
			x;//无人机与二维码之间的距离
			y;//无人机与二维码之间的距离
			z;//无人机与二维码之间的距离
			yaw;//无人机与二维码之间的角度
			qr_id;//识别到二维码的id
			}
		'''
		if mode == 0:
			return self._control_server.single_fly_Qrcode_align(2, 0, 0, qr_id)
		return self._control_server.single_fly_Qrcode_tracking(qr_id, 2, 0)
	
	def single_fly_track_Qrcode(self, qr_id, time):
		'''
			描述:
			追踪[0-9]号二维码[time]秒
			参数:
		    qr_id:二维码id
		    time:追踪时间
			返回:
			result：0:成功，1:失败

		'''

		return self._control_server.single_fly_Qrcode_tracking(qr_id, 1, time)
	
	def single_fly_getColor(self, Mode = 1):
		'''
			描述:
			颜色识别，获取当前视频流一帧的颜色
			参数:
		    Mode:1开始,跑一帧
			返回:
			r,g,b:色域
            state:0失败 1成功

		'''
		return self._control_server.single_fly_getColor(Mode)
	#灯光
	def	single_fly_lamplight(self, r, g, b, time, mode):
		'''
			描述:
			设置灯光颜色和模式
			不会阻塞主线程
			参数:
		    r,g,b:色域
		    time: 灯光时长/s
		    mode: 12/开灯,13/关灯,16/开启七色RGB闪烁,17/关闭七色RGB闪烁,18/开启流水灯,19/关闭流水灯
			返回:
			True:执行成功
			False:执行失败

		'''
		return	self._control_server.single_fly_lamplight( r, g, b, time, mode)
	
	#8.Linux端业务控制指令
	def Plane_fly_line_walking(self):
        
		return self._control_server.Plane_Linux_cmd(7, 1, type, 0, 0)
	
	def plane_fly_generating(self, type, data ,reserve):
		'''
			描述:
			发射激光
			参数:
			type = 0;  // 激光: 0-单发,1-连发，2-开启激光接收，3-关闭激光接收 4-一直连发无弹量 5-关闭发射 6-认证测试
			data = 10; // 激光连发频率，次/秒，范围1-14
			reserve = 100 //弹量,数据范围1-255   
		'''
		return self._control_server.Plane_Linux_cmd(7 ,1 , type, data, reserve)

	def Plane_fly_take_photo(self):
		'''
			描述:
			拍照,必须开启视频流后调用
			参数:
		'''
		return self._control_server.Plane_Linux_cmd(5 ,1 ,0 ,1 ,0)
	def Plane_cmd_swith_rtp(self,type):
		'''
			描述:
			开启视频流
			参数:
			type:0-开启，1-关闭
		'''
		return self._control_server.Plane_Linux_cmd(9, 1, type, 0, 0)
	
	
	def single_fly_flip_rtp(self):
		'''
			描述:
			打开视频流(调用前需开启视频流)
			参数:
			
		'''
		self._control_server.single_fly_flip_rtp()
	def	Plane_cmd_camera_angle(self, type, data):
		'''
			描述:
			设置主摄俯仰角度
			参数:
			type = 0;  // 转动的方向: 0-上,1-下(绝对),2和3算法控制，4-校准，5-积木上，6-积木下（相对）
			data = 30; // 转动的角度: 0~90	
		'''
		return self._control_server.Plane_Linux_cmd(8, 1, type, data, 0)
	
	


#=================================================Plane Control===================================================================#
		
	def plane_led_on(self, plane_id_start, plane_id_end):
		'''
			描述:
			无人机开灯
			参数:
			plane_id_start:起始无人机编号
			plane_id_end:结束无人机编号
		'''
		self._control_server.plane_led_on(plane_id_start, plane_id_end)
		
	def plane_led_off(self, plane_id):
		'''
			描述:
			无人机关灯
			参数:
			plane_id_start:起始无人机编号
			plane_id_end:结束无人机编号
		'''
		return self._control_server.plane_led_off(plane_id)

	def plane_fly_arm(self):
		'''
			描述:
			低速转动螺旋桨
			参数:
		
		'''
		return self._control_server.plane_fly_arm()

	def plane_fly_disarm(self):
		'''
			描述:
			停止低速转动螺旋桨
			参数:
	
		'''
		return self._control_server.plane_fly_disarm()


		
	def Plane_getBarrier(self):
		'''
			描述:
			获取避障信息
			参数:
			
			返回: 字典 每个方向的障碍物状态，True:有障碍物，False:无障碍物
			{
            'forward': True
            'back': True,
            'left': True,
            'right': True,   
            }
		'''
		return self._control_server.Plane_getBarrier()
	def get_battery(self):
		'''
			描述:
			获取无人机电量百分比
			参数:
			plane_id:无人机编号
			返回值:
			整数:电量百分比
		'''
		return self._control_server.get_battery()
		
	def get_coordinate(self):
		'''
			描述:
			获取无人机坐标(x,y,z)
			参数:
	
			返回值:
			(x, y, z)
		'''
		return self._control_server.get_coordinate()
		
	def get_yaw(self):
		'''
			描述:
			获取无人机偏航角（度）
			参数:
			plane_id:无人机编号
			返回值:
			整数:偏航角
		'''
		return self._control_server.get_yaw()
		

	
	def get_timesync(self):
		'''
			描述:
			判断无人机是否同步时间成功
			参数:
			plane_id:无人机编号
			返回值:
			True:成功 False:不成功
		'''
		return self._control_server.get_timesync()
	


	def get_ip(self, plane_id):
		'''
			描述:
			取ip地址
			参数:
			plane_id:无人机编号
			返回值:
			True:一致 False:不一致
		'''
		return self._control_server.get_ip(plane_id)
	



################################################