# st-sdk

提供给Strategy Module使用的python sdk。

## 设计架构

1. utils：是最底层的一些封装，对于http，websocket做一些集成性的封装，包括intercept之类的拦截器实现。
2. api: 基于封装的request代码，对接oms，dms对应的接口和websocket封装
3. model：设计strategy module，order manager，position manager等对策略曝光的最上层模块
4. config：一些常用的配置项
5. common：主要存放constant和error等常量
6. test：python测试文件目录

## 开发配置

st-sdk使用poetry作为核心的包管理工具，工具地址：https://python-poetry.org/。直接抛弃了pip的方式开发，把包版本控制&发版都简单收敛到一个工具和命令行中。

## 开发流程

- 执行test demo,我们通过下面的命令行，可以执行test的python代码，其他的和python代码使用没有任何区别

```
poetry run python stsdk/test/st_demo_1.py
```

## 设计细节

### cache设计

每一个key会对应一个map，map中的cache是用户订阅参数产生的topic，然后创建出来的自定义数据。

举个例子：
1. BBO MAP数据：是一个以bbo_cache作为key的map。

当我们订阅一个topic: BBO.EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED的数据，那么这个时候这个topic就是新的map的一个key，这个里面会存放最近10条数据(默认配置10条数据)


## 指令设计

- 仅支持placeOrder和cancelOrder两个指令