# «El Mohán» — Ruleta de leyendas (salió al azar). Termina en tragedia. Final cerrado.
# Voces: N narrador, P papá, M Rosa (tu hermana), V la tía (voz desde el río), X el Mohán
STYLE = "clasico"
TITLE = ("Ruleta de leyendas de miedo:", "la que salga, te la cuento")
RULETA = {"scene": "t00", "start": 0.4, "dur": 6.2, "target": 3}   # 3 = El Mohán

PARTS = {
1: [
 ("t00", "N", "Gira la ruleta de leyendas. La que salga, te cuento su historia. Y te advierto: ninguna termina bien.", 0.8),
 ("t01", "N", "El Mohán.", 1.2),
 ("t02", "N", "Vives en Natagaima, Tolima, a la orilla del río Magdalena. Tu papá es pescador, y tu hermana Rosa lava ropa en las piedras.", 0.4),
 ("t03", "N", "En tu casa hay una regla: antes de tirar la atarraya, se deja un tabaco y un trago de aguardiente en la piedra grande. Para él.", 0.6),
 ("t04", "P", "El Mohán es el dueño del río. Si le pagas, te deja pescar. Si no le pagas, se cobra solo.", 0.6),
 ("t05", "N", "Pero esta noche te fumas el tabaco y te tomas el trago. Total, eso es un cuento de viejos.", 0.6),
 ("t06", "N", "Tiras la atarraya. Y cuando la jalas, pesa. Pesa demasiado.", 0.6),
 ("t07", "N", "Adentro no hay pescados. Hay pelo. Pelo largo y verde, como musgo. Y enredado, un diente de oro.", 0.6),
 ("t08", "N", "Entonces, desde el agua negra, suena un tiple. Una música suave, que no sale de ningún lado.", 0.5),
 ("t09", "N", "En las piedras, Rosa deja de lavar. Se pone de pie. Y camina hacia el río, como dormida.", 0.4),
 ("t10", "M", "¿No la oyes? Me está llamando. Dice que tiene una casa de oro debajo del agua.", 0.6),
 ("t11", "N", "Le alumbras la cara con la linterna. Tiene los ojos en blanco. Y está sonriendo.", 0.6),
 ("t12", "N", "Detrás de ella, el agua se abre. Sale una cabeza enorme, peluda, con dos ojos rojos como brasas. Fumando tabaco. Tu tabaco.", 1.0),
 ("t13", "N", "¿Qué haces? Opción A: agarras a Rosa y corres al rancho. Opción B: le devuelves algo al Mohán para calmarlo. Comenta A o B. Y sígueme, que la parte dos sale hoy.", 2.0),
],
2: [
 ("u01", "N", "Agarras a Rosa del brazo y la arrastras hasta el rancho. Ella patalea, te araña, quiere volver al río.", 0.4),
 ("u02", "N", "Tu papá se despierta. Cuando ve la atarraya llena de pelo verde, se pone blanco.", 0.4),
 ("u03", "P", "No le pagaste. Ahora ya no quiere tabaco. Ahora quiere a tu hermana.", 0.7),
 ("u04", "N", "Tu papá te cuenta algo que nunca te había contado. Su hermana, tu tía Carmen, desapareció igual hace treinta años. Lavando en esas mismas piedras.", 0.6),
 ("u05", "N", "Amarran a Rosa a la cama. Tu papá riega sal en la puerta, prende una vela y dice: hasta que amanezca, nadie abre. Oigan lo que oigan.", 0.6),
 ("u06", "N", "A la medianoche, la música vuelve. Pero ya no suena en el río. Suena debajo del rancho.", 0.6),
 ("u07", "N", "Huele a tabaco. A agua podrida. Y por las rendijas del piso empieza a subir humo.", 0.5),
 ("u08", "V", "Rosa, mija. Soy tu tía Carmen. Aquí abajo se está bueno. Venga.", 0.7),
 ("u09", "N", "Miras la cama. Rosa ya no está. Las cuerdas están mordidas. Y la ventana, abierta.", 0.6),
 ("u10", "N", "Corres al río con tu papá. Rosa está metida hasta la cintura, caminando derecho hacia el remolino.", 0.4),
 ("u11", "N", "Y en medio del remolino, él. Medio cuerpo afuera del agua. Las manos enormes, con uñas negras, abiertas para recibirla.", 0.6),
 ("u12", "N", "Tu papá se tira al río a sacarla. Y el remolino se lo traga. A él primero.", 0.8),
 ("u13", "N", "¿Qué haces? Opción A: te tiras al río por los dos. Opción B: le ofreces al Mohán lo que más quiere. Comenta A o B. Y sígueme, que el final sale hoy.", 2.0),
],
3: [
 ("v01", "N", "Te tiras al río. El agua está helada, y te jala hacia el fondo como si tuviera manos.", 0.4),
 ("v02", "N", "Abajo no está oscuro. Hay una luz dorada. Una cueva llena de oro, de ollas de barro y de atarrayas viejas.", 0.5),
 ("v03", "N", "Sentadas en las piedras, peinándose, hay mujeres pálidas, con los ojos en blanco. Una tiene la cara de tu papá: es tu tía Carmen. No ha envejecido ni un día.", 0.6),
 ("v04", "N", "El Mohán está sentado, tocando el tiple. Rosa duerme a sus pies. Tu papá, enredado en una atarraya, no se mueve.", 0.6),
 ("v05", "X", "Me robaste el tabaco. Me robaste el trago. Ahora algo tuyo se queda conmigo.", 0.7),
 ("v06", "N", "Y le ofreces lo único que te queda: quédese conmigo. Pero suelte a Rosa y a mi papá.", 0.6),
 ("v07", "N", "El Mohán se ríe. Tiene la boca llena de dientes de oro. Y acepta el trato.", 0.6),
 ("v08", "N", "Te pone la mano en la cara. Sientes cómo te crece el pelo, verde y largo. Cómo se te olvida tu nombre.", 0.8),
 ("v09", "N", "Al amanecer, Rosa despierta en las piedras. Viva. Y a su lado está tu papá. Pero tu papá ya no respira.", 0.6),
 ("v10", "N", "El Mohán cumplió. Los soltó a los dos. Nunca dijo que vivos.", 1.0),
 ("v11", "N", "A ti nunca te encontraron. Rosa se fue de Natagaima y jamás volvió a un río.", 0.6),
 ("v12", "N", "Pero los pescadores dicen que, cuando alguien no deja el tabaco en la piedra, en la atarraya sale un gorro naranja. El tuyo.", 0.8),
 ("v13", "N", "¿Y tú qué hubieras hecho? Opción A: dejarle el tabaco desde el principio. Opción B: soltar la atarraya al ver el pelo. Comenta A o B. Y sígueme, que la ruleta vuelve a girar.", 2.0),
],
}

