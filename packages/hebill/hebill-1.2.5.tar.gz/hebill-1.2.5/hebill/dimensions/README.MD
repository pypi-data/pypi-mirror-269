# hebill.dimensions

## 应用

通用部件尺寸处理模板类

## 示例
```python
import math
import hebill


class Dims(hebill.dimensions.Dimensions):
    names = ['diameter', 'height']

    def __init__(self, dimensions:dict):
        super().__init__(dimensions)

    @property
    def diameter(self): return self['diameter']

    @diameter.setter
    def diameter(self, dim: float): self['diameter'] = dim

    @property
    def height(self): return self['height']

    @height.setter
    def height(self, dim: float): self['height'] = dim

    def volume(self):
        return math.pi * pow(self.diameter * 2, 2) * self.height


dims = Dims({
    'diameter': 1500,
    'height': 1500,
})
print(f'Diameter: {dims.diameter}')
print(f'Height: {dims.height}')
print(f'Volume: {dims.volume()}')

```