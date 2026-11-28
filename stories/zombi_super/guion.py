# «Brote zombi: atrapado en el supermercado» — formato trend TikTok nov-2026 (historias de supervivencia zombi,
# segunda persona, por días, cada parte termina en decisión). Historia original. Final cerrado en el Día 3.
STYLE = "clasico"
TITLE = ("Brote zombi en Bogotá:", "quedaste atrapado en el supermercado")

PARTS = {
1: [
 ("d01", "N", "Día uno. La señora de adelante en la fila del supermercado... muerde a la cajera.", 0.4),
 ("d02", "N", "La cajera cae al piso. Diez segundos después, se levanta. Y ya no parpadea.", 0.4),
 ("d03", "N", "El vigilante baja la reja de golpe. Adentro quedan seis personas. Afuera, en cinco minutos, ya son veinte.", 0.4),
 ("d04", "N", "Tú. Don Héctor, el carnicero. Una mamá con su niña. Un repartidor. Y una muchacha con el brazo vendado.", 0.4),
 ("d05", "N", "Don Héctor apaga las luces y dice: los de afuera se cansan. Los de adentro, no.", 0.5),
 ("d06", "N", "A medianoche, el repartidor te despierta. La venda de la muchacha tiene sangre fresca. Y ella no deja de rascarse.", 0.5),
 ("d07", "N", "¿Qué haces? Opción A: la encierras en el cuarto frío. Opción B: le crees y la dejas con el grupo. Comenta A o B. Y sígueme, que el día dos sale hoy.", 1.8),
],
2: [
 ("e01", "N", "Día dos. La encerraron en el cuarto frío. A las tres de la mañana, la puerta empieza a golpear desde adentro.", 0.4),
 ("e02", "N", "Pero el golpe que de verdad importa no viene de ahí. Viene del techo.", 0.5),
 ("e03", "N", "Los zombis aprendieron a trepar por los canastos de la parte de atrás. Y son más rápidos de lo que parecen.", 0.4),
 ("e04", "N", "El repartidor dice que su moto está en el parqueadero. Le queda gasolina. Y cabe uno más.", 0.4),
 ("e05", "N", "La mamá te mira. La niña tiene fiebre, y no ha dicho una sola palabra en todo el día.", 0.5),
 ("e06", "N", "Y entonces, el vidrio del techo se raja.", 0.6),
 ("e07", "N", "¿Qué haces? Opción A: te vas en la moto. Opción B: te quedas con la mamá y la niña. Comenta A o B. Y sígueme, que el final sale hoy.", 1.8),
],
3: [
 ("f01", "N", "Día tres. Te quedaste con ellas. El repartidor arrancó solo, y desde la ventana lo ves caer en la esquina.", 0.4),
 ("f02", "N", "A las seis de la mañana, el techo cede. Don Héctor toca la campana de la carnicería, para llevárselos a todos hacia él.", 0.5),
 ("f03", "N", "Ustedes corren a la bodega. Hay una puerta al callejón. Y en el callejón, un camión del ejército.", 0.4),
 ("f04", "N", "Los soldados revisan a todos con linterna. Tú pasas. La mamá pasa.", 0.5),
 ("f05", "N", "La niña no. Tiene una mordida en el tobillo. Desde la primera noche. Nadie la vio.", 0.6),
 ("f06", "N", "La mamá no la suelta. Y el camión arranca sin ellas.", 0.6),
 ("f07", "N", "Desde atrás del camión, las ves quedarse en el callejón, abrazadas. Hasta que la niña levanta la cabeza. Y ya no parpadea.", 0.8),
 ("f08", "N", "Así terminó el brote del barrio. ¿Tú te habrías subido al camión? Opción A: sí. Opción B: me quedo con ellas. Comenta A o B. Y sígueme para más historias de supervivencia.", 2.0),
],
}

KEY = {"uno", "dos", "tres", "supermercado", "bogotá", "muerde", "cajera", "piso", "levanta", "parpadea", "reja", "seis", "veinte",
       "tú", "héctor", "mamá", "niña", "repartidor", "vendado", "cansan", "no", "medianoche", "sangre", "rascarse", "frío",
       "golpear", "techo", "trepar", "rápidos", "moto", "uno", "fiebre", "palabra", "raja", "esquina", "cede", "campana",
       "bodega", "callejón", "ejército", "linterna", "pasas", "mordida", "tobillo", "nadie", "suelta", "sin", "abrazadas",
       "cabeza", "a", "b", "comenta", "sígueme"}

ENDCARD = {
 1: ("¿QUÉ HACES?", "La encierras en el cuarto frío", "Le crees y se queda", "DÍA 2 HOY · SÍGUEME"),
 2: ("¿QUÉ HACES?", "Te vas en la moto", "Te quedas con ellas", "EL FINAL SALE HOY · SÍGUEME"),
 3: ("¿TE HABRÍAS SUBIDO?", "Sí, al camión", "Me quedo con ellas", "SÍGUEME PARA MÁS"),
}

FX = {
 "d01": [("muerde", "flash"), ("muerde", "shake"), ("muerde", "red")], "d02": [("levanta", "shake"), ("parpadea", "red")],
 "d03": [("golpe", "shake"), ("veinte", "red")], "d06": [("sangre", "red")],
 "e01": [("golpear", "shake")], "e02": [("techo", "red")], "e03": [("rápidos", "shake")],
 "e06": [("raja", "flash"), ("raja", "shake"), ("raja", "red")],
 "f01": [("caer", "red")], "f02": [("cede", "shake")], "f05": [("mordida", "flash"), ("tobillo", "red")],
 "f06": [("arranca", "shake")], "f07": [("cabeza", "flash"), ("parpadea", "red")],
}
CUES = {
 "d01": [("muerde", "boom", 1.3), ("muerde", "growl", 0.9)], "d02": [("piso", "boom_s", 0.6), ("levanta", "growl", 0.8)],
 "d03": [("golpe", "boom", 1.1), ("veinte", "knock3", 0.8)], "d05": [("apaga", "ping", 0.4)], "d06": [("sangre", "heart", 0.8)],
 "e01": [("golpear", "knock3", 1.1)], "e02": [("techo", "boom_s", 0.8)], "e03": [("trepar", "scrape", 0.7), ("rápidos", "growl", 0.8)],
 "e04": [("moto", "ping", 0.3)], "e05": [("fiebre", "heart", 0.7)], "e06": [("raja", "boom", 1.3), ("raja", "growl", 1.0)],
 "f01": [("caer", "boom_s", 0.9), ("caer", "growl", 0.7)], "f02": [("cede", "boom", 1.2), ("campana", "ping", 0.8)],
 "f03": [("corren", "steps", 0.8), ("ejército", "boom_s", 0.6)], "f04": [("linterna", "ping", 0.3)],
 "f05": [("mordida", "boom", 1.3)], "f06": [("arranca", "boom_s", 0.8)], "f07": [("cabeza", "boom", 1.2), ("cabeza", "growl", 1.0)],
}
MUSIC = {
 1: [("d01", "tense"), ("d04", "dark"), ("d06", "tense")],
 2: [("e01", "tense"), ("e04", "dark"), ("e06", "tense")],
 3: [("f01", "tense"), ("f04", "dark"), ("f07", "piano")],
}
