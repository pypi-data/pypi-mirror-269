import enum
import traceback
import redis
import types
import pika
import time
import pickle
import os
import copy
from dotenv import find_dotenv, load_dotenv
from typing import Callable
from peewee import SqliteDatabase, Model, CharField

from huojiweiguoba import lbw_datetime

env_path = find_dotenv(os.path.join(os.path.expanduser('~'), '.huojiweiguoba'))
assert env_path, "Not found .huojiweiguoba file"
load_dotenv(env_path)
assert os.getenv('RABBITMQ_HOST'), "RABBITMQ_HOST is None"
assert os.getenv('RABBITMQ_U'), "RABBITMQ_U is None"
assert os.getenv('RABBITMQ_P'), "RABBITMQ_P is None"
assert os.getenv('RABBITMQ_PORT'), "RABBITMQ_PORT is None"
assert os.getenv('RABBITMQ_QUEUENAME'), "RABBITMQ_QUEUENAME is None"
assert os.getenv('REDIS_HOST'), "REDIS_HOST is None"
assert os.getenv('REDIS_PORT'), "REDIS_PORT is None"
assert os.getenv('REDIS_PASSWORD'), "REDIS_PASSWORD is None"
assert os.getenv('REDIS_DB'), "REDIS_DB is None"

MAX_BODY_SIZE = 200 * 1024 * 1024

class RedisClient:
    pscript_key = "pscript"

    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            password=os.getenv('REDIS_PASSWORD'),
            db=os.getenv('REDIS_DB'),
            max_connections=300,
            decode_responses=True)
        self.client = redis.Redis(
            connection_pool=self.pool,
            decode_responses=True,
            socket_connect_timeout=5
        )

    def lpush(self, value):
        if not isinstance(value, str):
            value = pickle.dumps(value)
        self.client.lpush(self.pscript_key, value)

    def __alldata__(self):
        return self.client.lrange(self.pscript_key, 0, -1)

rds = RedisClient()


class ResultFormat(enum.Enum):
    basic = "基本格式"
    listing = "上新格式"


class ScriptType(enum.Enum):
    single = "单件装"
    multiple = "多件装"
    buyershow = "买家秀"


class PsdTask:

    def __init__(self, uname, name, stamp_items, template_items, script_type: ScriptType,
                 result_format: ResultFormat, is_random=False, random_num=10):
        self.script_type = script_type  # 脚本类型
        self.stamp_items = stamp_items  # 印花
        self.template_items = template_items  # 模板
        self.upload_time = lbw_datetime.get_local_now_date()  # 上传时间
        self.end_time = None  # 结束时间
        self.cost_time = None  # 耗时
        self.result_format: ResultFormat = result_format  # 结果格式
        self.is_random = is_random  # 是否随机组数
        self.random_num = random_num  # 随机组数
        self.uname = uname  # 提起人
        self.cache_path = None  # 缓存地址
        self.run_result = None  # 运行结果

    @property
    def __idata__(self):
        result = {}
        result['script_type'] = self.script_type.value
        result['stamp_items'] = self.stamp_items
        result['template_items'] = self.template_items
        result['upload_time'] = self.upload_time
        result['end_time'] = self.end_time
        result['cost_time'] = self.cost_time
        result['result_format'] = self.result_format.value
        result['is_random'] = self.is_random
        result['random_num'] = self.random_num
        result['uname'] = self.uname
        result['cache_path'] = self.cache_path
        result['run_result'] = self.run_result
        return result


class RabbitMQ:
    def __init__(self, exchange):
        self.host = os.getenv('RABBITMQ_HOST')
        self.port = os.getenv('RABBITMQ_PORT')
        self.user = os.getenv('RABBITMQ_U')
        self.password = os.getenv('RABBITMQ_P')
        self.queue_name = os.getenv('RABBITMQ_QUEUENAME')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=pika.PlainCredentials(self.user, self.password),
                client_properties={'connection_name': exchange},
                heartbeat=0
            )
        )
        self.channel = self.connection.channel()
        self.exchange = exchange

    def bind_queue(self):
        '''绑定队列'''
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def get_queue_info(self):
        '''获取队列信息'''
        result = []
        for method_frame, header_frame, body in self.channel.consume(self.queue_name, inactivity_timeout=3):
            if not body:
                break
            result.append(pickle.loads(body).__idata__)
        return result

    def bind_exchange(self):
        '''绑定交换机'''
        self.channel.exchange_declare(
            exchange="1号伞兵卢本伟",
            exchange_type='direct',
            durable=True
        )
        self.channel.queue_bind(
            exchange="1号伞兵卢本伟",
            queue=self.queue_name
        )

    def publish(self, data: PsdTask):
        '''生产者'''
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        data = pickle.dumps(data)
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=data,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print("任务已发送")
        self.connection.close()

    def consume(self, func: Callable, **kwargs):
        '''消费者'''
        assert callable(func), f"Type of method_callback {type(func)} is not types.MethodType"

        def callback(ch, method, properties, body):
            '''
            收到消息的回调函数
            :param ch: ch代表信道
            :param method: method代表信道的方法
            :param properties: properties代表信道的属性
            :param body: body代表信道的内容
            :return:
            '''
            try:
                assert len(body) <= MAX_BODY_SIZE, "消息体大小超过限制"
                body = pickle.loads(body)
                assert isinstance(body, PsdTask), "body is not PsdTask..."
                new_body = func(body, **kwargs)
                rds.lpush(new_body)
                print("run_result", new_body)
            except Exception as e:
                body.run_result = [str(e)]
                body = pickle.loads(body)
                rds.lpush(body)
                traceback.print_exc()
                print("失败持久化 : " + str(e))
            finally:
                # 手动标记消息已接收并处理完毕，RabbitMQ可以从queue中移除该条消息
                ch.basic_ack(delivery_tag=method.delivery_tag)

        self.bind_queue()
        self.bind_exchange()
        self.channel.basic_qos(prefetch_count=1)  # prefetch_count=1 表示每次只接收一个
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback,
            auto_ack=False  # auto_ack代表是否自动确认
        )
        print("等待任务处理中...")
        self.channel.start_consuming()
