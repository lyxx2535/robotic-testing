# 基于机械臂视觉识别的非侵入式GUI界面自动化探索

## 1. 运行方式

### 1.1 运行要求

1.  每次运行前需要在img目录下新建input、output、output_tree目录（内容为空）

2.  img目录下已有output_click目录，若无则需新建该目录，并在该目录下新建click.txt

3.  开始运行前必须把treegraph.py中parse_json函数中的项目路径修改为本地对应的绝对路径

4.  运行时前端图片每次必须清空数据

5.  运行结束后必须删除要求1中新建目录内的所有内容

### 1.2 运行步骤

1.  运行main，弹出前端页面

![](https://docimg9.docs.qq.com/image/AgAABnOijIlt-jqAKHpCq6bA7D-gEjAt.png?w=2216&h=1374)

2.  运行main2

3.  点击上传图片，图片解析后弹出识别过程图，关闭过程图，图片节点自动添加到树图

4.  输入图片节点id，显示组件框图

5.  根据screen提示点击坐标click（x，y）确定组件，先清空GUI预览数据，再上传点击组件后的图片

6.  若点击组件后上传图片不变，根据提示点击下一个组件；若点击组件后上传图片改变，则进入下一个节点继续执行步骤4，或在合并组件后回到原节点；若点击组件后返回上一级节点，则根据提示点击回到原节点并选择下一组件。

7.  某一节点（即图片）组件全部遍历后，根据提示回到上一级节点，继续执行步骤4。

![](https://docimg7.docs.qq.com/image/AgAABnOijIkyy7nvPOBLBa01ASsKLDuF.png?w=2175&h=1126)

### 1.3 探索成果

1.树图

以主屏幕界面图片为根节点，点击后新生成页面图片为子节点生成树图，用边连接，边持有两端节点属性。图中节点为图片，节点数字为id，边上显示属性为点击父节点图片能到达子节点的组件坐标。

![](https://docimg7.docs.qq.com/image/AgAABnOijIlxTOF4HelPtKOJEnBHhU3b.png?w=1200&h=800)

2. json

图像识别后返回该图片识别出的所有组件列表及组件属性，其中组件属性按顺序分别为：组件id、组件属性、组件最小列、组件最小行、组件最大列、组件最大行（这四项即为组件占据坐标）、组件宽度、组件高度。

![](https://docimg7.docs.qq.com/image/AgAABnOijIkIH3N69EtKepoUjlIbssfY.png?w=1649&h=1094)

3.jpg

图像识别后生成标注所有组件的框图

![](https://docimg5.docs.qq.com/image/AgAABnOijImtKcylKa1K-ZXwbt3JRHHA.png?w=360&h=800)

## 2. 功能模块

### 2.1 目标识别

使用openCV+numpy库

i 屏幕识别

1. 原图：

<img src="https://docimg7.docs.qq.com/image/AgAABnOijIkl8SrT25NDc7IoFIB4OTEK.jpeg?imageMogr2/thumbnail/1600x%3E/ignore-error/1" title="" alt="" width="299">

2. 识别过程：

原图-高斯模糊-转灰度图-中值滤波-canny边缘检测-自适应阈值处理(使轮廓闭合)-提取轮廓

- 自适应阈值处理后的结果：

<img src="https://docimg7.docs.qq.com/image/AgAABnOijImtTIvZcFpIH65bWiwerlxm.png?imageMogr2/thumbnail/1600x%3E/ignore-error/1" title="" alt="" width="307">

- 检测后的结果：

<img src="https://docimg7.docs.qq.com/image/AgAABnOijIkfRoLSOl9F7Zrv-dCmD_Dw.png?imageMogr2/thumbnail/1600x%3E/ignore-error/1" title="" alt="" width="306">

3. 存在的问题：识别后的屏幕图片无法进行UI元素的识别，因此UI元素识别的图片为屏幕截图。

ii. UI元素识别

目前的目标识别主要使用了UIED库([GitHub - MulongXie/UIED: An accurate GUI element detection approach based on old-fashioned CV algorithms [Upgraded on 5/July/2021]](https://github.com/MulongXie/UIED))。

UIED库的处理流程是：

1.  原图转灰度图再转二值图

2.  检测闭合轮廓，选择其中为矩形的

3.  结果处理，合并其中较小的矩形

4.  获得所有识别出元素的坐标，写入json文件，并在图中画出。

<img src="https://docimg7.docs.qq.com/image/AgAABnOijImL51rzwhlMxpsyMQe0rxnk.png?imageMogr2/thumbnail/1600x%3E/ignore-error/1" title="" alt="" width="242">

iii. 相似页面检测

流程：关键点检测-关键点匹配(使用汉明距离)-knn筛选匹配点。再由关键点计算相似度（0=<similarity<=1），将相似度>0.5的视为相似。

### 2.2 机械臂操作

安装机械臂后，使用YamboomRobot与机械臂完成连接并进行初始化校准工作。

![](https://docimg5.docs.qq.com/image/AgAABnOijInmXaLujlRIQ7pbdFywmTuL.jpeg?imageMogr2/thumbnail/1600x%3E/ignore-error/1)

正常进行动作组执行后，机械臂舵机发生故障无法正常运转，扭矩处于关闭状态。在尝试远程连接打开总线舵机扭矩、按K1K2调整急停状态、重新设置舵机ID、烧录镜像等方式后仍无法运行，咨询客服认为涉及到底层单片机功能需要寄回检测调试。

于是我们仅了解了机械臂操作相关的API，并给出操作的处理思路。

控制6个总线舵机对对应的api为Arm_serial_servo_write6(S1, S2, S3, S4, S5, S6, time)。我们使用JupyterLab与机械臂进行远程连接，定义对应的move函数进行操作。在拍摄第一张图片后，机械臂首先进行识别定位，记忆屏幕左上角为原点位置(init_x, init_y)，记忆屏幕长度height和宽度width。之后定义move(x, y)，x和y为treegraph分析过程中产生的下一个点击位置相对于原点的长宽百分比，根据此百分比计算出机械臂在屏幕上的目标定位，映射到机械臂的六自由度控制，完成机械臂移动。

### 2.3 GUI界面探索策略

为了利用机械臂模拟真正用户对app的使用，我们未集成已有的侵入式GUI界面探索策略，而是将测试过程建模成一个个状态，利用机械臂对每个组件进行遍历操作，将页面跳转关系最终建模成树图，完成未知路径的探索，并支持已知路径的引导。

软件测试过程建模成4类对象：组件Compo、状态State、操作Action和树图TreeGraph，其中State、Action分别对应TreeGraph的Node和Edge。

1.  Compo(x, y, height, width, is_used)

    a.  x, y, height, width：相对左上角原点(0, 0)的相对坐标和高宽，范围在(0, 1)之间，百分比保留三位小数。

    b.  is_used：bool值，默认False，记录该组件是否被机械臂操作。每个组件只能被操作一次。

2.  State(screen_id, screenshot_path, compo_list)

    a.  screen_id：屏幕id，唯一标识屏幕，如10。

    b.  screenshot_path：屏幕的截图路径，保存在img/input路径下，如img/input/test10.jpg。

    c. compo_list：屏幕所有可操作组件组成的列表。

3.  Action(action_type, compo)

    a.  action_type：理论上是与机械臂操作类型一一对应的操作列表，如[click, input, roll, swipe....]。因本项目规模与时间有限，仅针对“点击”操作进行测试，故该字段定义为“click”字符串。

    b.  compo：存储本次操作的组件。

4.  TreeGraph(graph)

    a.  graph=nx.MultiDiGraph(sub_graph=True)：利用[networkx库](https://www.osgeo.cn/networkx/reference/classes/multidigraph.html)建立可以存储多边的有向图。

    b.  graph.add_node(new_state, id=new_state.screen_id)：graph的结点类型为State，属性为'id'。

    c.  graph.add_edge(curr_state, new_state, action=curr_action)：graph的边属性'action'类型为Action，连接两个State。

探索策略的基本思路是机械臂不断拍摄当前GUI界面的图片，通过目标识别算法识别所有可操作组件（存储为State的compo_list），机械臂通过DFS算法遍历操作组件，记录操作后的跳转界面，上传，如此往复获得该软件的状态转移图graph。具体流程见1.2运行步骤和项目视频，下面重点介绍DFS算法中的4种情况：

1.  点击compo后跳转的页面在树中

    a.  界面没有变化等于curr_state：本项目树图不保存自循环，继续遍历curr_state组件。（对应dfs_wrapper的case1）

    b.  界面有变化：

        i.  是curr_state的子state：说明之前已有其他compo跳转到该界面，并且该界面探索已结束。故利用State.upt_compo_list方法合并组件，如将“朋”“友”“圈”合并为“朋友圈”大组件，并更新树图边的action属性，然后继续遍历curr_state组件。（对应dfs_wrapper的case2）

        ii.  不是子state：说明形成环，并且该界面探索已结束。故只需要添加有向边，然后继续遍历curr_state组件。（对应dfs_wrapper的case3）

2.  点击compo后跳转的页面不在树中

    a.  添加点和有向边，然后进入new_state遍历组件。（对应dfs_wrapper的case4）

最终我们可以得到1.3中的探索成果，注意经过软件特性和实验观察边都是双向的，所以绘制graph时uv之间的边其实均为v->u的action类型，但存储的edges中因为有向性不会被覆盖，u->v和v->u均有。

![](https://docimg7.docs.qq.com/image/AgAABnOijIlxTOF4HelPtKOJEnBHhU3b.png?w=1200&h=800)

### 2.4 机械臂调度

1.  坐标转换

为了实现机械臂所处的实际坐标与GUI应用所处的虚拟坐标转换，我们以百分比的形式解析并存储各组件坐标，过程如下：

    1.  在探索前测量测试手机的实际宽高。

    2.  利用parse_json(json_path)函数解析每个compo的相对坐标和宽高

    3.  通过curr_action_info(curr_state, curr_action)函数获得当前compo的中心坐标百分比，可换算成实际坐标供机械臂点击。

2.  关键操作引导

虽然算法以未知路径探索为主体，但在case2、case3和compo_list全部遍历完毕时，我们需要利用已知路径信息引导机械臂到指定页面：

    1.  case3进入的界面探索已结束，需要返回curr_state。![](https://docimg1.docs.qq.com/image/AgAABnOijIn8Pfm9Y_xK76uHcfsEvsA9.png?w=2135&h=1285)

    2.  case2进入的子界面探索已结束，需要返回curr_state。![](https://docimg7.docs.qq.com/image/AgAABnOijInf4DKk2wxArqBWXDhHoizD.png?w=2017&h=1180)

    3.  当curr_staate的compo_list全部遍历完毕时，需要返回父节点。![](https://docimg5.docs.qq.com/image/AgAABnOijInSosI4XhJHSJURvhkmPI_-.png?w=1914&h=1132)

实现已知路径引导的函数为find_path(source_node, target_node)，它利用nx.all_pairs_shortest_path(graph)库函数获得任意两点间的最短路径path[source_node][target_node]，并利用image_recognition.is_similar函数跟踪用户上传的图片是否符合引导预期，若偏离则报错。

### 2.5 交互界面设计与实现

交互界面使用python的TKinter库进行实现。

![](https://docimg7.docs.qq.com/image/AgAABnOijInYVk1RwrpOlLkq60-cnKTj.png?w=2305&h=1119)

分为左中右三个部分。

- 第一部分：GUI预览与图片上传。测试者可以点击上传图片，上传对应的屏幕GUI，点击清空数据将当前预览图片清空，但由于图片已进行上传，清空数据不影响后续树图执行，仅对当前GUI预览产生影响。（若使用机械臂进行操作，则同样使用定时捕捉图片信息更新的情况来获得机械臂拍摄的图片）

- 第二部分：实时操作指令与树图展示。实时捕捉click.txt信息的变更和树图的更新情况并进行展示。clicktxt中的信息指示了应当进行操作的屏幕和屏幕内点击位置。坐标(x,y)中的x代表相对于屏幕宽度的百分比（以屏幕左侧为起点），y代表相对于屏幕高度的百分比（以屏幕顶部为起点）。

- 第三部分：组件框图查询。该部分主要用于让测试者可以随时查询已经生成的识别后组件框图，用于方便定位或分析。在上方输入框内输入序号即可得到对应的组件框图（若未查找到对应图片则无显示）

交互界面形成后的展示效果如下。相关代码主要位于tkinterGUI.py中，使用main.py启动。

![](https://docimg3.docs.qq.com/image/AgAABnOijIlAT9guPXJPCaKIFkMYZ06I.png?w=2316&h=1117)

## 3. 模块间的交互

- treegraph中调用img_rec is_similar

img_rec()与is_similar()均为图像识别类image_recognition.py中的函数，其作用分别为图像识别与判断两图片是否相同，treegraph类通过from image_recognition import img_rec, is_similar调用函数，执行相关操作。

- treegraph中的get_newest_img_path，get_upload

前端上传图片后，图片会通过tkinterGUI中的方法存入img目录下的input目录中，treegraph中的get_newest_img_path()函数可通过时间戳判断目录下最新添加的文件，并返回该最新文件，get_upload()调用该函数并赋值返回，即获取到前端上传的最新截图。

- tkinterGUI中的交互

由于TKinter运行时使用mainloop陷入主循环，无法调用其他函数，因此使用了Tk类提供的after方法，在每个规定时间间隔后执行update函数。识别clicktxt和output_tree中的更新内容并显示到GUI界面。

## 4. 不足与展望

由于时间、规模和能力限制，本项目存在以下不足：

- 未使用机械臂进行操作：因为机械臂损坏的问题，我们用人为操作代替，加入了“显示组件框图”作为辅助。但目前的建模（如坐标以百分比表示）是完全可以支持机械臂自主探索的。

- 目标识别在识别屏幕后无法进行UI元素的识别：暂时使用屏幕截图代替。

- 操作类型只有click，未定义组件类型：项目初期我们计划使用机器学习算法识别组件类型，如[button, input]，但因算法效果不佳停滞。操作本来计划参考RoScript设置[click, swipt, input]多种类型，并与组件类型对应，但因开销较大（仅有click就需要处理上千张输入图片），技术难度大（input用机械臂较难）停滞。

- 在进行已有树图的引导时未处理偏移：目前find_path函数跟踪到用户偏离后，未重新规划路线，而是直接报错。这与探索阶段树图构建不完整、算法复杂度增大均有关联。

这些不足是项目未来的发展方向，我们期望用更丰富的知识储备进行优化。
