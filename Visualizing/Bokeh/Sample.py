import numpy as np
from bokeh.plotting import figure, show, output_notebook

#output_notebook()

# generate data
data = np.random.random_sample((5,2)) * 10
print(data)

# set x, y
x = data[:,0]
y = data[:,1]


def mscatter(p, x, y, marker="circle", size=5,
               line_color="navy", fill_color="orange" , alpha=0.5):
    p.scatter(x, y, marker=marker, size=size,
        line_color= line_color, fill_color= fill_color, alpha=alpha)

def mtext(p, x, y, text):
    p.text(x, y, text=[text],
           text_color="firebrick", text_align="center", text_font_size="10pt")

# set figure
p = figure(title="Bokeh Markers")
p.grid.grid_line_color = None
p.background_fill_color = "white"
p.width = 400
p.height = 400

# scatter plot
mscatter(p, x, y)

# annotation
for idx in range(data.shape[0]):
    x_ = data[idx,0] + 0.05
    y_ = data[idx,1] + 0.05
    text = 'point #{}'.format(idx+1)
    mtext(p, x_, y_, text)

# show
show(p)

# resize
p.width = 200
p.height = 200

# show
show(p)