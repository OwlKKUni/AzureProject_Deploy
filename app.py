from flask import Flask, render_template, request
from SQL.queries import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/input')
def input():
    return render_template('input.html')


@app.route('/dive')
def dive():
    return render_template('dive.html')


@app.route('/all_dives')
def all_dives():
    return render_template('all_dives.html')


@app.route('/combat')
def data_option1():
    return render_template('data/combat.html')


@app.route('/currency_gained')
def data_option2():
    return render_template('data/currency_gained.html')


@app.route('/objectives_completed')
def data_option3():
    return render_template('data/objectives_completed.html')


@app.route('/samples_gained')
def data_option4():
    return render_template('data/samples_gained.html')


@app.route('/input_combat')
def data_option5():
    return render_template('inputs/input_combat.html')


@app.route('/input_currency_gained')
def data_option6():
    return render_template('inputs/input_currency_gained.html')


@app.route('/input_objectives_completed')
def data_option7():
    return render_template('inputs/input_objectives_completed.html')


@app.route('/input_samples_gained')
def data_option8():
    return render_template('inputs/input_samples_gained.html')


@app.route('/submit_data_objectives', methods=['POST'])
# Get last id, assign id column number
def submit_data_objectives():
    # Extract form data
    id_ = query_get_last_id_value(Server1, 'objectives_completed',)
    main_objectives = request.form['main_objectives']
    optional_objectives = request.form['optional_objectives']
    helldivers_extracted = request.form['helldivers_extracted']
    outposts_destroyed_light = request.form['outposts_destroyed_light']
    outposts_destroyed_medium = request.form['outposts_destroyed_medium']
    outposts_destoryed_heavy = request.form['outposts_destroyed_heavy']
    mission_time_remaining = request.form['mission_time_remaining']

    # Insert data into the database
    query_put_row(Server1, 'objectives_completed',
                  id=int(id_) + 1,
                  main_objectives=int(main_objectives),
                  optional_objectives=int(optional_objectives),
                  helldivers_extracted=int(helldivers_extracted),
                  outposts_destroyed_light=int(outposts_destroyed_light),
                  outposts_destroyed_medium=int(outposts_destroyed_medium),
                  outposts_destoryed_heavy=int(outposts_destoryed_heavy),
                  mission_time_remaining=mission_time_remaining)

    return 'Data submitted successfully'


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
