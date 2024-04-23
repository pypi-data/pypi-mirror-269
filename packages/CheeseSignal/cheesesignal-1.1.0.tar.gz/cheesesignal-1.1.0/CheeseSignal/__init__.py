from typing import List, Callable, overload, Any, TYPE_CHECKING

if TYPE_CHECKING:
    class Signal:
        ...

class Receiver:
    def __init__(self, signal: 'Signal', fn: Callable, *, expected_receive_num: int, auto_remove: bool):
        '''
        - Args

            - expected_receive_num: 期望接受信号的次数，超过该次数则不再响应信号；0为无限次。

            - auto_remove: 是否自动删除响应次数超出期望次数的接收器。
        '''

        self._signal: 'Signal' = signal
        self.fn: Callable = fn
        self._expected_receive_num: int = expected_receive_num
        self._auto_remove: bool = auto_remove
        self._total_receive_num: int = 0
        self._active: bool = True

    def reset(self):
        '''
        重统计置数据。

        在有期望信号接受次数的情况下，`auto_remove is False`的接收器会重新开始计数并接收信号。
        '''

        self._total_receive_num = 0

    @property
    def expected_receive_num(self) -> int:
        '''
        期望接受信号的次数，超过该次数则不再响应信号；0为无限次。

        设置值小于`total_receive_num`且`auto_remove is True`，则会立刻删除。
        '''

        return self._expected_receive_num

    @expected_receive_num.setter
    def expected_receive_num(self, value: int):
        self._expected_receive_num = value

        if self._auto_remove and self.is_expired:
            self._signal.receivers.remove(self)

    @property
    def auto_remove(self) -> bool:
        '''
        是否自动删除响应次数超出期望次数的接收器。

        设置为`True`时若该receiver过期，则会立刻删除。
        '''

        return self._auto_remove

    @auto_remove.setter
    def auto_remove(self, value: bool):
        self._auto_remove = value

        if self._auto_remove and self.is_expired:
            self._signal.receivers.remove(self)

    @property
    def active(self) -> bool:
        '''
        是否激活；未激活将忽略信号。
        '''

        return self._active

    @active.setter
    def active(self, value: bool):
        self._active = value

    @property
    def total_receive_num(self) -> int:
        '''
        【只读】 总计信号接受次数。
        '''

        return self._total_receive_num

    @property
    def remaining_receive_num(self) -> int:
        '''
        【只读】 剩余的期望信号接受次数；返回为-1代表无期望信号接受次数。
        '''

        if not self.expected_receive_num:
            return -1
        return self.expected_receive_num - self.total_receive_num

    @property
    def is_expired(self) -> bool:
        '''
        【只读】 是否过期。
        '''

        return not self.is_unexpired

    @property
    def is_unexpired(self) -> bool:
        '''
        【只读】 是否未过期。
        '''

        if self.remaining_receive_num == -1:
            return True
        return True if self.remaining_receive_num else False

