---
name: "华北活动日历订阅页" # 我们定的 —— 本次为两个独立订阅页面命名
colors:
  primary: "#92382F" # 我们定的 —— 规范主色，等同订阅行动强调色
  paper: "#F3EFE5" # 我们定的 —— 选定的黄色刊物底色
  paper_deep: "#E7E0D2" # 我们定的 —— 分区与选中态的纸张层次
  ink: "#292820" # 我们定的 —— 长文阅读用的深墨色
  ink_muted: "#625D52" # 我们定的 —— 辅助说明与元数据
  crimson: "#92382F" # 我们定的 —— 行动、票务与当前状态强调色
  rule: "#C8C0B2" # 我们定的 —— 刊物式分隔线
  surface: "#FFFDF8" # 我们定的 —— 表单与复制链接承载面
typography:
  display:
    fontFamily: 'Georgia, "Songti SC", "STSong", serif' # 我们定的 —— 中西文都可用的刊物标题字族
    fontSize: 3.125rem # 我们定的 —— 桌面主标题上限
    fontWeight: 700 # 我们定的 —— 标题使用可获得的粗体档
    lineHeight: 1.13 # 我们定的 —— 两行中文标题的紧凑行距
    letterSpacing: 0em # 我们定的 —— 中文标题不使用负字距
  heading:
    fontFamily: 'Georgia, "Songti SC", "STSong", serif' # 我们定的 —— 分区标题字族
    fontSize: 1.75rem # 我们定的 —— 分区标题尺寸
    fontWeight: 700 # 我们定的 —— 分区标题字重
    lineHeight: 1.25 # 我们定的 —— 中文分区标题行距
    letterSpacing: 0em # 我们定的 —— 中文分区标题字距
  body:
    fontFamily: 'Inter, "PingFang SC", "Noto Sans SC", sans-serif' # 我们定的 —— 操作文本与中文正文
    fontSize: 1rem # 我们定的 —— 正文基准字号
    fontWeight: 400 # 我们定的 —— 正文字重
    lineHeight: 1.8 # 我们定的 —— 中文正文可读行距
    letterSpacing: 0em # 我们定的 —— 正文字距
  meta:
    fontFamily: 'ui-monospace, "SFMono-Regular", Menlo, monospace' # 我们定的 —— 订阅地址与数据状态
    fontSize: 0.8125rem # 我们定的 —— 辅助地址字号
    fontWeight: 400 # 我们定的 —— 地址字重
    lineHeight: 1.5 # 我们定的 —— 长链接换行行距
    letterSpacing: 0em # 我们定的 —— 代码式地址字距
spacing:
  content_max_width: 72rem # 我们定的 —— 桌面阅读版心上限
  reading_width: 46rem # 我们定的 —— 引导文与清单的舒适阅读宽度
  page_padding: 1.5rem # 我们定的 —— 小屏两侧留白基准
  section_gap: 4.5rem # 我们定的 —— 主分区之间的刊物留白
  grid_gap: 1rem # 我们定的 —— 表单与卡片间距
rounded:
  panel_radius: 0rem # 我们定的 —— 刊物语言采用直角面板
  control_radius: 0.375rem # 我们定的 —— 仅让可点击控件保留轻微圆角
components:
  page:
    backgroundColor: "{colors.paper}" # 我们定的 —— 全页黄色纸张背景
    textColor: "{colors.ink}" # 我们定的 —— 全页主文本颜色
    typography: "{typography.body}" # 我们定的 —— 全页正文排版
    padding: "{spacing.page_padding}" # 我们定的 —— 页面内边距
  status:
    backgroundColor: "{colors.paper_deep}" # 我们定的 —— 数据状态底色
    textColor: "{colors.ink_muted}" # 我们定的 —— 数据状态文字
    typography: "{typography.meta}" # 我们定的 —— 状态信息排版
  divider:
    backgroundColor: "{colors.rule}" # 我们定的 —— 刊物式分隔线颜色
    height: 0.0625rem # 我们定的 —— 分隔线厚度
  primaryAction:
    backgroundColor: "{colors.primary}" # 我们定的 —— 主订阅行动颜色
    textColor: "{colors.surface}" # 我们定的 —— 主按钮文本颜色
    height: 2.75rem # 我们定的 —— 触控与鼠标均易操作的高度
    rounded: "{rounded.control_radius}" # 我们定的 —— 主按钮圆角
  secondaryAction:
    backgroundColor: "{colors.surface}" # 我们定的 —— 次要按钮底色
    textColor: "{colors.ink}" # 我们定的 —— 次要按钮文字
    height: 2.75rem # 我们定的 —— 次要按钮高度
    rounded: "{rounded.control_radius}" # 我们定的 —— 次要按钮圆角
  subscriptionRow:
    backgroundColor: "{colors.surface}" # 我们定的 —— 日历链接承载面
    textColor: "{colors.ink}" # 我们定的 —— 订阅行文字颜色
    typography: "{typography.body}" # 我们定的 —— 订阅行排版
    rounded: "{rounded.panel_radius}" # 我们定的 —— 订阅行保持直角
  ticketLink:
    backgroundColor: "{colors.crimson}" # 我们定的 —— 票务链接强调色
    textColor: "{colors.surface}" # 我们定的 —— 票务链接文字色
    rounded: "{rounded.control_radius}" # 我们定的 —— 票务链接圆角
