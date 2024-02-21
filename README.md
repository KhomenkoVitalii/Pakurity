# Software developer test task.

1. Create a Google Airflow DAG which reads random timeseries data ({random_character, random_digit}) 
which is in the BigQuery table (you need to write a simple shell script which publishes that random crap there :). 
And generates every 5 minutes an aggregated value into another BQ table. 
The output includes the sum of random_digits for each character and max value  and count for all alphabet. E.g. generation:
‘B’, 5
‘Z’, 1
‘B’, 2
Output:
Timestamp (rounded to 1 minute), ‘B’, 7,5,3  (because last minute we had 5+2 for ‘B’ , total 3 outputs, 5 was the max)
Timestamp (rounded to 1 minute),‘Z’,1,5,3 (cause ‘Z’ was only one time)


2. Setup a simple GKE docker container with nginx web-server
Setup export of web access logs from this container into GCS bucket using Google Cloud Logging sink.
Create a Google Airflow DAG which reads the text files parses that with regular expressions and stores in the BigQuery. 
Write also a test case for this Airflfow task, using Unit testing approach for streaming data. You’ll need dynamically generate the test strings with some delay between them, properly assign timestamps, assess the result with asserts.


3. Create a Python script which reads an OpenAPI specification file (JSON) and adds an example to each parameter with a basic datatype. Practice with some popular OpenAPI files (for example take them from the google dork search inurl:"swagger-ui/index.html"). See the OpenAPI specification for basic types and examples:
https://swagger.io/docs/specification/data-models/data-types/  
https://swagger.io/docs/specification/adding-examples/  


4. Create a script which patches your OpenAPI parsing Python script using AST approach and changes the example strings to some other.


Branches:
1. 'working_with_airflow' - branch with first and second tasks
2. 'working_with_open_api' - branch with third and fourth tasks
