# rwmapeditor-exgcdwu

___一个铁锈战争 (Rusted Warfare) 地图编辑 python 库___

![released version](https://img.shields.io/pypi/v/rwmapeditor-exgcdwu.svg)

## 目标

python实现铁锈地图文件地块编辑和宾语编辑。

暂时不打算接触地块集。

重点减轻城市争夺地图的宾语编辑工作量

基本框架已完成。

地块组框架已完成。

## 安装

```console
pip install rwmapeditor-exgcdwu
```

## 使用之前

### 1.使用地图编辑器(Tiled,notTiled)创建新地图

地图格式：zlib、gzip

渲染顺序：右下(right-down)

方向：orthogonal

#### 2.手动载入地块集

#### 3.手动创建所需的地块层和宾语层

#### 4.即可使用python库改变地块和宾语

## 简易使用例子

```python
# coding: utf-8
import rwmap as rw

map_dir = 'D:/Game/steam/steamapps/common/Rusted Warfare/mods/maps/'#此为地图所在文件夹
map_name = '[p2]example_skirmish_(2p).tmx'#输入地图
map_name_out = '[p2]example_skirmish_(2p)(1).tmx'#输出地图

mygraph:rw.RWmap = rw.RWmap.init_mapfile(map_dir + map_name)#地图载入
print(mygraph)#地图输出【部分】

mygraph.addObject(
    "Triggers", 
    {"name": "刷兵实验", "type": "unitAdd", "x": "1500", "y":"1100", "width": "20", "height": "20", "visible": "0"}, 
    {"resetActivationAfter":"5s", "spawnUnits": "heavyTank*10", "team" :"0", "warmup":"5s"})
#添加宾语：第一项图层名称（Triggers），第二项默认属性，第三项可选属性
#默认属性可添加id也可不添加，没有id项会自动添加

mygraph.addObject(
    "Triggers", 
    {"name": "刷兵实验", "type": "unitAdd", "x": "1000", "y":"1500", "width": "20", "height": "20"}, 
    {"resetActivationAfter":"5s", "spawnUnits": "heavyTank*10", "team" :"0", "warmup":"5s"})

for tobject in mygraph.iterator_object("Triggers", {"y": "1500"}):#返回属性成功匹配正则表达式的宾语（生成器）
    del tobject#宾语被删除

for tobject in mygraph.iterator_object("Triggers", {"y": "1100"}):
    tobject.assignDefaultProperty("name", "名字改变了")#宾语默认属性被赋值
    tobject.assignOptionalProperty("team", "1")#宾语可选属性被赋值
    print(tobject.returnDefaultProperty("name"))#输出宾语默认属性
    print(tobject.returnOptionalProperty("team"))#输出宾语可选属性
    tobject.deleteDefaultProperty("visible")#删除宾语默认属性
    tobject.deleteOptionalProperty("resetActivationAfter")#删除宾语可选属性

mygraph.addObject_group(rw.data.RefreshBuilding.init_building(rw.Coordinate(1500, 1000), rw.Coordinate(40, 40), 
                                               "turret", "acti_tu1", 10, 10,
                                               name_add = "城市添加", name_detect = "城市检测", 
                                               warmup_add = 10, warmup_detect = 5))
#建立一个可自动刷新的建筑

mygraph.addObject_group(rw.data.City.init_city(rw.Coordinate(1500, 1500), rw.Coordinate(40, 40), 
                                               "turret", "acti_tu2", 10, 10, "城市", textColor = "white", 
                                               textSize = 50, name_add = "城市添加", name_detect = "城市检测", 
                                               name_maptext = "城市文本", warmup_add = 10, warmup_detect = 5))
#建立一个自动刷新的城市，有名字


mygraph.addTile("Ground", rw.Coordinate(1, 0), "Long Grass", rw.Coordinate(0, 0))
mygraph.addTile("Ground", rw.Coordinate(2, 0), "Long Grass", rw.Coordinate(1, 2))
mygraph.addTile("Ground", rw.Coordinate(0, 1), "Long Grass", rw.Coordinate(0, 0))
#改变地块类型：第一项地块层名称，第二项地块层改变位置，第三项地块集名称（全名），第四项所用地块位置（在地块集中）

mygraph.addTile_square("Ground", rw.Rectangle(rw.Coordinate(5, 5), rw.Coordinate(10, 10)), "Deep Water", rw.Coordinate(0, 0))
mygraph.addTile_square("Ground", rw.Rectangle(rw.Coordinate(20, 5), rw.Coordinate(30, 10)), "Long Grass", rw.Coordinate(2, 1))
#改变地块类型（矩形）：第一项地块层名称，第二项地块层改变位置（前者为起始位置，后者为增量），第三项地块集名称（全名），第四项所用地块位置（在地块集中）

mygraph.addTile_group(rw.Coordinate(5, 20), rw.data.tile_group_grid.fill_tile_group_one_ground_water_28_24)
#改变地块类型（地块组）：第一项位置，第二项地块组（使用默认）

tilegroup_matrix = rw.tile.TileGroup_Matrix([['a'] * 6  if i % 2 == 0 else ['b'] * 6 for i in range(10)])
#创建匿名地块组
tilegroup_addlayer = rw.tile.TileGroup_AddLayer.init_tilegroup_matrix("Ground", tilegroup_matrix)
#匿名地块组确定地块层
tile_dict = {
    "a": rw.TagCoordinate("Long Grass", rw.Coordinate(0, 0)), 
    "b": rw.TagCoordinate("Dirt", rw.Coordinate(0, 0))
}
tilegroup_one = rw.tile.TileGroup_One.init_tilegroup_addlayer(
    tile_dict, tilegroup_addlayer)
#匿名地块组确定地块类型

mygraph.addTile_group(rw.Coordinate(20, 20), tilegroup_one)
#添加地块组

mygraph.write_file(map_dir + map_name_out)
#输出到新地图文件

```

## 其他

### 外部文件

本库使用了铁锈战争的默认地块集，存放在rwmap/other_data/maps/
