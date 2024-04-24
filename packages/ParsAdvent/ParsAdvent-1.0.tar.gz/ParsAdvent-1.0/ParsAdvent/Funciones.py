## Clase que cotiene todos los tokens del comunicador.		
class Token:
	NADA=0
	IR=1
	DESCRIBIR=2
	EXAMINAR=3
	COGER=4
	DEJAR=5
	DEPOSITAR=6
	USAR=7
	OBJETO=8
	INVENTARIAR=9
	ABRIR=10
	CERRAR=11
	DEF_USU=12
	FIN=13

## Esta clase contiene la tabla de símbolos, la cual almacena la siguiente información en
## cada una de las estradas de la misma: identificador - token - tipos_argumentos/cosa - nº argumentos - acción/cosa
class TablaSimbolos:
	ts = {	'ir': [Token.IR,['direccion','lugar','portal'],1,'accion'],
			'n': [Token.IR,'direccion',1,'accion'],
			's': [Token.IR,'direccion',1,'accion'],
			'e': [Token.IR,'direccion',1,'accion'],
			'o': [Token.IR,'direccion',1,'accion'],
			'norte': [Token.IR,'direccion',1,'accion'],
			'sur': [Token.IR,'direccion',1,'accion'],
			'este': [Token.IR,'direccion',1,'accion'],
			'oeste': [Token.IR,'direccion',1,'accion'],
			'describir': [Token.DESCRIBIR,[],0,'accion'],
			'inventariar': [Token.INVENTARIAR,[],0,'accion'],
			'examinar': [Token.EXAMINAR,['herramienta','objeto','lugar','portal','contenedor'],1,'accion'],
			'coger': [Token.COGER,['herramienta','objeto'],1,'accion'],
			'dejar': [Token.DEJAR,['herramienta','objeto'],1,'accion'],
			'depositar': [Token.DEPOSITAR,['herramienta','objeto','lugar'],2,'accion'],
			'usar': [Token.USAR,['herramienta','objeto','portal'],2,'accion'],
			'abrir': [Token.ABRIR,['portal','contenedor'],1,'accion'],
			'cerrar': [Token.ABRIR,['portal','contenedor'],1,'accion'],
			'fin': [Token.FIN,[],0,'accion']
		}
		
## Clase Personaje: implementa la jugador con su mochila y sus "stats".
class Personaje:
	mochila = {}
	
	# Muestra el contenido de la mochila.
	def inventario(self):
		if self.mochila == {}:
			print('La mochila está vacía')
		else:
			texto='En la mochila llevas: '
			for obj in self.mochila.keys():
				texto+=Texto.articulo(obj,'indeterminado')+' '+obj+', '
			texto=Texto.terminaCopulativa(texto)
			print(texto)
			
	# Pone un objeto dentro de la mochila.
	# Se pasa por parámetros el nombre del objeto y la información del mismo.
	# Si existiera un objeto igual, lo perdería.
	def poner(self,objeto,info):
		self.mochila[objeto]=info
		self.mochila[objeto][3]='visible'
	
	# Suelta un objeto de la mochila.
	def soltar(self,obj):
		if obj not in self.mochila:
			print('No encuentro ese objeto')
			return []
		else:
			info=self.mochila[obj]
			del self.mochila[obj]
			return info

