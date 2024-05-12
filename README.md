# Blue Archive Auto Rhythm Game (BAARG)

### A Python-based program for real-time recognition and automatic operation of the Blue Archive in a Rhythm mini-game.

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/shadlc/Blue-Archive-Auto-Rhythm-Game)
![GitHub - License](https://img.shields.io/github/license/shadlc/Blue-Archive-Auto-Rhythm-Game)
![platform](https://img.shields.io/badge/platform-windows11-blue)
![GitHub last commit](https://img.shields.io/github/last-commit/shadlc/Blue-Archive-Auto-Rhythm-Game)


## 💬 简介
**这是一个基于Python的蔚蓝档案音游实时识别并自动操作的小程序，适用于WSA，即[适用于Android™️ 的Windows 子系统](https://learn.microsoft.com/zh-cn/windows/android/wsa/)(∠·ω< )⌒☆**

## ✨ 主要功能
**在蔚蓝档案的音游中实时读谱，自动执行，实现Full Perfect**

## 📸 演示视频
**[Bilibili夏日音游](https://www.bilibili.com/video/BV1SC4y1M77F)**
**[Bilibili初音音游](https://www.bilibili.com/video/BV1Uz421m7pm)**

## 📝 使用指南
- 为了保证每个音符的分离与丝滑，需要设置音符速度最快(7倍)、最小
- 活动已经结束力，没啥使用价值了，代码学习参考吧
- 安装 python3.11，以及Python虚拟环境工具pipenv
- 执行 `pipenv install`
- 执行 `pipenv run app.py`

## 💡 实现记录
- 夏日音游命中效果和溅起来的水花太大了，初音光效影响颜色严重，必须在较远的地方检测再点击才可以不被干扰，还得小心100Combo的全屏光环
- 鼠标点击无法实现多点触控，且音游内不支持鼠标点击，因此采用Win32API模拟触控实现
- Pillow库的截屏较慢，无法实现稳定的在一帧的时间(即0.018s)内识别，因此实时识别使用了[mss](https://github.com/BoboTiG/python-mss)库，它调用了Win32API，且可以进行局部截屏
- 使用Win32API截屏速度虽快，但是图像数据需进行色彩空间的转化导致失真，因此采用手动补录颜色列表的方式逐步将识别率提高到100%
- 实时识别挺吃帧数稳定性，尽量不要太高分辨率，测试使用分辨率为720P
- 本项目仅供学习参考

## 🔒️ 许可协议
- 本项目在遵循 [**GNU GENERAL PUBLIC LICENSE v3.0**](https://www.gnu.org/licenses/gpl-3.0.html) 许可协议下进行发布

## 🏆 特别鸣谢
- 感谢`jonas-hurst` 提供的项目[touchcontrol](https://github.com/jonas-hurst/touchcontrol)为Win32API模拟触控实现省下了大量时间