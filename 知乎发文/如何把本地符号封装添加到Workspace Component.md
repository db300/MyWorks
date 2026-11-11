# 如何把本地符号封装添加到 Workspace Component？

这事儿其实不复杂，先搞清楚一个概念：Workspace Component 不是"把 SchLib 拷到云端"，而是把符号、封装、3D 模型打包成一个带版本号、带生命周期的托管元件。所以加进去的方式分两种情况：

## 一、就加几个器件：右键迁移就完事了

不用开什么导入工具：

1. 先确认 AD 右上角已经连上你的 Workspace。
2. 打开本地的 SchLib，在库面板里右键那个器件，选 **Migrate to Server**。
3. 确认下扔到哪个文件夹、元件类型是啥，符号封装会自己跟过去，不用你操心。
4. 完事。去浏览器端 Workspace 的 Components 页面就能看到它，已经是带版本的托管元件了。

要是你 AD 版本老、没这个选项，也行：在 Components 面板里新建一个托管元件，手动把本地符号、封装指定成它的模型，再 Release 一样。

## 二、整个库批量搬：这才轮到 Library Importer

1. **File » Library Importer** 打开向导。
2. 把你的 .SchLib / .PcbLib / .IntLib 一股脑加进去。
3. 选模式：
   - **Simple**：库本身整理得比较规范，一键跑完；
   - **Advanced**：库比较乱、器件没分类，选这个，能逐个补元件类型、改参数、指定放到哪个文件夹。
4. 跑导入。向导会自动把符号、封装、3D 模型拆开传到 Workspace 各自的模型库里，重复的模型会自动合并，不会传两份。
5. 导完一定要去网页端抽查一下：分类对不对、封装关联上没、3D 模型丢没丢。

## 三、老项目别忘了同步

库是迁了，但老图纸里用的还是本地引用。打开项目，**Tools » Item Manager**，配好匹配规则点 Auto Match，审一眼结果再 Update，图纸里的器件就批量换成托管版本了。

## 几个坑，提前说

- 前提是你得有 Workspace 的编辑权限，AD 版本建议 21 以上；
- 导入前先在网页端把文件夹结构和生命周期想好，不然几千个器件导进去再分类，想死的心都有；
- 正式迁移前拿个小库试跑一次，Simple 和 Advanced 各试一遍，确认参数映射没问题再全量上。

一句话总结：**几个就右键 Migrate to Server，一批就 File » Library Importer，迁完用 Item Manager 把老项目里的引用换掉。** 搞定。

---

参考资料：

- [Importing Existing Libraries to Your Connected Workspace - Altium Documentation](https://www.altium.com/documentation/altium-designer/components-libraries/importing-existing-libraries-workspace)
- [KB: Replace Local Project Components with Workspace or Server-Managed Components](https://www.altium.com/documentation/knowledge-base/altium-designer/replace-local-project-components-with-workspace-or-server-managed-components)
- [Library Migration: Onboarding Guide - Altium Resources](https://resources.altium.com/p/library-migration-onboarding-guide)
- [Components and Library Management Tutorial](https://resources.altium.com/p/components-and-library-management-tutorial)
