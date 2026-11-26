# «El Pollo Maligno» — Ruleta de leyendas (salió al azar). Termina en tragedia. Final cerrado.
# Voces: N narrador, V abuela, P tío Aurelio, K Valentina (hermanita), X el Pollo Maligno
STYLE = "clasico"
TITLE = ("Ruleta de leyendas de miedo:", "la que salga, te la cuento")
RULETA = {"scene": "t00", "start": 0.4, "dur": 6.2, "target": 7}   # 7 = El Pollo Maligno

PARTS = {
1: [
 ("t00", "N", "Gira la ruleta de leyendas. La que salga, te cuento su historia. Y te advierto: ninguna termina bien.", 0.8),
 ("t01", "N", "El Pollo Maligno.", 1.2),
 ("t02", "N", "Vives en una finca cafetera en La Plata, Huila. Los sábados, tu tío Aurelio y sus amigos juegan cartas en el corredor. Con aguardiente.", 0.4),
 ("t03", "N", "Tu abuela tiene una regla: si de noche se oye piar un pollo en el monte, se botan las cartas y se reza a San Miguel. Y nunca se le arremeda el canto.", 0.6),
 ("t04", "V", "Ese pollo odia a los que juegan y beben de noche. Si canta agudito, se muere un niño. Si canta grueso, se muere un grande.", 0.6),
 ("t05", "N", "Esta noche, a las doce, se oye. Pío. Pío. Pío. Agudito. Lejísimos, al fondo del cafetal.", 0.6),
 ("t06", "N", "Tu abuela se pone pálida. Porque con ese pollo es al revés: cuando suena lejos, es que está cerca.", 0.6),
 ("t07", "P", "¡Pío, pío, pío! Venga, pollito, siéntese a jugar con nosotros.", 0.5),
 ("t08", "N", "Los amigos se ríen. Y de golpe, el cafetal se queda en silencio. Y las cartas de la mesa se voltean solas.", 0.5),
 ("t09", "N", "Tu hermanita Valentina, de seis años, está en la puerta, en pijama. Mirando hacia el techo.", 0.4),
 ("t10", "K", "Hay un pollo grandote en el techo. Tiene cara de murciélago. Y me está mirando a mí.", 0.6),
 ("t11", "N", "Alumbras con la linterna. Unas garras rayan el techo de zinc. Y por el borde asoma una cresta roja como sangre, y dos ojos amarillos.", 1.0),
 ("t12", "N", "¿Qué haces? Opción A: escondes a Valentina debajo de la cama. Opción B: rezas a San Miguel con tu abuela. Comenta A o B. Y sígueme, que la parte dos sale hoy.", 2.0),
],
2: [
 ("u01", "N", "Escondes a Valentina debajo de la cama y le tapas la boca. Arriba, algo camina por el techo. Rasguña el zinc. De un lado al otro.", 0.4),
 ("u02", "N", "Tu abuela prende una vela, saca la camándula y empieza: San Miguel Arcángel, defiéndenos en la batalla.", 0.5),
 ("u03", "V", "Hay que rezarla nueve veces. Sin parar. Si uno para, ese animal entra.", 0.6),
 ("u04", "N", "Una. Dos. Tres. El piar se va alejando. Cuatro. Cinco. Cada vez más lejos. Y tú sabes lo que eso significa.", 0.6),
 ("u05", "N", "Seis. El piar ya no viene de afuera. Viene de adentro de la casa. Del cuarto donde escondiste a Valentina.", 0.6),
 ("u06", "N", "Siete. Tu tío Aurelio, borracho, se levanta con el machete en la mano y abre la puerta del cuarto de una patada.", 0.4),
 ("u07", "P", "¡Salga, pollo del diablo! ¡A mí es al que busca!", 0.5),
 ("u08", "N", "Y tu abuela deja de rezar. Solo un segundo. Para gritarle que no entre.", 0.6),
 ("u09", "N", "El canto cambia. Ya no es agudito. Es grueso. Ronco. Como un gallo con la garganta llena de tierra.", 0.6),
 ("u10", "N", "La luz se va. En lo oscuro se oyen alas enormes golpeando las paredes. Tu tío grita. Y luego, nada.", 0.8),
 ("u11", "N", "Prendes la linterna. El machete está en el piso. Tu tío ya no está. Solo quedan plumas negras, y las cartas regadas, todas boca arriba.", 0.6),
 ("u12", "N", "Y debajo de la cama, Valentina ya no tiembla. Está sonriendo, con los ojos en blanco. Y empieza a piar.", 0.8),
 ("u13", "N", "¿Qué haces? Opción A: sacas a Valentina y corres al pueblo. Opción B: terminas las nueve oraciones. Comenta A o B. Y sígueme, que el final sale hoy.", 2.0),
],
3: [
 ("v01", "N", "Te subes a Valentina a la espalda y corres por la trocha, hacia el pueblo. Tu abuela se queda rezando, para darles tiempo.", 0.4),
 ("v02", "N", "Valentina va abrazada a tu cuello. Y sigue piando. Bajito. Pegada a tu oreja.", 0.6),
 ("v03", "N", "En la curva del camino, el canto suena delante de ti. Agudito. Esperándote.", 0.6),
 ("v04", "N", "Tu abuela te lo dijo: si el pollo canta adelante, uno se devuelve. Si sigue, le cae la desgracia.", 0.5),
 ("v05", "N", "Te devuelves corriendo. Y adentro del escaparate, llorando, está Valentina. La de verdad. Escondida ahí desde que se fue la luz.", 0.8),
 ("v06", "N", "Entonces, ¿qué es lo que llevas cargado en la espalda?", 1.0),
 ("v07", "N", "Unas garras se te clavan en los hombros. Unas alas negras de buitre te envuelven. Y por tu hombro se asoma una cabeza de murciélago, con cresta de gallo.", 0.6),
 ("v08", "X", "Canté agudito. Por un niño. Nunca dije cuál.", 1.0),
 ("v09", "N", "Tienes catorce años. Todos pensaron en Valentina. Nadie pensó en ti.", 0.6),
 ("v10", "N", "Tu abuela termina la novena oración. Amén. Pero ya es tarde. Las alas se abren, y el corredor queda vacío.", 0.8),
 ("v11", "N", "Al amanecer los encuentran en el cafetal, a ti y a tu tío, debajo de un guamo. Sin una gota de sangre. Con plumas negras en la boca.", 0.6),
 ("v12", "N", "En esa finca nunca más se jugaron cartas. Y cuando alguien arremeda a un pollo, Valentina le tapa la boca y reza nueve veces.", 0.5),
 ("v13", "N", "¿Y tú qué hubieras hecho? Opción A: quedarte rezando con tu abuela. Opción B: callar a tu tío a tiempo. Comenta A o B. Y sígueme, que la ruleta vuelve a girar.", 2.0),
],
}

