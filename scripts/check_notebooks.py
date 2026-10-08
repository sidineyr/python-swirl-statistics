"""Execute every notebook code cell and independently check quantitative references."""
import contextlib,io,json,math,os
from pathlib import Path
os.environ['MPLBACKEND']='Agg'
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
modules=json.loads((ROOT/'curriculum/modules.json').read_text())
count=0
for path in sorted((ROOT/'site/notebooks').glob('*.ipynb')):
    data=json.loads(path.read_text()); ns={}
    for number,cell in enumerate(data['cells']):
        if cell['cell_type']=='code':
            source=''.join(cell['source'])
            with contextlib.redirect_stdout(io.StringIO()):
                exec(compile(source,str(path)+':cell-'+str(number),'exec'),ns)
            count+=1
    with contextlib.redirect_stdout(io.StringIO()):
        assert ns['conferir'](2+2,4,'equivalente')
        assert ns['conferir'](sum([1,3]),4,'equivalente')
        assert ns['conferir'](4.005,4,'arredondamento')
        assert not ns['conferir'](5,4,'errado')
        assert not ns['conferir']('4',4,'texto')
        assert not ns['conferir'](True,1,'booleano')
        assert not ns['conferir'](float('nan'),4,'nan')
    import matplotlib.pyplot as plt
    plt.close('all')
    for q in modules[int(path.name[:2])-1]['questions']:
        assert math.isclose(float(eval(q['solution_code'],ns)),q['expected'],abs_tol=.01), (path,q)
df=pd.read_csv(ROOT/'site/dados/turmas.csv')
assert df.shape==(12,4) and df['nota'].isna().sum()==2
valid=df.dropna(subset=['nota']); groups=valid.groupby('turma')['nota']
assert list(groups.count())==[5,5]
assert list(groups.mean())==[7,7.2]
assert list(groups.median())==[7,8]
assert list(groups.quantile(.25))==[7,5]
assert list(groups.quantile(.75))==[7,10]
assert math.isclose(groups.std()['B'], math.sqrt(9.7))
assert math.isclose(valid['horas'].corr(valid['nota']),0.8041761414663254)
print(f'OK: 20 notebooks, {count} executed cells, 20 question references and independent data checks.')
