## 验证器

#### 快速打印所需序列化类

```python
serializer = UserSerilzier()
print(repr(serializer))
```

#### 验证唯一性

```python
from rest_framework.validators import UniqueValidator
# queryset参数为当前需要序列化类的all()查询
UniqueValidator(queryset=User.objects.all())
```



