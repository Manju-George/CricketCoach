from flask import render_template,request, url_for
from app import app
from flask_table import Table, Col,LinkCol, ButtonCol
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View
import pygal, calendar
from app.cricket_data import all_records, daily_record


app.secret_key = b'_546(*_gd$%&g23]/'



#Navigation Bar
nav = Nav(app)
nav.register_element("insights", Navbar(
											'navbar',
											View('About this app','about'),
											View('Registered players','index'),
											Subgroup('Insights',
												View('Top 5 batsmen(based on last practice session)','top5batsmen'),
												View('Monthly performance(top 5 batsmen)','monthlyRecords'),
												View('Top 5 ballers(based on last practice session)','top5ballers'))
										)
									)

class PlayerTable(Table):
    name = LinkCol('Name', 'progress_review',
                   url_kwargs=dict(id='id'), attr='name')
    phone = Col('Phone')
    add_record = LinkCol('Actions', 'add_record',
    				url_kwargs=dict(id='id'), attr='add_record')

@app.route('/index')
def index():
	table = PlayerTable(all_records.players(), classes = ['playerclass'])
	return render_template('index.html', title='Home', table = table)

@app.route('/item/<int:id>', methods = ['GET'])
def progress_review(id):
	if request.method == 'GET':
		player_name, player_records = all_records.get_element_by_id(id)
		line_chart = pygal.Line()
		
		all_months = []
		all_scores = []
		months_names = calendar.month_name
		for mth, year, aggregate_score in sorted(player_records, key = lambda a: a[0]):
			all_months.append(months_names[mth][:3])
			all_scores.append(aggregate_score)
		line_chart.add('',all_scores)
		line_chart.x_labels = all_months
		line_chart.title = 'Performance History data for {} for the year {}'.format(player_name, year)
		graph_data = line_chart.render_data_uri()
		return render_template('graphing.html', title='player performance', graph_data=graph_data)
	else:
		return redirect('/')

@app.route('/add_record/<int:id>', methods = ['GET','POST'])
def add_record(id):
	if request.method == 'GET':
		#form = ScoreData()
		player = all_records.get_player_by_id(id)
		return render_template('player_score.html',player=player, balls = range(1,21)) 
		

@app.route('/')   
@app.route('/about')
def about():
	return render_template('about.html', title='About this app')

@app.route('/top5batsmen')
def top5batsmen():
	graph = pygal.HorizontalBar()
	dt = None
	for dt, player_name, record in all_records.list_top_batsmen(5):
		graph.add(player_name, record.batting_score)
		if not dt:
			dt = record.date
	graph.title = 'Last Day Batting Performance: ({})'.format(dt)
	graph_data = graph.render_data_uri()
	
	return render_template('graphing.html', title='player perfromance', graph_data=graph_data)

@app.route('/monthlyrecords')
def monthlyRecords():
	line_chart = pygal.Line()
	months_names = calendar.month_name
	all_months = []
	
	for player_name, records in all_records.list_top_batsmen(5,filter_type = 2):
		all_scores = []
		for mth, year, score in records:
			if len(records) != len(all_months):
				all_months.append(months_names[mth][:3])
			all_scores.append(score)
		line_chart.add(player_name,all_scores)
	line_chart.x_labels = all_months
	line_chart.title = 'Performance History data for the year {}'.format(year)
	graph_data = line_chart.render_data_uri()
	return render_template('graphing.html', title='Monthly Perfromance Review', graph_data=graph_data)

@app.route('/top5ballers/')
def top5ballers():
	pass

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500