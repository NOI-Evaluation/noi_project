#-*- coding:utf-8 -*-

from app01 import models
from stark.service.stark import site, StarkConfig


site.register(models.User)


