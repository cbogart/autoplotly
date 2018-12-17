import csv
import click
from colorhash import ColorHash
from random import random
from dateutil.parser import parse
import plotly
import plotly.graph_objs as go
from collections import defaultdict

def pragmatic(row):
    try: row["issueid"] = int(float(row["issueid"]))
    except: pass

@click.command()
@click.argument('csvfiles', type=click.File('rb'), nargs=-1)
@click.option('-o', '--output', type=click.Path(), help="output html file for plotly", default="outfile.html")
@click.option('-h', '--horizontal', type=str, help="Column name for horizontal time axis")
@click.option('-v', '--vertical', type=str, help="Column name for vertical separation of timelines")
@click.option('-f', '--filter', type=str, help="column=val1,val2,val3")
@click.option('-c', '--color', type=str, help="column name for color")
@click.option('-l', '--label', type=str, help="column name for label")
@click.option('-t', '--title', type=str, help="Title", default="(title)")
#@click.option('-s', '--shape', type=str, help="column name for shape of icon")
def main(csvfiles, horizontal, vertical, title, color, output,label,filter): 
    print(horizontal,vertical,color,title,label)
    hbounds = (0,0)
    vert = defaultdict(lambda: {"label": [], "color": [], "x":[], "y":[]})   # vertkey -> x:xs, y:ys
    if filter is not None:
        (key,vals) = filter.split("=")
        vals = vals.split(",")
        filter = lambda row: str(row[key]) in vals
    else:
        filter = lambda row: True
    for csvfile in csvfiles:
        incsv = csv.DictReader(csvfile)
        for row in incsv:
            pragmatic(row)
            time = parse(row[horizontal])
            vtick = row[vertical]
            if not filter(row): continue
            vert[vtick]["x"].append(time)
            if label is not None and label in row:
                vert[vtick]["label"].append(row[label])
            else:
                vert[vtick]["label"].append(None)
            if color is not None and color in row:
                vert[vtick]["color"].append(ColorHash(row[color]).hex)
            else:
                vert[vtick]["color"].append(None)
    data = [go.Scatter(x=vert[vtick]["x"], text=vert[vtick]["label"], y=[vtick  for item in vert[vtick]["x"]], 
              marker = { "color": vert[vtick]["color"]}, mode="markers", name=vtick) for vtick in sorted(vert.keys())]        
    plotly.offline.plot({"data": data},{"title": title}, filename=output, auto_open=True)

def example2():
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
    
    for i in range(len(cases)):
        ax.plot(yy[:, i], marker='o', label=str(cases[i]))
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    
    plt.title('Support for axes.prop_cycle cycler with markevery')

    plt.show()

def example():
    link = dwg.add(dwg.a("http://link.to/internet"))
    square = link.add(dwg.rect((0, 0), (1, 1), fill='blue'))
    
    # draw a red box
    dwg.add(dwg.rect((10, 10), (300, 200),
        stroke=svgwrite.rgb(10, 10, 16, '%'),
        fill='red')
    )
    
    # Draw a small white circle in the top left of box
    dwg.add(dwg.circle(center=(25,25),
        r=10, 
        stroke=svgwrite.rgb(15, 15, 15, '%'),
        fill='white')
    )
    dwg.save()

if __name__ == '__main__':
    main()
