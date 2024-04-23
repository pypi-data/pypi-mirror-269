#=============================================================#
###  CREATED AT     : 29 FEBRUARI 2024                      ###
###  UPDATED AT     : 07 MARET 2024                         ###
###  COPYRIGHT      : ANDRI ARIYANTO                        ###
###  DESCRIPTION    : Module untuk pembuatan spark session  ###
#=============================================================#

from pyspark.sql import SparkSession

def sparkSession(appname="Bribrain Spark Session", executor="small", instances=2, cores=4, memory=4, overhead=2):
  """Membuat spark session yang dapat digunakan untuk proses data engineering

  Args:
      appname (str): Nama dari spark session
          (default is Bribrain Spark Session)
      executor (str): Standard resource yang dapat dipilih untuk spark session 
          (optional is small, medium, high, custom)
          (default is small)
          (notes is small (2,4,4,2), medium (4,4,6,2), high (6,5,8,4))
      instances (int): Config untuk menentukan instance spark session
          (default is 2)
      cores (int): Config untuk menentukan cores spark session
          (default is 4)
      memory (int): Config untuk menentukan memory spark session
          (default is 4)
      overhead (int): Config untuk menentukan overhead spark session
          (default is 2)
    
  Returns:
      pyspark.sql.session.SparkSession: Spark session untuk proses data engineering
  """
  
  # pendefinisian resouce pyspark
  if   executor=="small":
    config = [2, 4, 4, 2]
  elif executor=="medium":
    config = [4, 4, 6, 2]
  elif executor=="high":
    config = [6, 5, 8, 4]
  elif executor=="custom":
    config = [instances, cores, memory, overhead]
  
  # pembuatan spark session
  spark = SparkSession\
    .builder\
    .appName(appname)\
    .config("spark.sql.crossJoin.enabled", "true")\
    .config("spark.dynamicAllocation.enabled", "false")\
    .config("spark.executor.instances", "{}".format(config[0]))\
    .config("spark.executor.cores", "{}".format(config[1]))\
    .config("spark.executor.memory", "{}g".format(config[2]))\
    .config("spark.yarn.executor.memoryOverhead", "{}g".format(config[3]))\
    .config("spark.sql.broadcastTimeout", "36000")\
    .config("spark.sql.legacy.allowCreatingManagedTableUsingNonemptyLocation", "true")\
    .config("spark.ui.showConsoleProgress", "false")\
    .config("spark.network.timeout", 60)\
    .enableHiveSupport()\
    .getOrCreate()
    
  return spark