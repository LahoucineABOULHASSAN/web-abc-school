#----------------------------------------------------------------------------#
# imports.
#----------------------------------------------------------------------------#

from flask import Flask, request, jsonify, abort
from models.model import setup_db, Parent, Child

#----------------------------------------------------------------------------#
# main app.
#----------------------------------------------------------------------------#

def create_app(test_config=None):
	print("\n\n**************************************************************\n\n")
	app = Flask(__name__)
	setup_db(app)

	#----------------------------------------------------------------------------#
	# api racine endpoint.
	#----------------------------------------------------------------------------#
	@app.route('/')
	def get_api():
		try:
			return jsonify({
				'code': 200,
			    'success': True,
				'api_version': '1.0.0',
				'message': 'Welcome to the ABC_School Taking children Managing System API',
				'api_endpoints': ["/","/parents", "/children", "/parents/<int:parent_id>", "/children/<int:child_id>"],
				'api_description': 'This API is Primary School, Taking children Managing System. It allows you to create, read, update and delete parents and children.'
			})
		except:
			abort(500)

	#----------------------------------------------------------------------------#
	# api parents endpoint.
	#----------------------------------------------------------------------------#
	@app.route('/parents')
	def get_parents():
		try:
			data = Parent.query.order_by(Parent.id).all()
			parents = [parent.format() for parent in data]
			return jsonify({
				'code': 200,
				'success': True,
				'total': len(data),
				'parents': parents
			})
		except:
 			abort(404)

	# create a new parent
	@app.route('/parents', methods=['PUT'])
	def create_user():
		default_image = 'https://via.placeholder.com/900x600?text=Prent+Image'
		
		try:
			body = request.get_json()
			card_id = body.get('card_id', None)
			first_name = body.get('first_name', None)
			last_name = body.get('last_name', None)
			image_url = body.get('image_url', default_image)

			try:
				parent = Parent(card_id, first_name, last_name, image_url)
				parent.insert()
				return jsonify({
					'code': 201,
					'success': True,
					'created': parent.id
				})
			except:
				abort(405)
		except:
			abort(400)

	#----------------------------------------------------------------------------#
	# api children endpoint.
	#----------------------------------------------------------------------------#
	@app.route('/children')
	def get_children():
		try:
			data = Child.query.order_by(Child.id).all()
			children = {d.id: d.format() for d in data}
			if len(data) == 0:
			    abort(404)
			return jsonify({
				'code': 200,
			    'success': True,
			    'total': len(data),
			    'children': children
			})
		except:
			abort(500)
	
	# --------------------------------------------------------
    # ERROR HUNDLING
    # --------------------------------------------------------
	@app.errorhandler(400)
	def bad_request(error):
		return jsonify({
			'message': str(error),
			'success': False,
			'code': getattr(error, 'code')
		}), 400

	@app.errorhandler(401)
	def unauthorized(error):
		return jsonify({
			'message': str(error),
			'success': False,
			'code': getattr(error, 'code')
		}), 401

	@app.errorhandler(404)
	def not_found(error):
		return jsonify({
			'message': str(error),
			'success': False,
			'code': getattr(error, 'code')
		}), 404

	@app.errorhandler(405)
	def not_allowed(error):
		return jsonify({
			'message': str(error),
			'success': False,
			'code': getattr(error, 'code')
		}), 405

	@app.errorhandler(422)
	def unprocessable(error):
		return jsonify({
			'message': str(error),
			'success': False,
			'code': getattr(error, 'code')
		}), 422

	@app.errorhandler(500)
	def internal_server_error(error):
		return jsonify({
			'message': str(error),
			'success': False,
			'code': getattr(error, 'code')
		}), 500

	print("\n\n**************************************************************\n\n")
	return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
