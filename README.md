# TubeReSave
中转 youtube ，支持下载与播放 

## TubeReSave 使用步骤 

### 克隆仓库

```
$ git clone https://github.com/chenli118/TubeReSave.git
$ cd TubeReSave
```
### 创建 & 激活虚拟环境 & 安装依赖包

（下面两种方式二选一）：

Option 1 使用 venv/virtualenv + pip：
```
$ python -m venv env  # Python 2 使用 virtualenv env 命令
$ source env/bin/activate  # Windows 使用 env\Scripts\activate 命令
$ pip install -r requirements.txt
```

对于上面的第一条命令，如果你在 Linux 或 macOS 上使用 Python 3，则使用 `python3 -m venv env`。

Option 2 使用 Pipenv：
```
$ pipenv install --dev
$ pipenv shell
```
如果你还没有安装Pipenv，那么可以在运行`pipenv`命令前通过pip安装（`pip install pipenv`）。

### 运行示例程序 

$ flask initdb --drop  
$ flask run  
```
现在使用浏览器打开http://localhost:5000
```
### 静态ip+80端口方式运行示例程序

$ flask initdb --drop  
$ flask run --host=0.0.0.0 --port=80 
```
现在使用浏览器打开 http://ip
``` 

## License

该项目可自由使用


