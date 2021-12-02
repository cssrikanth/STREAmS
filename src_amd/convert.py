import os
import argparse
import re
import json

def create_subroutines(ofile,nfile,config,preproc=None):
    #Old file from STREAmS
    old_file = open(ofile+nfile, "r")
    old_lines = old_file.readlines()
    
    #Create a new file for hip conversion
    new_file = open(nfile, "w")
    
    #Get the file name for module creation
    subroutine = nfile.replace('.F90', '')
  
    #Add module in the first line
    new_file.write("module mod_"+subroutine+"\n")
    new_file.write("contains"+"\n")
    
    #grid block definition marker
    marker = 1
    
    for i,line in enumerate(old_lines):
      stripped_line = line.strip()
  
      #TODO: A bug now, remove when updated
      if "!" in stripped_line and "cuf" not in stripped_line:
        idx = stripped_line.index('!')
        stripped_line = stripped_line.replace(stripped_line[idx:],"")
        new_file.write(stripped_line+"\n")
        continue
  
      #TODO: A bug now, remove when updated
      if len(stripped_line)==0:
        continue
      
      if "::" in stripped_line and marker == 1:
        new_file.write("type(dim3) :: grid, tBlock"+"\n")
        marker=0
  
      if "<<<" in stripped_line:
        line_1 = stripped_line
  
        #Fine size of cuf
        nloop = int(re.findall(r'\d+',line_1)[0])
        
        #Go through the lines to extract variable size 
        for n in range(nloop):
          loop_line = old_lines[i+n+1].rstrip("\n")
          sp_1 = loop_line.split(",")
          idx2 = sp_1[1]
          idx1 = sp_1[0].split("=")[1]
          if n == 0:
            st0 = "real("+idx2+"-("+idx1+")+1"+")"
          elif n  == 1:
            st1 = "real("+idx2+"-("+idx1+")+1"+")"
          elif n == 2:
            st2 = "real("+idx2+"-("+idx1+")+1"+")"
        if nloop == 1:
          spec = "grid = dim3(ceiling("+st0+")/tBlock%x,1,1)"
          tx = config["one"]["thx"]
          ty = config["one"]["thy"]
          tz = config["one"]["thz"]
          new_file.write(f"tBlock = dim3({tx},{ty},{tz})"+"\n")
          new_file.write(spec+"\n\n")
        elif nloop == 2:
          spec = "grid = dim3(ceiling("+st1+")/tBlock%x,"+"ceiling("+st0+")/tBlock%y,"+"1)"
          tx = config["one"]["thx"]
          tx = config["two"]["thx"]
          ty = config["two"]["thy"]
          tz = config["two"]["thz"]
          new_file.write(f"tBlock = dim3({tx},{ty},{tz})"+"\n")
          new_file.write(spec+"\n\n")
        elif nloop == 3:
          spec = "grid = dim3(ceiling("+st2+")/tBlock%x,"+"ceiling("+st1+")/tBlock%y,"+"ceiling("+st0+")/tBlock%z)"
          tx = config["three"]["thx"]
          ty = config["three"]["thy"]
          tz = config["three"]["thz"]
          new_file.write(f"tBlock = dim3({tx},{ty},{tz})"+"\n")
          new_file.write(spec+"\n\n")
        new_file.write(f"!$cuf kernel do({nloop}) <<<grid,tBlock>>>"+"\n")
          
        continue 
      
      #TODO: Currently cant handle iercuda. Solve it when fixed 
      if "iercuda" in stripped_line:
        continue
     
      #To make sure C directives dont get indented 
      new_file.write(stripped_line+"\n")
    
    #Add module in the last line
    new_file.write("end module mod_"+subroutine)
    old_file.close()
    new_file.close()

    if preproc:
      tmp_new = "tmp_"+nfile
      c_prepro(nfile,tmp_new,preproc)
      os.system("mv "+tmp_new+" "+nfile)

def create_config(filename,precision):
  gpufort_config = open(filename, "w")
  if precision == 'single':
    gpufort_config.write('translator.FORTRAN_2_C_TYPE_MAP["real"]["mykind"]    = "float"\n')
    gpufort_config.write('translator.FORTRAN_TYPE_2_BYTES_MAP["real"]["mykind"]    = "4"\n\n')
  else:
    gpufort_config.write('translator.FORTRAN_2_C_TYPE_MAP["real"]["mykind"]    = "double"\n')
    gpufort_config.write('translator.FORTRAN_TYPE_2_BYTES_MAP["real"]["mykind"]    = "8"\n\n')

def c_prepro(old_file,new_file,options):
    os.system("gfortran -cpp -E "+options+" "+old_file+" > "+new_file)
    os.system("sed -i '/^#/d' "+new_file)

def create_module(old_module,new_module,precision):
  if precision == 'single':
    c_prepro(old_module,new_module,"-DSINGLE_PRECISION -DUSE_CUDA")
  else:
    c_prepro(old_module,new_module,"-DUSE_CUDA")

  #TODO: kind=iercuda not recognised. Ask Dom gpufort
  os.system('sed -i s/"(kind=cuda_stream_kind)"/""/g '+new_module)
 
def main():
  #Load thread parameters
  with open("config.json","r") as f:
        config = json.load(f)

  parser = argparse.ArgumentParser()

  parser.add_argument("-p", "--precision", help="Precision option", type=str,default="double")
  
  args = parser.parse_args()
  
  #Create gpufort config file 
  create_config("options.py.in",args.precision)   

  mod_file = "mod_streams.F90" 
  
  streams_src = "../src/"

  #Get module
  create_module(streams_src+mod_file,mod_file,args.precision)
  
  create_subroutines(streams_src,"bcdf.F90",config)
  create_subroutines(streams_src,"alloc.F90",config,"-DUSE_CUDA")


if __name__ == "__main__":
    main()
