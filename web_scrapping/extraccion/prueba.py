cadena = "AGUJAS DE ANESTESIA MONOPROTECT 27G 0,40X36MM LARGA - INIBSA"

# Dividir la cadena en función del carácter '-'
partes = cadena.split('-')

# Seleccionar el último elemento y eliminar los espacios en blanco al principio y al final
resultado = partes[-1].strip()

print(resultado)