# Auto-Batch-Pull
Created by Guofeng Yi

## 📝 Introduction (介绍)
When you clone a bunch of similar repository codes for the purpose of learning a specific knowledge point and want to mimic and study, do you also find it **a headache to manually execute `git pull` in each folder every time?** 
This project aims to help you automatically execute the `git pull` command in bulk on all folders containing '.git' in a specified directory, updating all repositories to the latest version, thereby saving you time.

当你为了学习某一个知识点克隆了一堆类似的仓库代码想要模仿学习时，你是否也**头疼于每次要手动在每个文件夹执行一次 `git pull`**？
本项目旨在帮助你在指定目录下所有包含.git的文件夹上自动批量执行“git pull”命令，以将所有存储库更新到最新版本，节省你的时间。

## 🏋️‍️ QuickStart

### Install
```python
pip install auto_batch_pull
# or from source
pip install .
```

### Command Line Tools
```python
abp --base_dir . # or abp -b .
```
