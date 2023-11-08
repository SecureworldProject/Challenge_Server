
# Challenge Server

## Pasos:

- Crear entorno virtual
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python create_database.py`
- `python api.py`

## Funcionamiento

La interacción con el challenge se hace mediante una API Rest. Para facilitar las llamadas se proporciona una interfaz en Swagger. La aplicación del servidor dispone de persistencia mediante una base de datos SQL. La API dispone de 4 métodos:

- GET /readings: devuelve todas las lecturas registradas en la base de datos
- GET /reading/id: devuelve un registro concreto mediante su id
- DEL /reading/id: borra un registro concreto mediante su id
- POST /readings: da de alta un nuevo registro. Se describe a continuación su funcionamiento, ya que internamente llama al challenge.

### POST /readings

El ḿetodo acepta 3 variables:
- reading_id: identificador de la lectura
- ip: una dirección IP. Por el momento no se hace validación de la variable en el servidor
- data: una numero con un dato. Por el momento no se hace validación de la variable en el servidor

Con estos 3 datos, el challenge hace un cálculo y devuelve en la respuesta del método POST un número, que es el resultado del challenge. La lógica sobre cómo se calcula este número se ha definido en la función *challenge()*, pudiendo modificarse.

En concreto, intenta extraer las variables longitud y latitud en caso de que se trate de una IP pública, para lo que utiliza una librería de geolocalización. El inconveniente es que las librerías de geolocalización dependen en su totalidad de bases de datos, las cuales la mayoría son de pago. Existen algunas gratuitas, como la que se ha utilizado para el piloto pero no están actualizadas.