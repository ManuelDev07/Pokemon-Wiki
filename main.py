from unicodedata import category
import requests 
import json
from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import null

app = Flask(__name__)

#Página Principal:
@app.route('/WELCOME')
def index():
    return render_template('index.html')

#Página de Búsqueda Pokémon:
@app.route('/info-pokemon/', methods=["GET",'POST'])
def search_pokemon():
    if request.method == 'POST':
        name_id = request.form['name_id']
        
        return rq_api_pk(name_id)

    return render_template('search_pok.html')

#Request API Pokémon:
@app.route('/info-pokemon/<name_id>')
def rq_api_pk(name_id):

    if name_id != '':
        #Petición a la API sobre datos del Pokémon:
        url = f'https://pokeapi.co/api/v2/pokemon/{name_id}'
        r = requests.get(url)
        json_doc = r.json()

        #Datos del Pokémon:
        id_ = json_doc['id']
        name = json_doc['name']
        weight = json_doc["weight"] / 10
        height = json_doc["height"] / 10
        stats = json_doc['stats']
        abilities = json_doc["abilities"]

        #Requests para los datos del Pokémon:
        url_specie = json_doc['species']['url']
        r_specie = requests.get(url_specie)
        doc_json_specie = r_specie.json()

        base_happiness = doc_json_specie['base_happiness']
        ratio = doc_json_specie['capture_rate']
        egg_groups = doc_json_specie['egg_groups']
        gen = doc_json_specie['generation']['name']
        descriptions = doc_json_specie['flavor_text_entries']
        categories = doc_json_specie['genera']

        #Obteniendo el Color en español
        color_url = doc_json_specie['color']['url']
        r_color = requests.get(color_url)
        doc_json_color = r_color.json()
        #Color
        color = doc_json_color['names'][5]['name']

        #Obteniendo el La Forma en español
        shape_url = doc_json_specie['shape']['url']
        r_shape = requests.get(shape_url)
        doc_json_shape = r_shape.json()
        #Forma
        name_shape = doc_json_shape['names'][1]['name']
      

        #Sus tipos:
        types1 = json_doc['types'][0]
        type1 = types1['type']['name']
        try:   
            if json_doc["types"][1] in json_doc["types"]:
                types2 = json_doc["types"][1]
                type2 = types2["type"]['name']

        except: 
                type2 = "No tiene segundo tipo"

        #Imágen del Pokémon:
        imgn = json_doc['sprites']['other']['official-artwork']['front_default']


        return render_template('info_pok.html', id_=id_, name=name, weight=weight, height=height, type1=type1, type2=type2, abilities=abilities, imgn=imgn, stats=stats,base_happiness=base_happiness,ratio=ratio, egg_groups=egg_groups, gen=gen, descriptions=descriptions, color=color, name_shape=name_shape, categories=categories)
           
    else:

        return redirect(url_for('search_pokemon'))





#Página de Búsqueda Bayas/Berries:
@app.route('/info-berries/', methods=["GET",'POST'])
def search_berrie():
    if request.method == 'POST':
        berrie = request.form['berrie']
        
        return rq_api_berrie(berrie)

    return render_template('search_berrie.html')

