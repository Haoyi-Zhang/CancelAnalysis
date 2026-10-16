"""Vector drawing primitives; copied into each independent project generator."""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch

plt.rcParams.update({'font.family':'STIXGeneral', 'mathtext.fontset':'stix',
                     'font.size':9, 'pdf.fonttype':42, 'ps.fonttype':42,
                     'text.usetex':False, 'axes.unicode_minus':False})
CM = 1 / 2.54

class Drawing:
    def __init__(self, bounds):
        x0,y0,x1,y1 = bounds
        self.fig = plt.figure(figsize=((x1-x0)*CM,(y1-y0)*CM))
        self.ax = self.fig.add_axes([0,0,1,1], xlim=(x0,x1), ylim=(y0,y1))
        self.ax.set_aspect('equal'); self.ax.axis('off')
        self.nodes = {}
        self.labels = []

    def text(self,x,y,label,size=9,ha='center',va='center'):
        artist=self.ax.text(x,y,label,fontsize=size,ha=ha,va=va,
                            linespacing=1.15,clip_on=False,zorder=4)
        self.labels.append([artist,None])
        return artist

    def box(self,name,x,y,w,h,label,dashed=False,shape='rect',size=9):
        style = {'edgecolor':'black','facecolor':'white','linewidth':.55,
                 'linestyle':(0,(4,3)) if dashed else 'solid', 'zorder':2}
        if shape == 'diamond':
            obj = Polygon([(x-w/2,y),(x,y+h/2),(x+w/2,y),(x,y-h/2)],**style)
        elif shape == 'circle': obj = Circle((x,y),w/2,**style)
        else: obj = Rectangle((x-w/2,y-h/2),w,h,**style)
        self.ax.add_patch(obj); self.text(x,y,label,size)
        self.labels[-1][1]=(x-w/2,y-h/2,x+w/2,y+h/2)
        self.nodes[name] = (x,y,w,h,shape)

    def point(self,name,side):
        x,y,w,h,_ = self.nodes[name]
        return {'n':(x,y+h/2),'s':(x,y-h/2),'e':(x+w/2,y),
                'w':(x-w/2,y),'nw':(x-w/2,y+h/2),
                'ne':(x+w/2,y+h/2),'c':(x,y)}[side]

    def line(self,points,dashed=False):
        xs,ys=zip(*points)
        self.ax.plot(xs,ys,color='black',linewidth=.55,
                     linestyle=(0,(4,3)) if dashed else 'solid',zorder=1)

    def arrow(self,p,q,dashed=False,via=()):
        points=[p,*via,q]
        if via:self.line(points[:-1],dashed)
        self.ax.add_patch(FancyArrowPatch(points[-2],points[-1],
                         arrowstyle='-|>',mutation_scale=7.5,linewidth=.55,
                         color='black',shrinkA=0,shrinkB=0,
                         linestyle=(0,(4,3)) if dashed else 'solid',zorder=1))

    def edge(self,a,b,sa='s',sb='n',**kwargs):
        self.arrow(self.point(a,sa),self.point(b,sb),**kwargs)

    def frame(self,x,y,w,h):
        self.ax.add_patch(Rectangle((x,y),w,h,fill=False,edgecolor='black',
                                   linewidth=.55,linestyle=(0,(4,3)),zorder=0))

    def save(self,out,name):
        # Fixed physical canvas: do not enlarge or rasterize the scientific figure.
        self.fig.canvas.draw()
        renderer=self.fig.canvas.get_renderer()
        x0,x1=self.ax.get_xlim();y0,y1=self.ax.get_ylim()
        for artist,node in self.labels:
            b=artist.get_window_extent(renderer).transformed(self.ax.transData.inverted())
            if b.x0<x0-.02 or b.x1>x1+.02 or b.y0<y0-.02 or b.y1>y1+.02:
                raise ValueError(name+': clipped label '+repr(artist.get_text()))
            if node and (b.x0<node[0]-.02 or b.x1>node[2]+.02 or b.y0<node[1]-.02 or b.y1>node[3]+.02):
                raise ValueError(name+': label exceeds node '+repr(artist.get_text()))
        self.fig.savefig(out/(name+'.pdf'),format='pdf',
                         metadata={'Creator':'Python Matplotlib','Producer':None,
                                   'CreationDate':None,'ModDate':None})
        plt.close(self.fig)

