from base.config import settings
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class FaceInfo(Model):
    table = "face_info"
    id_ = fields.IntField(pk=True, index=True, description="系统生成的id，长整型")
    uid = fields.CharField(max_length=255, index=True, description='用户id来自于其它管控系统')
    name = fields.CharField(max_length=255, index=True, description='姓名')
    face_path = fields.CharField(max_length=255, index=True, description='人脸图片所在路径')
    face_url = fields.CharField(max_length=255, index=False, description="人脸所在静态文件路(url)")
    created_time = fields.DatetimeField(null=True, auto_now_add=True)
    update_time = fields.DatetimeField(null=True, auto_now=True)

    def __str__(self):
        return self.name

    class PydanticMeta:
        exclude = []

    def to_dict(self):  # 这个方法自定义的时候使用
        data = {i: getattr(self, i) for i in self.__dict__ if not i.startswith('_')}
        return data


# 可以和pydanic配合使用
User_orm = pydantic_model_creator(FaceInfo, name="FaceInfo")  # ORM 推荐的用法 配合fastapi 的模型

if __name__ == '__main__':
    # 创建数据表
    from tortoise import Tortoise, run_async


    async def init():
        await Tortoise.init(
            db_url=settings.DB_URL,  #
            modules={'models': ['models']}
        )
        await Tortoise.generate_schemas()  # 创建数据库表


    run_async(init())
