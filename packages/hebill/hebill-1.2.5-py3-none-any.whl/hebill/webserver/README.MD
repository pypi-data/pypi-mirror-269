# hebill.webserver

## 应用
快速布置服务器

## 示例
```python
import hebill


if __name__ == '__main__':
    app = hebill.webserver.WebServer('', 1080, '')
    app.start()
```