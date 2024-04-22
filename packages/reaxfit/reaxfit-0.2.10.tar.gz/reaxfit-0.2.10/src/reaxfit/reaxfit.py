from lammps import lammps
import json,os,sys,re
import numpy as np
from scipy.optimize import differential_evolution, minimize

# global parameters are required for multiprocessing
def wrap_eval(): pass
def dump_best(): pass
default_option={
            "refE_file":"refE", # reference energy file
            "refF_file":"refF", # reference force norm file
            "ref_eV":True, # units for reference energy is in eV
            "relative_force":True, # force norms are relative as refE
            "force_weight":1e-6, # penalty weight for force norms
            "harmonic":0, # harmonic constraint on initial parameters
            "datafile":"data0", # data file with initial structure
            "initfile":"ffield.temp", # initial template file
            "midfile":"ffield.currentbest", # intermediate file
            "endfile":"ffield.end", # final file
            "bound":0.1, # define range of parameters with "{"
            "bound2":0.1, # define range of parameters  with "["
            "stopfile":"STOP", # file for early stopping
            "seed":None, # seed for random number
            "tol":0.01, # tolerance for convergence
            "workers":4, # number of cpus
            "maxiter":1000, # maximum number of iteration
            "optimizer":"differential_evolution", # maximum number of iteration
            "scrdir":"scr", # scratch directory
            "uniform":"False"
}

