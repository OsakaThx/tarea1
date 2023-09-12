import time
import os
import conexion as conn

db = conn.DB()

def validar_numeros(cadena):
    return cadena.isdigit()

def validar_letras(cadena):
    return all(caracter.isalpha() or caracter.isspace() for caracter in cadena)

def create():
    print("************************")
    print("\tCRUD con SQLite")
    print("************************")

def realizar_retiro(num_cuenta, monto):
    # Código para realizar el retiro
    sql_select = "SELECT monto_disponible FROM cuentas WHERE num_cuenta = ?"
    resultado = db.ejecutar_consulta(sql_select, (num_cuenta,))
    saldo_actual = resultado.fetchone()[0]
    if monto > saldo_actual:
        print("No tiene suficiente saldo para realizar el retiro.")
    else:
        nuevo_saldo = saldo_actual - monto
        sql_update = "UPDATE cuentas SET monto_disponible = ? WHERE num_cuenta = ?"
        db.ejecutar_consulta(sql_update, (nuevo_saldo, num_cuenta))
        print("Retiro exitoso. Nuevo saldo: ${:.2f}".format(nuevo_saldo))

def realizar_deposito(num_cuenta, monto):
    # Código para realizar el depósito
    sql_select = "SELECT monto_disponible FROM cuentas WHERE num_cuenta = ?"
    resultado = db.ejecutar_consulta(sql_select, (num_cuenta,))
    saldo_actual = resultado.fetchone()[0]
    
    nuevo_saldo = saldo_actual + monto
    sql_update = "UPDATE cuentas SET monto_disponible = ? WHERE num_cuenta = ?"
    db.ejecutar_consulta(sql_update, (nuevo_saldo, num_cuenta))
    print("Depósito exitoso. Nuevo saldo: ${:.2f}".format(nuevo_saldo))

def cambiar_estado_cuenta(num_cuenta, nuevo_estado):
    # Código para cambiar el estado de la cuenta
    sql_update = "UPDATE cuentas SET estado_cuenta = ? WHERE num_cuenta = ?"
    db.ejecutar_consulta(sql_update, (nuevo_estado, num_cuenta))
    print("Estado de la cuenta actualizado: {}".format(nuevo_estado))
    
def verificar_estado_cuenta(num_cuenta):
    sql_select_estado = "SELECT estado_cuenta FROM cuentas WHERE num_cuenta = ?"
    resultado = db.ejecutar_consulta(sql_select_estado, (num_cuenta,))
    estado_actual = resultado.fetchone()
    
    if estado_actual is None:
        return "no_existe"
    else:
        return estado_actual[0]

    if estado_actual == "activa":
        return True
    elif estado_actual == "inactiva":
        print("La cuenta está inactiva. No se pueden realizar depósitos ni retiros.")
        return False
    else:
        print("Estado de cuenta no reconocido.")
        return False
    
def mostrar_cuentas():
    sql_select_cuentas = "SELECT * FROM cuentas"
    cuentas = db.ejecutar_consulta(sql_select_cuentas).fetchall()
    
    print("Lista de cuentas:")
    for cuenta in cuentas:
        print(f"Número de cuenta: {cuenta[0]}")
        print(f"Monto disponible: ${cuenta[1]:.2f}")
        print(f"Estado de cuenta: {cuenta[2]}")
        print("------------------------")

def mostrar_datos_personas():
    sql_select_datos = "SELECT * FROM datos"
    datos_personas = db.ejecutar_consulta(sql_select_datos).fetchall()

    if datos_personas:
        print("Lista de datos de personas:")
        for persona in datos_personas:
            print(f"Nombre: {persona[0]}")
            print(f"Cédula: {persona[1]}")
            print(f"Primer apellido: {persona[2]}")
            print(f"Segundo apellido: {persona[3]}")
            print("------------------------")
    else:
        print("No hay datos de personas disponibles.")
        
def mostrar_menu():
    print("************************")
    print("\tCRUD con SQLite")
    print("************************")
    print("\t(1) Ingresar datos")
    print("\t(2) Ingresar datos de la cuenta")
    print("\t(3) Retiro")
    print("\t(4) Deposito")
    print("\t(5) Activar o desactivar cuenta")
    print("\t(6) Salir del sistema")
    print("\t(7) Mostrar cuentas y datos")
    print("\t(8) Mostrar usuarios")
    print("++++++++++++")

