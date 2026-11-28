# «Brote zombi: atrapado en un TransMilenio» — formato trend TikTok nov-2026 (supervivencia zombi, segunda persona,
# por días, cada parte termina en decisión A/B). Historia original. Final cerrado y trágico en el Día 3.
STYLE = "clasico"
TITLE = ("Brote zombi en Bogotá:", "quedaste atrapado en un TransMilenio")

PARTS = {
1: [
 ("d01", "N", "Día uno. En un TransMilenio lleno, un señor muerde a la muchacha de al lado.", 0.4),
 ("d02", "N", "Ella cae entre los pies de todos. Cuando se levanta, tiene los ojos rojos. Y muerde al primero que encuentra.", 0.4),
 ("d03", "N", "El conductor frena en seco en plena troncal y bloquea las puertas. Los de atrás quedan con ellos. Los de adelante, contigo.", 0.4),
 ("d04", "N", "Tú. Doña Gloria, la de los dulces. Un policía bachiller. Y el conductor, que no suelta el radio.", 0.4),
 ("d05", "N", "Entre los dos vagones solo hay un fuelle de caucho. Lo trancan con el carrito de dulces. Del otro lado, algo empieza a arañar.", 0.5),
 ("d06", "N", "A medianoche, una mujer con un bebé en brazos golpea la puerta de vidrio. Detrás de ella, a una cuadra, viene la horda.", 0.5),
 ("d07", "N", "¿Qué haces? Opción A: abres la puerta. Opción B: la dejas cerrada. Comenta A o B. Y sígueme, que el día dos sale hoy.", 1.8),
],
2: [
 ("e01", "N", "Día dos. Abriste. La mujer y el bebé entran, y la puerta se cierra a un centímetro de la horda.", 0.4),
 ("e02", "N", "Afuera hay cuarenta caras pegadas al vidrio. Te miran. Y empiezan a sacudir el bus.", 0.5),
 ("e03", "N", "Al amanecer, el radio se queda mudo. Y la batería empieza a morir: las luces parpadean.", 0.4),
 ("e04", "N", "El conductor dice: si arrancamos ya, llegamos al portal del Norte. Allá está el ejército.", 0.4),
 ("e05", "N", "Y entonces lo oyes. El fuelle de caucho se está rasgando. Desde el vagón de atrás.", 0.5),
 ("e06", "N", "Te acercas a mirar. Una mano gris sale por el hueco... y te agarra el brazo.", 0.6),
 ("e07", "N", "¿Qué haces? Opción A: le gritas al conductor que arranque. Opción B: tapas el hueco con lo que encuentres. Comenta A o B. Y sígueme, que el final sale hoy.", 1.8),
],
3: [
 ("f01", "N", "Día tres. Te soltaste de esa mano a tiempo. O eso crees. El bus arranca a toda velocidad por la Autopista Norte.", 0.4),
 ("f02", "N", "Con cada zombi que atropella, el fuelle se rasga más. Doña Gloria lo tapa con su espalda.", 0.5),
 ("f03", "N", "Ya ves el portal. Faltan cien metros. Y el fuelle se rompe.", 0.5),
 ("f04", "N", "Los de atrás caen encima de doña Gloria. Ella solo alcanza a decir: corra, mijo.", 0.6),
 ("f05", "N", "El bus se estrella contra la reja. El conductor ya no se mueve. El policía te jala hacia afuera.", 0.5),
 ("f06", "N", "Un soldado te alumbra el brazo. Ahí está: un rasguño gris.", 0.6),
 ("f07", "N", "El policía, la mujer y el bebé se suben al camión. A ti te dejan del otro lado de la reja. Y ya no sientes nada.", 0.8),
 ("f08", "N", "¿Tú habrías abierto la puerta? Opción A: sí. Opción B: no. Comenta A o B. Y sígueme para más historias de supervivencia.", 2.0),
],
}

