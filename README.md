1.该包可用于绘制SNP等变异位点的位置分布图，并可给SNP打上标签
主要用于绘制核心（关键）变异位点在染色体上的位置分布图

2.运行库依赖：Bio、reportlab

3.准备SNP的VCF文件，例如：test.vcf

4.准备染色体长度信息文件，例如：test_chrom_location.txt
#注：文件列顺序请勿随便改动！另外，文件可以加head也可以不加head，如果要加head请用"#"将head注释起来
	#Chr	Start	End
	A01	0	112029331
	A02	0	106041875
	A03	0	116396180

5.统一两文件的染色体名

6.直接运行DrawSNPLoc.py脚本可进行测试

7.安装：直接将DrawSNPLoc.py拖入python包库即可
