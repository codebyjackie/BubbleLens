# BubbleLens

一个完全本地、轻量的 Danbooru 标签选择、复制与提示词编辑工具。它不加载模型、不调用生图，也不会把标签或提示词发送到互联网。

## 系统要求与启动

- Windows 10/11、Microsoft Edge，以及 Python 3.10 或更高版本。
- 下载完整项目后双击 `BubbleLens.exe`。
- 应用会在独立的 Edge 应用窗口中打开。
- 如果需要手动启动，可运行 `StartBubbleLens.bat`。
- 也可以在项目目录执行 `python server.py`，再打开 `http://127.0.0.1:7873`。

## 界面逻辑

- 最右侧是“大提示词库”，相当于上一级文件夹；点击后切换整个用途词库。
- 左上角显示当前词库内的细分类，可选择、新增、重命名或删除。
- 当前大分类标题与细分类保持同一行；细分类采用单行横向滚动，不会挤压下方标签区与提示词修改器。
- 顶部搜索可切换“全局”“当前词库”或“当前分类”，结果同时显示标签、说明、细分类和大分类；点击结果会复制标签本身，并跳转、选中和滚动高亮。
- 中上区域显示当前细分类的全部标签；点击标签会选择并复制标签本身。
- 左下角是当前已选提示词修改器，可排序、修改权重、直接编辑或删除。
- 右侧预览区显示最终提示词，可一键复制。
- “复制提示词”右侧的设置按钮用于调整整个界面布局缩放，并自动保存。

## 自定义管理

- 管理模式支持新增、编辑和删除大词库、细分类与标签，并可通过拖动手柄分别调整三层内容的顺序。
- 内置数据采用“本地隐藏”，可在设置中恢复；不会改坏原始 CSV。
- 自建内容和界面缩放保存在 `%LocalAppData%\BubbleLens\EdgeProfile`，关闭或重启后仍会保留；旧版 `PromptAtelier` 配置会在首次启动时迁移。

## 标签数据库与分类

- 数据源：`data/tags_enhanced.csv`
- 原始行数：49,844
- 去重后唯一标签：49,837
- 默认大词库：53
- 当前非空细分类：395
- 当前目录版本：v14
- v8 将过宽的身体、服装、配饰、场景、动物、符号与成人内容重新分层；例如服装分为日常服装、外套套装、制服装扮、传统服饰、盔甲护具、服装外观、服装剪裁与穿着状态。
- v9 按“人物与作品、外貌动作、服装配饰、道具生物、场景镜头、风格文字、成人敏感”的工作流重新排列大分类。
- 制服进一步分为校服款式、作品校服、水手服、服务制服、职业制服、军警制服、运动服、作品制服和主题装扮；配饰则拆为头部配饰、首饰珠宝与穿戴配饰。
- 分类按英文标签、中文名称和 wiki 说明联合审计，而不是只按词面关键词：眉毛与鼻子、嘴唇与舌齿、手臂姿势与手势符号、普通穿孔与私密穿孔均独立归档。
- 原“符号标志”的 414 项已逐项拆为通用符号、数学几何、乐谱、宗教、星相、旗帜、纹章和科学标识；纸条与音符、星座意象与星相符号分别处理。
- 原“纹身伤疤”和“身体状态”共 468 项已拆为纹身、痣斑、伤痕、绷带、体表沾染、体毛、肢体差异、生理反应等；视觉血液集中归入“暴力敏感”，不再混进成人内容或身体状态。
- 当前仅 2,673 个作品专名或多义长尾词保守留在“其他标签”，避免缺少证据时强行错分。
- 版本升级会迁移旧分类位置；已隐藏的内置标签按标签名继续保持隐藏，自建标签与分类设置不会因内置标签重排而丢失。
- 每个唯一标签恰好归档一次；语义不够明确的专有长尾词保守放入按字母划分的“其他通用标签”，避免强行错分。
- 保留英文标签、中文名称、说明、热度和 NSFW 标记。

## 开发与测试

运行服务不需要安装第三方 Python 包。目录分类测试可执行：

```powershell
python test_taxonomy.py
node test_migration.js
```

界面自动化测试需要 Node.js，并先安装 Playwright：

```powershell
npm install
npm run test:ui
```

Windows EXE 只是一个轻量启动器；它会查找系统 Python、`py -3`、项目内的 `python\python.exe` / `runtime\python.exe`，或环境变量 `BUBBLELENS_PYTHON` 指向的解释器。可使用 .NET Framework 自带的 C# 编译器重新编译：

```powershell
& "$env:WINDIR\Microsoft.NET\Framework64\v4.0.30319\csc.exe" /nologo /target:winexe /out:BubbleLens.exe /win32icon:assets\grimoire-logo-transparent-v2.ico /reference:System.Windows.Forms.dll BubbleLensLauncher.cs
```

## 许可证与数据来源

本项目以 [GNU GPL v3.0](LICENSE) 发布。内置 `tags_enhanced.csv` 衍生自 [DanbooruSearchOnline](https://github.com/SuzumiyaAkizuki/DanbooruSearchOnline) 与 [danbooru-tag-pipeline](https://github.com/SuzumiyaAkizuki/danbooru-tag-pipeline)；详情见 [NOTICE.md](NOTICE.md)。数据库可能包含成人或敏感文字术语，但不包含 Danbooru 图片。

## 为什么会使用本地端口

界面是 HTML/JavaScript，标签由本机 Python 读取 CSV 后提供给界面，因此需要一个仅限本机的通信地址 `127.0.0.1:7873`。这不是模型服务，也不是互联网服务；它只监听本机回环地址，外部设备无法访问。采用这个方式可以直接复用系统 Edge，避免打包大型浏览器内核，让 EXE 保持轻量。
