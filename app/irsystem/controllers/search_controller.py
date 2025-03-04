from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import json
import pandas as pd
import csv
import scripts.sim as sim
from scripts.search import run_search, get_recipe, get_closest
project_name = "Screen to Table"
net_id = "Olivia Zhu(oz28), Daniel Ye(dzy3), Shivank Nayak(sn532), Kassie Wang(klw242), Elizabeth Healy(eah255)"
v_1 = "link to v1"
v_2 = "link to v2"

with open('./data/recipe_data/allergy_dict.json') as f:
    allergy_dict = json.load(f)
with open('./data/movie_script_list.txt') as f:
    titles = [line.rstrip('\n ') for line in f.readlines()]
with open('./data/recipe_data/review_keywords.json') as f:
    review_keywords = json.load(f)
with open('./data/movie_food_quotes.json') as f:
    quotes = json.load(f)

@irsystem.route('/', methods=['GET'])
def home():
    query = request.args.get('search')
    allergies = request.args.get('search2')
    #print("alergies: ", allergies)

    if not query:
        return render_template('search.html',allergy_lst=list(allergy_dict.keys()),
        movies=titles, name=project_name, netid=net_id, v1=v_1, v2=v_2)
    else:
        return redirect(url_for('irsystem.results', query=query, allergies=allergies))


@irsystem.route('/results')
def results():
    query = request.args.get("query").strip()
    allergies = request.args.get("allergies").strip()

    data = run_search(query, allergies)

    if data == None:
        return "Did you mean " + get_closest(query)
    else:
        return render_template('results.html', res=data, movies=titles,
        allergy_lst=list(allergy_dict.keys()))


@irsystem.route('/recipe')
def recipe():
    idx = int(request.args.get("idx"))
    query = request.args.get("query")
    r = get_recipe(idx)
    movie_quotes = quotes[query]
    food_words = r["Recipe Name"].lower().split()
    word_quotes = dict()
    for fw in food_words:
        if fw in movie_quotes:
            word_quotes[fw] = (movie_quotes[fw])
        if fw[:-1] in movie_quotes:
            word_quotes[fw] = (movie_quotes[fw[:-1]])
    r["Quotes"] = word_quotes
    if r["RecipeID"] in review_keywords:
        r["ReviewWords"] = ', '.join(review_keywords[r["RecipeID"]]).rstrip(', ')
    else:
        r["ReviewWords"]="No reviews"
    # r['Ingredients'] = r['Ingredients']
    # r['Directions'] = r['Directions']
    # ingredients = ",".split(r['Ingredients'])
    # steps = ",".split(r['Directions'])
    # author = r['Author']

    return jsonify(r)
    # return render_template('results.html',
    #                        title=title,
    #                        ingredients=ingredients,
    #                        steps=steps,
    #                        author=author)