KEY = {"ruleta", "leyendas", "ninguna", "bien", "mohán", "natagaima", "tolima", "magdalena", "pescador", "rosa", "piedras",
       "regla", "atarraya", "tabaco", "aguardiente", "piedra", "él", "dueño", "pagas", "cobra", "solo", "escondidas", "viejos",
       "pesa", "demasiado", "pescado", "pelo", "verde", "musgo", "diente", "oro", "tiple", "música", "ningún", "dormida",
       "llamando", "casa", "agua", "blanco", "sonriendo", "enorme", "ojos", "rojos", "brasas", "tu", "araña", "río", "hermana",
       "carmen", "treinta", "sal", "vela", "amanezca", "nadie", "medianoche", "debajo", "humo", "podrida", "venga", "mordidas",
       "ventana", "abierta", "cintura", "remolino", "manos", "uñas", "negras", "traga", "primero", "helada", "fondo", "dorada",
       "cueva", "mujeres", "pálidas", "papá", "envejecido", "conmigo", "robaste", "quédese", "suelte", "ríe", "acepta", "cara",
       "nombre", "viva", "respira", "cumplió", "vivos", "nunca", "jamás", "gorro", "naranja", "tuyo", "a", "b", "comenta", "sígueme"}

ENDCARD = {
 1: ("¿QUÉ HACES?", "Agarras a Rosa y corres", "Le devuelves algo al Mohán", "PARTE 2 HOY · SÍGUEME"),
 2: ("¿QUÉ HACES?", "Te tiras al río por los dos", "Le ofreces lo que más quiere", "EL FINAL SALE HOY · SÍGUEME"),
 3: ("¿QUÉ HUBIERAS HECHO?", "Dejarle el tabaco desde el principio", "Soltar la atarraya al ver el pelo", "LA RULETA VUELVE A GIRAR · SÍGUEME"),
}

