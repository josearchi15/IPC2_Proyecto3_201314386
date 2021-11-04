import matplotlib.pyplot as plt
import base64, datetime
from io import BytesIO

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x, y, title, xlabel, ylabel):
    plt.switch_backend('AGG')
    plt.figure(figsize=(6,3))
    plt.title(title)
    plt.plot(x,y,'o')
    plt.xticks(rotation=45)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    graph = get_graph()
    return graph

def toDate(fecha, separator): #dd/mm/yyyy
    arrDate = fecha.split(separator)
    day = int(arrDate[2])
    month = int(arrDate[1])
    year = int(arrDate[0])
    print(day, month, year)
    date = datetime.date(year, month, day)
    return date