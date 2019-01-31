0.修改config.py 29行，修改为自己的微小宝账号密码。 

1. 执行程序
先执行python wxb.py 0 生成原生json文本f.txt
再执行python wxb.py 1 转成csv wxb.csv

2. 如果要后台执行（关闭shell后能继续执行）,以nohup方式运行
nohup python -u wxb.py > wxb.log &
