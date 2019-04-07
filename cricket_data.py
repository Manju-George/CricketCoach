import random
from collections import namedtuple, defaultdict
import datetime, names

player_record = namedtuple("PlayerRecord",["id","name","age","address","phone","email",'add_record'])
daily_record = namedtuple("PlayerPerformance",["id","player_record","date","attended","balls_bowled","bowling_score","batting_score","balls_faced","fielding_score"])
monthly_aggregation_record = namedtuple("monthly",
					['id','player_record','date','aggregated_batting_score'])

DAILY_FILTER = 1
MONTHLY_FILTER = 2
YEARLY_FILER = 3


class PlayerPerfRecords:
	"""Encapsulate all the records, to filter and sort as required
	"""
	def __init__(self):
		self.daily_records = {}
		self.monthly_records = {}
		self.yearly_records = {}
		self._all_dates = None
		self.player_details = {}

	@property
	def all_dates(self):
		return self._all_dates

	@all_dates.setter
	def all_dates(self,value):
		self._all_dates = value

	def players(self):
		return [player for player in self.player_details.values()]

	def get_player_by_id(self,id):
		return self.players()[id]

	def get_element_by_id(self, id):
		player = self.get_player_by_id(id)
		return (player.name,self.monthly_batting_perf_for(player.name))

	def list_top_batsmen(self, n, filter_type = DAILY_FILTER):
		top_batsmen = []
		if filter_type == DAILY_FILTER:
			top_batsmen = self.daily_batting_performance_records()

		if filter_type == MONTHLY_FILTER:
			top_batsmen = self.monthly_batting_performance()
		
		return top_batsmen[:n]

	def daily_batting_performance_records(self):
		'''
			returns a list of tuple(name,date,score)
		'''
		batting_records = []
		for player_name in self.daily_records:
			batting_records.extend(self.daily_batting_performance(player_name))
		if batting_records:
			return sorted(batting_records, key = lambda a : a[2].batting_score, reverse = True)
		return batting_records
	
	def daily_batting_performance(self, player_name, start = None, end = None):
		'''
			Default: Returns the data for the most recent date
		'''
		latest_date = self.all_dates[0]

		player_daily_records = self.daily_records.get(player_name,{})
		return [(dt, player_name, record) for dt, record in player_daily_records.items() if record.attended and dt.day == latest_date.day and (dt.month == latest_date.month and dt.year == latest_date.year)]


	def monthly_batting_performance(self):
		monthly_performance = {}
		player_batting_score = {}
		for player_name in self.monthly_records:
			player_batting_record = self.monthly_batting_perf_for(player_name)
			player_batting_score[player_name] = [batting_score for mth, year, batting_score in player_batting_record]
			monthly_performance[player_name] = player_batting_record
		 
		players = sorted(player_batting_score, 
					key = lambda player_name:player_batting_score.get(player_name,0.0), reverse = True)
		return [(player,monthly_performance.get(player,[])) for player in players]

	def monthly_batting_perf_for(self, player_name, year = None):
		if not year:
			latest_date = self.all_dates[0]
			year = latest_date.year
		player_monthly_records = self.monthly_records.get(player_name,{}).get(year,{})
		records = sorted(player_monthly_records, key = lambda a: a[0] )
		#print (player_monthly_records)
		return [(mth, year, record.aggregated_batting_score) for mth, record in records]
		
	
def generate_dates():
	now = datetime.datetime.now()
	for year in range(2015, 2020):
		for month in list(range(1,now.month+1)):
			for dt in range(1,now.day+1,7):
				yield datetime.date(year,month,dt)

def process_dates(perf_records):
	all_dates = sorted(generate_dates(), key = lambda a : (a.year, a.month, a.day), reverse = True)
	perf_records.all_dates = all_dates
	return all_dates

def generate_player_record(total_records = 16):
	perf_records = PlayerPerfRecords()
	all_dates = process_dates(perf_records)
	
	for id_val in range(total_records):
		player_name = names.get_full_name(gender='male')
		player_detail = player_record(
								id = id_val,
								name = player_name,
								age = random.randint(20,50),
								email = "",
								address = "",
								phone=random.randint(1000000000, 9999999999),
								add_record = "  Input Score")
		perf_records.player_details[player_name] = player_detail
		daily_records, monthly_records = generate_practice_record(all_dates,player_detail)
		perf_records.daily_records[player_name] = daily_records
		perf_records.monthly_records[player_name] = monthly_records
	return perf_records

def generate_practice_record(all_dates,player_detail):
	daily_records = {}
	monthly_records = defaultdict(list)
	prev_month = None
	aggregated_batting_score = 0.0
	for dt in all_dates:
		balls_faced = 0
		balls_bowled = 0
		attended = random.choice((True,False))
		if attended:
			balls_faced = random.randint(1,101)
			balls_bowled = random.randint(1,100)
		batting_score =  sum(random.randint(1,3) for i in range(balls_faced))
		dr = daily_record(
							id = "daily_{}".format(player_detail.id),
							player_record = player_detail,
							date = dt,
							attended = attended,
							batting_score =  batting_score,
							bowling_score = sum(random.randint(1,3) for i in range(balls_bowled)),
							balls_faced = balls_faced,
							balls_bowled = balls_bowled,
							fielding_score = 0
					)
		aggregated_batting_score += batting_score
		if dt.month != prev_month:
			mr = monthly_aggregation_record(
									id = "monthly_{}".format(player_detail.id),
									player_record = player_detail,
									date = dt,
									aggregated_batting_score = aggregated_batting_score)
			aggregated_batting_score = 0.0
			monthly_records[dt.year].append((dt.month,mr))
		
		prev_month = dt.month
		daily_records[dt] = dr
	return (daily_records, monthly_records)

#Data Generator
all_records = generate_player_record()
