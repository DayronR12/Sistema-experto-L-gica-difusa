(deffacts initial-facts
)

(defrule dieta-bajopeso-razagrande
   (peso ?w&:(<= ?w 5))
   (raza "Grande")
   (edad ?a&:(>= ?a 7))
   (enfermedades "Si")
   =>
      (printout t "Regla 'dieta-bajopeso-razagrande' activada." crlf)
   (printout t "Se Recomienda una dieta alta en proteinas y ademas asistir al veterinario." crlf)
)

(defrule dieta-saludarticular
   (peso ?w&:(> ?w 30))
   (raza "Grande")
   (edad ?a&:(> ?a 5))
   (enfermedades "No")
   =>
      (printout t "Regla 'dieta-saludarticular' activada." crlf)
   (printout t "Se recomienda una dieta con menos grasa y suplementos para la salud articular." crlf)
)

(defrule dieta-balanceada
   (peso ?w&:(and (> ?w 10) (<= ?w 20)))
   (raza "Mediana")
   (edad ?a&:(<= ?a 7))
   (enfermedades "No")
   =>
      (printout t "Regla 'dieta-balanceada' activada." crlf)
   (printout t "Se recomienda una dieta balanceada con enfoque en mantener peso saludable." crlf)
)

(defrule dieta-alta-energia
   (peso ?w&:(< ?w 10))
   (raza "Pequeña")
   (edad ?a&:(> ?a 8))
   (enfermedades "No")
   =>
      (printout t "Regla 'dieta-alta-energia' activada." crlf)
   (printout t "Se recomienda una dieta de alta energia y un suplemento para la salud general." crlf)
)

(defrule dieta-proteinas
   (peso ?w&:(and (>= ?w 20) (<= ?w 30)))
   (raza ?b&:(or (eq ?b "Grande") (eq ?b "Mediana")))
   (edad ?a&:(and (>= ?a 1) (<= ?a 4)))
   (enfermedades "No")
   =>
      (printout t "Regla 'dieta-proteinas' activada." crlf)
   (printout t "Se recomienda una dieta rica en proteinas para crecimiento y desarrollo." crlf)
)

(defrule dieta-estandar
   (declare (salience -10)) ; Baja prioridad para que se ejecute después de las demás reglas
   =>
   (printout t "Plan de alimentacion de grasas y proteinas, además de vegetales constantemente.." crlf)
)