# active_record_py
Python Psql ORM

## Features
  - Dynamically creates Python object model for inheriting classes
  - SELECT, UPDATE and INSERT psql interactions
  - Asynchonous, cursor queries
  - Object validation
  - Query sanitation

## Overview

ActiveRecord is an object-relational manager for Python and Postgresql. Like any ORM, it dynamically defines object models in Python. The running themes are don't repeat yourself and easy access.

## Dependencies
  - psycopg2 (Psql binding)
  - colorama (Prettifying console outputs:... Ok, yeah, in hindsight this was great for me but bad for others. I'll write it out or something later)
  
 
## Getting started

Dump the contents of `./lib/` into your project's lib/src or whatever folder. (Again, the separate files is a bit of a bugger for others, but I'll sort it at some point)

Below outlines its basic use. The content is taken from `./example.py`. 
```ruby

from lib.active_record import ActiveRecord
####################################
# Create an example class
####################################
print("""
##
# ActiveRecord example: (Written for Psql, should work with others)
#
# The AR module provides data manipulation (DML) and data querying (DQL)
# through standard objects.
#
# There are three steps required to get started 
#
# 1) Install Psql and create the table "tv_shows"
# 2) Create class for the table
# 3) Connect to the database and load the definitions
##
""")

##
#  Create the new class
##
print("""
##
# AR automatically figures out the table name from the Camel
# Case singluar name. For example: "TvShow" will become "tv_shows". If
# you need a name to be singular, say for example "Data" add the foloowing 
# your model.
#		"pluralise = False"
##
""")
class TvShow(ActiveRecord):
	#pluralise = True
	pass

##
# Connect to the database
##
print("""
##
# Before initiating AR you'll need to connect to the database. This
# example is for Psql and only requires username, database and password
# but it'll probably work with other if you use all inputs:
#
# Param 1:				String user name
# Param 2:				String  database name
# Param 3:				String password
# Param 4 (optional):	String connector name "postgres", "mysql",...
# Param 5 (optional*):	Integer database prot number
#
# * If the Connector name isn't postgres then the port number will
# 	likely not match your database. I'd recommend passing 4 and 5 
#	together or exclude both.
##
""")
PASSWORD = False
if not PASSWORD:
	print("Error: You need to define PASSWORD at line 58")
	exit()
ActiveRecord.connect("postgres", "example", SET_THIS_PASSWORD_HERE)
##
# Load ActiveRecord definitions
##
print("""
##
# ActiveRecord dynamically builds object definitions from
# the database for data validation and query generation. In order
# to do this you need to tell it when to do it.
##
""")
ActiveRecord.load()
##
# Enable DEBUG mode. This'll print any query made by AR to the console.
##
print("""
##
# ActiveRecord support debug printing the queries to the console through
# through setting the @classmethod debug_mode.
#
# Since it's a class method, this can be enabled for specific classes only.
##
""")
ActiveRecord.debug_mode = True
########################################
# Interacting with the database
########################################
##
# Creating new records
##
print("""
##
# There are three ways to create new records:
#
# 1) Instantiate directly. (Doesn't create the record implicitly)
# 2) The create() method. (Instantiates, saves and returns new record)
# 3) The find_or_create_by() method. (Queries the database for an existing record first)
#
# NOTE: 
#	You can add a default filter condition to the class to save on writing
# 	the same query numerous times or if you want to scope classes. For example:
#	say you have two categories. Old and new TV shows. You might create:
#
#	class OldTvShow(ActiveRecord):
#		proxy_table_class	= TvShow
#		default_filter = "year < 2000"
#	class NewTvShow(ActiveRecord):
#		proxy_table_class	= TvShow
#		default_filter = "year > 1999"
#
# 	In the above example, "proxy_table_class" effectively tells it the parent table name
#	but doesn't splice Python object functionality. If you want to extend the TV class use:
#
#	class InheritedTvShowClass(TvShow):
#		proxy_table_class = TvShow
##
""")
# New record without saving
houseMD 			= TvShow({"name":"House M.D.", "year": 2004})
print(houseMD)
# Save the record: This allocates an ID.
houseMD.save()
# New record saved at creation
boothAtTheEnd 		= TvShow.create({"name":"The Booth at the End", "year": 2010})
print(boothAtTheEnd)
print("==== NOTE: Check out the following three queries. You'll notice the second UPDATE doesn't happen ===")
eizel 				= TvShow.find_or_create_by([["name", "Eizel"], ["year", 2009], ["comment", "Çok iyi"]])
eizel 				= TvShow.find_or_create_by([["name", "Eizel"], ["year", 2009], ["comment", "Çok iyi"]])

print("""------
##
# Multi-INSERT:
#
# If you use the TvShow() approach to creating entries you can
# run an INSERT for all@
#
#		TvShow.multiInsert(setOfNewRecords)
##
""")

##
# Setting values
#
# ActiveRecord supports dotted and subscripted property setting. It will
# let you set any value whether a column or not, figuring out what should
# end up with the database when creating queries.
##
houseMD.comment 	= "Loved it!"
houseMD["comment"]	= "Loved it! Holds up after the years"
# Save it
houseMD.save()
# Retrieve it again. WARNING: Don't do this in production it's just for an example.
# There's little concurrency support in the library bar transactions handling.
print(TvShow.find_by("name = 'House M.D.'"))
print("---")
##
# Update existing records
##
houseMD.save()
##
# Querying the database
##
print("""
##
# Retrieving data from the database
#
# All query methods can take two / three forms of input parameter,
# a String, an Array of key values or (not sure about this, can't
# remember) a Hash (must do though, why'd you skip that?)
#
# WARNING: Ok, spent 20 seconds testing Hash. Doesn't support it
# apparently. Leave it with me, I'll implement it soon... My bad
#
# TODO: 
#	- enable passing operators through Array input
#	- use Array nesting to support AND / OR
##
""")
##
# Get every record
##
allTvShows 	= TvShow.get_all()
##
# Retrieve singe record
##
houseMD 	= TvShow.find_by("name = 'House M.D.'")
houseMD 	= TvShow.find_by([["name", "House M.D."]])
# houseMD = TvShow.find_by({"name": "House M.D."}) WORK IN PROGRESS
##
# Retrieve multiple records
##
tvShows	= TvShow.find_all_by("year > 2002")
tvShows	= TvShow.find_all_by([["year", 2004]])
for tvShow in tvShows:
	print(tvShow)
##
# Get random record
##
randomTvShow = TvShow.random()
########################
# Iteration
########################
print("""
####################
# Table cursors
#
# ActiveRecord supports basic cursors through the next()
# method and config properties. The config can be told
# how many records to cache during each next() call or 
# query on every call. There are two class properties and 
# one method that affect the next() method:
#
# next_filter:		String SQL condition that filters the results
# next_cache_size:	Integer number of records to cache for a cursor. Set
#					to False for non caching
#
# offset_next:		Integer how many records to skip before iterating
# 
#					
#####
""")
## 
# Ordered iteration
##
currentTvShow = TvShow.next()
while currentTvShow:
	print(currentTvShow)
	currentTvShow = TvShow.next()
```
