from rest_framework.response import Response
from rest_framework import status

class BaseResponseSerializer:
    """統一回應格式處理器"""
    
    @staticmethod
    def success(data=None, message="操作成功"):
        """成功回應"""
        return Response({
            "result": True,
            "errorCode": "",
            "message": message,
            "data": data
        }, status=status.HTTP_200_OK)
    
    @staticmethod
    def created(data=None, message="建立成功"):
        """建立成功回應"""
        return Response({
            "result": True,
            "errorCode": "",
            "message": message,
            "data": data
        }, status=status.HTTP_201_CREATED)
    
    @staticmethod
    def fail(message="操作失敗", error_code="OPERATION_FAILED", data=None, status_code=status.HTTP_400_BAD_REQUEST):
        """失敗回應"""
        return Response({
            "result": False,
            "errorCode": error_code,
            "message": message,
            "data": data
        }, status=status_code)
    
    @staticmethod
    def not_found(message="資源不存在", error_code="NOT_FOUND"):
        """404回應"""
        return Response({
            "result": False,
            "errorCode": error_code,
            "message": message,
            "data": None
        }, status=status.HTTP_404_NOT_FOUND)