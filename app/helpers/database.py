import pymysql
import sys
import simplejson as json


# Returns MySQL database connection
def con_db(host, port, user, passwd, db):
    try:
        con = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)

    except pymysql.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    return con


def query_db(con, dict):
    data_array = []

    # Request args
    home = dict["home"]
    year_built = dict["year_built"]
    zip_code = dict["zip_code"]
    list_price = dict["list_price"]
    beds = dict["beds"]
    baths = dict["baths"]
    sqft = dict["sqft"]
    dom = dict["dom"]
    parking = dict["parking"]
    prediction = dict["prediction"]
    bike_score = dict["bike_score"]
    transit_score = dict["transit_score"]
    walk_score = dict["walk_score"]
    order_by = dict["order_by"]
    sort = dict["sort"]

    # Query database
    cur = con.cursor()
    cur.execute(
        """
        SELECT DISTINCT home_index.home, list_price, prediction*sqft, prediction*sqft-list_price AS difference,url, neighborhood
        FROM home_index
        JOIN home_url ON home_index.home = home_url.home
		WHERE sqft > 0 AND beds >= {1} AND list_price <= {0}
        ORDER BY difference DESC
        """.format(list_price, beds)
    )

    data = cur.fetchall()
    for home in data:
        index = {}

        index["home"] = home[0]
        index["list_price"] = home[1]
        index["prediction"] = home[2]
        index["difference"] = home[3]
        index["home_url"] = home[4]
        index["neighborhood"] = home[5]

        


        data_array.append(index)

    cur.close()
    con.close()
    return data_array