class reaxfit():
  def __init__(self,cfile="config.json"):
    self.cfile=cfile
    self.option=default_option
    return

  def changes(self,para,file_name,atm1,atm2,numbers):
    with open(file_name) as f:
        text=f.read().splitlines()
    general =text[1].split()
    generals = int(general[0]) + 1
    atom=text[generals+1].split()
    atoms = int(atom[0])*4 +1 +3
    x = generals +atoms
    j=1 
    atm=[]
    atm_dict={}
    while j <= int(atom[0]):
        y = text[generals+1+j*4].split()
        atm.append(y[0])
        atm_dict[y[0]]=j
        j+=1
    bonds=text[x+1].split()
    bond_max =int(bonds[0])*2+2+x
    #print(x)
    i=x+1
    while i <= bond_max:
        regax=re.compile(f"^\s*{atm_dict[atm1]}\s+{atm_dict[atm2]}\s|^\s*{atm_dict[atm2]}\s+{atm_dict[atm1]}\s")
        fire=regax.findall(text[i])
        if len(fire) != 0:
            #print(i)
            #print(text[i])
            #print(text[i+1])
            d = text[i].split()
            if numbers <= 8:
                if d[numbers+1].startswith("{") or d[numbers+1].startswith("["):
                    pass
                elif para=="{":
                    d[numbers+1]="{"+d[numbers+1]
                    print(text[i])
                    print(d[numbers+1])
                else:
                    d[numbers+1]="["+d[numbers+1]
                    print(text[i])
                    print(d[numbers+1])
                result =" ".join(d)
                gyou = i
            else:
                i+=1
                gyou = i
                d = text[i].split()
                if d[numbers-9].startswith("{") or d[numbers-9].startswith("["):
                    pass
                elif para=="{":
                    d[numbers-9]="{"+d[numbers-9]
                    print(text[i])
                    print(d[numbers-9])
                    i-=1
                else:
                    d[numbers-9]="["+d[numbers-9]
                    print(text[i])
                    print(d[numbers-9])
                    i-=1
                    
                result=" ".join(d)
        i+=1
    with open(file_name) as f:
        l = f.readlines()
    del l[gyou]
    l.insert(gyou,f"{result}\n")
    with open(file_name,mode="w")as f:
        f.writelines(l)

  def config(self,**kwargs):
    global dump_best
    if hasattr(kwargs,"cfile"): self.cfile=kwargs["cfile"]
    opt=self.option
    isconfig=os.path.isfile(self.cfile)
    if isconfig:
        print(f"read {self.cfile}")
        with open(self.cfile) as f:
            jwargs=json.load(f)
            optk=opt.keys()&jwargs.keys()
            opt.update(**{k:jwargs[k] for k in optk})
            if(optk != jwargs.keys()): 
                print("unrecognized options: ",*(jwargs.keys()-optk))
    # overwrite options if given
    if kwargs:
        optk=opt.keys()&kwargs.keys()
        opt.update(**{k:kwargs[k] for k in optk})
        if(optk != kwargs.keys()): 
            print("unrecognized options: ",*(kwargs.keys()-optk))
    self.option=opt
    midfile=opt["midfile"]
    stopfile=opt["stopfile"]
    for k in opt:
        setattr(self,k,opt[k])
    # create scratch directory
    os.makedirs(self.scrdir,exist_ok=True)
    # conver eV to kcal/mol if refE is in eV
    _coeff = 1.0/0.043364124 if self.ref_eV else 1.0
    if os.path.isfile(self.refE_file):
      with open(self.refE_file) as f:
        refE=f.read().split()
        _idx=[ i for i,v in enumerate(refE) if "*" in v ]+[len(refE)]
        if _idx[0] != 0: _idx = [0] + _idx # initial snapshot must be reference
        self.baseIdx=np.hstack([[_idx[i]]*(_idx[i+1]-_idx[i]) for i in range(len(_idx)-1)])
        refE=[en.replace("*","") for en in refE]
    else:
      self.baseIdx=np.array([0])
      refE=[0.0]
    if os.path.isfile(self.refF_file):
      with open(self.refF_file) as f:
        refF=f.read().split()
    else:
      refF=[0.0]
    refE=np.array(refE,dtype=float)*_coeff # relative energy
    refE-=refE[self.baseIdx]
    refF=np.array(refF,dtype=float)*_coeff
    if self.relative_force: refF-=refF[self.baseIdx]
    # read template and x0
    with open(self.initfile) as f:
      _template=f.read()
    regex=re.compile("[\{\[][\d.-]+")
    x0=regex.findall(_template)
    isBound1=[]
    x1 = 0
    for x1 in range(len(x0)):
        if x0[x1].startswith("{"):
            isBound1.append("True")
            x0[x1]=x0[x1].strip("{")
        else:
            isBound1.append("False")
            x0[x1]=x0[x1].strip("[")
        x1+=1
    #print(x0)
    self.x0=[float(x) for x in x0]
    #print(x1)
    self.template = _template
    # change {S
    # define bounds
    for x in self.x0:
        if x==0:
            print("error:0 cannot be used as a parameter.")
            sys.exit(1)
        else:
            pass
    bounds=[]
    for i,x in enumerate(self.x0):
        if isBound1[i] =="True":
            delta = abs(float(self.bound)*x)
            t = (x-delta,x+delta)
            bounds.append(t)
        else:
            sigma = abs(float(self.bound2)*x)
            k=(x-sigma,x+sigma)
            bounds.append(k)
    #print(bounds)
    self.bounds=bounds
    template=regex.sub("{}",_template)
    self.template=template
    # get elements from templates
    eles=re.findall(r"\n *(:?[A-Z][a-z]?)",template)
    self.elements=" ".join(eles)
    self.refE=refE
    self.refF=refF
    def callbackF(xk,convergence=False,fout=None):
      fname=midfile
      sys.stdout.flush()
      if fout: fname=fout
      with open(fname,"w") as f:
          _x=np.round(xk,5)
          y=[f"{{{xx}" for xx in _x]
          f.write(template.format(*y))
      if os.path.isfile(stopfile):
          print("optimization will be stopped by the stop file")
          os.remove(stopfile)
          return True
    dump_best=callbackF
    return
  def set_eval(self,func):
    global wrap_eval
    _x0=np.array(self.x0)
    def wrap_eval(*args,**kwargs):
      pid=os.getpid()
      pes,fns=self.reax(*args,pid=pid)
      output = func(pes,fns,self.refE,self.refF) 
      if self.harmonic > 0:
        deltax=(np.array(args[0])-_x0)/(_x0+0.01)
        output+=deltax@deltax*self.harmonic
      return output
    return wrap_eval
  def reax(self,xk=None,pid=0):
      x=xk if xk is not None else self.x0
      ffname=f"{self.scrdir}/ffield.reax.{pid}"
      elements=self.elements
      pes,fns=[],[]
      with open(ffname,"w") as f:
          f.write(self.template.format(*np.round(x,6)))
      lmp=lammps(cmdargs=["-log", "none", "-screen", "none",  "-nocite"])
      for i in range(1):
          cmds=["units real",
              "atom_style charge",
              f"read_data {self.datafile}",
              "pair_style      reaxff NULL",
              f"pair_coeff      * * {ffname} {elements}",
              "fix             1 all qeq/reaxff 1 0.0 10.0 1.0e-6 reaxff"]
          lmp.commands_list(cmds)
          lmp.command("run 0")
          pes.append(lmp.get_thermo("pe"))
          fns.append(lmp.get_thermo("fnorm"))
      if self.uniform == "False":
        b="add yes purge yes replace no "
      else:
        b=""
      for i in range(1,len(self.refE)):
        a=f"read_dump {i}.xyz 0 x y z box no "
        c="format xyz"
        lmp.command(a+b+c)
        lmp.command("run 0")
        pes.append(lmp.get_thermo("pe"))
        fns.append(lmp.get_thermo("fnorm"))
      lmp.close()
      pes=np.array(pes)
      fns=np.array(fns)
      return pes,fns

  def fit(self,func=None):
      global dump_best
      if not hasattr(self,"x0"): self.config()
      print("config parameters for fitting")
      json.dump(self.option,sys.stdout)
      print("")
      #refE,refF=self.refE,self.refF
      print(f"initial {len(self.x0)} parameters : {self.x0}")
      if not func:
          @self.set_eval
          def default_eval(pes,fns,refE,refF):
            pes0=pes[0]
            pes-=pes[self.baseIdx] # initial structure is reference by default
            pes-=refE
            if self.relative_force: fns-=fns[self.baseIdx]
            fns-=refF
            fns*=self.force_weight
            fmax=np.abs(fns).max()
            #return np.sign(pes0)*np.log10(np.abs(pes0)+1) + np.log10(fns@fns+1)
            return pes@pes + np.linalg.norm(fns)+np.abs(pes).max()*np.abs(fns).max()+fmax**2
            #return pes@pes + np.linalg.norm(fns)/len(fns)/10+fns[0]*fns[0]/10
          func=default_eval
      if self.optimizer == "differential_evolution":
        result = differential_evolution(func, self.bounds,workers=self.workers,x0=self.x0,updating='deferred',
                                  disp=True,maxiter=self.maxiter,tol=self.tol,callback=dump_best,popsize=16,seed=self.seed)
      else:
        result = minimize(func,x0=self.x0,method=self.optimizer,tol=self.tol,callback=dump_best,jac='3-point') 
      print(result)
      dump_best(result.x,fout=self.endfile)
      self.result=result
      self.E,self.F=self.reax(result.x)
      return result

if __name__ =='__main__':
    pass
