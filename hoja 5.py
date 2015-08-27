import random
import simpy
import math

intervarlo= 5
numero_instrucciones= 0
random.seed(42)

def procesoGen(env, nombre, timex, CpuProc, memoria, numInstruccion, numWait, intervalo, posicion):
     global tiempototal
     global tiempolista
     global mem
     numram = numInstruccion
     timex= random.expovariate(1.0 / intervalo)
     yield  env.timeout(timex)
     #if (memoria.level>numInstruccion):
     memoria.get(numram)
     primerT= env.now 
     print('%s Generando:  %7.4f y la memoria es %7.4f' % (nombre,  primerT, numram))
     with CpuProc.request() as req2:
          yield req2
          while (numInstruccion > 0):
               segundoT= env.now
               print('%s starting to CPU at %7.4f' % (nombre, segundoT))
               if (numInstruccion >= 6): 
                    numInstruccion = numInstruccion -6
                    yield env.timeout(1)
                    if (numWait == 1):
                         env.timeout(random.randint(1, 10))
               else:
                    print('%s waitin at %7.4f' % (nombre, env.now))
                    #yield env.timeout(numInstruccion)
                    numInstruccion = 0
     segundoT= env.now
     tiempoProm= segundoT - primerT
     tiempolista.append(tiempoProm)
     tiempototal=tiempototal+tiempoProm
     print('%s terminar at %7.4f' % (nombre, segundoT))
     print( 'su tiempo del proceso es: %7.4f ' % (tiempoProm))
     memoria.put(numram)
     mem= memoria.level
     print( 'cantidad de memoria at %7.4f'% (mem))
     #else:
          #print('putos at %7.4f' % (env.now))
          #yield memoria.get(numram)
     
     
mem=0
tiempototal=0
total=0
tiempolista=[]
numprocesos= 200

env = simpy.Environment()               
memoria= simpy.Container(env, init = 100, capacity= 100)
CpuProc = simpy.Resource(env, capacity = 1)

# crear los procesos
for i in range(numprocesos):
    numIns = random.randint(1,10)
    numWait= random.randint(0,1)
    env.process(procesoGen(env, 'Proceso %d' % i,i, CpuProc, memoria, numIns, numWait, 1,i ))
    
env.run()
tiempototal=tiempototal/numprocesos
print('su tiempo final es: %7.4f ' % (tiempototal))

def desviacion_standar(lists, media):
     global total
     for i in range(0,len(lists)):
          value = lists[i]
          value = value - media
          value = value**2
          total = total + value
          total = total/float(len(lists))
          return math.sqrt(total)
     
total = desviacion_standar(tiempolista, tiempototal)
print('su desviacion estandar es: %7.4f ' % (total))

