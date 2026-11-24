# «La Llorona» — Ruleta de leyendas (salió al azar). Termina en tragedia. Final cerrado.
# Voces: N narrador, M voz de mujer (la Llorona / la voz de mamá), V abuela, K Luz (niña)
STYLE = "clasico"
TITLE = ("Ruleta de leyendas de miedo:", "la que salga, te la cuento")
RULETA = {"scene": "t00", "start": 0.4, "dur": 6.2, "target": 0}   # 0 = La Llorona

PARTS = {
1: [
 ("t00", "N", "Gira la ruleta de leyendas. La que salga, te cuento su historia. Y te advierto: ninguna termina bien.", 0.8),
 ("t01", "N", "La Llorona.", 1.2),
 ("t02", "N", "Vives en Honda, Tolima, en una casa vieja a la orilla del río Magdalena. Con tu abuela y tu hermanita Luz, de seis años.", 0.4),
 ("t03", "N", "Tu mamá se ahogó en ese río hace un año. Y Luz todavía la espera, todas las noches, en la ventana.", 0.6),
 ("t04", "N", "Tu abuela tiene una sola regla, y te la repite cada noche: si oyes a una mujer llorando en el río, no la mires. Y nunca, nunca le contestes.", 0.6),
 ("t05", "N", "Esta noche, a las doce en punto, te despierta un llanto.", 0.6),
 ("t06", "M", "¡Ay, mis hijos! ¿Dónde están mis hijos?", 0.8),
 ("t07", "N", "Luz ya está en la ventana. Con los ojos abiertos. Sin parpadear.", 0.4),
 ("t08", "K", "Es mi mamá. Está llorando porque no nos encuentra.", 0.5),
 ("t09", "N", "Te asomas. Abajo, en las piedras del río, hay una mujer vestida de blanco, arrodillada, lavando ropa. El pelo negro le tapa toda la cara.", 0.4),
 ("t10", "N", "Y lo que lava es un vestidito rosado. Igualito al que Luz tiene puesto.", 0.6),
 ("t11", "K", "¡Mami! ¡Aquí estoy!", 0.6),
 ("t12", "N", "El llanto se corta. Silencio. La mujer se pone de pie. Y sigue subiendo, y subiendo. Mide más de tres metros.", 1.0),
 ("t13", "N", "¿Qué haces? Opción A: le tapas la boca a Luz y cierras la ventana. Opción B: despiertas a tu abuela. Comenta A o B. Y sígueme, que la parte dos sale hoy.", 2.0),
],
2: [
 ("u01", "N", "Cierras la ventana y le tapas la boca a Luz. Ella te muerde la mano, llorando: suéltame, es mi mamá.", 0.4),
 ("u02", "N", "Tu abuela sale del cuarto con un rosario. Cuando le cuentas que Luz contestó, el rosario se le cae al piso.", 0.3),
 ("u03", "V", "Le contestó. Ahora la Llorona cree que es su hija. Y viene por ella.", 0.6),
 ("u04", "N", "Hace muchos años, una mujer ahogó a sus hijos en ese río. Cuando se arrepintió, ya era tarde. Desde entonces los busca cada noche. Y se lleva a cualquier niño que le conteste.", 0.4),
 ("u05", "N", "Tu abuela prende una vela y dice que hasta que cante el gallo, no puede entrar. Pero Luz no puede salir. Ni tocar el agua.", 0.6),
 ("u06", "N", "Entonces tocan la puerta. Tres golpes. Mojados.", 0.6),
 ("u07", "M", "Luz, mi amor, ábreme. Soy mamá. Tengo mucho frío.", 0.6),
 ("u08", "N", "Es la voz de tu mamá. Idéntica. Y tú la viste enterrar hace un año.", 0.5),
 ("u09", "N", "Por debajo de la puerta empieza a entrar agua. Agua del río, fría y negra. Con pelos largos flotando, enredándose en tus pies.", 0.4),
 ("u10", "N", "El agua sube. Te llega a los tobillos. A las rodillas. El río se está metiendo a la casa.", 0.4),
 ("u11", "N", "Y debajo del agua, algo te roza la pierna. Una mano. Buscando a Luz.", 0.5),
 ("u12", "N", "Luz grita. La mano la tiene agarrada del tobillo.", 0.8),
 ("u13", "N", "¿Qué haces? Opción A: subes con Luz al techo. Opción B: le contestas tú a la Llorona. Comenta A o B. Y sígueme, que el final sale hoy.", 2.0),
],
3: [
 ("v01", "N", "Jalas a Luz con todas tus fuerzas. La mano la suelta. Y subes con ella al techo por el zarzo.", 0.4),
 ("v02", "N", "Desde el techo ves la calle inundada. Y en medio del agua, de pie, la mujer de blanco. Con los brazos abiertos.", 0.5),
 ("v03", "N", "Tu abuela se quedó abajo. Ya no la escuchas.", 0.6),
 ("v04", "M", "¿Dónde están mis hijos?", 0.6),
 ("v05", "N", "Luz se suelta de tu mano. Camina hacia el borde del techo. Hacia ella.", 0.5),
 ("v06", "N", "Y haces lo único que puedes hacer. Gritas: ¡aquí estoy yo! ¡Lléveme a mí!", 0.6),
 ("v07", "N", "Luz se detiene. La Llorona voltea a mirarte. Y despacio, se abre el pelo con las manos.", 0.6),
 ("v08", "N", "No tiene cara. Tiene una calavera con dos ojos que arden. Y en los brazos carga un bulto envuelto en trapos, que llora.", 0.5),
 ("v09", "N", "Te lo entrega. Pesa como una piedra. Y te hunde con él hasta el fondo del río.", 1.0),
 ("v10", "N", "Al amanecer, el agua baja. Los vecinos encuentran a tu abuela viva, abrazada a un poste. Y a Luz dormida en el techo.", 0.5),
 ("v11", "N", "De ti solo encuentran los zapatos. Uno al lado del otro. En las piedras del río.", 0.6),
 ("v12", "N", "Tu abuela se llevó a Luz lejos, a la sabana, donde no hay ríos. Nunca volvieron. Pero los pescadores de Honda dicen que ahora la Llorona no llora sola. Llora con un muchacho que pregunta por su hermanita.", 0.8),
 ("v13", "N", "¿Y tú qué hubieras hecho? Opción A: contestarle tú desde el principio. Opción B: no asomarte nunca a la ventana. Comenta A o B. Y sígueme, que la ruleta vuelve a girar.", 2.0),
],
}