KEY = {"ruleta", "leyendas", "ninguna", "bien", "pollo", "maligno", "plata", "huila", "cafetera", "sábados", "aurelio", "cartas",
       "madrugada", "aguardiente", "regla", "piar", "botan", "radio", "san", "miguel", "nunca", "arremeda", "odia", "agudito",
       "niño", "grueso", "grande", "doce", "pío", "lejísimos", "pálida", "revés", "lejos", "cerca", "pollito", "jugar", "silencio",
       "solas", "valentina", "seis", "pijama", "techo", "grandote", "murciélago", "mí", "linterna", "garras", "zinc", "cresta",
       "sangre", "amarillos", "parpadean", "cama", "boca", "camina", "rasguña", "vela", "camándula", "batalla", "nueve", "entra",
       "significa", "adentro", "cuarto", "machete", "patada", "diablo", "busca", "segundo", "entre", "ronco", "tierra", "luz",
       "alas", "enormes", "nada", "plumas", "negras", "arriba", "blanco", "sonriendo", "espalda", "trocha", "pueblo", "tiempo",
       "oreja", "delante", "esperándote", "devuelve", "desgracia", "escaparate", "verdad", "cargado", "hombros", "buitre",
       "gallo", "cuál", "catorce", "ti", "amén", "tarde", "vacío", "amanecer", "guamo", "gota", "creció", "veces", "a", "b",
       "comenta", "sígueme"}

ENDCARD = {
 1: ("¿QUÉ HACES?", "Escondes a Valentina debajo de la cama", "Rezas a San Miguel con tu abuela", "PARTE 2 HOY · SÍGUEME"),
 2: ("¿QUÉ HACES?", "Sacas a Valentina y corres", "Terminas las nueve oraciones", "EL FINAL SALE HOY · SÍGUEME"),
 3: ("¿QUÉ HUBIERAS HECHO?", "Quedarte rezando con tu abuela", "Callar a tu tío a tiempo", "LA RULETA VUELVE A GIRAR · SÍGUEME"),
}

