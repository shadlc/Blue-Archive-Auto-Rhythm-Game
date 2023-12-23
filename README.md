# Blue Archive Auto Rhythm Game (BAARG)

### A Python-based program for real-time recognition and automatic operation of the Blue Archive in a Rhythm mini-game.

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/shadlc/Blue-Archive-Auto-Rhythm-Game)
![GitHub - License](https://img.shields.io/github/license/shadlc/Blue-Archive-Auto-Rhythm-Game)
![platform](https://img.shields.io/badge/platform-windows11-blue)
![GitHub last commit](https://img.shields.io/github/last-commit/shadlc/Blue-Archive-Auto-Rhythm-Game)

## 💬 简介
**这是一个基于Python的蔚蓝档案音游实时识别并自动操作的小程序，适用于WSA，即[适用于Android™️ 的Windows 子系统](https://learn.microsoft.com/zh-cn/windows/android/wsa/)，不想基于其他第三方模拟器(∠·ω< )⌒☆**

## ✨ 主要功能
**在蔚蓝档案的音游中实时读谱，自动执行，实现Full Combo，初音联动音未来可期**

## 📸 演示视频
**~~待补充~~**

## 📝 使用指南
- 为了保证每个音符的分离与丝滑，需要设置音符速度最快(7倍)、最小
- 活动已经结束力，没啥使用价值了，代码学习参考吧
- 安装 python3.11，以及Python虚拟环境工具pipenv
- 执行 `pipenv install`
- 执行 `pipenv run app.py`

## 💡 实现记录
- 音游命中效果和溅起来的水花也太大啦，必须在较远的地方检测再点击才可以不被干扰，还得小心100Combo的全屏光环
- 鼠标点击无法实现多点触控，且BA其他地方支持鼠标点击，而音游内不支持(令人摸不着头脑)，因此采用Win32API模拟触控实现
- Pillow库的截屏太慢了，无法实现稳定的在一帧的时间(即0.018s)内识别，因此实时识别使用了[mss](https://github.com/BoboTiG/python-mss)库，因为它截屏调用了Win32API，且可以进行局部截屏
- 虽然使用Win32API截屏速度快，但是图像数据转换的时候似乎会失真，因此采用手动补录颜色列表的方式逐步将识别率提高到100%
- 实时识别应该挺吃帧数稳定的，尽量不要太高分辨率，测试使用分辨率为720P
- 总之，Win32API的模拟触控是个大坑

## 🔒️ 许可协议
- 本项目在遵循 [**GNU GENERAL PUBLIC LICENSE v3.0**](https://www.gnu.org/licenses/gpl-3.0.html) 许可协议下进行发布

## 🏆 特别鸣谢
- 感谢`jonas-hurst` 提供的项目[touchcontrol](https://github.com/jonas-hurst/touchcontrol)令我省去了一番与Win32API搏斗的时间