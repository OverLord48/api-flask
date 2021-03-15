from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost:3306/api_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
# Creacion de tabla categoria
class Categoria(db.Model):
    cat_id = db.Column(db.Integer,primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))

    def __init__(self,cat_nom,cat_desp):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp

db.create_all()
# Esquema
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id','cat_nom','cat_desp')

# una sola respuesta
categoria_schema = CategoriaSchema()
# muchas respuestas
categorias_schema = CategoriaSchema(many=True)
# GET all
@app.route('/categoria',methods=['GET'])
def get_categorias():
    all_categoria = Categoria.query.all()
    result = categorias_schema.dump(all_categoria)
    return jsonify(result)

# GET por id
@app.route('/categoria/<id>', methods=['GET'])
def get_categoria(id):
    categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(categoria)

# POST
@app.route('/categoriapost',methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']

    nueva_categoria = Categoria(cat_nom,cat_desp)
    db.session.add(nueva_categoria)
    db.session.commit()
    return categoria_schema.jsonify(nueva_categoria)

# PUT
@app.route('/categoriaWrite/<id>', methods=['PUT'])
def update_categoria(id):
    categoria_updated = Categoria.query.get(id)

    cat_nom = request.json['cat_nom']
    cat_desp = request.json['cat_desp']

    categoria_updated.cat_nom = cat_nom
    categoria_updated.cat_desp = cat_desp

    db.session.commit()
    return categoria_schema.jsonify(categoria_updated)

# DELETE
@app.route('/categoriaDelete/<id>', methods=['DELETE'])
def delete_categoria(id):
    del_categoria = Categoria.query.get(id)
    db.session.delete(del_categoria)
    db.session.commit()
    return categoria_schema.jsonify(del_categoria)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'Mensaje':'Bienvenido a la contruccion de api rest con flask'})

if __name__=="__main__":
    app.run(debug=True)
