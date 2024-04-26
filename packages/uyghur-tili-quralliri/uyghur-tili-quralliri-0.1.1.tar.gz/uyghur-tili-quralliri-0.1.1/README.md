# Uyghur Language Tools

## 0. Description

> a tool box including some useful functions to handle with uyghur writing ...

## 1. Installing

```cmd
pip install -g uyghur-tili-quralliri
```

## 2. Usage

```python
from UyghurLanguageTools import UyghurLanguageTools as Tools
Tools.main()
# Uyghur Language Tools (0.1), for more infomation please visit ...
origin = "مەرھابا"
print(origin)
# مەرھابا
target = Tools.toExtended(origin)
print(target)
# مەر ھا با
```

## 3. others

> for more information please visit [github](https://github.com/kompasim/uyghur-tili-quralliri).
