import bpy
from bpy import data
from bpy import context 
from mathutils import *
from math import *
'''*********************************************************************'''
'''Funciones comunes útiles para selección/activación/borrado de objetos'''
'''*********************************************************************'''
def seleccionarObjeto(nombreObjeto): # Seleccionar un objeto por su nombre
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    bpy.ops.object.select_pattern(pattern=nombreObjeto) # ...excepto el buscado
    
def activarObjeto(nombreObjeto): # Activar un objeto por su nombre
    bpy.ops.object.select_pattern(pattern=nombreObjeto)
    bpy.context.active_object.select_set(state=True)

def borrarObjeto(nombreObjeto): # Borrar un objeto por su nombre
    seleccionarObjeto(nombreObjeto)
    bpy.ops.object.delete(use_global=False)

def borrarObjetos(): # Borrar todos los objetos
    if(len(bpy.data.objects) != 0):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
def unirObjetos(lista_objetos):
    for objeto in lista_objetos:
        activarObjeto(objeto)
        
    bpy.ops.object.join()
    
def restarObjetos(objName, objResta):
    objects = bpy.data.objects
    obj = objects[objName]
    resta = objects[objResta]
    bool_op = obj.modifiers.new(type="BOOLEAN", name="Boolean")
    bool_op.object = resta
    bpy.context.view_layer.objects.active = obj
    
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
    
def color(objName, r, g, b):
    activarObjeto(objName)
    mat = bpy.data.materials.new("material")
    bpy.context.active_object.data.materials.append(mat)
    bpy.context.object.active_material.diffuse_color = (r, g, b, 1)

def textura(objName, m, r):
    activarObjeto(objName)
    bpy.context.object.active_material.metallic = m
    bpy.context.object.active_material.roughness = r
    
'''****************************************************************'''
'''Clase para realizar transformaciones sobre objetos seleccionados'''
'''****************************************************************'''
class Seleccionado:
    def mover(v):
        bpy.ops.transform.translate(
            value=v, constraint_axis=(True, True, True))

    def escalar(v):
        bpy.ops.transform.resize(value=v, constraint_axis=(True, True, True))

    def rotarX(v):
        bpy.ops.transform.rotate(value=v, orient_axis='X')

    def rotarY(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Y')

    def rotarZ(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Z')
        
'''**********************************************************'''
'''Clase para realizar transformaciones sobre objetos activos'''
'''**********************************************************'''
class Activo:
    def posicionar(v):
        bpy.context.object.location = v

    def escalar(v):
        bpy.context.object.scale = v

    def rotar(v):
        bpy.context.object.rotation_euler = v

    def renombrar(nombreObjeto):
        bpy.context.object.name = nombreObjeto

'''**************************************************************'''
'''Clase para realizar transformaciones sobre objetos específicos'''
'''**************************************************************'''
class Especifico:
    def escalar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].scale = v

    def posicionar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].location = v

    def rotar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].rotation_euler = v