FX = {
 "t01": [("mohán", "flash"), ("mohán", "shake"), ("mohán", "red")], "t03": [("él", "red")], "t04": [("cobra", "red")],
 "t05": [("viejos", "red")], "t06": [("demasiado", "shake")], "t07": [("pelo", "red"), ("diente", "flash")],
 "t08": [("tiple", "red")], "t09": [("dormida", "red")], "t11": [("blanco", "flash"), ("sonriendo", "red")],
 "t12": [("enorme", "flash"), ("enorme", "shake"), ("brasas", "red"), ("tu", "red")],
 "u01": [("araña", "flash")], "u02": [("blanco", "red")], "u03": [("hermana", "red")], "u04": [("desapareció", "red")],
 "u06": [("debajo", "shake")], "u07": [("humo", "red")], "u08": [("venga", "red")], "u09": [("mordidas", "flash"), ("abierta", "red")],
 "u10": [("remolino", "red")], "u11": [("manos", "flash"), ("manos", "shake"), ("uñas", "red")], "u12": [("traga", "flash"), ("traga", "shake"), ("primero", "red")],
 "v01": [("fondo", "red")], "v02": [("oro", "flash")], "v03": [("tía", "red"), ("envejecido", "red")],
 "v05": [("conmigo", "red"), ("conmigo", "shake")], "v06": [("quédese", "flash")], "v07": [("oro", "red")],
 "v08": [("cara", "flash"), ("nombre", "red")], "v09": [("respira", "flash"), ("respira", "red")], "v10": [("vivos", "shake"), ("vivos", "red")],
 "v11": [("nunca", "red")], "v12": [("gorro", "flash"), ("tuyo", "red")],
}
CUES = {
 "t01": [("mohán", "boom", 1.3)], "t03": [("él", "boom_s", 0.7)], "t04": [("cobra", "boom_s", 0.7)],
 "t05": [("fumas", "whisper", 0.5)], "t06": [("pesa", "creak", 0.7), ("demasiado", "boom_s", 0.8)],
 "t07": [("pelo", "heart", 0.7), ("diente", "boom", 1.1)], "t08": [("tiple", "riser_end", 0.5)],
 "t09": [("dormida", "steps", 0.6)], "t10": [("oro", "whisper", 0.6)], "t11": [("blanco", "boom_s", 0.9)],
 "t12": [("enorme", "boom", 1.3), ("tu", "boom_s", 0.9)],
 "u01": [("araña", "boom_s", 0.7)], "u02": [("blanco", "ping", 0.5)], "u03": [("hermana", "boom", 1.0)],
 "u04": [("desapareció", "whisper", 0.6)], "u05": [("vela", "ping", 0.3)], "u06": [("debajo", "boom", 1.1)],
 "u07": [("humo", "creak", 0.6)], "u08": [("venga", "whisper", 0.8)], "u09": [("mordidas", "boom_s", 0.9), ("abierta", "creak", 0.6)],
 "u10": [("remolino", "heart", 0.8)], "u11": [("manos", "boom", 1.2)], "u12": [("traga", "boom", 1.3)],
 "v01": [("helada", "boom_s", 0.7)], "v02": [("dorada", "riser_end", 0.5)], "v03": [("tía", "boom", 1.0)],
 "v04": [("tiple", "whisper", 0.5)], "v05": [("conmigo", "boom", 1.2)], "v06": [("quédese", "boom_s", 0.8)],
 "v07": [("ríe", "whisper", 0.7)], "v08": [("cara", "boom", 1.1), ("nombre", "heart", 0.7)],
 "v09": [("respira", "boom", 1.2)], "v10": [("vivos", "boom_s", 1.0)], "v11": [("nunca", "heart", 0.6)],
 "v12": [("gorro", "boom", 1.2)],
}
MUSIC = {
 1: [("t00", "tense"), ("t02", "dark"), ("t06", "tense")],
 2: [("u01", "tense"), ("u04", "dark"), ("u06", "tense")],
 3: [("v01", "tense"), ("v06", "dark"), ("v09", "piano"), ("v12", "dark")],
}
