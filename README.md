# Cmder

这是一款命令行模式下运行的命令生成框架。目标是帮助渗透测试人员快速生成测试命令。并且记录所选择的参数，方便下次使用。

# 特色

- 自定义的命令语法，可以快速添加自定义的命令。
- 自动记录上一次输入结果，并显示在推荐中
- 手动定义推荐变量
- 划分工作区
- 多行命令合并

# 安装方法

```
git clone https://github.com/Elinpf/cmder
cd cmder
python3 setup.py install --user
```


# 使用方法

```
usage: cmder [-h] {show,search,info,use,workspace} ...

Generate a pentesting command

positional arguments:
  {show,search,info,use,workspace}
                        sub-command help
    show                show the latest table
    search              Search tools in the database
    info                show command information
    use                 use command
    workspace           workspace config

optional arguments:
  -h, --help            show this help message and exit
```

# 自定义命令

运行后会创建`~/.cmder`目录，其中`db`是用户可以自定义添加的命令文件，可以自行添加目录或者按照软件中的目录路径添加命令文件。

命令文件语法请参考[这里](https://github.com/Elinpf/cmder/blob/master/db/readme.md)。

# 灵感来源与命令来源

这个项目的灵感来源于[shellerator](https://github.com/ShutdownRepo/shellerator), 一些命令来源于以下链接：

- https://github.com/ShutdownRepo/shellerator
- https://book.hacktricks.xyz/
- https://www.ired.team/offensive-security-experiments/offensive-security-cheetsheets