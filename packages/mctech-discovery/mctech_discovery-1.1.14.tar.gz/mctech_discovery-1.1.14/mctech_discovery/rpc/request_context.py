from __future__ import absolute_import

from typing import Dict, Any, Union, Tuple, Mapping
import re
import io
import httpx
from abc import ABC, abstractmethod
from .web_error import WebError
from urllib.parse import urlparse, urljoin, urlencode, parse_qsl, urlunparse
from mctech_core.context import get_async_context

PARAM_PARTERN = re.compile(':(\\w+)')
HEADER_PARTTERN = re.compile('[A-Z]')


class AbstractInvoker(ABC):
    def __init__(self, path: str,
                 params: Dict[str, Any] = None,
                 query: Dict[str, Any] = None,
                 headers: Dict[str, Any] = None,
                 context: Dict[str, Any] = None
                 ):
        self.path = path
        self.params = params
        self.query = query
        self.headers = headers
        self.context = context


class WebSocketInvoker(AbstractInvoker):
    pass


JsonObject = Any


class RpcInvoker(AbstractInvoker):
    def __init__(self, path: str,
                 params: Mapping[str, Any] = None,
                 query: Mapping[str, Any] = None,
                 body: Union[JsonObject, bytes, str] = None,
                 headers: Mapping[str, Any] = None,
                 retry: int = None,
                 context: Mapping[str, Any] = None,
                 timeout: float = None,
                 **kwargs
                 ):
        '''
        path: api接口端点路径，可以包含':param'这样的参数格式
        params: 当传入的path对应的端点路径中包含参数时，params提供参数的替换值
        query: api接口端点路径的query参数
        body: 传递给调用的api接口的body内容
        headers: 需要传递的额外header头。
                 默认会设置'content-type'为'application/json'，如果需要别的类型可以在此替换
        retry: 出错重试次数，默认值为0。目前并未使用
        context: 额外传递的上下文信息，最终会转换成通过header方式传递。
                 与headers参数不一样的是context里的值会把驼峰格式转换成'x-'开头的'-'分隔的小写字符格式。
                 例如tenantId会转换成 'x-tenant-id'，这个参数仅是为了兼容与目前node框架调用的服务
        timeout: 接口调用客户端超时时间，单位秒。超过设置的超时时间，调用端直接抛出超时异常
        '''
        super().__init__(path, params=params, query=query,
                         headers=headers, context=context)
        self.body = body
        # 仅在execute方法内有效，调用返回的类型是否是json,如果为false则返回原始字符串文本
        self.json = kwargs.get('json', True)
        assert isinstance(self.json, bool), "json属性类型应变为bool类型"
        self.retry = retry
        self.timeout = timeout


class PipeRpcInvoker(RpcInvoker):

    def __init__(self, path: str,
                 method: str,
                 params: Mapping[str, Any] = None,
                 query: Mapping[str, Any] = None,
                 body: Union[JsonObject, io.IOBase] = None,
                 headers: Mapping[str, Any] = None,
                 retry: int = None,
                 context: Mapping[str, Any] = None,
                 timeout: int = None,
                 **kwargs):
        '''
        method: stream调用模式下使用的http请求方法
        path: api接口端点路径，可以包含':param'这样的参数格式
        params: 当传入的path对应的端点路径中包含参数时，params提供参数的替换值
        query: api接口端点路径的query参数
        body: 传递给调用的api接口的body内容
        headers: 需要传递的额外header头。
                 默认会设置'content-type'为'application/json'，如果需要别的类型可以在此替换
        retry: 出错重试次数，默认值为0。目前并未使用
        context: 额外传递的上下文信息，最终会转换成通过header方式传递。
                 与headers参数不一样的是context里的值会把驼峰格式转换成'x-'开头的'-'分隔的小写字符格式。
                 例如tenantId会转换成 'x-tenant-id'，这个参数仅是为了兼容与目前node框架调用的服务
        timeout: 接口调用客户端超时时间，单位秒。超过设置的超时时间，调用端直接抛出超时异常
        '''
        super().__init__(path, params=params, query=query, body=body,
                         headers=headers, retry=retry,
                         context=context, timeout=timeout, **kwargs)
        self.method = method


class RpcServiceInfo():
    def __init__(self,
                 service_id: str = None,
                 url: str = None,
                 rpc_type: str = None,
                 path: str = None,
                 timeout: int = None
                 ):
        self.service_id = service_id
        self.url = url
        self.path = path
        self.rpc_type = rpc_type
        self.timeout = timeout


class EndPoint():
    def __init__(self, id: str, host: str, port: int):
        self.id = id
        self.host = host
        self.port = port