## Utilidades varias para texto.
class Texto:
	# Devuelve el artículo determinado o indeterminado de la palabra
	# pasada por parámetros.
	def articulo(sustantivo,tipo):
		listArtic=[[['la','el'],['las','los']],[['una','un'],['unas','unos']]]
		if '_' in sustantivo:
			palabra=sustantivo[0:sustantivo.find('_')]
		else:
			palabra=sustantivo
		vocs=palabra
		characters = "bcdfghjklmnñpqrstvwxyz"
		vocs = "".join(x for x in vocs if x not in characters)
		if tipo=='indeterminado':
			det=1
		else:
			det=0
		if palabra[len(palabra)-1]=='s':
			plural=1
		else:
			plural=0
		if len(palabra) <= 3 or len(vocs) <= 1:
			fem=1
		else:
			ultVoc=vocs[len(vocs)-1]
			penVoc=vocs[len(vocs)-2]
			if ultVoc == palabra[len(palabra)-1]:
				termVoc = True
			else:
				termVoc = False
			if ultVoc == 'a' or ultVoc == 'á':
				fem=0
			elif (ultVoc == 'e' or ultVoc == 'é') and (penVoc == 'a' or penVoc == 'á') and termVoc:
				fem=0
			else:
				fem=1
		return listArtic[det][plural][fem]
		
	## Termina una lista de conjunciones copultivas separadas por coma. 
	## Quita los dos últimos caracteres, que se suponen que son una coma y un espacion
	## y sustituya la nueva última coma por la conjunción y. Termina la frase poniendo
	## un punto.
	def terminaCopulativa(texto):
		if texto[len(texto)-2:len(texto)]==', ':
			texto = texto[0:len(texto)-2]
		inx=texto.rfind(',')
		if inx != -1:
			texto=texto[0:inx]+' y'+texto[inx+1:len(texto)]
		return texto+'.'
	
## Clase Lugar: implementa un lugar. Dicho lugar contiene:
## Un Identificador
## Una Descripcióno
## Una lista de salidas (cada salida es a su vez una lista dirección-identficador).
## Una lista de objetos (cadenas).

class Lugar:
	objetos = {}
	
	# Establece la descripción.
	def setDescripcion(self,desc):
		self.descripcion=desc
		
	# Establece las salidas.
	def setSalidas(self,exs):
		self.salidas=exs
	
	# Establece la lista de objetos.
	# Añade los objetos nuevos a la tabla de símbolos.
	# Cada objeto vendrá descrito en un mapa cuya clave es el nombre del objeto
	# y una lista con las características del mismo:
	# {'nombre':['descripción','estado','objeto/herramienta/lugar'],'visible/oculto','objeto','relevante/irrelevante}
	# Descripción: descripción detallada del objeto.
	# Estado: Característica o situación en la que se encuentra el objeto antes de ser usado o después de ser usado.
	# Objeto/herramienta/lugar: Tipo de objeto, puede ser una herramienta (algo que se puede usar) o un lugar, el cual puede contener algo.
	# Visible/oculto: Si se desea que el narrador diga o no que el objeto está en el lugar.
	# Objeto: En caso de tratarse de un lugar, este puede albergar un objeto (ya definido en el sitio). Si no tuviera ninguno vale 'None'
	# Relevante: En caso de haber un objeto, si a este se le quiere dar especial importancia o no.
	def setObjetos(self,obs):
		self.objetos=obs
		for obj in self.objetos.keys():
			TablaSimbolos.ts[obj]=[Token.OBJETO,obs[obj][2],0,'cosa']
	
	# Muestra la información de los objetos.
	def muestraObjetos(self):
		if self.objetos != {} and not self.todosObjsOcultos():
			texto = 'Allí hay '
			for obj in self.objetos.keys():
				if self.objetos[obj][3] == 'visible':
					texto += Texto.articulo(obj,'indeterminado')+' '+obj +', '
			texto = Texto.terminaCopulativa(texto)
			print(texto)

	# Devuelve true si todos los objetos están ocultos.
	def todosObjsOcultos(self):
		if len(self.objetos) == 0:
			return False
		for obj in self.objetos.keys():
			if self.objetos[obj][3] == 'visible':
				return False
		return True

	# Muestra por pantalla la información del lugar.
	def muestra(self):
		print(self.descripcion)
		self.muestraObjetos()
		if hasattr(self,"salidas"):
			texSals="Salidas: "
			for sal in self.salidas:
				texSals+= sal+", "
			texSals=texSals[0:len(texSals)-2]
			print(texSals)
		 
