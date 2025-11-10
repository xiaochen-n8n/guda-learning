from django.db import models

# Create your models here.
# 设计字段：为 Host 模型添加以下字段，并为其选择合适的字段类型和约束：
# hostname：主机名（字符串类型，要求唯一）。
# ip：IP 地址（使用 IP 地址专用字段）。
# cpu：CPU 信息（字符串类型）。
# mem：内存信息（字符串类型）。
# disk：磁盘信息（字符串类型）。
# desc：备注信息（字符串类型，允许为空）。
class Host(models.Model):
    hostname = models.CharField(max_length=255, verbose_name="主机名", unique=True, blank=False)
    ip = models.GenericIPAddressField(verbose_name="IP地址", blank=False)
    disk = models.CharField(max_length=255, null=True, blank=False)
    mem = models.CharField(max_length=255, null=True, blank=False)
    cpu = models.CharField(max_length=255, null=True, blank=False)
    desc = models.CharField(max_length=255, null=True, blank=False)
    
    def __str__(self): #优化显示：为 Host 模型定义一个 __str__ 方法，使其在后台显示时能返回主机名，便于识别。
        return self.hostname