def main():
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Seleccione una opcion: "))
            
            if opcion == 1:
                # Código para ingresar datos de la persona
                name = input("Ingrese el nombre de la persona: ")
                if not validar_letras(name):
                    print("¡Error! Solo se aceptan letras en el nombre.")
                    continue
                cedula = input("Ingrese su cedula: ")
                if not validar_numeros(cedula):
                    print("Debe ingresar números para la cédula.")
                    continue
                apellido1 = input("Ingrese su primer apellido: ")
                if not validar_letras(apellido1):
                    print("¡Error! Solo se aceptan letras en el primer apellido.")
                    continue
                apellido2 = input("Ingrese su segundo apellido: ")
                if not validar_letras(apellido2):
                    print("¡Error! Solo se aceptan letras en el segundo apellido.")
                    continue
                if len(name) > 0 and len(cedula) > 0 and len(apellido1) > 0 and len(apellido2) > 0:
                    sql = "INSERT INTO datos(name, cedula, apellido1, apellido2) VALUES(?, ?, ?, ?)"
                    parametros = (name, cedula, apellido1, apellido2)
                    db.ejecutar_consulta(sql, parametros)
                    print("Registros ingresados con éxito")
                else:
                    print("Campos vacíos. No se ha ingresado ningún registro.")
                
            elif opcion == 2:
                # Código para ingresar datos de la cuenta
                num_cuenta = input("Ingrese el número de cuenta: ")
                if not validar_numeros(num_cuenta):
                    print("Debe ingresar un número válido para el número de cuenta.")
                    continue
                monto_disponible = input("Ingrese el monto disponible en la cuenta: ")
                if not validar_numeros(monto_disponible):
                    print("Debe ingresar un número válido para el monto disponible.")
                    continue
                estado_cuenta = input("Ingrese el estado de la cuenta (activa o inactiva): ").lower()
                if estado_cuenta not in ("activa", "inactiva"):
                    print("¡Error! Por favor, ingrese el estado de cuenta correcto (activa o inactiva).")
                    continue
                if len(num_cuenta) > 0 and len(monto_disponible) > 0 and len(estado_cuenta) > 0:
                    sql = "INSERT INTO cuentas(num_cuenta, monto_disponible, estado_cuenta) VALUES(?, ?, ?)"
                    parametros = (num_cuenta, monto_disponible, estado_cuenta)
                    db.ejecutar_consulta(sql, parametros)
                    print("Registros ingresados con éxito")
                else:
                    print("Campos vacíos. No se ha ingresado ningún registro.")
 
            elif opcion == 3:
                # Código para realizar un retiro
                num_cuenta_retiro = input("Ingrese el número de cuenta: ")
                estado_actual = verificar_estado_cuenta(num_cuenta_retiro)

                if estado_actual == "no_existe":
                    print("El número de cuenta ingresado no existe.")
                elif estado_actual == "activa":
                    monto_retiro = float(input("Ingrese el monto a retirar: "))
                    realizar_retiro(num_cuenta_retiro, monto_retiro)
                elif estado_actual == "inactiva":
                    print("La cuenta está inactiva. No se pueden realizar depósitos ni retiros.")
            elif opcion == 4:
                # Código para realizar un depósito
                num_cuenta_deposito = input("Ingrese el número de cuenta: ")
                estado_actual = verificar_estado_cuenta(num_cuenta_deposito)

                if estado_actual == "no_existe":
                    print("El número de cuenta ingresado no existe.")
                elif estado_actual == "activa":
                    monto_deposito = float(input("Ingrese el monto a depositar: "))
                    realizar_deposito(num_cuenta_deposito, monto_deposito)
                elif estado_actual == "inactiva":
                    print("La cuenta está inactiva. No se pueden realizar depósitos ni retiros.")

            elif opcion == 5:
                # Código para activar o desactivar cuenta
                num_cuenta_estado = input("Ingrese el número de cuenta: ")
                
                sql_cuenta_existente = "SELECT COUNT(*) FROM cuentas WHERE num_cuenta = ?"
                cuenta_existente = db.ejecutar_consulta(sql_cuenta_existente, (num_cuenta_estado,)).fetchone()[0]
                
                if cuenta_existente:
                    sql_select_estado = "SELECT estado_cuenta FROM cuentas WHERE num_cuenta = ?"
                    estado_actual = db.ejecutar_consulta(sql_select_estado, (num_cuenta_estado,)).fetchone()[0]
                    
                    if estado_actual == "activa":
                        print("La cuenta está activa.")
                        opcion_estado = input("¿Desea desactivarla? (s/n): ")
                        if opcion_estado.lower() == "s":
                            cambiar_estado_cuenta(num_cuenta_estado, "inactiva")
                            print("Cuenta desactivada.")
                    elif estado_actual == "inactiva":
                        print("La cuenta está desactivada.")
                        opcion_estado = input("¿Desea activarla? (s/n): ")
                        if opcion_estado.lower() == "s":
                            cambiar_estado_cuenta(num_cuenta_estado, "activa")
                            print("Cuenta activada.")
                    else:
                        print("Estado de cuenta no reconocido.")
                else:
                    print("El número de cuenta ingresado no existe.")
                
            elif opcion == 6:
                break
            
            elif opcion == 7:
                # Mostrar cuentas y datos
                mostrar_cuentas()

            elif opcion == 8:
                #Mostrar usuarios
                mostrar_datos_personas()
                
        except ValueError:
            print("Opción incorrecta. Por favor, ingrese un número válido.")
        
        time.sleep(1)
        os.system("clear")

if __name__ == "__main__":
    main()

