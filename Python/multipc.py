from multiprocessing import Process
import os

# child processing func
def run_proc(name):
         print 'Run child processing %s (%s)' %(name,os.getpid())

if __name__=='__main__':
         print 'Parent process %s. ' %os.getpid()
         p = Process(target=run_proc,args=('test',))
         print'Process will start'
         p.start()
         p.join()
         print 'process end.'