KEY = {"uno", "dos", "tres", "transmilenio", "bogotá", "muerde", "muchacha", "cae", "levanta", "rojos", "frena", "puertas", "atrás", "contigo",
       "tú", "gloria", "dulces", "policía", "conductor", "radio", "fuelle", "caucho", "carrito", "arañar", "medianoche", "bebé", "vidrio",
       "horda", "abriste", "centímetro", "cuarenta", "vidrio", "sacudir", "mudo", "batería", "parpadean", "portal", "ejército",
       "rasgando", "mano", "gris", "brazo", "soltaste", "crees", "velocidad", "atropella", "espaldas", "soldados", "cien", "rompe",
       "grita", "corra", "estrella", "reja", "mueve", "linterna", "rasguño", "camión", "miedo", "nada", "a", "b", "comenta", "sígueme"}

ENDCARD = {
 1: ("¿QUÉ HACES?", "Abres la puerta", "La dejas cerrada", "EL DÍA 2 SALE HOY · SÍGUEME"),
 2: ("¿QUÉ HACES?", "Le gritas que arranque", "Tapas el hueco", "EL FINAL SALE HOY · SÍGUEME"),
 3: ("¿HABRÍAS ABIERTO?", "Sí, abro la puerta", "No, la dejo cerrada", "SÍGUEME PARA MÁS HISTORIAS"),
}

FX = {
 "d01": [("muerde", "flash"), ("muerde", "shake"), ("muerde", "red")], "d02": [("rojos", "red"), ("muerde", "shake")],
 "d03": [("frena", "shake")], "d05": [("arañar", "red")], "d06": [("horda", "red")],
 "e01": [("centímetro", "shake")], "e02": [("sacudir", "shake")], "e03": [("parpadean", "flash")],
 "e05": [("rasgando", "red")], "e06": [("agarra", "flash"), ("agarra", "shake"), ("agarra", "red")],
 "f01": [("arranca", "shake")], "f02": [("atropella", "shake")], "f03": [("rompe", "flash"), ("rompe", "shake")],
 "f04": [("encima", "red")], "f05": [("estrella", "flash"), ("estrella", "shake")], "f06": [("rasguño", "red")],
 "f07": [("nada", "red")],
}
CUES = {
 "d01": [("muerde", "boom", 1.3), ("muerde", "growl", 1.0)], "d02": [("cae", "boom_s", 0.6), ("rojos", "growl", 0.9)],
 "d03": [("frena", "boom", 1.1), ("puertas", "lock", 0.7)], "d04": [("radio", "ping", 0.3)],
 "d05": [("arañar", "scrape", 0.8)], "d06": [("golpea", "knock3", 1.0), ("horda", "growl", 0.9)],
 "e01": [("centímetro", "boom", 1.2), ("centímetro", "growl", 0.8)], "e02": [("cuarenta", "growl", 0.7), ("sacudir", "boom_s", 0.9)],
 "e03": [("mudo", "ping", 0.3), ("parpadean", "boom_s", 0.5)], "e04": [("portal", "heart", 0.6)],
 "e05": [("rasgando", "scrape", 0.9)], "e06": [("agarra", "boom", 1.3), ("agarra", "growl", 1.1)],
 "f01": [("arranca", "boom_s", 0.9)], "f02": [("atropella", "boom", 1.0), ("espalda", "growl", 0.7)],
 "f03": [("cien", "heart", 0.8), ("rompe", "boom", 1.3), ("rompe", "growl", 1.0)], "f04": [("encima", "growl", 1.0)],
 "f05": [("estrella", "boom", 1.4)], "f06": [("alumbra", "ping", 0.3), ("rasguño", "boom", 1.1)],
 "f07": [("camión", "boom_s", 0.6), ("nada", "growl", 1.0)],
}
MUSIC = {
 1: [("d01", "tense"), ("d04", "dark"), ("d06", "tense")],
 2: [("e01", "tense"), ("e03", "dark"), ("e05", "tense")],
 3: [("f01", "tense"), ("f05", "dark"), ("f07", "piano")],
}
