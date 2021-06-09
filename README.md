# Bitmap-Font / Dot-Matrix Font Generator 位图字体产生器

位图字型产生器，用于从点阵字库里抽取特定文字的点阵信息后，存到一个较小的文件中，适合嵌入式开发使用。

环境依赖：

需要安装 python3 和 numpy

使用方式：

```
$ python3 bmpfnt-gen.py [-h] [-f FONT_FILE] [-i INPUT] [-o OUTPUT]

参数:
  -h, --help            显示帮助
  -f FONT_FILE, --font-file FONT_FILE
                        点阵字体文件。默认值：fonts/HZK12
  -i INPUT, --input INPUT
                        包含所需文字的输入文件。默认值：input.txt
  -o OUTPUT, --output OUTPUT
                        输出的点阵文件。默认值: hzk12.fnt
```

由于涉及版权问题，本仓库并不包含存放点阵字型文件的 *fonts* 目录。大家可以到以下第三方链接进行下载、解压缩后使用。

点阵字库[下载](https://pan.baidu.com/s/1xFEAaoPXqvc5q-mo1q8UaA)，网盘提取码：n3wr
