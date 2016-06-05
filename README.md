### Sales BI Real-time Dashboard
Alexander Mendoza, Jayadev Vallath and Maria Mendoza

#### A. Low Latency Data Pipeline Architecture
![](architecture.png)

#### B. Components
1. Data Generator (python)
2. PostgreSQL Database 9.4 (Third Party Software)
   + Replication
   + Logical Decoding
3. Kafka Producer (using Logical Decoding SQL Interface, python)
4. Analytics REST API (using Kafka Consumer to pickup messages on demand, python flask)
5. Analytics Dashboard (D3js, datamaps)

#### C. Setup

**Setup Azure VM**

   - Option: Ubuntu Server 14.04 LTS
   - Size: Standard DS11 v2 (2 cores, 14 GB memory)
   - Location: East US
   - DNS Name: auimbigdata2.eastus.cloudapp.azure.com
   - Static IP: Yes
   - Use SSH Key: Yes
   - Open TCP Port 80 for HTTP

**Install PostgreSQL 9.4**

```
$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install postgresql-9.4 postgresql-server-dev-9.4 postgresql-contrib-9.4
```

**Create salesbi user, database and setup replication**

```
$ sudo su - postgres
$ createuser -U postgres -d -e -E -l -P -r -s --replication salesbi
$ sudo adduser salesbi
$ sudo su - salesbi
$ createdb salesbi
```

add the below lines to `/etc/postgresql/9.4/main/postgresql.conf`

```
wal_level = logical
max_wal_senders = 8
wal_keep_segments = 4
max_replication_slots = 4
```

add the below lines to `/etc/postgresql/9.4/main/pg_hba.conf`

```
local   replication     all                 trust
host    replication     all  127.0.0.1/32   trust
host    replication     all  ::1/128        trust
```

**Install Psycopg PostgreSQL adapter for Python**

```
$ sudo service postgresql stop
$ sudo apt-get install python-psycopg2
$ sudo service postgresql start
```

**Install Kafka**

install dependencies `jre` and `zookeeper`

```
$ sudo apt-get update
$ sudo apt-get install default-jre
$ sudo apt-get install zookeeperd
```

create kafka user

```
$ sudo su -
$ useradd kafka -m
$ passwd kafka
$ adduser kafka sudo
```

install kafka binaries

```
$ su - kafka
$ mkdir -p ~/Downloads
$ wget "http://mirror.cc.columbia.edu/pub/software/apache/kafka/0.8.2.1/kafka_2.11-0.8.2.1.tgz" -O ~/Downloads/kafka.tgz
$ mkdir -p ~/kafka && cd ~/kafka
$ tar -xvzf ~/Downloads/kafka.tgz --strip 1
```

add the following lines to `~/kafka/config/server.properties`

```
delete.topic.enable = true
auto.create.topics.enable=true
```

start the Kafka Server

```
$ nohup ~/kafka/bin/kafka-server-start.sh ~/kafka/config/server.properties > ~/kafka/kafka.log 2>&1 &
```

**Install and prepare Python virtualenv**

install virtualenv

```
$ sudo apt-get install python-virtualenv
```

create project virtualenv

```
$ sudo su - salesbi 
$ mkdir webapi
$ cd webapi
$ virtualenv venv
```

activate virtualenv

```
$ . venv/bin/activate
```

**Install required Python packages for data pipeline**

install flask

```
(venv)$ pip install Flask
```

install flask socketio and eventlet

```
(venv)$ pip install flask-socketio
(venv)$ pip install eventlet
```

install twitter bootstrap for flask

```
(venv)$ pip install flask-bootstrap
```

install psycopg2

```
(venv)$ pip install psycopg2 
```

install python kafka client

```
(venv)$ pip install kafka-python
```

#### D. Prepare the database

```
$ sudo su - salesbi
$ psql

salesbi=# \i create_salesbi_1.sql
salesbi=# \i create_salesbi_2.sql
```

#### E. Running the Data Pipeline

**Start the kafka producer**

```
(venv)$ python salesbi-kafka-postgres-producer.py transaction_slot 5
```

where transaction_slot is the postgresql replication slot name and 5 is the sleep time in between pg_logical_slot_get_changes calls

This producer does the following:

+ create a new replication slot using given slot name
+ loop continuously until Ctrl-C or Keyboard Interrupt
+ for each loop iteration
    - read the logical changes from the replication slot 
    - format the data into json
    - send the formatted json data to topic with the same name as replication slot
    - sleep for a specified number of seconds
    - **note:** kafka is configured to auto create topics
+ drop the replication slot and close database connection

**Run the data generator**

```
(venv)$ python generator.py
```

**Start the webapi server**

```
(venv)$ python webapi.py runserver &
```

**Open the dashboard**

go to [http://auimbigdata2.eastus.cloudapp.azure.com/](http://auimbigdata2.eastus.cloudapp.azure.com/)

#### E. Dashboard

**References:**

Installing Apache Kafka

[https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-14-04](https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-14-04)

Python client for Apache Kafka

[https://github.com/dpkp/kafka-python](https://github.com/dpkp/kafka-python)

Installing PostgreSQL

[https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04)

Logical Decoding in PostgreSQL 9.4

[https://www.postgresql.org/docs/9.4/static/logicaldecoding-example.html](https://www.postgresql.org/docs/9.4/static/logicaldecoding-example.html)

Install Psycopg - Python adapter for PostgreSQL

[http://initd.org/psycopg/docs/install.html#installation](http://initd.org/psycopg/docs/install.html#installation)

Python Flask (web microframework) installation

[http://flask.pocoo.org/docs/0.11/installation/](http://flask.pocoo.org/docs/0.11/installation/)

Datamaps: Interactive maps for data visualization

[https://github.com/markmarkoh/datamaps/blob/master/README.md#getting-started](https://github.com/markmarkoh/datamaps/blob/master/README.md#getting-started)
