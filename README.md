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
5. Analytics Dashboard (D3js)

#### C. Setup

**Setup Azure VM**

   - Option: Ubuntu Server 14.04 LTS
   - Size: Standard DS11 v2 (2 cores, 14 GB memory)
   - Location: East US
   - DNS Name: auimbigdata2.eastus.cloudapp.azure.com
   - Static IP: Yes
   - Use SSH Key: Yes

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

restart the database

```
$ sudo /etc/init.d/postgresql restart
```

**Install Kafka**

*reference:* [https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-14-04](https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-14-04)

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
```

start the Kafka Server

```
$ nohup ~/kafka/bin/kafka-server-start.sh ~/kafka/config/server.properties > ~/kafka/kafka.log 2>&1 &
```

**Install Psycopg PostgreSQL adapter for Python**

```
$ sudo service postgresql stop
$ sudo apt-get install python-psycopg2
$ sudo service postgresql start
```

**Install Flask (python web framework)**

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

install flask

```
$ pip install Flask
```

install twitter bootstrap for flask

```
$ pip install flask-bootstrap
```

install psycopg2 inside virtualenv

```
$ pip install psycopg2 
```

#### D. Running the Data Pipeline


#### E. Dashboard

