# «La estatua del payaso» — basada en la leyenda urbana viral de la niñera y la estatua (versión propia, 3 partes)
# Voces: N narrador, K niño/niña, P papá, M mamá, X voz ronca
STYLE = "clasico"
TITLE = ("La estatua del payaso", "que nadie compró")

PARTS = {
1: [
 ("g01", "N", "Estás cuidando a dos niños en una casa enorme del norte de Bogotá. Son las once de la noche. Y hay algo en la sala que no te deja ver televisión tranquilo.", 0.4),
 ("g02", "N", "Una estatua de payaso. De tamaño real. Sentada en la esquina, al lado de la chimenea.", 0.6),
 ("g03", "N", "Los papás se fueron a un matrimonio en Chía. Te dejaron una lista: los niños se acuestan a las nueve. No le abras a nadie. Y si pasa algo, escríbenos.", 0.4),
 ("g04", "N", "Sofi y Tomás se durmieron temprano. Pero antes, Tomás te dijo algo raro:", 0.2),
 ("g05", "K", "No te sientes en el sofá grande. Ahí se sienta Pepe.", 0.6),
 ("g06", "N", "Te reíste. Pensaste que Pepe era un amigo imaginario.", 0.4),
 ("g07", "N", "Ahora estás en el sofá chiquito. Y cada vez que miras el celular, sientes que la estatua te está mirando.", 0.4),
 ("g08", "N", "Tiene la cara blanca. La boca pintada hasta las orejas. Y los ojos... se ven mojados.", 0.8),
 ("g09", "N", "No aguantas más. Le escribes al papá: perdón, ¿puedo tapar la estatua del payaso con una cobija? Me da cosa.", 0.4),
 ("g10", "N", "Pasa un minuto. Dos. Y te responde:", 0.3),
 ("g11", "P", "Saca a los niños de la casa. Ya. Llama a la policía.", 0.5),
 ("g12", "N", "Le escribes: ¿por qué? Y te contesta con una sola frase:", 0.3),
 ("g13", "P", "Nosotros no tenemos ninguna estatua de payaso.", 1.0),
 ("g14", "N", "Levantas la mirada despacio. La esquina de la chimenea está vacía.", 0.6),
 ("g15", "N", "Y el sofá grande está hundido. Como si alguien acabara de sentarse.", 1.0),
 ("g16", "N", "¿Qué haces? Opción A: corres al cuarto de los niños. Opción B: sales a pedir ayuda. Comenta A o B. Y sígueme, que la parte dos sale hoy.", 2.0),
],
2: [
 ("h01", "N", "La estatua ya no está en la esquina. Y el sofá grande sigue hundido.", 0.4),
 ("h02", "N", "Subes la escalera de dos en dos. El cuarto de los niños está oscuro. Las dos camas están vacías.", 0.5),
 ("h03", "N", "Escuchas risitas. Vienen del clóset.", 0.5),
 ("h04", "N", "Abres despacio. Sofi y Tomás están ahí, en piyama, abrazados. Y Sofi te dice, muy seria:", 0.2),
 ("h05", "K", "Shhh. Estamos jugando a las escondidas con Pepe. Él cuenta hasta cien.", 0.4),
 ("h06", "N", "Y desde abajo, una voz ronca, lenta, empieza a contar:", 0.2),
 ("h07", "X", "Noventa y uno... noventa y dos...", 0.5),
 ("h08", "N", "Agarras a los niños. La ventana del cuarto da al techo del garaje. Es la única salida.", 0.4),
 ("h09", "N", "Bajas primero. Recibes a Sofi. Pero Tomás se queda pegado a la ventana.", 0.2),
 ("h10", "K", "Pepe dice que no me puedo ir. Que yo soy su favorito.", 0.5),
 ("h11", "X", "Cien.", 0.8),
 ("h12", "N", "Pasos subiendo la escalera. Lentos. Con zapatos grandes, de payaso, que suenan en cada escalón.", 0.4),
 ("h13", "N", "Estiras los brazos y le gritas a Tomás que salte. Y Tomás salta.", 0.5),
 ("h14", "N", "Corren hasta la portería del conjunto. El celador llama a la policía. Llegan en ocho minutos.", 0.4),
 ("h15", "N", "Revisan la casa entera. No hay nadie. Pero en el sofá grande hay un vaso de leche a medio tomar. Y una nota escrita con crayola:", 0.3),
 ("h16", "X", "Gracias por cuidarlos. Ya sé dónde vives.", 1.0),
 ("h17", "N", "¿Qué haces? Opción A: te quedas a dormir en esa casa. Opción B: te vas para la tuya. Comenta A o B. Y sígueme, que el final sale hoy.", 2.0),
],
3: [
 ("i01", "N", "El payaso te dejó una nota: ya sé dónde vives. La policía dice que es una broma de mal gusto.", 0.4),
 ("i02", "N", "Los papás llegan a las doce y media, pálidos. Abrazan a los niños. Y la mamá te hace una pregunta:", 0.2),
 ("i03", "M", "¿Los niños te hablaron de Pepe?", 0.6),
 ("i04", "N", "Hace ocho meses que los niños hablan de Pepe. Que les deja dulces debajo de la almohada. Que les canta cuando hay tormenta.", 0.4),
 ("i05", "N", "Los papás creían que era un amigo imaginario. Hasta hoy.", 0.6),
 ("i06", "N", "La policía vuelve con perros. Y uno de los perros se pone a ladrar contra la pared del clóset de los niños.", 0.4),
 ("i07", "N", "Detrás de la pared hay un hueco. Un cuartico del tamaño de un ataúd. Con una cobija, latas vacías, y cientos de dibujos.", 0.5),
 ("i08", "N", "Dibujos de la familia durmiendo. Vistos desde arriba. Uno por cada noche.", 0.6),
 ("i09", "N", "El último dibujo es de hoy. Eres tú. En el sofá chiquito, mirando el celular.", 0.5),
 ("i10", "N", "Y debajo, escrita con crayola, una dirección. La tuya.", 1.0),
 ("i11", "N", "Esa noche no vuelves a tu casa. Te quedas donde un amigo. Tres días.", 0.4),
 ("i12", "N", "Al cuarto día, por fin vuelves. Todo está igual. Tu cama. Tu ropa. Tus cosas.", 0.4),
 ("i13", "N", "Hasta que abres la nevera. Hay un vaso de leche a medio tomar.", 0.8),
 ("i14", "N", "Y en la sala, en la esquina, al lado del televisor, hay una estatua de payaso. Que tú nunca compraste.", 1.2),
 ("i15", "N", "¿Qué haces? Opción A: sales corriendo sin mirar atrás. Opción B: te acercas a ver si es solo una estatua. Comenta A o B. Y si quieres la segunda temporada, sígueme.", 2.0),
],
}

