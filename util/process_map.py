#coding: utf-8
'''
This script has to objective read a picture and return the list of cities
and this neighbors

'''
import geobr

STATE = "PB" # pegar depois do processamento da imagem em si'
PROJ_TO_METERS = 5880 # SIRGAS 2000 / Brazil Polyconic (Padrão do IBGE)

print(f"==\nCarregando cidades do estado: {STATE}")

# Cidades do estado, simplified fica lento, mas fica preciso pq vem mais poligonos.
municipalities = geobr.read_municipality(code_muni=STATE,
                                         year=2020,
                                         simplified=False)


print(f"==\nCorrigindo topologia e projetando para coords euclidianas(plano)")
# uso de buffer para atenuar e conseguir encontrar os muni vizinhos corretamente
#municipalities['geometry'] = municipalities.geometry.buffer(0)

# Precisa converter de graus(lat/long)(globo) para coordenadas projetadas(x,y)(plano)
# Sirgas 2000, entender e como converter? Nao confiei no inplace.
munis_projected = municipalities.to_crs(epsg=PROJ_TO_METERS)

print(f"==\nCalculando centróides dos municípios...")

munis_projected['centroid'] = munis_projected.geometry.centroid

print(f"==\nGerando lista com cidades vizinhas do estado: {STATE}")


# ===== start refactoring=====
# add coluna com dicionario dos códigos dos vizinhos e distancias vazias.
# munis_projected['neighbors'] = {}

# popula coluna com vizinhança das cidades
print(f"==\nCalculando distâncias...")

# dicionario de dicionarios no formato
# [(cod_cidade1, { cod_vizinho1: [nome_vizinho1, distacia],
#                cod_vizinho2: [nome_vizinho2, distacia]] }),
# (cod_cidade2, { cod_vizinho1: [nome_vizinho1, distacia],
#                cod_vizinho2: [nome_vizinho2, distacia]] })]]
munis_refactored = {}

for index, row in munis_projected.iterrows():

    neighbors = munis_projected[
        munis_projected.geometry.touches(row['geometry'])
        ]
    
    neighbors_dict = dict.fromkeys(neighbors['code_muni'].to_list(), 0)
    
    for _, neighbor in neighbors.iterrows():
        #print(f"\n==== abaixo, temos um vizin de {row['name_muni']} ====\n", neighbor)
        distance = row['centroid'].distance(neighbor.centroid)
        distance_km = round(distance / 1000, 2)

        neighbors_dict[neighbor.code_muni] = [neighbor.name_muni, distance_km] # type: ignore

    #add vizinhos com as distancias populadas
    #munis_projected.at[index,'neighbors'] = neighbors_dict # pyright: ignore[reportArgumentType]
    key = str(row['code_muni']) + "|" + row['name_muni']
    munis_refactored[key] = neighbors_dict

#print(munis_refactored.items())


# print(munis_projected.iloc[:1, lambda municipalities: [False, True, False, False, False, False, False, False, True, True]])



print(f"==\nCarregando distâncias...")

#for _, row in munis_projected.iterrows():
#    for muni in row['neighbors'].items():
#        print(f"A distancia de {row['name_muni']}, até {muni[1][0]} é de {muni[1][1]}km")
#
#    
#    break # parando no primeiro para testes

for tuple in munis_refactored.items():
    print(f"===\ncod_cidade: {tuple[0]}")
    for cidade in tuple[1].items():
        print(f"  cod_vizinho: {cidade[0]}, nome_vizinho: {cidade[1][0]}, dist_vizinho: {cidade[1][1]}")


#print(munis_projected.iloc[:, lambda municipalities: [True, True, False, False, False, False, False, False, True]])

