from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.faker import Faker
# 内置主题类型可查看 pyecharts.globals.ThemeType
from pyecharts.globals import ThemeType

c = (
    Bar(
        # 初始化配置项
        init_opts=opts.InitOpts(

            # 设置宽度、高度
            width='1024px',
            height='768px',

            # 设置背景颜色
            # bg_color='#00FFCC',

            # 主题
            theme=ThemeType.LIGHT,

            # 远程 js host，如不设置默认为 https://assets.pyecharts.org/assets/"
            # 参考 `全局变量` 章节
            # js_host: str = "",

            # 图表 ID，图表唯一标识，用于在多图表时区分
            # chart_id = 'i1',

            # 设置动画
            # animation_opts=opts.AnimationOpts(animation_delay=1000, animation_easing="elasticOut"),
            # animation_opts=opts.AnimationOpts(animation=False),

            # 渲染风格，可选 "canvas", "svg"
            renderer='RenderType.CANVAS',

            # 网页标题
            page_title="Bar基本示例",
        )
    )
    .add_xaxis(Faker.choose())
    .add_yaxis("商家", Faker.values())

    .set_global_opts(title_opts=opts.TitleOpts(title="Bar基本示例", subtitle="我是副标题"),
                     toolbox_opts=opts.ToolboxOpts(is_show=True))
    .render()
)
