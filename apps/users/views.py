import logging
console_logger = logging.getLogger("console")

from rest_framework.views import APIView
from libs import exceptionlib, handlerlib

from django.contrib.auth import authenticate, login, logout
from users.models import Account, Police


class LoginView(APIView):

    authentication_classes = ()
    permission_classes = ()

    @exceptionlib.exception_handler
    def post(self, request):
        """
        登录
        :param request:
        :param format:
        :return:
        """
        result = handlerlib.reset_response_data("登录成功", code=200)
        response = handlerlib.JSONResponse(result)

        data = request.data
        police_code = data.get("police_code")
        password = data.get("password")
        try:
            user = Account.objects.get(police_code=police_code)
        except:
            raise exceptionlib.CustomException("用户不存在")

        login_type = data.get("login_type")
        imei = data.get("imei")
        if login_type == 1 :
            try:
                police = Police.objects.get(police_code=police_code)
            except:
                raise exceptionlib.CustomException("警察信息不存在，登录失败")
            if not imei == police.imei:
                raise exceptionlib.CustomException("物理串号不匹配，登录失败")

        username = user.username
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                csrf_token = request.META["CSRF_COOKIE"]
                response.set_cookie("csrf_token", csrf_token)
            else:
                raise exceptionlib.TokenException("登录失败，账号已失效")
        else:
            raise exceptionlib.TokenException("登录失败, 用户名或密码错误")

        return response


class LogoutView(APIView):

    @exceptionlib.exception_handler
    def post(self, request):
        """
        登出
        :param request:
        :return:
        """
        logout(request)
        result = handlerlib.init_response_data()
        response = handlerlib.JSONResponse(result)
        return response