class RequestContext(ABC):
    def __init__(self, invoker: RpcInvoker, service: RpcServiceInfo,
                 app_name: str):
        self.invoker = invoker
        self.service = service
        self.app_name = app_name

        path = invoker.path
        query = invoker.query if invoker.query is not None else {}
        params = invoker.params if invoker.params is not None else {}

        headers = dict(invoker.headers) if invoker.headers else {}
        self._add_headers(headers, invoker.context)
        self.headers = headers

        base_url, path_and_query = self._get_path_and_query(path)
        parse_result = urlparse(urljoin(base_url, path_and_query))
        query_list = parse_qsl(parse_result.query)
        for name, value in query.items():
            query_list.append((name, value))

        def _replacement(matched, params):
            var_name: str = matched.group(1)
            # 获取传入参数
            value = params.get(var_name)
            if (value is None):
                error_msg = "不存在的属性：'%s'" % var_name
                raise RuntimeError(error_msg)
            return str(value)

        new_path = PARAM_PARTERN.sub(
            lambda matched: _replacement(matched, params), parse_result.path)
        new_qs = urlencode(query_list)
        self.url = urlunparse([
            parse_result.scheme,
            parse_result.netloc,
            new_path,
            "",
            new_qs, ""])
        self.url_port = parse_result.port
        self.url_host = parse_result.hostname
        self.path_and_query = new_path + "?" + new_qs

    @property
    def timeout(self):
        if self.invoker.timeout:
            return self.invoker.timeout
        else:
            return self.service.timeout

    def process_request_option(self, option: Dict[str, Any]):
        # 什么也不做
        pass

    @abstractmethod
    def resolve_error(self, err: BaseException):
        pass

    @abstractmethod
    def _get_path_and_query(self, path: str) -> Tuple[str, str]:
        '''
        :return [baseUrl: str, path_and_query: str]
        '''
        pass

    @abstractmethod
    def _add_headers(self, headers: Dict[str, Any], context: Dict[str, Any]):
        pass

    def _to_header_name(self, name: str, prefix: str):
        key = HEADER_PARTTERN.sub(
            lambda matched: '-' + matched.group(0).upper(), name)

        # 补充'x-'前缀
        if key.startswith('-'):
            return prefix + key
        return prefix + '-' + key


class InternalRequestContext(RequestContext):
    def _get_path_and_query(self, path: str):
        base_url = self.service.url
        if not base_url:
            base_url = "http://%s" % self.service.service_id

        path_prefix = self.service.path if self.service.path else '/'
        path_and_query = urljoin(path_prefix, path)
        return (base_url, path_and_query)

    def _add_headers(self, headers: Dict[str, Any], context: Dict[str, Any]):
        asynctx = get_async_context()
        principal: Dict[str, any] = {}
        extras: Dict[str, any] = {}
        webContext = asynctx.webContext
        if webContext:
            # 当前调用是在处理web请求的时候发生的
            if webContext.principal:
                # website身份认证信息
                principal['id'] = webContext.principal.get('id')
                if not principal.get('userId') and principal.get('id'):
                    principal['userId'] = principal['id']

                principal['tenantId'] = webContext.principal['tenantId']
                principal['tenantCode'] = webContext.principal['tenantCode']

                # TODO: 应该删除掉
                principal['orgId'] = webContext.principal['orgId']
                principal['applicationId'] = webContext.principal['applicationId']  # noqa
            extras = webContext.extras

        if not principal.get('tenantId'):
            # 当前调用是在消息队列或定时任务等其它非web请求中调用的
            # 消息队列处理器中中没有webContext对象
            principal['tenantId'] = asynctx.tenant_id

        mergedCtx = {}
        mergedCtx.update(principal)
        mergedCtx.update(extras)
        # 用户调用api时显示设置的信息
        if context:
            mergedCtx.update(context)

        for name, value in mergedCtx.items():
            if value is None:
                continue
            key = self._to_header_name(name, 'x')
            headers[key] = str(value)

        if self.app_name:
            headers['i-rpc-client'] = self.app_name

        tracing = asynctx.tracing
        if not tracing:
            return

        # 用于调用链跟踪的信息
        for name, value in asynctx.tracing.items():
            headers[name] = value

    def resolve_error(self, res: httpx.Response, err: WebError):
        try:
            data = res.json()
        except Exception:
            # 什么也不做
            data = {
                'code': 'json_format_error',
                'desc': res.text
            }
        # 默认json格式
        err.code = data.get("code")
        err.desc = data.get("desc")
        err.details = data.get("details")
