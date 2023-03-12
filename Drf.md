## Serializer

##### 借助ModelSerializer快速创建一个Serializer

```python
class GeneralUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


serializer = UserSerilzier()
print(repr(serializer))
```

## 验证器

##### 唯一性验证器

https://www.django-rest-framework.org/api-guide/validators/#uniquevalidator

```python
from rest_framework.validators import UniqueValidator

UniqueValidator(queryset=User.objects.all())
```

##### 自定义验证器

将`validate_<field_name>`方法添加到`Serializer`子类来指定自定义字段级验证

```python
from rest_framework import serializers


class BlogPostSerializer(serializers.Serializer):
  title = serializers.CharField(max_length=100)
  content = serializers.CharField()

  def validate_title(self, value):
    """
    Check that the blog post is about Django.
    """
    if 'django' not in value.lower():
      raise serializers.ValidationError("Blog post is not about Django")
    return value
```

## 默认值

- 注意
    - 用于模型类的默认值要到验证运行后才会生成

```python
# 仅在创建时有默认值
created_at = serializers.DateTimeField(default=serializers.CreateOnlyDefault(timezone.now))
```