#Request API Berries:
@app.route('/info-berries/<int:name>')
@app.route('/info-berries/<string:name>')
def rq_api_berrie(name):
    if name != '':
        #Petición a la API sobre la Baya:
        url = f'https://pokeapi.co/api/v2/berry/{name}/'
        r = requests.get(url)
        json_doc_berrie = r.json()

        #Datos de la Baya:
        growth_time = json_doc_berrie['growth_time']
        id_ = json_doc_berrie['id']
        size = json_doc_berrie['size'] / 10
        max_harvest = json_doc_berrie['max_harvest']
        smoothness = json_doc_berrie['smoothness']
        natural_gift_power = json_doc_berrie['natural_gift_power']
        flavors = json_doc_berrie['flavors']

        #Request para información del item en español
        #Nombre en español:
        url_item = json_doc_berrie['item']['url']
        r_item = requests.get(url_item)
        json_doc_item_name = r_item.json()
        name_spanish = json_doc_item_name['names'][5]['name']
        name_english =  json_doc_item_name['names'][7]['name']

        #Efecto en español (misma request usada en el nombre):
        effect_spanish = json_doc_item_name['flavor_text_entries'][32]['text']

        #Don Natural en español:
        url_item = json_doc_berrie['natural_gift_type']['url']
        r_item = requests.get(url_item)
        json_doc_item_gift = r_item.json()
        gift_name_type = json_doc_item_gift['names'][5]['name']

        #Dureza en español:
        firmness_url = json_doc_berrie['firmness']['url']
        r_firmness = requests.get(firmness_url)
        json_doc_firmness = r_firmness.json()
        firmness = json_doc_firmness['names'][1]['name']

        
        #Imágen de la Baya (misma request usada en el nombre):
        imgn_berrie = json_doc_item_name['sprites']['default']


        return render_template('info_berrie.html', name_english=name_english, firmness=firmness, growth_time=growth_time, id_=id_, size=size, max_harvest=max_harvest, smoothness=smoothness, natural_gift_power=natural_gift_power, name_spanish=name_spanish, effect_spanish=effect_spanish, gift_name_type=gift_name_type, imgn_berrie=imgn_berrie, flavors=flavors)

    else:
        return redirect(url_for('search_berrie'))





#Página de Búsqueda Habilidades/Abilities:
@app.route('/info-abilities/', methods=["GET",'POST'])
def search_abilitie():
    if request.method == 'POST':
        abilitie = request.form['abilitie']
        
        return rq_api_abilitie(abilitie)

    return render_template('search_abilitie.html')

#Request API Abilities:
@app.route('/info-abilities/<int:name>')
@app.route('/info-abilities/<string:name>')
def rq_api_abilitie(name):
    if name != '':
        #Petición a la API sobre la Habilidad:
        url = f'https://pokeapi.co/api/v2/ability/{name}/'
        r = requests.get(url)
        json_doc_ab = r.json()

        #Datos de la Habilidad:
        id_ = json_doc_ab['id']
        name = json_doc_ab['names'][7]['name']
        name_spanish = json_doc_ab['names'][5]['name']
        
        effects = json_doc_ab['flavor_text_entries']
        for effect in effects:
            if effect['language']['name'] == 'es':
                effect_spanish = effect['flavor_text']

        gen = json_doc_ab['generation']['name']
        pok_ab = json_doc_ab['pokemon']

        return render_template('info_abilitie.html', name=name, name_spanish=name_spanish, effect_spanish=effect_spanish, gen=gen, id_=id_, pok_ab=pok_ab)
    
    else:
        return redirect(url_for('search_abilitie'))





#Página de Búsqueda Objetos/Items:
@app.route('/info-item/', methods=['GET','POST'])
def search_item():
    if request.method == 'POST':
        item = request.form['item']

        return rq_api_item(item)
    
    return render_template('search_item.html')

#Request a la API Objetos/Items:
@app.route('/info-item/<item_id>')
def rq_api_item(item_id):
    if item_id != '':
        url = f'https://pokeapi.co/api/v2/item/{item_id}/'
        r = requests.get(url)
        doc_json = r.json()

        #Datos del Objeto/Item:
        namess = doc_json['names']
        for namee in namess:
            if namee['language']['name'] == 'es':
                name_spanish = namee['name']

        for namee in namess:
            if namee['language']['name'] == 'en':
                name = namee['name']

        id_ = doc_json['id']
        cost = doc_json['cost']
        category = doc_json['category']['name']
        
        #Descripción del Objeto/Item:
        descs = doc_json['flavor_text_entries']
        for desc in descs:
            if desc['language']['name'] == 'es':
                spanish_desc = desc['text']
        

        #Imágen del Objeto/Item:
        imgn_item = doc_json['sprites']['default']

        return render_template('info_item.html',name=name, name_spanish=name_spanish, imgn_item=imgn_item, id_=id_, spanish_desc=spanish_desc, cost=cost, category=category)

    else:
        return redirect(url_for('search_item'))