class Signal:
    def __init__(self):
        self._receivers: List[Receiver] = []
        self._total_send_num: int = 0

    @overload
    def connect(self, fn: Callable, *, expected_receive_num: int = 0, auto_remove: bool = False):
        '''
        通过函数注册响应函数。

        ```python
        from CheeseSignal import Signal

        def receiver(*args, **kwargs):
            ...

        signal = Signal()
        signal.connect(receiver)
        ```

        - Args

            - expected_receive_num: 期望接受信号的次数，超过该次数则不再响应信号；0为无限次。

            - auto_remove: 是否自动删除响应次数超出期望次数的接收器。

        - Raise

            - ValueError: 已有重复的函数接收器。
        '''

    @overload
    def connect(self, *, expected_receive_num: int = 0, auto_remove: bool = False):
        '''
        通过装饰器注册响应函数。

        ```python
        from CheeseSignal import Signal

        signal = Signal()

        @signal.connect()
        def receiver(*args, **kwargs):
            ...
        ```

        - Args

            - expected_receive_num: 期望接受信号的次数，超过该次数则不再响应信号；0为无限次。

            - auto_remove: 是否自动删除响应次数超出期望次数的接收器。

        - Raise

            - ValueError: 已有重复的函数接收器。
        '''

    def connect(self, arg1: Callable | None = None, *, expected_receive_num: int = 0, auto_remove: bool = False):
        if not arg1:
            def wrapper(fn):
                self._connect(fn, expected_receive_num = expected_receive_num, auto_remove = auto_remove)
                return fn
            return wrapper

        self._connect(arg1, expected_receive_num = expected_receive_num, auto_remove = auto_remove)

    def _connect(self, fn: Callable, *, expected_receive_num: int, auto_remove: bool):
        for receiver in self.receivers:
            if receiver.fn == fn:
                raise ValueError('已有重复的函数接收器')

        self.receivers.append(Receiver(self, fn, expected_receive_num = expected_receive_num, auto_remove = auto_remove))

    def send(self, *args, **kwargs) -> List[Any]:
        '''
        发送信号。

        ```python
        from CheeseSignal import Signal

        signal = Signal()
        signal.send('data1', 'data2', **{
            'key1': 'value1',
            'key2': 'value2'
        })
        ```
        '''

        self._total_send_num += 1

        results = []
        for receiver in self.receivers[:]:
            if receiver.active and receiver.is_unexpired:
                receiver._total_receive_num += 1
                results.append(receiver.fn(*args, **kwargs))

                if receiver.is_expired:
                    self.receivers.remove(receiver)
        return results

    async def async_send(self, *args, **kwargs) -> List[Any]:
        '''
        在协程环境中发送信号，并请保证所有接收函数都是协程函数。

        ```python
        import asyncio

        from CheeseSignal import Signal

        async def run_asyncio():
            signal = Signal()
            await signal.async_send('data1', 'data2', **{
                'key1': 'value1',
                'key2': 'value2'
            })

        asyncio.run(run_asyncio())
        ```
        '''

        self._total_send_num += 1

        results = []
        for receiver in self.receivers[:]:
            if receiver.active and receiver.is_unexpired:
                receiver._total_receive_num += 1
                results.append(await receiver.fn(*args, **kwargs))

                if receiver.is_expired:
                    self.receivers.remove(receiver)
        return results

    def disconnect(self, fn: Callable):
        '''
        断开接收器。

        ```python
        from CheeseSignal import Signal

        def receiver(*args, **kwargs):
            ...

        signal = Signal()
        signal.connect(receiver)
        signal.disconnect(receiver)
        ```

        - Raise

            - ValueError: 未找到该函数的接收器。
        '''

        for receiver in self.receivers:
            if receiver.fn == fn:
                self.receivers.remove(receiver)
                return

        raise ValueError('未找到该函数的接收器')

    def reset(self):
        '''
        重置统计数据；所有的接收器的统计数据也会同步清空。
        '''

        self._total_send_num = 0
        for receiver in self.receivers:
            receiver.reset()

    def disconnect_all(self):
        '''
        断开所有接收器。
        '''

        self._receivers = []

    def get_receiver(self, fn: Callable) -> Receiver:
        '''
        获取接收器。

        ```python
        from CheeseSignal import Signal

        def receiver(*args, **kwargs):
            ...

        signal = Signal()
        signal.connect(receiver)

        print(signal.get_receiver(receiver))
        ```

        - Raise

            - ValueError: 未找到该函数的接收器。
        '''

        for receiver in self.receivers:
            if receiver.fn == fn:
                return receiver

        raise ValueError('未找到该函数的接收器')

    def index(self, fn: Callable) -> int:
        '''
        获取接收器的顺序位置。

        ```python
        from CheeseSignal import Signal

        def receiver(*args, **kwargs):
            ...

        signal = Signal()
        signal.connect(receiver)

        print(signal.index(receiver))
        ```

        - Raise

            - ValueError: 未找到该函数的接收器。
        '''

        i = 0
        for receiver in self.receivers:
            if receiver.fn == fn:
                return i
            i += 1

        raise ValueError('未找到该函数的接收器')

    @property
    def receivers(self) -> List[Receiver]:
        '''
        【只读】 接收器的列表，按注册顺序排序。
        '''

        return self._receivers

    @property
    def total_send_num(self) -> int:
        '''
        【只读】 总计信号发送次数。
        '''

        return self._total_send_num