KEY = {"ruleta", "leyendas", "ninguna", "bien", "llorona", "honda", "tolima", "magdalena", "luz", "seis", "ahogó", "ventana",
       "regla", "llorando", "mires", "nunca", "contestes", "doce", "llanto", "hijos", "parpadear", "mamá", "encuentra", "blanco",
       "arrodillada", "lavando", "pelo", "cara", "vestidito", "rosado", "igualito", "aquí", "silencio", "subiendo", "tres", "metros",
       "muerde", "rosario", "cae", "contestó", "hija", "ella", "ahogó", "tarde", "niño", "gallo", "agua", "golpes", "mojados",
       "frío", "idéntica", "enterrar", "negra", "pelos", "tobillos", "rodillas", "casa", "mano", "grita", "tobillo", "techo",
       "zarzo", "inundada", "abiertos", "abajo", "escuchas", "borde", "yo", "mí", "despacio", "calavera", "arden", "bulto", "llora",
       "piedra", "fondo", "amanecer", "viva", "dormida", "zapatos", "sola", "hermanita", "a", "b", "comenta", "sígueme"}

ENDCARD = {
 1: ("¿QUÉ HACES?", "Le tapas la boca y cierras", "Despiertas a tu abuela", "PARTE 2 HOY · SÍGUEME"),
 2: ("¿QUÉ HACES?", "Subes con Luz al techo", "Le contestas tú", "EL FINAL SALE HOY · SÍGUEME"),
 3: ("¿QUÉ HUBIERAS HECHO?", "Contestarle tú desde el principio", "No asomarte nunca a la ventana", "LA RULETA VUELVE A GIRAR · SÍGUEME"),
}