'''************************'''
'''Clase para crear objetos'''
'''************************'''
class Objeto:
    def crearCubo(objName):
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearEsfera(objName):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearCono(objName):
        bpy.ops.mesh.primitive_cone_add(radius1=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)
    
    def crearCilindro(objName):
        bpy.ops.mesh.primitive_cylinder_add(enter_editmode=False, location=(0, 0, 0))
        Activo.renombrar(objName)
    
    def crearToro(objName, maxr, minr):
        bpy.ops.mesh.primitive_torus_add(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), major_radius=maxr, minor_radius=minr)
        Activo.renombrar(objName)
    
    def crearBase(objName):
        Objeto.crearCubo('CuboSuelo')
        Especifico.escalar('CuboSuelo', (0.7, 0.8, 0.02))
        Especifico.posicionar('CuboSuelo', (0, 0, 0.02))
        Objeto.crearCilindro('CilindroSuelo')
        Especifico.escalar('CilindroSuelo', (0.7, 0.4, 0.02))
        Especifico.posicionar('CilindroSuelo', (0, 0.8, 0.02))
        
        Objeto.crearCubo('CuboBase')
        Especifico.escalar('CuboBase', (0.5, 0.7, 0.5))
        Especifico.posicionar('CuboBase', (0, 0, 0.54))
        Objeto.crearCilindro('CilindroBase')
        Especifico.escalar('CilindroBase', (0.5, 0.5, 0.5))
        Especifico.posicionar('CilindroBase', (0, 0.7, 0.54))  
              
        Objeto.crearCubo('CuboResta')
        Especifico.escalar('CuboResta', (0.7, 0.7, 0.7))
        Especifico.posicionar('CuboResta', (0, 1.1, 1.3))
        Seleccionado.rotarX(0.6)
        
        restarObjetos('CilindroBase', 'CuboResta')
        restarObjetos('CuboBase', 'CuboResta')
        borrarObjeto('CuboResta')
        
        Objeto.crearCilindro('CilindroCentro')
        Especifico.escalar('CilindroCentro', (0.45, 0.45, 0.6))
        Especifico.posicionar('CilindroCentro', (0, 0.7, 0.6)) 
        
        unirObjetos(['CuboBase','CilindroBase', 'CuboSuelo', 'CilindroSuelo'])
        
        Activo.renombrar(objName)
        color(objName, 0.5, 0.5, 0.5)
        textura(objName, 0.3, 0.2)
        
    def crearBarra(objName, height, width, long):
        Objeto.crearCilindro('Cil')
        Especifico.escalar('Cil', (width, width,height ))
        Especifico.posicionar('Cil', (0, 0, 0)) 
        
        Objeto.crearCubo('Cubo')
        Especifico.escalar('Cubo', (width, long, height))
        Especifico.posicionar('Cubo', (0, long, 0))
        
        Objeto.crearCilindro('Cil2')
        Especifico.escalar('Cil2', (width, width,height))
        Especifico.posicionar('Cil2', (0, long*2, 0)) 
        unirObjetos(['Cil', 'Cubo', 'Cil2'])
        Activo.renombrar(objName)
        
    def crearMidStruct(objName):
        Objeto.crearCilindro('CilSup')
        Especifico.escalar('CilSup', (0.2, 0.2, 0.02))
        Especifico.posicionar('CilSup', (0, 0, 0)) 
        
        Objeto.crearBarra('BarraMid', 0.15, 0.45, 1)
        Especifico.posicionar('BarraMid', (0, 2, 0.17)) 
       
        Objeto.crearCilindro('CilSup2')
        Especifico.escalar('CilSup2', (0.3, 0.3, 0.02))
        Especifico.posicionar('CilSup2', (0, 2, 0.34)) 
        
        unirObjetos(['BarraMid','CilSup', 'CilSup2'])
        
        Activo.renombrar(objName)
        color('objName',0.5,0.5,0.5)
        textura(objName, 0.3, 0.2)
        
    def crearTopStruct(objName):
        Objeto.crearBarra('BarraInf', 0.12, 0.45, 0.9)
        Especifico.posicionar('BarraInf', (0, 0, 0)) 
        color('BarraInf',0.5,0.5,0.5)
        textura(objName, 0.3, 0.2)
        
        Objeto.crearBarra('BarraDeco', 0.01, 0.45, 0.9)
        Especifico.posicionar('BarraDeco', (0, 0, 0.12)) 
        color('BarraDeco',0,0.2,1)
        
        Objeto.crearCilindro('CilCuerpo')
        Especifico.escalar('CilCuerpo', (0.39, 0.39, 0.45))
        Especifico.posicionar('CilCuerpo', (0, -1.8, 0.58)) 
        color('CilCuerpo',1,1,1)
        
        Objeto.crearCubo('CuboCuerpo')
        Especifico.escalar('CuboCuerpo', (0.39, 0.9, 0.45))
        Especifico.posicionar('CuboCuerpo', (0, -0.9, 0.58))
        
        Objeto.crearCubo('CuboResta')
        Especifico.escalar('CuboResta', (0.5, 0.5, 0.5))
        Especifico.posicionar('CuboResta', (0, 0.3, 1.2))
        Seleccionado.rotarX(1.2)
        
        restarObjetos('CuboCuerpo', 'CuboResta')
        borrarObjeto('CuboResta')
        
        Objeto.crearCilindro('CilCentral')
        Especifico.escalar('CilCentral', (0.36, 0.36, 0.7))
        Especifico.posicionar('CilCentral', (0, 0, 0.83)) 
        
        Objeto.crearCilindro('CilDeco')
        Especifico.escalar('CilDeco', (0.5, 0.5, 0.2))
        Especifico.posicionar('CilDeco', (0, 0, 1.45)) 
        Seleccionado.rotarX(0.3)
        color('CilDeco',0,0.2,1)
        
        restarObjetos('CilCentral', 'CilDeco')
        Especifico.escalar('CilDeco', (0.375, 0.375, 0.05))
        Especifico.posicionar('CilDeco', (0, 0.015, 1.285))
        
        Objeto.crearCilindro('CilInf')
        Especifico.escalar('CilInf', (0.2, 0.2, 0.15))
        Especifico.posicionar('CilInf', (0, 0, -0.27)) 
       
        unirObjetos(['BarraInf','BarraDeco', 'CilCuerpo', 'CuboCuerpo', 'CilCentral', 'CilDeco'])
        
        Activo.renombrar(objName)
        
    def crearHerramienta(objName):
        Objeto.crearCilindro('CilHerramienta')
        Especifico.escalar('CilHerramienta', (0.05, 0.05, 1.3))
        Especifico.posicionar('CilHerramienta', (0, 0, 0)) 
        
        Objeto.crearToro('Tuerca1', 0.7, 0.5)
        Especifico.escalar('Tuerca1', (0.1, 0.1, 0.1))
        Especifico.posicionar('Tuerca1', (0, 0, 1.2)) 
        
        Objeto.crearToro('Tuerca2', 0.7, 0.5)
        Especifico.escalar('Tuerca2', (0.1, 0.1, 0.1))
        Especifico.posicionar('Tuerca2', (0, 0, -1.05)) 
        
        unirObjetos(['CilHerramienta','Tuerca1'])
        
        Activo.renombrar(objName)
        color(objName,0.2,0.2,0.2)
        textura(objName, 0.3, 0.2)
        
    def crearCable(objName):
        Objeto.crearToro('Cable', 2.3, 0.1)
        Especifico.escalar('Cable', (1, 0.7, 0.5))
        Especifico.posicionar('Cable', (0, 0, 1.4))
        Seleccionado.rotarY(1.57)
        
        Objeto.crearCubo('CuboResta')
        Especifico.escalar('CuboResta', (0.5, 2, 2))
        Especifico.posicionar('CuboResta', (0, 0.7, -0.8))
        Seleccionado.rotarX(1.2)
        restarObjetos('Cable', 'CuboResta')
        borrarObjeto('CuboResta')
        
        Objeto.crearToro('Tuerca1',1, 0.6)
        Especifico.escalar('Tuerca1', (0.1, 0.1, 0.2))
        Especifico.posicionar('Tuerca1', (0, -1.55, 0.8)) 
        
        Objeto.crearToro('Tuerca2', 1, 0.6)
        Especifico.escalar('Tuerca2', (0.1, 0.1, 0.2))
        Especifico.posicionar('Tuerca2', (0, 1.4, 2.5))
        unirObjetos(['Cable', 'Tuerca1', 'Tuerca2'])
        Activo.renombrar(objName)
        color(objName,0,0,0)
        
'''************'''
''' M  A  I  N '''
'''************'''
if __name__ == "__main__":
    borrarObjetos()
    
    Objeto.crearBase('MiBase')
    Objeto.crearMidStruct('Mid')
    Especifico.posicionar('Mid', (0, 2.7, 1.56))
    Objeto.crearTopStruct('Top')
    Especifico.posicionar('Top', (0, 4.5, 1.43))
    
    Objeto.crearHerramienta('Herr')
    Especifico.posicionar('Herr', (0, 4.5, 1.1))
    restarObjetos('Top', 'Herr')
    Objeto.crearCable('Cable')
    Especifico.posicionar('Cable', (0, 2.7, 2.8))
    
    bpy.ops.object.light_add(type='SUN', location=(0, 3,4))
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(-9, 10, 4.5), rotation=(1.38579, 7.03539e-06, -2.29687))
