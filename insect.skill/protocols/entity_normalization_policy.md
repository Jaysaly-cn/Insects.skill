# Entity Normalization Policy

本文档定义农业昆虫 Skill 中害虫实体的命名和标识规范。

## 1. pest_id 命名规则

### 1.1 基本规则

```
pest_id = 拉丁属名_拉丁种名
```

- 全部小写
- 属名和种名之间用下划线连接
- 不包含命名人和年份
- 不包含亚种信息（亚种单独建立 pest_id）

### 1.2 示例（仅供格式参考，非真实数据）

| 中文名 | 拉丁名 | pest_id |
|--------|--------|---------|
| (示例) | Genus species | genus_species |
| (示例) | AnotherGenus anotherSpecies | anothergenus_anotherspecies |

### 1.3 特殊情形

- **亚种**: 在基础 pest_id 后追加 `_subsp_` + 亚种名
  - 格式: `genus_species_subsp_subspeciesname`
- **同物异名**: 以最新接受的学名为 pest_id，旧学名列入 aliases
- **未定种**: 使用 `genus_sp` 或 `genus_sp_n`（n 为序号）
- **复合种**: 使用 `genus_species_complex`

## 2. 名称优先级

### 2.1 中文名

优先级：

1. 全国科学技术名词审定委员会公布的昆虫学名词
2. 《中国动物志》中使用的中文名
3. 中国农业农村部官方资料使用的中文名
4. 广泛使用的通用中文名

当一个害虫有多个中文名时：

- `name_cn` 填写最高优先级名称
- `aliases` 记录其他中文名

### 2.2 拉丁学名

优先级：

1. Catalogue of Life (COL) 接受的学名
2. GBIF 接受的学名
3. CABI 使用的学名
4. 最新分类学文献使用的学名

记录时包含命名人和年份，如: `Genus species Author, Year`

### 2.3 英文名

- 以 CABI、FAO 使用的英文名为准
- 无标准英文名时可留空

## 3. 别名处理

`aliases` 字段用于记录以下类型的别名：

- 中文俗名、方言名
- 历史曾用名、同物异名
- 常见拼写变体
- 数据集标签名

格式：

```yaml
aliases:
  - "俗名示例"
  - "ap162:label_example"
  - "insectagent:id_example"
```

## 4. 外部数据集标签映射

### 4.1 映射原则

当接入外部数据集（AP162、InsectAgent 等）时，不改变 pest_id，而是在 aliases 中记录外部标识符。

### 4.2 映射格式

```
aliases:
  - "ap162:<label_name>"
  - "insectagent:<entity_id>"
  - "ip102:<class_index>"
```

### 4.3 映射流程

1. 获取外部数据集的类别列表或实体列表
2. 逐一匹配到已有 pest_id，或为基础明确的实体创建新 pest_id
3. 在 aliases 中记录映射关系
4. 将映射记录存入 `data/` 下的索引文件
5. 无法明确匹配的条目标注 `unmapped`，暂不入库

### 4.4 冲突处理

当同一外部标识符可能对应多个 pest_id 时：

- 标注为 `ambiguous`
- 不强行映射
- 记录在 `data/staging/` 留待人工判断

## 5. 规范化脚本

`scripts/normalize_pest_name.py` 提供基础字符串清洗功能，未来可扩展别名解析。

规范化步骤：

1. 去除首尾空白
2. 合并连续空格为单个空格
3. 可选的小写转换
4. 未来：查找别名映射表，输出规范名称

## 6. 当前状态

- 命名规则: 已定义
- 别名映射表: 为空
- 外部数据集标签: 未接入
- 冲突条目: 无
