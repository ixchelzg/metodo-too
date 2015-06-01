from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import black, red, purple, green, maroon, brown, pink, white, HexColor
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
from reportlab.lib.validators import Auto
from reportlab.lib.colors import HexColor, black
from management.models import EquipoDeComputo, Tipo

pdf_chart_colors = [
        HexColor("#0000e5"),
        HexColor("#1f1feb"),
        HexColor("#5757f0"),
        HexColor("#8f8ff5"),
        HexColor("#c7c7fa"),
        HexColor("#f5c2c2"),
        HexColor("#eb8585"),
        HexColor("#e04747"),
        HexColor("#d60a0a"),
        HexColor("#cc0000"),
        HexColor("#ff0000"),
        ]

def setItems(n, obj, attr, values):
    m = len(values)
    i = m // n
    for j in xrange(n):
        setattr(obj[j],attr,values[j*i % m])

class BreakdownPieDrawing(_DrawingEditorMixin,Drawing):
    def __init__(self,width=600,height=400,*args,**kw):
        apply(Drawing.__init__,(self,width,height)+args,kw)
        # adding a pie chart to the drawing 
        self._add(self,Pie(),name='pie',validate=None,desc=None)
        self.pie.width                  = 300 #150
        self.pie.height                 = self.pie.width
        self.pie.x                      = 20
        self.pie.y                      = (height-self.pie.height)/2
        uno = EquipoDeComputo.objects.filter(tipo=1).count()
        dos = EquipoDeComputo.objects.filter(tipo=2).count()
        tres = EquipoDeComputo.objects.filter(tipo=3).count()
        cuatro = EquipoDeComputo.objects.filter(tipo=4).count()
        cinco = EquipoDeComputo.objects.filter(tipo=5).count()
        self.pie.data = [uno,dos,tres,cuatro,cinco]
        self.pie.labels = ['monitor','CPU','tablet','proyector','impresora']
        self.pie.simpleLabels           = 1
        self.pie.slices.label_visible   = 0
        self.pie.slices.fontColor       = None
        self.pie.slices.strokeColor     = white
        self.pie.slices.strokeWidth     = 1
        # adding legend
        self._add(self,Legend(),name='legend',validate=None,desc=None)
        self.legend.x               = 400 #200
        self.legend.y               = height/2
        self.legend.dx              = 8
        self.legend.dy              = 8
        self.legend.fontName        = 'Helvetica'
        self.legend.fontSize        = 14
        self.legend.boxAnchor       = 'w'
        self.legend.columnMaximum   = 10
        self.legend.strokeWidth     = 1
        self.legend.strokeColor     = black
        self.legend.deltax          = 75
        self.legend.deltay          = 10
        self.legend.autoXPadding    = 5
        self.legend.yGap            = 0
        self.legend.dxTextSpace     = 5
        self.legend.alignment       = 'right'
        self.legend.dividerLines    = 1|2|4
        self.legend.dividerOffsY    = 4.5
        self.legend.subCols.rpad    = 30
        n = len(self.pie.data)
        setItems(n,self.pie.slices,'fillColor',pdf_chart_colors)
        self.legend.colorNamePairs = [(self.pie.slices[i].fillColor, (self.pie.labels[i][0:20], '%0.2f' % self.pie.data[i])) for i in xrange(n)]

if __name__=="__main__": #NORUNTESTS
    drawing = BreakdownPieDrawing()
    # the drawing will be saved as pdf and png below, you could do other things with it obviously.
    drawing.save(formats=['gif','png','jpg','pdf'],outDir='.',fnRoot='piechart')
    # drawing.save(formats=['pdf','png'],outDir='.',fnRoot=None)