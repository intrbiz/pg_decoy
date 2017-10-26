# pg_decoy

PG Decoy is a simple honey pot system for PostgreSQL implemented as a Foreign Data Wrapper, built on top of Multicorn.

## PostgreSQL Honey Pots

PG Decoy allows you to create fake tables which when queried raise the alarm.  This allows you to detect an attacker which has found a way to execute SQL in your database, EG: via an SQL injection vulnerability in your web app.  An attacker can be lured towards these fake tables to distract them and then detect them.

## Installation

PG Decoy is built atop of Multicorn, follow the Multicorn installation instructions.  Then install the Multicorn extension into your database:

    psql> CREATE EXTENSION multicorn;

Next we need to install the PG Decoy Python modules:

    chris@local:PGDecoy> sudo python ./setup.py install
    
Next we can setup a foriegn server, which is handled by the PG Decoy Foriegn Data Wrapper.  At the server level we configure how and where alerts should be raised:

    CREATE SERVER my_decoy FOREIGN DATA WRAPPER multicorn OPTIONS (
        wrapper 'PGDecoy.PGDecoyFDW',
        host 'demo.bergamot-monitoring.org',
        key 'SSmV5Zxq54SLS280M3sNFPNaHlQTbhDGVSK4yLyYjO39eWgZpLHxuDIt2K7aghd-lflszCkjLp0OTQq-dySll1oKZtRO3iSAP0XowndW',
        trap '2979259f-9599-44e5-b797-670458141c84',
        driver 'bergamot'
    );

Next we need to create some fake tables, this is just a case of creating some Foreign Tables:

    CREATE FOREIGN TABLE customers (
        id UUID,
        username TEXT,
        password_hash TEXT,
        email TEXT,
        full_name TEXT,
        pref_name TEXT,
        mobile TEXT
    ) 
    SERVER my_decoy
    OPTIONS (
        pot 'customer'
    );

## Webhook Driver

Rather than raising alerts in Bergamot Monitoring, you can simply fire a webhook which can be processed with any HTTP server:

    CREATE SERVER webhook_test FOREIGN DATA WRAPPER multicorn OPTIONS (
        wrapper 'PGDecoy.PGDecoyFDW',
        url 'http://127.0.0.1/honey',
        driver 'webhook'
    );

    CREATE FOREIGN TABLE decoy_web (
        test character varying,
        test2 character varying
    ) 
    SERVER webhook_test
    OPTIONS (
        pot 'test'
    );

## State Of Play

PG Decoy is currently a proof of concept, hopefully I'll expand upon it.
