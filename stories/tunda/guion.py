# «La Tunda» — Ruleta de leyendas (salió al azar). Termina en tragedia.
# Voces: N narrador, M voz de mamá (la Tunda la imita), V abuela, K Josué (niño)
STYLE = "clasico"
TITLE = ("Ruleta de leyendas de miedo:", "la que salga, te la cuento")
RULETA = {"scene": "t00", "start": 0.4, "dur": 6.2, "target": 5}   # 5 = La Tunda

PARTS = {
1: [
 ("t00", "N", "Gira la ruleta de leyendas. La que salga, te cuento su historia. Y te advierto: ninguna termina bien.", 0.8),
 ("t01", "N", "La Tunda.", 1.2),
 ("t02", "N", "Vives en Guapi, en el Pacífico, en una casa de madera sobre pilotes, a la orilla del río. Tu hermanito Josué tiene siete años. Y tu mamá trabaja toda la semana en Buenaventura.", 0.4),
 ("t03", "N", "Tu abuela tiene una sola regla: si ves a tu mamá llegar caminando por el manglar, no le hables. Tu mamá siempre llega en lancha.", 0.6),
 ("t04", "K", "¡Mamá llegó! ¡Mamá llegó!", 0.4),
 ("t05", "N", "Te asomas. Al borde del manglar hay una mujer con el vestido amarillo de tu mamá. Con su mismo pañuelo rojo en la cabeza.", 0.4),
 ("t06", "N", "Pero no hay lancha. Y la mujer no camina. Cojea. Un paso normal, y el otro suena hueco, como un palo golpeando el barro.", 0.4),
 ("t07", "N", "Tum. Tum. Tum.", 0.8),
 ("t08", "M", "Josué, mijito, venga. Le traje camarones.", 0.6),
 ("t09", "N", "Josué ya va bajando la escalera. Lo agarras del brazo, y él te muerde la mano para soltarse.", 0.4),
 ("t10", "N", "Tiene los ojos perdidos. Como dormido con los ojos abiertos. Y repite una y otra vez: mamá me llama, mamá me llama.", 0.5),
 ("t11", "N", "La mujer levanta el vestido. Y ves su pierna derecha. No es una pierna. Es un palo negro y largo, como un molinillo de cocina.", 1.0),
 ("t12", "N", "¿Qué haces? Opción A: amarras a Josué a la cama. Opción B: corres a buscar a tu abuela. Comenta A o B. Y sígueme, que la parte dos sale hoy.", 2.0),
],
2: [
 ("u01", "N", "Amarras a Josué a la hamaca. Él llora con voz de niño chiquito. Y afuera, la mujer del vestido amarillo dice tu nombre.", 0.4),
 ("u02", "N", "Tu abuela sube corriendo con una vela y un frasco de agua bendita. Cuando ve a Josué, se pone a llorar.", 0.2),
 ("u03", "V", "Ya lo entundó. Si se lo lleva al manglar, no lo volvemos a ver.", 0.6),
 ("u04", "N", "La Tunda les da camarones podridos a los niños. Les quita la voluntad. Y se los lleva al manglar para criarlos como suyos. Para siempre.", 0.4),
 ("u05", "N", "Solo hay una forma de traerlo de vuelta: que alguien de su sangre le grite su nombre completo. Tres veces. Sin mirar a la Tunda a los ojos.", 0.6),
 ("u06", "N", "Tum. Tum. Tum. Ahora los golpes suenan debajo de la casa. Entre los pilotes.", 0.4),
 ("u07", "N", "Y por una rendija del piso, ves algo. Un ojo amarillo, mirándote desde abajo.", 0.4),
 ("u08", "M", "Mijo, ábrame. Soy su mamá.", 0.8),
 ("u09", "N", "Tu celular vibra. Es tu mamá. La de verdad. Te escribe: ya salí de Buenaventura, llego en tres horas.", 0.4),
 ("u10", "N", "Tres horas. Josué no aguanta tres horas. Ya está mordiendo la hamaca.", 0.5),
 ("u11", "N", "Y entonces la cuerda se rompe.", 0.6),
 ("u12", "N", "Josué salta por la ventana, cae al barro, y corre hacia el manglar. Hacia ella.", 0.8),
 ("u13", "N", "¿Qué haces? Opción A: corres detrás de él. Opción B: esperas a tu mamá. Comenta A o B. Y sígueme, que el final sale hoy.", 2.0),
],
3: [
 ("v01", "N", "Corres detrás de Josué. El barro te llega a las rodillas. Atrás, tu abuela te grita que no la mires a los ojos.", 0.4),
 ("v02", "N", "Lo encuentras en un claro del manglar. Sentado en el barro. Comiendo camarones de las manos de la mujer del vestido amarillo.", 0.5),
 ("v03", "N", "Ella te da la espalda. Y empieza a voltear la cabeza. Despacio.", 0.6),
 ("v04", "N", "Cierras los ojos y gritas su nombre completo: ¡Josué Angulo Rentería! Una vez.", 0.4),
 ("v05", "N", "¡Josué Angulo Rentería! Dos veces.", 0.4),
 ("v06", "N", "Y cuando vas a gritar la tercera, escuchas a tu mamá. Llamándote desde el río.", 0.3),
 ("v07", "M", "¡Mijo! ¿Dónde están?", 0.6),
 ("v08", "N", "Y abres los ojos. Solo un segundo.", 0.8),
 ("v09", "N", "La Tunda está a un metro de tu cara. Tiene la cara de tu mamá, pero estirada, como una máscara mojada. Y sonríe con una boca llena de dientes.", 0.4),
 ("v10", "N", "Con la voz de tu mamá, te dice: ya no grites, mijo. Ahora los dos son míos.", 1.0),
 ("v11", "N", "Al otro día, tu mamá llega a la casa vacía. En la mesa hay una olla de camarones. Todavía calientes.", 0.6),
 ("v12", "N", "Desde esa noche, cuando baja la marea, los pescadores ven dos niños jugando en el manglar. Y detrás de ellos, una mujer de vestido amarillo que cojea.", 0.5),
 ("v13", "N", "Tum. Tum. Tum.", 1.0),
 ("v14", "N", "¿Y tú qué hubieras hecho? Opción A: gritar la tercera vez sin abrir los ojos. Opción B: no ir nunca al manglar. Comenta A o B. Y sígueme, que la ruleta vuelve a girar.", 2.0),
],
}

