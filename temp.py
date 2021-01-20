Bueno @1357413960 (Juan)
Yo haría de esta manera el ciclo


# hago un ciclo que de inicio, será infinito
while True:
   
    # Pido al usuario que verifique sus datos
    confirmacion = print(input('Son estos datos correctos? Si o No: '))

    # Covierto la respuesta del usuario a minusculas y le quito los espacios en blanco. 
    str(confirmacion).lower().strip()

    # Si el usuario responde sí, entonces rompo el ciclo
    if confirmacion == "si": 
        break
    # Si el usuario responde otra cosa, vuelvo a preguntar los datos
    else: 
        print("Re-confirma tus datos")

        name = input("Por favor dime tu nombre: ")
        age = int(input("Ahora tu edad: "))

print'Ingresaste como nombre {name} y tu edad {age}")
