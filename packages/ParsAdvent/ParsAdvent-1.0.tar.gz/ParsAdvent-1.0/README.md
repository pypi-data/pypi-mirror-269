# Parser para la creación de aventuras conversacionales.
(Por Prof.88 Dionisio David Peñalosa Mauri).

Esta librería está formada por un conjunto de clases que permiten crear todo un mundo donde pueda ocurrir cualquier tipo de aventuras.
A continuación se oferce una lista de clases junto con la descripción de sus métodos.

## class Token
Clase que cotiene todos los tokens del comunicador.		

## class TablaSimbolos
Esta clase contiene la tabla de símbolos, la cual almacena la siguiente información en cada una de las estradas de la misma: identificador - token - tipos_argumentos/cosa - nº argumentos - acción/cosa

## class Personaje	
Clase Personaje: implementa la jugador con su mochila y sus "stats".
**Métodos:**	 
* inventario(self): Muestra el contenido de la mochila.
* poner(self,objeto,info): Pone un objeto dentro de la mochila. Se pasa por parámetros el nombre del objeto y la información del mismo. Si existiera un objeto igual, lo perdería.	
* soltar(self,obj): Suelta un objeto de la mochila.

## class Texto
Utilidades varias para texto.
**Métodos:**	 
* articulo(sustantivo,tipo): Devuelve el artículo determinado o indeterminado de la palabra pasada por parámetros.
* terminaCopulativa(texto): Termina una lista de conjunciones copultivas separadas por coma. Quita los dos últimos caracteres, que se suponen que son una coma y un espacion y sustituya la nueva última coma por la conjunción y. Termina la frase poniendo un punto.
	
##class Lugar
Clase Lugar: implementa un lugar. Dicho lugar contiene:
+ Un Identificador
+ Una Descripcióno
+ Una lista de salidas (cada salida es a su vez una lista dirección-identficador).
+ Una lista de objetos (cadenas).

**Métodos:**	 
* setDescripcion(self,desc): Establece la descripción.
* setSalidas(self,exs): Establece las salidas.
* setObjetos(self,obs): Establece la lista de objetos. Añade los objetos nuevos a la tabla de símbolos. Cada objeto vendrá descrito en un mapa cuya clave es el nombre del objeto y una lista con las características del mismo:
	**{'nombre':['descripción','estado','objeto/herramienta/lugar'],'visible/oculto','objeto','relevante/irrelevante}**
	+ Descripción: descripción detallada del objeto.
	+ Estado: Característica o situación en la que se encuentra el objeto antes de ser usado o después de ser usado.
	+ Objeto/herramienta/lugar: Tipo de objeto, puede ser una herramienta (algo que se puede usar) o un lugar, el cual puede contener algo.
	+ Visible/oculto: Si se desea que el narrador diga o no que el objeto está en el lugar.
	+ Objeto: En caso de tratarse de un lugar, este puede albergar un objeto (ya definido en el sitio). Si no tuviera ninguno vale 'None'
	+ Relevante: En caso de haber un objeto, si a este se le quiere dar especial importancia o no.
* muestraObjetos(self): Muestra la información de los objetos.
* todosObjsOcultos(self): Devuelve true si todos los objetos están ocultos.
* muestra(self): Muestra por pantalla la información del lugar.
		 
## class Mundo
Clase Mundo: implementa el conjunto de lugares que tiene un "mundo" con la información del lugar actual dónde se encuentra el personaje. La clase mundo contiene:
+ vacio: booleano que indica que no se ha creado ningún lugar.
+ mapa: diccionario de <identificadores>:<Lugar>
+ lugarInicio: es el identificador del lugar donde el personaje se encuentra al principio.
+ lugarActual: es el identificador del lugar donde el personaje ese encuentra actualmente. 
+ final: booleano que vale true cuando se haya llegado al final del mundo.

**Métodos:**	 
* añadeLugar(self, id, lugar): Añade un lugar junto con su identificador al mundo. Si el mundo está vación lo toma como lugar de inicio.
* inicio(self): Ubica al personaje en el lugar de inicio.
* describir(self): Método para describir el lugar.
* examinar(self,cosa): Método para examinar cosas.
* ir(self, dir): Método par cambiar de lugar yendo a alguna dirección.
* tomar(self, obj): Método que devuelve un objeto del lugar donde está y lo quita de allí. El objeto debe de estar en la lista de objetos de la habitación y no encontrarse dentro de "algo" que esté cerrado.
* dejar(self,obj,info): Método que deja un objeto en el lugar actual.
* depositar(self,cosa1,cosa2,info): Método que deja el objeto en un lugar determinado. Si donde se pretende dejar no es un lugar, lo deja en el suelo.
* abrir(self,cosa1,utensilio): Abre un portal o un contenedor.
* cerrar(self,cosa1,utensilio): Abre un portal o un contenedor.
* cambiaEstado(self,cosa,estado): Método para cambiar un objeto o cosa de estado.
* consultaEstado(self,cosa): Método que devuelve el estado de una objeto o cosa.
* hacerVisObjs(self): Método para hacer visible los objetos que estén ocultos en un lugar. Si el objeto se encontrara dentro de algún lugar o contenedor lo deja oculto.
* hayEnEscenario(self, cosa): Devuelve true si la "cosa" que se pasa por parámetros se encuentra dentro del escenario donde está el personaje.
		
## class Comunicador
Clase Comunicador. Clase que se utiliza para comunicarse con el usuario. Le pide a este que introduzca una orden y la analiza. En el atributo "acción" dejan un token con una de las acciones que hay en la clase Token y en el atributo "cosa" deja la "cosa" sobre la que recae la acción. La primera palabra la toma como la acción y la último como la cosa. Si es la misma y se trata de un punto cardina, toma la acción de "ir".
	
**Métodos:**	 
* preguntaUsuario(self): Método que pide al usuario que introduzca una orden. El método analiza sintáctica y semáticamente la frase buscando un total de 3 tokens: el primero ha de ser una acción y los otros dos los considera como "cosas" parámetors de la acción. Este método modifica los atributos "accion", "cosa1" y "cosa2". En el primero almacena el token de la acción y en cosa1 y cosa2 las palabras (no token) parámetros de la acción.				
* defAccion(self,accion,tipo,nArgs): Define una acción definida por el usuario. Se pasa por parámetros el nombre de la acción, el tipo de cosas a las que se aplica y el número de argumentos que esta tiene. Para ello lo da de alta en la tabla de símbolos.