#Página de Búsqueda Movimientos:
@app.route('/info-mt/', methods=['GET','POST'])
def search_mt():
    if request.method == 'POST':
        mt = request.form['mt']

        return rq_api_mt(mt)
    
    return render_template('search_mt.html')

#Request a la API Move:
@app.route('/info-mt/<mt_id>')
def rq_api_mt(mt_id):
    if mt_id != '':
        url = f'https://pokeapi.co/api/v2/move/{mt_id}/'
        r = requests.get(url)
        doc_json = r.json()

        #Datos de la MT/MO:
        id_ = doc_json['id']
        name = doc_json['name']
        name_spanish = doc_json['names'][5]['name']
        pp = doc_json['pp']
        gen = doc_json['generation']['name']
        descs = doc_json['flavor_text_entries']
        learned_by = doc_json['learned_by_pokemon']

        #Request Tipo del ataque en español:
        url_type_attack = doc_json['type']['url']
        r_type_attack = requests.get(url_type_attack)
        json_type_attack = r_type_attack.json()

        type_attack = json_type_attack['names'][5]['name']
        
        #Descripción del Movimiento:
        for desc in descs:
            if desc['language']['name'] == 'es':
                spanish_desc = desc['flavor_text']
        
        #Clase del Movimiento:
        dmg_cls = doc_json['damage_class']['name']

        #Potencia del Movimiento:
        if doc_json['power'] == None:
            power = 0
        else:
            power = doc_json['power']

        #Presición del Movimiento:
        if doc_json['accuracy'] == None:
            accuracy = 0
        else:
            accuracy = doc_json['accuracy']



        #Concursos Normales
        x,y,z,m = doc_json['contest_combos'], doc_json['contest_effect'], doc_json['contest_type'], doc_json['super_contest_effect']

        after_normal,before_normal,after_super,before_super,appeal_normal,effect_normal,jam_normal,effect_super,type = '','','','','','','','',''

        try:
                #Datos del Movimiento en Concursos:
            type = doc_json['contest_type']['name']
            contest_normal = doc_json['contest_combos']['normal']

            if contest_normal['use_after'] != None:
                after_normal = contest_normal['use_after'] #List

            if contest_normal['use_before'] != None:
                before_normal = contest_normal['use_before'] #List


            #Concursos Súper:
            contest_super = doc_json['contest_combos']['super']

            if contest_super['use_after'] != None:
                after_super = contest_super['use_after'] #List

            if contest_super['use_before'] != None:
                before_super = contest_super['use_before'] #List

            #Efecto en los concursos:
            #Normales:
            url_effect_normal = doc_json['contest_effect']['url']
            r_effect_normal = requests.get(url_effect_normal)
            json_effect_normal = r_effect_normal.json()

            appeal_normal = json_effect_normal['appeal']
            effect_normal = json_effect_normal['effect_entries'][0]["effect"]
            jam_normal = json_effect_normal['jam']

            #Súper:
            url_effect_super = doc_json['super_contest_effect']['url']
            r_effect_super = requests.get(url_effect_super)
            json_effect_super = r_effect_super.json()

            effect_super = json_effect_super['flavor_text_entries'][0]['flavor_text']

        except:
            contest_normal = 'Este Ataque no está en los concursos.'





        return render_template('info_mt.html', x=x, y=y, z=z, m=m,name=name, name_spanish=name_spanish, power=power, pp=pp, accuracy=accuracy, id_=id_, type_attack=type_attack,gen=gen, desc_spanish=spanish_desc,dmg_cls=dmg_cls, learned_by=learned_by, after_normal=after_normal, before_normal=before_normal, after_super=after_super, before_super=before_super, appeal_normal=appeal_normal, effect_normal=effect_normal, jam_normal=jam_normal, effect_super=effect_super, type=type)
    
    else:
        return redirect(url_for('search_mt'))


if __name__ == '__main__':
    app.run(debug=True)

