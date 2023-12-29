# ----
# $1 is the properties file
# ----
PROPS=$1
if [ ! -f ${PROPS} ] ; then
    echo "${PROPS}: no such file" >&2
    exit 1
fi

# ----
# getProp()
#
#   Get a config value from the properties file.
# ----
function getProp()
{
    grep "^${1}=" ${PROPS} | sed -e "s/^${1}=//"
}

# ----
# getCP()
#
#   Determine the CLASSPATH based on the database system.
# ----
function setCP()
{
    case "$(getProp db)" in
	firebird)
	    cp="../lib/firebird/*:../lib/*"
	    ;;
	oracle)
	    cp="../lib/oracle/*"
	    if [ ! -z "${ORACLE_HOME}" -a -d ${ORACLE_HOME}/lib ] ; then
		cp="${cp}:${ORACLE_HOME}/lib/*"
	    fi
	    cp="${cp}:../lib/*"
	    ;;
	mssql)
            cp="../lib/mssql-jdbc-9.2.0.jre8.jar:../lib/*"
	    ;;
	postgres)
	    cp="../lib/postgres/*:../lib/*"
	    ;;
	mysql)
       echo "!! GET MySQL JDBC Driver first into 'lib/' directory.!!!!"
	    cp="../lib/mysql/*:../lib/*"
	    ;;
	tidb)
       echo "!! GET MySQL JDBC Driver first into 'lib/' directory.!!!!"
	    cp="../lib/mysql/*:../lib/*"
	    ;;
	yugabyte)
	    cp="../lib/yugabyte/*:../lib/*"
	    ;;
	tibero)
	    cp="../lib/tibero/*"
	    if [ ! -z "${TB_HOME}" -a -d ${TB_HOME}/client/lib/jar ] ; then
		cp="${cp}:${TB_HOME}/client/lib/jar/tibero6-jdbc.jar"
	    fi
	    cp="${cp}:../lib/*"
	    ;;
	db2)
	    cp="${cp}:../lib/*"
	    cp="${cp}:../lib/db2/*"
	    ;;
    esac
    myCP=".:${cp}:../dist/*"
    export myCP
}

# ----
# Make sure that the properties file does have db= and the value
# is a database, we support.
# ----
case "$(getProp db)" in
    firebird|oracle|postgres|mysql|tidb|yugabyte|mssql|tibero|db2)
	;;
    "")	echo "ERROR: missing db= config option in ${PROPS}" >&2
	exit 1
	;;
    *)	echo "ERROR: unsupported database type 'db=$(getProp db)' in ${PROPS}" >&2
	exit 1
	;;
esac