FX = {
 "t01": [("pollo", "flash"), ("maligno", "shake"), ("maligno", "red")], "t03": [("arremeda", "red")], "t04": [("niño", "red")],
 "t05": [("pío", "red")], "t06": [("cerca", "flash"), ("cerca", "red")], "t08": [("silencio", "red"), ("solas", "shake")],
 "t09": [("techo", "red")], "t10": [("murciélago", "red"), ("mí", "shake")],
 "t11": [("garras", "shake"), ("cresta", "flash"), ("sangre", "red"), ("amarillos", "red")],
 "u01": [("rasguña", "shake")], "u03": [("entra", "red")], "u04": [("significa", "red")], "u05": [("adentro", "flash"), ("adentro", "red")],
 "u06": [("patada", "flash"), ("patada", "shake")], "u07": [("diablo", "red")], "u08": [("segundo", "red")],
 "u09": [("grueso", "shake"), ("ronco", "red")], "u10": [("luz", "flash"), ("alas", "shake"), ("grita", "red")],
 "u11": [("plumas", "red")], "u12": [("blanco", "flash"), ("piar", "shake"), ("piar", "red")],
 "v02": [("piando", "red")], "v03": [("delante", "flash"), ("delante", "red")], "v04": [("desgracia", "red")],
 "v05": [("verdad", "flash"), ("verdad", "red")], "v06": [("espalda", "shake"), ("espalda", "red")],
 "v07": [("garras", "flash"), ("garras", "shake"), ("murciélago", "red")], "v08": [("cuál", "shake"), ("cuál", "red")],
 "v09": [("ti", "red")], "v10": [("abren", "flash"), ("abren", "shake"), ("vacío", "red")], "v11": [("sangre", "red")],
}
CUES = {
 "t01": [("maligno", "boom", 1.3)], "t02": [("cartas", "paper", 0.5)], "t03": [("piar", "piar", 0.6)], "t04": [("niño", "boom_s", 0.7)],
 "t05": [("pío", "piar", 0.5)], "t06": [("cerca", "boom", 1.0)], "t07": [("pollito", "piar_grave", 0.3)],
 "t08": [("silencio", "riser_end", 0.5), ("solas", "paper", 0.7)], "t09": [("techo", "heart", 0.7)],
 "t10": [("mí", "boom_s", 0.8)], "t11": [("garras", "scrape", 0.9), ("cresta", "boom", 1.2), ("amarillos", "piar", 0.7)],
 "u01": [("rasguña", "scrape", 0.9), ("lado", "steps", 0.5)], "u02": [("vela", "ping", 0.3)], "u03": [("entra", "boom_s", 0.7)],
 "u04": [("alejando", "piar", 0.35), ("significa", "heart", 0.8)], "u05": [("adentro", "boom", 1.1), ("cuarto", "piar", 0.8)],
 "u06": [("patada", "boom_s", 0.9)], "u08": [("gritarle", "riser_end", 0.6)], "u09": [("ronco", "piar_grave", 1.0)],
 "u10": [("luz", "boom", 1.0), ("alas", "whoosh", 1.0), ("grita", "boom_s", 0.9)], "u11": [("linterna", "ping", 0.3)],
 "u12": [("blanco", "boom", 1.1), ("piar", "piar", 0.9)],
 "v01": [("trocha", "steps", 0.8)], "v02": [("piando", "piar", 0.45)], "v03": [("delante", "piar", 0.9)], "v04": [("desgracia", "boom_s", 0.7)],
 "v05": [("escaparate", "creak", 0.8), ("verdad", "boom", 1.1)], "v06": [("espalda", "heart", 0.9)],
 "v07": [("garras", "boom", 1.2), ("alas", "whoosh", 1.0)], "v08": [("cuál", "boom", 1.3)],
 "v10": [("amén", "ping", 0.4), ("abren", "whoosh", 1.0), ("vacío", "boom", 1.1)], "v11": [("plumas", "boom_s", 0.8)],
}
MUSIC = {
 1: [("t00", "tense"), ("t02", "dark"), ("t05", "tense")],
 2: [("u01", "tense"), ("u04", "dark"), ("u09", "tense")],
 3: [("v01", "tense"), ("v05", "dark"), ("v11", "piano")],
}