## Clase Mundo: implementa el conjunto de lugares que tiene un "mundo" con la información del 
## lugar actual dónde se encuentra el personaje. La clase mundo contiene:
## vacio: booleano que indica que no se ha creado ningún lugar.
## mapa: diccionario de <identificadores>:<Lugar>
## lugarInicio: es el identificador del lugar donde el personaje se encuentra al principio.
## lugarActual: es el identificador del lugar donde el personaje ese encuentra actualmente. 
## final: booleano que vale true cuando se haya llegado al final del mundo.

class Mundo:
	# Constructor de mundo.
	def __init__(self):
		self.vacio = True
		self.mapa = {}
		self.final = False

	# Añade un lugar junto con su identificador al mundo. 
	# Si el mundo está vación lo toma como lugar de inicio.
	def añadeLugar(self, id, lugar):
		if self.vacio:
			self.lugarInicio=id
			self.vacio=False
		self.mapa[id]=lugar
	
	# Ubica al personaje en el lugar de inicio.
	def inicio(self):
		self.lugarActual = self.lugarInicio
		self.mapa[self.lugarInicio].muestra()

	# Método para describir el lugar.
	def describir(self):
		self.mapa[self.lugarActual].muestra()
	
	# Método para examinar cosas.
	def examinar(self,cosa):
		if cosa in Personaje.mochila:
			print(Personaje.mochila[cosa][0]+ ", está "+Personaje.mochila[cosa][1])
		else:	
			objs=self.mapa[self.lugarActual].objetos
			if objs==None or cosa not in objs:
				print('No hay '+cosa)
			else:
				print(objs[cosa][0]+ ", está "+objs[cosa][1])
				if objs[cosa][2] == 'lugar' and len(objs[cosa]) == 6 and objs[cosa][4] != None and objs[cosa][5]=='relevante':
					print('Espera!!!, parece que hay '+Texto.articulo(objs[cosa][4],'indeterminado')+' '+objs[cosa][4]+'.')
				elif objs[cosa][2] == 'lugar' and len(objs[cosa]) >= 5  and objs[cosa][4] != None:
					print('Hay '+Texto.articulo(objs[cosa][4],'indeterminado')+' '+objs[cosa][4]+'.')
				elif objs[cosa][2] == 'contenedor' and objs[cosa][1] == 'abierto' and objs[cosa][4] != None:
					print('Hay '+Texto.articulo(objs[cosa][4],'indeterminado')+' '+objs[cosa][4]+'.')
				elif objs[cosa][2] == 'contenedor' and objs[cosa][1] == 'abierto' and objs[cosa][4] == None:
					print('No hay nada dentro.')
	
	# Método par cambiar de lugar yendo a alguna dirección.
	def ir(self, dir):
		error=False
		salidas=self.mapa[self.lugarActual].salidas
		objetos=self.mapa[self.lugarActual].objetos
		if dir in salidas:
			lug=salidas[dir]
		elif dir in objetos and objetos[dir][2]=='portal' and objetos[dir][1]=='abierto':
			lug=objetos[dir][4]	
		elif dir in objetos and objetos[dir][2]=='portal' and objetos[dir][1]=='cerrado':
			print("No puedes, la puerta está cerrada.")
			error=True
		else:	
			print ("No puedes ir en esa dirección.")
			error=True
		if not error:
			if lug not in self.mapa:
				print ("Error de diseño: el lugar "+ lug +" no está definido. Póngase en contacto con los desarrolladores.")
				self.final=True
			else:
				self.lugarActual=lug
				self.mapa[lug].muestra()
	
	# Método que devuelve un objeto del lugar donde está y lo quita de allí.
	# El objeto debe de estar en la lista de objetos de la habitación y no encontrarse
	# dentro de "algo" que esté cerrado.
	def tomar(self, obj):
		lisObj=self.mapa[self.lugarActual].objetos
		noAcces=False
		for atrib in lisObj.values():
			if obj in atrib and atrib[1]=='cerrado':
				noAcces=True
		if obj not in lisObj or noAcces:
			print('No encuentro ese objeto')
			return []
		else:
			info=self.mapa[self.lugarActual].objetos[obj]
			del self.mapa[self.lugarActual].objetos[obj]
			for ob in self.mapa[self.lugarActual].objetos:
				if obj in self.mapa[self.lugarActual].objetos[ob]:
					self.mapa[self.lugarActual].objetos[ob][4]=None
			return info
			
	# Método que deja un objeto en el lugar actual.
	def dejar(self,obj,info):
		self.mapa[self.lugarActual].objetos[obj]=info
		
	# Método que deja el objeto en un lugar determinado. Si donde se pretende
	# dejar no es un lugar, lo deja en el suelo.
	def depositar(self,cosa1,cosa2,info):
		self.mapa[self.lugarActual].objetos[cosa1]=info
		if self.mapa[self.lugarActual].objetos[cosa2][2] != 'lugar':
			print('Eso no es un lugar...lo dejaré en el suelo.')
		elif len(self.mapa[self.lugarActual].objetos[cosa2]) > 4 and self.mapa[self.lugarActual].objetos[cosa2][4] != None:
			print('Ese lugar está ocupado...lo dejaré en el suelo.')
		elif len(self.mapa[self.lugarActual].objetos[cosa2]) <= 4:
			self.mapa[self.lugarActual].objetos[cosa2].append(cosa1)
			self.mapa[self.lugarActual].objetos[cosa1][3]='oculto'	
			print('depositado!!!')	
		else:
			self.mapa[self.lugarActual].objetos[cosa2][4]=cosa1
			self.mapa[self.lugarActual].objetos[cosa1][3]='oculto'
			print('depositado!!')
	
	# Abre un portal o un contenedor.
	def abrir(self,cosa1,utensilio):
		if utensilio not in pers.mochila:
			print('Lo siento, no tienes nada con qué abrirlo')
		elif self.hayEnEscenario(cosa1):
			if self.consultaEstado(cosa1) == 'cerrado':
				self.cambiaEstado(cosa1,'abierto')
			print('ya está abierto!!!')
		else:
			print('No puedes abrir eso')
		
	# Abre un portal o un contenedor.
	def cerrar(self,cosa1,utensilio):
		if utensilio not in pers.mochila:
			print('Lo siento, no tienes nada con qué cerrarlo')
		elif self.hayEnEscenario(cosa1):
			if self.consultaEstado(cosa1) == 'abierto':
				self.cambiaEstado(cosa1,'cerrado')
			print('ya está cerrado!!!')
		else:
			print('No puedes cerrar eso')
			
	# Método para cambiar un objeto o cosa de estado.
	def cambiaEstado(self,cosa,estado):
		if cosa in self.mapa[self.lugarActual].objetos:
			self.mapa[self.lugarActual].objetos[cosa][1]=estado
		elif cosa in Personaje.mochila:
			Personaje.mochila[cosa][1]=estado
		else:
			print('no tengo ' + cosa)
		
	# Método que devuelve el estado de una objeto o cosa.
	def consultaEstado(self,cosa):
		return self.mapa[self.lugarActual].objetos[cosa][1]
		
	# Método para hacer visible los objetos que estén ocultos en un lugar. 
	# Si el objeto se encontrara dentro de algún lugar o contenedor lo deja oculto.
	# De igualmente si es secreto.
	def hacerVisObjs(self):
		for obj in self.mapa[self.lugarActual].objetos:
			dejOcult=False
			for atrib in self.mapa[self.lugarActual].objetos.values():
				if obj in atrib:
					dejOcult=True
			if not dejOcult and self.mapa[self.lugarActual].objetos[obj][3]=='oculto':
				self.mapa[self.lugarActual].objetos[obj][3]='visible'

	# Devuelve true si la cosa que se pasa por parámetros se encuentra 
	# dentro del escenario donde está el personaje.
	def hayEnEscenario(self, cosa):
		return cosa in self.mapa[self.lugarActual].objetos
		
