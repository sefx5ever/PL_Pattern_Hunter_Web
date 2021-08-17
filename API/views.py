from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions, status
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .models import Account, SymbolHistoryData, ResearcherModel
from .serializers import AccountSerializer
from datetime import datetime as dt
import hashlib

# https://docs.djangoproject.com/en/3.2/topics/auth/default/#changing-passwords
# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.check_password

class AccountViews(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        output = {'status' : False }
        try:
            result_required = self.__check_required('GET',request.query_params)
            if result_required:
                account = self.__get_object(request.query_params['user'])
                result_activate = self.__is_active(request.query_params['user'],request.query_params['password'])
                result_password = account.check_password(request.query_params['password'])
                if account and result_password and result_activate:
                    serializer = AccountSerializer(account)
                    output.update(serializer.data)
                    output.pop('password')
                    output['status'] = True
                    return Response(output,status=status.HTTP_200_OK)
        except Exception as err:
            output.update({'message' : str(err) })
        return Response(output,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    def post(self,request):
        output = {'status' : False }
        try:
            result_required = self.__check_required('POST',request.data)
            if result_required:
                serializer = AccountSerializer(data=request.data)
                if serializer.is_valid():
                    result_password = request.data['password'] == request.data['repassword']
                    user = request.data
                    if result_password:
                        self.__save_account_with_hash(user)
                        output.update(serializer.data)

                        ActivationMail().send_activation_mail(
                            user['user'],user['name'],
                            user['password'],user['email']
                        )

                        output.pop('password')
                        output['status'] = True
                        return Response(output,status=status.HTTP_201_CREATED)
                output.update(serializer.errors)
        except Exception as err:
            output.update({'message' : str(err) })
        return Response(output,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request):
        output = {'status' : False }
        try:
            result_required = self.__check_required('PUT',request.data)
            user = request.data
            if result_required:
                account = self.__get_object(request.data['user'])
                if account:
                    data = self.__update_account(
                        user['user'],user['name'],user['email'],
                        user['password'],user['repassword']
                    )
                    output.update(data)
                    output['status'] = True
                    return Response(output,status=status.HTTP_200_OK)
        except Exception as err:
            output.update({'message' : str(err) })
        return Response(output,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        output = {'status' : False }
        try:
            result_required = self.__check_required('DELETE',request.query_params)
            if result_required:
                account = self.__get_object(request.query_params['user'])
                account.delete()
                output['status'] = True
                return Response(output,status=status.HTTP_200_OK)
        except Exception as err:
            output.update({'message' : str(err) })
        return Response(output,status=status.HTTP_400_BAD_REQUEST)    

    def __save_account_with_hash(self,user):
        Account.objects.create_user(
            user['email'],user['user'],user['name'],
            user['password'],user['repassword'],user['role']
        )

    def __update_account(self,user,name,email,password,repassword):
        account = Account.objects.filter(user=user)[0]
        if (password != repassword):
            raise ValidationError('提示：帳號密碼輸入錯誤！')
        account.name = name
        account.set_password(password)
        account.save(update_fields=['password','name'])
        return {
            "user" : user,
            "name" : name,
            "email" : email
        }

    def __get_object(self,user:str):
        try:
            return Account.objects.filter(user=user)[0]
        except Account.DoesNotExist:
            return False

    def __is_active(self,user,password):
        result = authenticate(user=user,password=password)
        if result is None:
            # Reason
            # 1. 帳號或密碼可能不正確
            # 2. 帳號還沒激活
            raise ValueError('提示：您的帳號尚未激活，請到電子郵箱查詢並啟動服務！')
        return True

    def __check_required(self,method,request_data):
        required = {
            'GET' : ['user','password'],
            'POST' : ['user','name','email','role','password','repassword'],
            'PUT' : ['user','name','email','password'],
            'DELETE' : ['user']
        }
        return all(key in request_data for key in required[method])

class ActivationMail(APIView):
    def __init__(self):
        self.activation_subject = "[Pattern Hunter] Activation Mail"
        self.reset_password_subject = "[Pattern Hunter] Password Reset Mail"
        self.activation_text = """
            您好{}，感謝您使用 Pattern Hunter 服務，請點擊以下連接完成帳號激活！ \n
            激活連接：{}
        """
        self.reset_password_text = """
            您好{}，以下是您所申請新的密碼組，請使用改密碼進行登錄，並至「帳號設定」重置您的帳號密碼！ \n
            【Pattern Hunter 帳號資訊】 \n
            帳號：{}
            密碼：{}
        """
        self.fail_silently = False # False means raise error when mail is mail to send.
        self.sender_mail = '06170171@gm.scu.edu.tw'

    def get(self,request):
        output = {'status' : False }
        try:
            if ({'email','hash'} <= request.query_params.keys()):
                result_activate = self.__activate_by_hash(
                    request.query_params['email'],request.query_params['hash']
                )
                if result_activate:
                    output['status'] = True
                    output['message'] = '感謝您使用 Pattern Hunter 服務，您已成功激活帳號！'
                    return Response(output,status=status.HTTP_202_ACCEPTED)
        except Exception as err:
            output.update({'message' : str(err) })
        return Response(output,status=status.HTTP_206_PARTIAL_CONTENT)

    def post(self,request):
        output = {'status' : False }
        print(request.data)
        try:
            if ({'email'} <= request.data.keys()):
                account,new_password = self.__reset_passwor_by_email(request.data['email'])
                result_reset_password = self.send_reset_password_mail(
                    account.name,account.user,
                    new_password,request.data['email']
                )
                if result_reset_password:
                    output['status'] = True
                    output['message'] = '客服人員已重置密碼，請至您的電子郵箱查收！'
                    return Response(output,status=status.HTTP_202_ACCEPTED)
        except Exception as err:
            output.update({'message' : str(err) })
        return Response(output,status=status.HTTP_400_BAD_REQUEST)

    def send_activation_mail(self,user:str,name:str,password:str,recipent_mail:str):
        hash = self.__encrypt_data(user,password)
        
        self.__save_encrypt_data(user,hash_value=hash)

        link = f'http://127.0.0.1:8000/api/mail?email={recipent_mail}&hash={hash}'
        return send_mail(
            self.activation_subject,self.activation_text.format(name,link),
            self.sender_mail,[recipent_mail],self.fail_silently
        )

    def send_reset_password_mail(self,name:str,user:str,new_password:str,recipent_mail:str):
        return send_mail(
            self.reset_password_subject,self.reset_password_text.format(name,user,new_password),
            self.sender_mail,[recipent_mail],self.fail_silently
        )

    def __encrypt_data(self,user:str,password:str=''):
        hash = hashlib.new('sha512_256')
        text_to_encrypt = user+password+str(dt.now().microsecond)
        hash.update(text_to_encrypt.encode())
        return hash.hexdigest()

    def __save_encrypt_data(self,user:str,hash_value):
        account = Account.objects.filter(user=user)
        account.update(hash_value=hash_value)
        return hash_value

    def __reset_passwor_by_email(self,email):
        new_password = self.__encrypt_data(email)
        account = Account.objects.filter(email=email)[0]
        account.set_password(new_password)
        account.save(update_fields=['password'])
        return account,new_password

    def __activate_by_hash(self,email:str,hash_value:str):
        try:
            account = Account.objects.filter(email=email)

            if (account[0].hash_value != hash_value):
                raise ValidationError('提示：您的帳號金鑰輸入有誤！') 

            account.update(is_active=True)
        except Exception as err:
            raise ValueError(str(err))
        return True


