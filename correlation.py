
import json
import math

class correlation(object):
	def __init__(self, file_to_read):
		"""This class calculates the coefficient of correlation 
		of certain events where a person turns into squirrel in 
		certain evenings. In order to find out the reason why it 
		is happening to him, he started keeping all of his daily
		activities as logs given in log.txt. So the information
		here is the list of events of each day what he did and 
		if he turned into squirrel or not in that particular evening.  
		"""
		self.file_to_read = file_to_read

	def read_file(self, file_name):
		"""Reads a JSON format file.

		Parameters
		----------
		file_name: Name of the file

		Returns
		-------
		file_data: str
             data contained in the file. 
		"""
		with open(file_name, 'r') as file:
		    file_data = json.load(file)
		    return file_data

	def remove_duplicates(self, json_content, key_name):
		"""Stores strings into a list while filtering out if 
		already the same string exists.

		Parameters
		----------
		json_content: A JSON data structure.
		key_name: Name of the key in the JSON data from where
		          the strings will be appended to the list.

		Returns
		-------
		activities: list
		    A list of strings
		"""
		activities = []
		for items in json_content:
			for value in items[key_name]:
				if value not in activities:
					activities.append(value)
		return activities
		
	def occurences(self, activities, json_details):
		"""Calculation of the occurences of being squirrel or not
		versus each event the person mentioned in his daily routine.

		Parameters
		----------
		activities: A list of all the daily tasks that the person 
		    usually do or have done.
		json_details: The log file the person has maintained 
		    json data structure.

		Returns
		-------
		statistics: dict
		    All statistics stored into this dictionary for each event
		    and being or not being a squirrel. 
		"""
		statistics = {}

		for activity in activities:
			statistics[activity] = {}
			statistics[activity]['No Squirrel and ' + activity] = 0
			statistics[activity]['Squirrel and ' + activity] = 0
			statistics[activity]['No Squirrel and ' + 'No ' + activity] = 0
			statistics[activity]['Squirrel and ' + 'No ' + activity ] = 0

			for items in json_details:
				if items['Squirrel'] == False and activity in items['Events']:
					statistics[activity]['No Squirrel and ' + activity] += 1 
				if items['Squirrel'] == True and activity in items['Events']:
					statistics[activity]['Squirrel and ' + activity] += 1	
				if items['Squirrel'] == False and activity not in items['Events']:
					statistics[activity]['No Squirrel and ' + 'No ' + activity] += 1	
				if items['Squirrel'] == True and activity not in items['Events']:
					statistics[activity]['Squirrel and ' + 'No ' + activity ] += 1	
		return statistics

	def calculate_statistics(self, statistics_data):
		"""Calculate the statistics or phi coefficient. See WIKI link below
		https://en.wikipedia.org/wiki/Phi_coefficient.

		Parameters
		----------
		statistics_data: The numerical data of all events and occurences depends on
		    the end result.

		Returns
		-------
		result_coefficient_correlation: dict
		    The result against all events are stored in this dictionary.
		"""
		result_coefficient_correlation = {}
		for items, values in statistics_data.items():
			counts_list = list(values.values())
			numerator = counts_list[1] * counts_list[2] - counts_list[0] * counts_list[3]
			denominator = (counts_list[2] + counts_list[0]) * (counts_list[3] + counts_list[1]) * \
			            (counts_list[2] + counts_list[3]) * (counts_list[0] + counts_list[1])
			result = numerator/	math.sqrt(denominator)
			result_coefficient_correlation[items] = result
		return result_coefficient_correlation
	
	def give_interpretation(self, details):
		"""Interpretes or explains the result.

		Parameters
		----------
		details: A dictionary of all the results.

		Returns
		-------
		interpretation: str
		    A text displaying which events or factors actually led the person
		    turn into squirrel. 
		"""
		get_nearest_neg = 0
		get_nearest_pos = 0
		activity_neg = ""
		activity_pos = ""
		
		res = list(details.values())
		get_nearest_neg = min(res, key=lambda HN:abs(HN-(-1)))
		get_nearest_pos = min(res, key=lambda HP:abs(HP-1)) 

		for activity, result in details.items():
			if get_nearest_neg == result:
				activity_neg += activity
			if get_nearest_pos == result:
				activity_pos += activity
		
		interpretation = "The negative correlation is "  + str(get_nearest_neg) + " : " + activity_neg \
		                 + " and the postive correlation is " + str(get_nearest_pos) + " : " + activity_pos	\
		                 + ". The reason of this fate is due to the correlations mentioned."	
		return interpretation

################################################ MAIN ####################################################


file_path = 'log.txt'

cr = correlation(file_path) 

contents = cr.read_file(file_path)

acti = cr.remove_duplicates(contents, 'Events')

stats = cr.occurences(acti, contents)

calculation = cr.calculate_statistics(stats)

final_report = cr.give_interpretation(calculation)

print(final_report)

############################################# END OF MAIN #################################################