## Clase Comunicador. Clase que se utiliza para comunicarse con el usuario. Le pide a este
## que introduzca una orden y la analiza. En el atributo "acción" dejan un token con una
## de las acciones que hay en la clase Token y en el atributo "cosa" deja la "cosa" sobre
## la que recae la acción. La primera palabra la toma como la acción y la último como la
## cosa. Si es la misma y se trata de un punto cardina, toma la acción de "ir".
class Comunicador:
	# Constructor del Comunicador
	def __init__(self):
		self.accion=Token.NADA
		self.cosa1=""
		self.cosa2=""
	
	# Método que pide al usuario que introduzca una orden. El método analiza sintáctica y semáticamente la frase buscando 
	# un total de 3 tokens: el primero ha de ser una acción y los otros dos los considera como "cosas"
	# parámetors de la acción. Este método modifica los atributos "accion", "cosa1" y "cosa2". En el primero
	# almacena el token de la acción y en cosa1 y cosa2 las palabras (no token) parámetros de la acción.				
	def preguntaUsuario(self):
		nArg=0
		linea=input('#> ')
		
		## Análisis sintáctico.
		palabras=linea.split()
		if len(palabras) == 0 or palabras[0] not in TablaSimbolos.ts or palabras[0] in TablaSimbolos.ts and TablaSimbolos.ts[palabras[0]][3] != 'accion':
			print("No sabes hacer eso!!!")
			self.accion=Token.NADA
		else:
			self.accion=TablaSimbolos.ts[palabras[0]][0]
			self.cosa1=""
			self.cosa2=""
			i=1
			while(i <len(palabras) and palabras[i] not in TablaSimbolos.ts):
				i+=1
			if i < len(palabras):
				self.cosa1=palabras[i]
				nArg+=1
			i+=1
			while i <len(palabras) and palabras[i] not in TablaSimbolos.ts:
				i+=1
			if i < len(palabras):
				self.cosa2=palabras[i]
				nArg+=1
			if  self.accion == Token.IR and palabras[0] in ['norte','sur','este','oeste']:
				self.cosa1=palabras[0][0]
				nArg=1
			elif self.accion == Token.IR and palabras[0] in ['n','s','e','o']:
				self.cosa1=palabras[0]
				nArg=1
			elif self.accion == Token.IR and self.cosa1 in ['norte','sur','este','oeste']:
				self.cosa1=self.cosa1[0]
				nArg=1
			elif self.accion == Token.DEF_USU:
				self.texto=palabras[0]
				
			## Análisis Semántico.
			if TablaSimbolos.ts[palabras[0]][2] != nArg:
				print('No puedes hacer eso')
				self.accion=Token.NADA
			elif nArg >= 1 and TablaSimbolos.ts[palabras[0]][1] != TablaSimbolos.ts[self.cosa1][1] and TablaSimbolos.ts[self.cosa1][1] not in TablaSimbolos.ts[palabras[0]][1]:
				print('Eso no tiene sentido')
				self.accion=Token.NADA
			elif nArg == 2 and TablaSimbolos.ts[palabras[0]][1] != TablaSimbolos.ts[self.cosa2][1] and TablaSimbolos.ts[self.cosa2][1] not in TablaSimbolos.ts[palabras[0]][1]:
				print('Eso no tiene sentido hacerlo')
				self.accion=Token.NADA

	## Define una acción definida por el usuario.
	## Se pasa por parámetros el nombre de la acción, el tipo de cosas a las que se aplica y 
	## el número de argumentos que esta tiene. 
	## Para ello lo da de alta en la tabla de símbolos.
	def defAccion(self,accion,tipo,nArgs):
		if nArgs < 0 and nArgs > 2:
			print('Número de argumentos incorrectos')
		elif len(tipo)==0:
			print('Se debe de aplicar a algún tipo de objetos')
		else:
			TablaSimbolos.ts[accion]=[Token.DEF_USU,tipo,nArgs,'accion']