KEY = {"once", "noche", "estatua", "payaso", "real", "esquina", "chimenea", "nadie", "escríbenos", "pepe", "grande", "imaginario",
       "mirando", "blanca", "orejas", "mojados", "tapar", "cobija", "saca", "ya", "policía", "ninguna", "vacía", "hundido",
       "sentarse", "vacías", "risitas", "clóset", "escondidas", "cien", "ronca", "noventa", "ventana", "garaje", "favorito",
       "pasos", "zapatos", "salta", "leche", "crayola", "gracias", "dónde", "vives", "pálidos", "ocho", "meses", "dulces",
       "almohada", "perros", "ladrar", "hueco", "ataúd", "dibujos", "durmiendo", "arriba", "hoy", "tú", "dirección", "tuya",
       "nevera", "nunca", "compraste", "a", "b", "comenta", "sígueme"}

ENDCARD = {
 1: ("¿QUÉ HACES?", "Corres al cuarto de los niños", "Sales a pedir ayuda", "PARTE 2 HOY · SÍGUEME"),
 2: ("¿QUÉ HACES?", "Te quedas a dormir en esa casa", "Te vas para la tuya", "EL FINAL SALE HOY · SÍGUEME"),
 3: ("¿QUÉ HACES?", "Sales corriendo sin mirar atrás", "Te acercas a ver si es estatua", "¿2.ª TEMPORADA? · SÍGUEME"),
}

FX = {
 "g02": [("payaso", "red")], "g08": [("mojados", "shake")], "g11": [("ya", "flash")], "g13": [("ninguna", "flash"), ("payaso", "shake")],
 "g14": [("vacía", "red")], "g15": [("hundido", "shake")],
 "h02": [("vacías", "flash")], "h07": [("noventa", "red")], "h10": [("favorito", "red")], "h11": [("cien", "flash"), ("cien", "shake")],
 "h13": [("salta", "shake")], "h16": [("vives", "flash"), ("vives", "red")],
 "i06": [("ladrar", "shake")], "i07": [("ataúd", "red")], "i09": [("tú", "flash")], "i10": [("tuya", "red"), ("tuya", "shake")],
 "i13": [("leche", "flash")], "i14": [("estatua", "flash"), ("compraste", "shake"), ("compraste", "red")],
}
CUES = {
 "g02": [("payaso", "boom_s", 0.8)], "g05": [("pepe", "ping", 0.3)], "g08": [("mojados", "heart", 0.8)],
 "g09": [("escribes", "ping", 0.5)], "g10": [("responde", "ping", 0.6)], "g11": [("ya", "boom_s", 0.9)],
 "g13": [("ninguna", "boom", 1.2)], "g14": [("vacía", "boom_s", 0.8)], "g15": [("hundido", "creak", 0.9)],
 "h02": [("vacías", "boom_s", 0.8)], "h03": [("risitas", "whisper", 0.6)], "h04": [("abres", "creak", 0.7)],
 "h07": [("noventa", "heart", 0.8)], "h11": [("cien", "boom", 1.2)], "h12": [("pasos", "steps", 1.0)],
 "h13": [("salta", "boom_s", 0.7)], "h14": [("policía", "ping", 0.4)], "h15": [("nota", "paper", 0.6)], "h16": [("vives", "boom", 1.2)],
 "i03": [("pepe", "boom_s", 0.7)], "i06": [("ladrar", "knock3", 0.8)], "i07": [("hueco", "boom_s", 0.8)], "i08": [("dibujos", "paper", 0.6)],
 "i09": [("tú", "boom", 1.0)], "i10": [("tuya", "boom", 1.2)], "i12": [("vuelves", "creak", 0.6)], "i13": [("leche", "boom_s", 0.9)],
 "i14": [("estatua", "boom", 1.3)],
}
MUSIC = {
 1: [("g01", "tense"), ("g04", "dark"), ("g09", "tense"), ("g14", "dark")],
 2: [("h01", "tense"), ("h06", "dark"), ("h14", "tense")],
 3: [("i01", "dark"), ("i06", "tense"), ("i11", "dark"), ("i13", "tense")],
}
