# btcWarning

A Flask based version of this program is in development, however, in the mean time it can be run using a LAMP or MAMP stack. Presumably WAMP as well but this has not yet been tested. 

 To run this demo natively on your personal computer a number of software packages must be installed. These
instructions are tailored to mac users, however, it should be simple to adapt to any linux based OS.

STEPS:
1. Install the MAMP software package onto your computer. This program operates the APACHE and MYSQL
    servers used by this demo.
    > Once this is open, open the preferences. Under Ports set ports to default and under Web Server
        set the root directory to the htmlcssphp file within the BitcoinWarning file.
    > You can now access the website through a web browser at localhost:8888
    > The MYSQL database at is accessable through localhost:8888/phpMyAdmin
2. Next you must set up the MYSQL database. Open the following page in your browser:
      localhost:8888/phpMyAdmin/server_sql.php?db=
    > copy the following code into the box and run it to create the table:

CREATE TABLE `email_list`.`email_list` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `lastemail` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `lastemail%` int(11) NOT NULL,
  `confirmationsent` tinyint(1) NOT NULL,
  `lastmodified` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  `signuptime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `rsi` tinyint(1) NOT NULL,
  `up5` tinyint(1) NOT NULL,
  `up10` tinyint(1) NOT NULL,
  `up15` tinyint(1) NOT NULL,
  `up20` tinyint(1) NOT NULL,
  `up25` tinyint(1) NOT NULL,
  `up30` tinyint(1) NOT NULL,
  `down5` tinyint(1) NOT NULL,
  `down10` tinyint(1) NOT NULL,
  `down15` tinyint(1) NOT NULL,
  `down20` tinyint(1) NOT NULL,
  `down25` tinyint(1) NOT NULL,
  `down30` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

    > Next you will need to go to the User Accounts tab and create 2 new user accouts with
      the following information:
      
      username = python
      hostname = localhost
      password = nDM3KQyRmpmFNgAA
      priviledges = SELECT, INSERT, UPDATE
      
      username = btcwarning
      hostname = localhost
      password = P6iC2i7iNbn5Gci5
      priviledges = SELECT, INSERT, UPDATE, DELETE
      
3. Now you must install the ta-lib package used for RSI calculations:
    > Install the HOMEBREW package manager for MAC:
         Open terminal or another command line interface and enter the following:
              /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    > Now run the following command to install ta-lib:
        brew install ta-lib

4. Download and install ANACONDA from https://www.anaconda.com/download/#macos

5. Now you must install the modules used by the python portion of this program if you do
    not already have them:
    > Run the following on the command line:

pip3 install requests urllib3 chardet mysql-connector-python-rf deribit-api pandas pandas-datareader numpy TA-Lib

7. This program uses an API email client to avoid issues caused by blocked email ports on many residential ISPs. Elastic Email was used as it allows for thousands of free outgoing emails per month. If you sign up for this service all you will need to do is enter your API key and mailing address on the run_me.py file. If using another service much of the API integration may need to be modified. 

7. Using the SPYDER program within ANACONDA open the run_me.py file:
    > The top section contains options that can be modified by the user
    > When you are happy with the options you have selected, run the file and leave it running.
    > By default the system deletes old price data as it is started to prevent misleading results
      due to old data. It will take the program a short amount of time after startup to rebuild
      its price data to a usable level.

8. Now use the web portal at localhost:8888 to enter emails and notification options
    into the program