def masking(out):
    # Atom interchange is an involution; both local identity-transport
    # squares fail on an atom, while both composite tables are identity.
    identity = tuple(range(4))
    swap = (0, 2, 1, 3)
    assert tuple(swap[swap[x]] for x in range(4)) == identity
    assert swap != identity
    d = Drawing((-0.9, -3.15, 6.9, .65))
    for row, y in [('P', 0), ('Q', -1.5)]:
        for i, x in enumerate((0, 3, 6)):
            d.text(x, y, '$L('+row+')$')
            d.nodes[row+str(i)] = (x, y, 1.1, .38, 'rect')
    for row, y, label, dy in [('P', 0, r'$\mathrm{id}$', .30),
                              ('Q', -1.5, '$s$', -.28)]:
        for i, x in enumerate((0, 3)):
            d.edge(row+str(i), row+str(i+1), 'e', 'w')
            d.text(x+1.5, y+dy, label)
    for i, x in enumerate((0, 3, 6)):
        d.edge('P'+str(i), 'Q'+str(i))
        d.text(x+(.30 if i==2 else -.30), -.75, r'$\mathrm{id}$',
               ha='left' if i==2 else 'right')
    d.text(3, -2.7, '$Y$')
    d.arrow((3, -1.72), (3, -2.48), dashed=True)
    d.text(3.26, -2.1, '$q$', ha='left')
    d.save(out, 'masking')


def observations(out):
    d = Drawing((-2.25, -1.0, 7.3, 2.45))
    points = ((0, 0), (-1.1, 1), (1.1, 1), (0, 2))
    for offset, values, caption in [
        (0, tuple(x.bit_count() for x in range(4)), r'$r(I)=|I|$'),
        (5, tuple(int(bool(x & 1)) for x in range(4)),
         r'$q_{\{a\}}(I)=|I\cap\{a\}|$')]:
        for i, (x, y) in enumerate(points):
            d.text(offset+x, y, '$'+str(values[i])+'$')
        for i,j in ((0,1),(1,3),(3,2),(2,0)):
            x,y=points[i]; u,v=points[j]
            # Leave the values clear of the Hasse edges.
            d.line([(offset+x+.16*(u-x),y+.16*(v-y)),
                    (offset+u-.16*(u-x),v-.16*(v-y))])
        d.text(offset-1.5, 1, r'$\{a\}$', ha='right')
        d.text(offset+1.5, 1, r'$\{b\}$', ha='left')
        d.text(offset, -.65, caption)
    rank=tuple(x.bit_count() for x in range(4))
    atom=tuple(int(bool(x & 1)) for x in range(4))
    assert rank[1] == rank[2] and atom[1] != atom[2]
    assert atom[0] == atom[2]  # flattened comparable pair
    assert all(rank[x] < rank[y] for x in range(4) for y in range(4)
               if x != y and x & y == x)
    d.save(out, 'observations')


def generate(out):
    out.mkdir(parents=True, exist_ok=True)
    masking(out)
    observations(out)


def main():
    import tempfile
    parser=argparse.ArgumentParser(description='Rebuild the two finite-interface vector diagrams directly in Python.')
    parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--check',action='store_true',help='Check mathematical labels and deterministic fresh generation.')
    args=parser.parse_args()
    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            a,b=Path(tmp)/'a',Path(tmp)/'b'
            generate(a); generate(b)
            for name in ('masking.pdf','observations.pdf'):
                if (a/name).read_bytes() != (b/name).read_bytes():
                    raise SystemExit('Non-deterministic figure: '+name)
        print('Two diagrams: mathematical relations and deterministic fresh generation passed.')
    else:
        generate(args.output_dir)
        print('Wrote masking.pdf and observations.pdf')


if __name__=='__main__':
    main()

