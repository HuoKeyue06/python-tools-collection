import pandas as pd
data = {
  '姓名': ['张三', '李四', '王五'],
  '语文': [90, 85, 88],
  '数学': [80, 75, 90],
}
df = pd.DataFrame(data)

df['总分'] = df['语文'] + df['数学']
df['平均分'] = round(df['总分'] / 2, 1)
df.to_excel('score.xlsx', index=False)
print("成绩报告.xlsx已生成")