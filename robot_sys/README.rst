### CentOS release 6.8 环境爬虫系统部署手册
#### 1. 安装git

    yum install git -y

#### 2. 安装pyenv

    curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
    echo 'eval "$(pyenv init -)"' >> ~/.bash_profile

#### 3. 安装Python3

    yum install readline readline-devel readline-static -y
    yum install openssl openssl-devel openssl-static -y
    yum install sqlite-devel -y
    yum install bzip2-devel bzip2-libs -y
    pyenv install 3.4.4 -v
    pyenv global 3.4.4
    
#### 4. 安装mysql

    yum install mysql -y

#### 5. 安装Redis

    yum install redis -y
    
#### 6. 安装subversion

    yum install subversion -y
    
#### 7. 安装phantomjs

    yum install freetype fontconfig -y
    wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
    bunzip2 phantomjs-2.1.1-linux-x86_64.tar.bz2
    tar xvf phantomjs-2.1.1-linux-x86_64.tar.bz2.out
    mv phantomjs-2.1.1-linux-x86_64 /usr/local/src/
    ln -sf /usr/local/src/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs
    
#### 8. 下载爬虫代码并安装依赖

    svn checkout svn://101.201.121.245/Collection
    cd Collection/robot_sys/
    pip install -r requirements.txt
    
#### 9 . 测试环境

    python run.py 0 
    如显示以下则环境OK
    <title>交叉滚珠单元【价格 型号 参数 采购 批发】-西域</title>


#### 10. 软件使用,以西域为例子

* 修改数据库地址及账户信息
  编辑config/config.py 文件 将db_url变量里对应的数据库地址,账户信息修改成新的.

* 更新ez_parity_brand 表
    
    python run.py 1

* 添加ez_parity_site 表
  
    python run.py 4

* 更新ez_parity_product 和 ez_parity_price 表
  
    python run.py 5

* 多进程更新 ez_parity_product 和 ez_parity_price 表
  
    python run.py 3

* 下载brand图片
  
    python run.py 6

* 上述方法在程序运行时会产生很多打印日志，而且程序会随着关闭shell远程链接终端而退出，建议正式使用时以如下方式进行启动：

        nohup python -u run.py xx > nohup.out &
其中nohup.out是日志文件，可通过ps aux | grep "run.py" 来看程序是否执行结束

#### 11. 手动执行商品更新

    步骤：
    1. svn checkout 最新代码
    2. 修改config 数据库路径
       将config.py中yishidong023的db_url的注释#去掉,然后把其他的db_url加上注释#.
    3. 执行对应商城的一键脚本，例如：
       ./ehsy_onekey.sh 
       ./vipmor_onekey.sh
       ./digikey_oneksy.sh
	   ./grainger_onekey.sh 
	   ./rs_onekey.sh
	   goon 续传
    4. 终止爬虫，执行对应的商城stop脚本,例如：
       ./ehsy_stop.sh 
       ./vipmor_stop.sh
       ./digikey_stop.sh

           
#### 12. 定期执行商品更新
    步骤：
    1. 将对应的一键脚本添加到crontab 任务 