FX = {
 "t01": [("llorona", "flash"), ("llorona", "shake"), ("llorona", "red")], "t03": [("ahogó", "red")], "t04": [("nunca", "red")],
 "t05": [("llanto", "shake")], "t06": [("hijos", "red")], "t07": [("parpadear", "red")], "t09": [("cara", "red")],
 "t10": [("igualito", "flash"), ("igualito", "red")], "t11": [("aquí", "flash"), ("aquí", "shake")],
 "t12": [("silencio", "red"), ("metros", "flash"), ("metros", "shake")],
 "u01": [("muerde", "flash")], "u02": [("cae", "shake")], "u03": [("viene", "red")], "u06": [("golpes", "shake")],
 "u07": [("frío", "red")], "u08": [("enterrar", "red")], "u09": [("pelos", "red")], "u10": [("rodillas", "shake")],
 "u11": [("mano", "flash"), ("mano", "red")], "u12": [("grita", "flash"), ("tobillo", "shake"), ("tobillo", "red")],
 "v02": [("brazos", "red")], "v03": [("escuchas", "red")], "v04": [("hijos", "shake")], "v05": [("borde", "red")],
 "v06": [("yo", "flash"), ("mí", "shake")], "v07": [("despacio", "red")],
 "v08": [("calavera", "flash"), ("calavera", "shake"), ("arden", "red")], "v09": [("hunde", "flash"), ("fondo", "red")],
 "v11": [("zapatos", "red")], "v12": [("sola", "red")],
}
CUES = {
 "t01": [("llorona", "boom", 1.3)], "t03": [("ahogó", "boom_s", 0.7)], "t04": [("nunca", "boom_s", 0.6)],
 "t05": [("doce", "ping", 0.4), ("llanto", "whisper", 0.8)], "t06": [("hijos", "boom_s", 0.6)], "t07": [("parpadear", "heart", 0.8)],
 "t09": [("blanco", "creak", 0.6)], "t10": [("igualito", "boom", 1.1)], "t11": [("aquí", "boom_s", 0.9)],
 "t12": [("silencio", "riser_end", 0.6), ("metros", "boom", 1.2)],
 "u01": [("muerde", "boom_s", 0.7)], "u02": [("cae", "ping", 0.5)], "u03": [("viene", "boom_s", 0.8)],
 "u04": [("ahogó", "whisper", 0.6)], "u05": [("gallo", "ping", 0.3)], "u06": [("tocan", "knock3", 1.1)],
 "u07": [("ábreme", "whisper", 0.6)], "u08": [("enterrar", "boom_s", 0.7)], "u09": [("agua", "scrape", 0.6)],
 "u10": [("rodillas", "heart", 0.8)], "u11": [("mano", "boom", 1.1)], "u12": [("grita", "boom", 1.2)],
 "v01": [("jalas", "boom_s", 0.7)], "v02": [("brazos", "riser_end", 0.6)], "v03": [("escuchas", "heart", 0.7)],
 "v04": [("hijos", "whisper", 0.7)], "v05": [("borde", "steps", 0.7)], "v06": [("yo", "boom_s", 0.9)],
 "v07": [("despacio", "creak", 0.8)], "v08": [("calavera", "boom", 1.3)], "v09": [("hunde", "boom", 1.2)],
 "v10": [("amanecer", "ping", 0.3)], "v11": [("zapatos", "boom_s", 0.8)], "v12": [("sola", "whisper", 0.7)],
}
MUSIC = {
 1: [("t00", "tense"), ("t02", "dark"), ("t05", "tense")],
 2: [("u01", "tense"), ("u04", "dark"), ("u06", "tense")],
 3: [("v01", "tense"), ("v06", "dark"), ("v10", "piano"), ("v12", "dark")],
}