---

## Overview

用户在电脑或手机上选择日历源并将其加入自己的日历客户端；网页只负责清楚地引导订阅、展示时间地点与购票去向，不承担把漫展和其他活动混成一张活动资讯流的角色。漫展订阅页与华北活动订阅页是两个独立 URL、独立数据源、独立日历源；页面之间只保留克制的互相跳转链接。

选择的是“取其神”样张：像一页浅黄色活动刊物，而不是紫色工具面板或深色数据驾驶舱。关键是让用户先知道自己订阅的是什么，再一键拿到可复制的 ICS 地址或交给 Google / Apple Calendar。

## Colors

浅黄纸张是背景，不做大面积渐变、纹理或插画。深墨文字负责阅读，砖红色只标出主行动、票务、当前选择与少量状态。所有信息层次优先通过留白、字级和细分隔线建立；不要用多种彩色标签制造“活动很多”的错觉。

## Typography

中文标题使用宋体感衬线字族，正文与控制项使用系统无衬线。主标题在实际页面用 `clamp(2.2rem, 6vw, 3.125rem)`，而 YAML 只锁定上限；小屏不应因追求海报感而牺牲城市名称可读性。中文正文保持 1.8 倍行距；中西文混排预留约 0.25em 的视觉呼吸，不使用负字距，也不依赖 500 这种可能被合成的中文字重。

订阅地址、更新时间与事件编号使用等宽字体，允许自动换行，不以省略号截断真正需要复制的 URL。

## Layout

页面采用单列刊物式版心：页首为产品名、数据说明和另一个订阅页的文本链接；第一主区是“订阅全部”活动源，第二主区是按城市选择，第三主区用真实事件样本说明最终进入日历的信息。桌面上地址、按钮与状态可并排，小屏自动纵向排列。

城市选择不是标签云：每项均是一个完整、可勾选的说明行，并在选中后出现相应的订阅地址和日历客户端操作。保定即使暂时没有已核验活动，也保留独立订阅入口并明确说明“后续新增会自动出现”。

## Elevation & Depth

常规内容不使用浮起卡片。以纸张层次、细横线和左侧编号形成层级；只有短暂的“已复制”反馈可以使用轻阴影，且不遮挡订阅链接。不要把每个城市、事件或功能都包进有阴影的圆角卡片。

## Shapes

版面边界、分隔线和事件清单保持方正、克制。按钮和复选框可以有极小圆角，帮助识别为可操作控件；圆角不承担装饰职责。边框使用单层细线，避免双边框、虚线框或渐变描边。

## Components

“加入全部活动”是页面唯一的高强调主行动，旁边始终提供复制 URL、Google Calendar 与 Apple Calendar 三种等价路径。城市订阅行遵循相同操作顺序，并显示该城市已核验条目数和最近更新时间。

事件预览必须使用真实已核验数据，逐项露出日期/时间、场地、城市；有票务链接时显示“购票”，没有时显示“查看来源”。数据状态、来源与去重边界放在订阅源说明中：活动页排除漫展、同人展、动漫展等已由漫展订阅覆盖的内容。

可访问性是组件规格的一部分：所有按钮保留清晰键盘焦点、文字对比度足够、触控高度不低于 YAML 中锁定的高度；图标只作辅助，不能替代“复制 / Google / Apple / 购票”等可见文字。

## Do's and Don'ts

### Do's

- 用一句明确的产品说明区分“漫展订阅”与“活动订阅”，让用户在点击前就知道将添加哪个日历源。
- 让每个订阅源提供稳定的 ICS URL，并把日期、地点、来源和可用的购票链接写进日历事件本身。
- 用真实数据、更新时间和空城市状态建立可信度，而不是伪造热闹的活动数量。

### Don'ts

- ❌「漫展订阅一个页面，活动订阅一个页面。」— 用户明确否决把两个订阅源合到同一页面或同一筛选器里。
- ❌「按那个黄色的来吧。」— 用户选择黄色刊物方案，因此不采用“贴着做”的紫色面板或“反着来”的深色数据台。
- 不把漫展、同人展、动漫展、二次元、Cosplay 内容写入华北活动日历，避免与漫展订阅重复。
- 不把票务聚合页、社交转发页当作购票链接；没有官方票务链接时宁可只留来源链接。

## 什么时候别用这套

当产品需要高密度的运营后台、分钟级实时调度、复杂地图浏览或大量图片售卖时，不要套用这份刊物式单列设计；它会让筛选和监控效率下降。此时应另建数据工作台或票务详情页，而不是在订阅页上不断叠加筛选器、图表和促销模块。

## 实现时的创意指令

在尊重本文件已确认的设计方向、真实内容和用户原话约束的前提下，充分发挥你的设计创造力。

开始实现前，用工具生成一串随机字母与数字，从其中的组合、节奏和联想中寻找灵感，用于尚未确定的构图、排版、色彩、图像和交互设计。随机字符串仅供创作启发，不要出现在页面中。

大胆做出具体、有个性的设计选择，尝试你通常不会首先采用的表达。需要时使用图片生成来实现关键视觉。运用你的判断，让这些选择形成一个完整、有吸引力、适合这个产品的设计。
