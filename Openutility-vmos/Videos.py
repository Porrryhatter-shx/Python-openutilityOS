import time
from threading import Thread
try:
    import cv2
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
class OpenCVVideoPlayer:
    def __init__(self, video_source=0, window_name="OpenCV Video Player"):
        """
        初始化视频播放器
        
        参数:
            video_source: 视频源(可以是摄像头索引、视频文件路径)
            window_name: 显示窗口的名称
        """
        self.video_source = video_source
        self.window_name = window_name
        self.cap = None
        self.playing = False
        self.current_frame = None
        self.fps = 0
        self.frame_count = 0
        self.duration = 0
        self.width = 0
        self.height = 0
        
    def open(self):
        """打开视频源"""
        self.cap = cv2.VideoCapture(self.video_source)
        if not self.cap.isOpened():
            raise ValueError("无法打开视频源: " + str(self.video_source))
            
        # 获取视频属性
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if self.fps > 0:
            self.duration = self.frame_count / self.fps
            
    def close(self):
        """关闭视频源"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        cv2.destroyAllWindows()
        
    def play(self):
        """开始播放视频"""
        if not self.cap or not self.cap.isOpened():
            self.open()
            
        self.playing = True
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        
        # 计算帧间延迟以保持正确播放速度
        delay = int(1000 / self.fps) if self.fps > 0 else 1
        
        while self.playing:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            self.current_frame = frame
            cv2.imshow(self.window_name, frame)
            
            # 检查用户是否按下了ESC键
            key = cv2.waitKey(delay) & 0xFF
            if key == 27:  # ESC键
                self.stop()
                break
                
        self.close()
        
    def stop(self):
        """停止播放"""
        self.playing = False
        
    def play_async(self):
        """异步播放视频(在新线程中)"""
        self.thread = Thread(target=self.play)
        self.thread.start()
        
    def get_current_frame(self):
        """获取当前帧"""
        return self.current_frame
        
    def get_video_info(self):
        """获取视频信息"""
        return {
            "width": self.width,
            "height": self.height,
            "fps": self.fps,
            "frame_count": self.frame_count,
            "duration": self.duration
        }

if __name__ == "__main__":
    #使用摄像头
    #player = OpenCVVideoPlayer(0)
    
    #使用视频文件
    player = OpenCVVideoPlayer("example.mp4")
    
    try:
        #同步播放
        player.play()        
        #或者异步播放
        #player.play_async()
        #while player.playing:
        #    time.sleep(0.1)
    finally:
        player.close()