KEY = {"ruleta", "leyendas", "ninguna", "bien", "tunda", "guapi", "pacífico", "pilotes", "josué", "siete", "regla", "manglar",
       "lancha", "llegó", "amarillo", "pañuelo", "rojo", "cojea", "hueco", "palo", "tum", "camarones", "muerde", "perdidos",
       "llama", "pierna", "negro", "molinillo", "hamaca", "nombre", "vela", "entundó", "podridos", "siempre", "sangre", "tres",
       "veces", "ojos", "debajo", "rendija", "ojo", "abrame", "ábrame", "mamá", "verdad", "horas", "cuerda", "rompe", "ventana",
       "barro", "ella", "claro", "espalda", "despacio", "una", "dos", "río", "segundo", "metro", "máscara", "dientes", "míos",
       "vacía", "calientes", "niños", "a", "b", "comenta", "sígueme"}

ENDCARD = {
 1: ("¿QUÉ HACES?", "Amarras a Josué a la cama", "Corres a buscar a tu abuela", "PARTE 2 HOY · SÍGUEME"),
 2: ("¿QUÉ HACES?", "Corres detrás de él", "Esperas a tu mamá", "EL FINAL SALE HOY · SÍGUEME"),
 3: ("¿QUÉ HUBIERAS HECHO?", "Gritar la 3.ª vez sin abrir los ojos", "No ir nunca al manglar", "LA RULETA VUELVE A GIRAR · SÍGUEME"),
}

FX = {
 "t01": [("tunda", "flash"), ("tunda", "shake"), ("tunda", "red")], "t05": [("amarillo", "red")], "t06": [("cojea", "shake")],
 "t07": [("tum", "shake")], "t09": [("muerde", "flash")], "t11": [("palo", "flash"), ("molinillo", "shake"), ("molinillo", "red")],
 "u01": [("nombre", "red")], "u03": [("entundó", "shake")], "u06": [("debajo", "shake")], "u07": [("ojo", "flash"), ("ojo", "red")],
 "u08": [("mamá", "red")], "u11": [("rompe", "flash"), ("rompe", "shake")], "u12": [("ella", "red")],
 "v03": [("despacio", "red")], "v08": [("segundo", "flash")], "v09": [("metro", "flash"), ("dientes", "shake"), ("dientes", "red")],
 "v10": [("míos", "shake"), ("míos", "red")], "v11": [("calientes", "red")], "v13": [("tum", "shake")],
}
CUES = {
 "t01": [("tunda", "boom", 1.3)], "t04": [("llegó", "ping", 0.4)], "t06": [("hueco", "knock3", 0.7)], "t07": [("tum", "knock3", 1.1)],
 "t09": [("muerde", "boom_s", 0.8)], "t10": [("perdidos", "heart", 0.8)], "t11": [("palo", "boom", 1.2)],
 "u01": [("nombre", "whisper", 0.7)], "u02": [("vela", "ping", 0.3)], "u03": [("entundó", "boom_s", 0.8)], "u06": [("tum", "knock3", 1.1)],
 "u07": [("ojo", "boom", 1.1)], "u08": [("ábrame", "whisper", 0.6)], "u09": [("vibra", "ping", 0.6)], "u10": [("mordiendo", "heart", 0.8)],
 "u11": [("rompe", "boom", 1.1)], "u12": [("salta", "boom_s", 0.8)],
 "v01": [("barro", "steps", 0.8)], "v03": [("voltear", "creak", 0.8)], "v04": [("josué", "boom_s", 0.7)], "v05": [("josué", "boom_s", 0.8)],
 "v06": [("mamá", "riser_end", 0.6)], "v08": [("abres", "boom", 1.2)], "v09": [("dientes", "boom", 1.2)], "v10": [("míos", "boom", 1.3)],
 "v11": [("calientes", "boom_s", 0.8)], "v13": [("tum", "knock3", 1.2)],
}
MUSIC = {
 1: [("t00", "tense"), ("t02", "dark"), ("t05", "tense")],
 2: [("u01", "tense"), ("u04", "dark"), ("u06", "tense")],
 3: [("v01", "tense"), ("v06", "dark"), ("v11", "piano"), ("v13", "dark")],
}
