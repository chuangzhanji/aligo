"""分享相关"""
from typing import List, overload

from aligo.core import *
from aligo.request import *
from aligo.response import *
from aligo.types import *
from aligo.types.Enum import *


class Share(Core):
    """..."""

    def share_file(self,
                   file_id_list: List[str],
                   share_name: str = None,
                   share_pwd: str = None,
                   expiration: str = None,
                   drive_id: str = None,
                   description: str = None) -> CreateShareLinkResponse:
        """
        官方：分享文件
        :param file_id_list: [必选] 文件id列表
        :param share_name: [可选] 分享名称
        :param share_pwd: [可选] 分享密码，默认：None，表示无密码
        :param expiration: [可选] 有效期，utc时间字符串：YYYY-MM-DDTHH:mm:ss.SSSZ
        :param drive_id: [可选] 所属网盘id
        :param description: [可选] 描述
        :return: [CreateShareLinkResponse]

        用法示例：
        >>> from aligo import Aligo
        >>> ali = Aligo()
        >>> share = ali.share_file(['<file1_id>','<file2_id>'], share_name='share_name', share_pwd='2020', expiration='2021-12-01T00:00:00.000Z', description='description')
        >>> print(share)
        """
        body = CreateShareLinkRequest(
            file_id_list=file_id_list,
            share_name=share_name,
            share_pwd=share_pwd,
            expiration=expiration,
            drive_id=drive_id,
            description=description,
        )
        return self._core_share_file(body)

    def update_share(self,
                     share_id: str,
                     share_pwd: str = None,
                     expiration: str = None,
                     description: str = None,
                     share_name: str = None) -> UpdateShareLinkResponse:
        """
        官方：更新分享
        :param share_id: [必选] 分享id
        :param share_pwd: [可选] 分享密码，默认：None，表示无密码
        :param expiration: [可选] 有效期，utc时间字符串：YYYY-MM-DDTHH:mm:ss.SSSZ
        :param description: [可选] 描述
        :param share_name: [可选] 分享名称
        :return: [UpdateShareLinkResponse]

        用法示例：
        >>> from aligo import Aligo
        >>> ali = Aligo()
        >>> old_share = ali.share_file(['<file_id>'], share_name='old share')
        >>> new_share = ali.update_share(old_share.share_id, share_name='new share')
        >>> print(new_share)
        """
        body = UpdateShareLinkRequest(
            share_id=share_id,
            share_pwd=share_pwd,
            expiration=expiration,
            description=description,
            share_name=share_name,
        )
        return self._core_update_share(body)

    def cancel_share(self, share_id: str) -> CancelShareLinkResponse:
        """
        官方：取消分享
        :param share_id: [必选] 分享id
        :return: [CancelShareLinkResponse]

        用法示例：
        >>> from aligo import Aligo
        >>> ali = Aligo()
        >>> share = ali.share_file(['<file_id>'])
        >>> cancel_share = ali.cancel_share(share.share_id)
        >>> print(cancel_share)
        """
        body = CancelShareLinkRequest(share_id=share_id)
        return self._core_cancel_share(body)

    def batch_cancel_share(self, share_id_list: List[str]) -> List[BatchSubResponse]:
        """
        官方：批量取消分享
        :param share_id_list: [必选] 分享id列表
        :return: [List[BatchSubResponse]]

        用法示例：
        >>> from aligo import Aligo
        >>> ali = Aligo()
        >>> share1 = ali.share_file(['<file1_id>'])
        >>> share2 = ali.share_file(['<file2_id>'])
        >>> share_id_list = [share1.share_id, share2.share_id]
        >>> cancel_share = ali.batch_cancel_share(share_id_list)
        >>> print(cancel_share)
        """
        body = BatchCancelShareRequest(share_id_list=share_id_list)
        result = self._core_batch_cancel_share(body)
        return [i for i in result]

    def get_share_list(self,
                       order_by: GetShareLinkListOrderBy = 'created_at',
                       order_direction: OrderDirection = 'DESC',
                       include_canceled: bool = False) -> List[ShareLinkSchema]:
        """
        官方：获取分享列表
        :param order_by: [可选] 排序字段，默认：created_at
        :param order_direction: [可选] 排序方向，默认：DESC
        :param include_canceled: [可选] 是否包含已取消的分享，默认：False
        :return: [List[ShareLinkSchema]]

        用法示例：
        >>> from aligo import Aligo
        >>> ali = Aligo()
        >>> share_list = ali.get_share_list()
        >>> print(share_list)
        """
        body = GetShareLinkListRequest(
            creator=self.user_id,
            limit=100,
            order_by=order_by,
            order_direction=order_direction,
            include_canceled=include_canceled,
        )
        result = self._core_get_share_list(body)
        return [i for i in result]

    # 处理其他人的分享
    def get_share_info(self, share_id: str) -> GetShareInfoResponse:
        """
        官方：获取分享信息
        :param share_id: [必选] 分享id
        :return: [GetShareInfoResponse]

        用法示例：
        >>> from aligo import Aligo
        >>> ali = Aligo()
        >>> share = ali.share_file(['<file_id>'])
        >>> share_info = ali.get_share_info(share.share_id)
        >>> print(share_info)
        """
        body = GetShareInfoRequest(share_id=share_id)
        return self._core_get_share_info(body)

    def get_share_token(self, share_id: str, share_pwd: str = '') -> GetShareTokenResponse:
        """
        官方：获取分享token
        :param share_id: [必选] 分享id
        :param share_pwd: [可选] 分享密码，默认：None，表示无密码
        :return: [GetShareTokenResponse]

        用法示例：
        >>> from aligo import Aligo
        >>> ali = Aligo()
        >>> share = ali.share_file(['<file_id>'])
        >>> share_token = ali.get_share_token(share.share_id)
        >>> print(share_token.share_token)
        """
        body = GetShareTokenRequest(share_id=share_id, share_pwd=share_pwd)
        return self._core_get_share_token(body)

    @overload
    def get_share_file_list(
            self,
            share_id: str,
            share_token: str,
            **kwargs
    ) -> List[BaseShareFile]:
        """
        官方：获取分享文件列表
        :param share_id: [必选] 分享id
        :param share_token: [必选] 分享token
        :param kwargs: [可选] 其他参数
        :return: [List[BaseShareFile]]

        用法示例：
        >>> from aligo import Aligo
        >>> ali = Aligo()
        >>> share = ali.share_file(['<file_id>'])
        >>> share_token = ali.get_share_token(share.share_id)
        >>> share_file_list = ali.get_share_file_list(share.share_id, share_token.share_token)
        >>> print(share_file_list)
        """

    @overload
    def get_share_file_list(self, body: GetShareFileListRequest) -> List[BaseShareFile]:
        """
       官方：获取分享文件列表
        :param body: [必选] 请求体
        :return: [List[BaseShareFile]]

        用法示例：
        >>> from aligo import Aligo, GetShareFileListRequest
        >>> ali = Aligo()
        >>> share = ali.share_file(['<file_id>'])
        >>> share_token = ali.get_share_token(share.share_id)
        >>> body = GetShareFileListRequest(share_id=share.share_id, share_token=share_token.share_token)
        >>> share_file_list = ali.get_share_file_list(body=body)
        >>> print(share_file_list)
        """

    def get_share_file_list(
            self,
            share_id: str = None,
            share_token: str = None,
            body: GetShareFileListRequest = None,
            **kwargs
    ) -> List[BaseShareFile]:
        """get_share_file_list"""
        if body is None:
            body = GetShareFileListRequest(share_id=share_id, **kwargs)
        result = self._core_get_share_file_list(body, share_token)
        return [i for i in result]

    @overload
    def get_share_file(
            self,
            share_id: str,
            file_id: str,
            share_token: str,
            **kwargs
    ) -> BaseShareFile:
        """
        官方：获取分享文件
        :param share_id: [必选] 分享id
        :param file_id: [必选] 文件id
        :param share_token: [必选] 分享token
        :param kwargs: [可选] 其他参数
        :return: [BaseShareFile]

        用法示例：
        >>> from aligo import Aligo
        >>> ali = Aligo()
        >>> share = ali.share_file(['<file_id>'])
        >>> share_token = ali.get_share_token(share.share_id)
        >>> share_file = ali.get_share_file(share.share_id, share.file_id, share_token.share_token)
        >>> print(share_file)
        """

    @overload
    def get_share_file(self, body: GetShareFileRequest) -> BaseShareFile:
        """
        官方：获取分享文件
        :param body: [必选] 请求体
        :return: [BaseShareFile]

        用法示例：
        >>> from aligo import Aligo, GetShareFileRequest
        >>> ali = Aligo()
        >>> share = ali.share_file(['<file_id>'])
        >>> share_token = ali.get_share_token(share.share_id)
        >>> body = GetShareFileRequest(share_id=share.share_id, file_id=share.file_id, share_token=share_token.share_token)
        >>> share_file = ali.get_share_file(body=body)
        >>> print(share_file)
        """

    def get_share_file(
            self,
            share_id: str = None,
            file_id: str = None,
            share_token: str = None,
            body: GetShareFileRequest = None,
            **kwargs
    ) -> BaseShareFile:
        """get_share_file"""
        if body is None:
            body = GetShareFileRequest(share_id=share_id, file_id=file_id, **kwargs)
        return self._core_get_share_file(body, share_token)

    @overload
    def get_share_link_download_url(
            self,
            share_id: str,
            file_id: str,
            share_token: str,
            **kwargs
    ) -> GetShareLinkDownloadUrlResponse:
        """
        官方：获取分享文件下载链接
        :param share_id: [必选] 分享id
        :param file_id: [必选] 文件id
        :param share_token: [必选] 分享token
        :param kwargs: [可选] 其他参数
        :return: [GetShareLinkDownloadUrlResponse]

        用法示例：
        >>> from aligo import Aligo
        >>> ali = Aligo()
        >>> share = ali.share_file(['<file_id>'])
        >>> share_token = ali.get_share_token(share.share_id)
        >>> share_link_download_url = ali.get_share_link_download_url(share.share_id, share.file_id, share_token.share_token)
        >>> print(share_link_download_url)
        """

    @overload
    def get_share_link_download_url(self, body: GetShareLinkDownloadUrlRequest) -> GetShareLinkDownloadUrlResponse:
        """
        官方：获取分享文件下载链接
        :param body: [必选] 请求体
        :return: [GetShareLinkDownloadUrlResponse]

        用法示例：
        >>> from aligo import Aligo, GetShareLinkDownloadUrlRequest
        >>> ali = Aligo()
        >>> share = ali.share_file(['<file_id>'])
        >>> share_token = ali.get_share_token(share.share_id)
        >>> body = GetShareLinkDownloadUrlRequest(share_id=share.share_id, file_id=share.file_id, share_token=share_token.share_token)
        >>> share_link_download_url = ali.get_share_link_download_url(body=body)
        >>> print(share_link_download_url)
        """

    def get_share_link_download_url(
            self,
            share_id: str = None,
            file_id: str = None,
            share_token: str = None,
            body: GetShareLinkDownloadUrlRequest = None,
            **kwargs
    ) -> GetShareLinkDownloadUrlResponse:
        """get_share_link_download_url"""
        if body is None:
            body = GetShareLinkDownloadUrlRequest(share_id=share_id, file_id=file_id, **kwargs)
        return self._core_get_share_link_download_url(body, share_token)

    @overload
    def share_file_saveto_drive(
            self,
            share_id: str,
            file_id: str,
            share_token: str,
            to_parent_file_id: str = 'root',
            to_drive_id: str = None,
            new_name: str = None,
            **kwargs
    ) -> ShareFileSaveToDriveResponse:
        """
        官方：保存分享文件到指定的网盘
        :param share_id: [必选] 分享id
        :param file_id: [必选] 文件id
        :param share_token: [必选] 分享token
        :param to_parent_file_id: [必选] 目标父文件夹id，默认为根目录
        :param to_drive_id: [可选] 目标网盘id，默认为当前网盘
        :param new_name: [可选] 新文件名
        :param kwargs: [可选] 其他参数
        :return: [ShareFileSaveToDriveResponse]

        用法示例：
        >>> from aligo import Aligo
        >>> ali = Aligo()
        >>> share = ali.share_file(['<file_id>'])
        >>> share_token = ali.get_share_token(share.share_id)
        >>> share_file_saveto_drive = ali.share_file_saveto_drive(share.share_id, share.file_id, share_token.share_token)
        >>> print(share_file_saveto_drive)
        """

    @overload
    def share_file_saveto_drive(self, body: ShareFileSaveToDriveRequest = None) -> ShareFileSaveToDriveResponse:
        """
        官方：保存分享文件到指定的网盘
        :param body: [必选] 请求体
        :return: [ShareFileSaveToDriveResponse]

        用法示例：
        >>> from aligo import Aligo, ShareFileSaveToDriveRequest
        >>> ali = Aligo()
        >>> share = ali.share_file(['<file_id>'])
        >>> share_token = ali.get_share_token(share.share_id)
        >>> body = ShareFileSaveToDriveRequest(share_id=share.share_id, file_id=share.file_id, share_token=share_token.share_token)
        >>> share_file_saveto_drive = ali.share_file_saveto_drive(body=body)
        >>> print(share_file_saveto_drive)
        """

    def share_file_saveto_drive(
            self,
            share_id: str = None,
            file_id: str = None,
            share_token: str = None,
            to_parent_file_id: str = 'root',
            to_drive_id: str = None,
            new_name: str = None,
            body: ShareFileSaveToDriveRequest = None,
            **kwargs
    ) -> ShareFileSaveToDriveResponse:
        """share_file_saveto_drive"""
        if body is None:
            body = ShareFileSaveToDriveRequest(
                share_id=share_id,
                file_id=file_id,
                to_parent_file_id=to_parent_file_id,
                to_drive_id=to_drive_id,
                new_name=new_name,
                **kwargs
            )
        return self._core_share_file_saveto_drive(body, share_token)

    @overload
    def batch_share_file_saveto_drive(
            self,
            share_id: str,
            file_id_list: List[str],
            share_token: str,
            to_parent_file_id: str = 'root',
            to_drive_id: str = None,
            **kwargs
    ) -> List[BatchShareFileSaveToDriveResponse]:
        """
        官方：批量保存分享文件到指定的网盘
        :param share_id: [必选] 分享id
        :param file_id_list: [必选] 文件id列表
        :param share_token: [必选] 分享token
        :param to_parent_file_id: [必选] 目标父文件夹id，默认为根目录
        :param to_drive_id: [可选] 目标网盘id，默认为当前网盘
        :param kwargs: [可选] 其他参数
        :return: [List[BatchShareFileSaveToDriveResponse]]

        用法示例：
        >>> from aligo import Aligo
        >>> ali = Aligo()
        >>> share = ali.share_file(['<file_id>'])
        >>> share_token = ali.get_share_token(share.share_id)
        >>> batch_share_file_saveto_drive = ali.batch_share_file_saveto_drive(share.share_id, share.file_id_list, share_token.share_token)
        >>> print(batch_share_file_saveto_drive[0].file_id)
        """

    @overload
    def batch_share_file_saveto_drive(self, body: BatchShareFileSaveToDriveRequest) -> List[
        BatchShareFileSaveToDriveResponse]:
        """
        官方：批量保存分享文件到指定的网盘
        :param body: [必选] 请求体
        :return: [List[BatchShareFileSaveToDriveResponse]]

        用法示例：
        >>> from aligo import Aligo, BatchShareFileSaveToDriveRequest
        >>> ali = Aligo()
        >>> share = ali.share_file(['<file_id>'])
        >>> share_token = ali.get_share_token(share.share_id)
        >>> body = BatchShareFileSaveToDriveRequest(share_id=share.share_id, file_id_list=share.file_id_list, share_token=share_token.share_token)
        >>> batch_share_file_saveto_drive = ali.batch_share_file_saveto_drive(body=body)
        >>> print(batch_share_file_saveto_drive[0].file_id)
        """

    def batch_share_file_saveto_drive(
            self,
            share_id: str = None,
            file_id_list: List[str] = None,
            share_token: str = None,
            to_parent_file_id: str = 'root',
            to_drive_id: str = None,
            body: BatchShareFileSaveToDriveRequest = None,
            **kwargs
    ) -> List[BatchShareFileSaveToDriveResponse]:
        """batch_share_file_saveto_drive"""
        if body is None:
            body = BatchShareFileSaveToDriveRequest(
                share_id=share_id,
                file_id_list=file_id_list,
                to_parent_file_id=to_parent_file_id,
                to_drive_id=to_drive_id,
                **kwargs
            )
        result = self._core_batch_share_file_saveto_drive(body, share_token)
        return [i for i in result]
