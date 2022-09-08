# Cmder

这是一款命令行模式下运行的命令生成框架。目标是帮助渗透测试人员快速生成测试命令。并且记录所选择的参数，方便下次使用。

![Example](assert/example_2.gif)

# 特色

- 自定义的命令语法，可以快速添加自定义的命令。
- 自动记录上一次输入结果，并显示在推荐中
- 手动定义推荐变量
- 划分工作区
- 多行命令合并执行
- 可更新数据库

# 安装方法

```
pip3 install cmder-elinpf
```

安装完成后需要获取数据库[cmder_db](https://github.com/Elinpf/cmder_db)

```
cmder --update
```


# 使用方法

![](assert/app_help.png)

![](assert/app_use_help.png)

直接输入`cmder`进行查找命令，使用`cmder use <index>` 选择命令执行。


## 自定义命令

运行后会创建`~/.cmder`目录，其中`db`是用户可以自定义添加的命令文件，可以自行添加目录或者按照软件中的目录路径添加命令文件。

命令文件语法请参考[这里](https://github.com/Elinpf/cmder_db)。

## 工作区

工作区是为了方便在不同的项目中使用不同的参数环境，可以通过`cmder workspace -a <name>`添加工作区。`-c`进行切换。

![](assert/app_workspace_help.png)


## 自定义推荐

`cmder`会自动记录上一次的输入参数作为第一推荐，另外数据库中会有对相应参数的推荐，同时也可以自定义推荐，例如：

```bash
cmder workspace -s DOMAIN backdoor.htb
```

这样就添加了一个其定义参数，在后面的使用中，同一工作区内，`DOMAIN`变量就会自动推荐`backdoor.htb`。

查看所有自定义推荐：

```bash
cmder workspace -g all
```

# 灵感来源与命令来源

这个项目的灵感来源于[shellerator](https://github.com/ShutdownRepo/shellerator), 一些命令来源于以下链接：

- https://github.com/ShutdownRepo/shellerator
- https://book.hacktricks.xyz/
- https://www.ired.team/offensive-security-experiments/offensive-security-cheetsheets