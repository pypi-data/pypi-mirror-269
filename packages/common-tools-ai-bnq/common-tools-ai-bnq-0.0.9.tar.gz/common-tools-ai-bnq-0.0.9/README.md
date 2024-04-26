1.NacConnect类，用于连接nacos服务，获取配置文件信息

    NacConnect类中参数信息如下：
        server_addresses: 地址
        namespace: 命名空间
        username: 用户名
        password: 密码
        group: 组合字典， 包括group_name和data_ids
        conf_type: 配置文件类型， 非必需，值为json或yaml

    示例如下：
        test_data = {
                        'group': {'t-dev': ['project_name_1', 'project_name_2']},
                        'username': 'nacos',
                        'password': 'nacos',
                        'server_addresses': '127.0.0.1:8080',
                        'namespace': 't-dev'
                    }
        conf_test = NacConnect(**test_data)
        print(conf_test())

2.LoggingRecord类，用于记录日志信息

    LoggingRecord类中参数信息如下：
        max_bytes: 日志文件最大大小， 默认值20M
        backup_count: 日志备份最大数量， 默认值为10
        log_level: 日志级别， 默认值为INFO
        log_dir: 日志文件路径，默认在根目录下创建log文件夹

    示例如下：
        testLog = LoggingRecord(log_level=logging.DEBUG)
        for i in range(10):
            print(i, 'i')
            print(testLog, "testLog")
            testLog.debug(i)
            testLog.info("中文测试")
            testLog.error(i)
            testLog.warning(i)
            testLog.exception(i)

3.SingletonMeta类，用于实现单例模式

    示例如下：
        class TestClass(metaclass=SingletonMeta):
            def __init__(self):
                pass

4.CosConnect类，用于连接腾讯云存储平台cos

    CosConnect类中参数信息如下：
        secret_id: 腾讯云secret_id
        secret_key: 腾讯云secret_key
        region: 腾讯云存储区域

    示例如下：
        test_data = {
                        'secret_id': 'AKIDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
                        'secret_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
                        'region': 'ap-guangzhou'
                    }
        cos_test = CosConnect(**test_data)
        print(cos_test())