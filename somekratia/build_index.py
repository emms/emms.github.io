import json, datetime
import psycopg2
import sys
from urllib.request import urlopen


if len(sys.argv) != 2:
    print("no output file provided. using 'app/static/issue_index.json")
    output = 'app/static/issue_index.json'
else:
    output = sys.argv[1]
print(output)
def get_url_as_string(url):
    json_str = urlopen(url).read().decode('utf-8')
    return json_str


def get_url_as_json(url):
    return json.loads(get_url_as_string(url))


def create_geo_json_feature(issue, coordinates):
    return {
            "id": issue['id'],
            "type": "Feature",
            "geometry": {
                "type": "Point", "coordinates": coordinates
                },
            "properties": {
                    "category_origin_id": issue["category_origin_id"],
                    "latest_decision_date": issue["latest_decision_date"],
                }
            }


conn = psycopg2.connect("dbname='somekratia' user='somekratia' host='localhost' password='extemporizers735!laboriously'")
server = 'http://dev.hel.fi'
path = '/paatokset/v1/issue/?limit=1000&order_by=last_modified_time'
issue_index = []
issues = []
geo_json = {'type': 'FeatureCollection', 'features': issue_index}
while path is not None:
    url = "%s%s" % (server, path)
    request_start = datetime.datetime.now()
    print("loading %s" % url)
    data = get_url_as_json(url)
    request_end = datetime.datetime.now()
    print("loaded %sms" % (request_end - request_start))
    meta = data['meta']
    path = meta['next']
    issues += data['objects']

for issue in issues:
    print("%s - %s" % (issue['last_modified_time'], issue['subject']))
    point_count = 0
    if 'summary' not in issue:
        issue['summary'] = ""
    for geometry in issue['geometries']:
        if geometry['category'] == 'address' and len(geometry['coordinates']) == 2:
            point_count += 1
            print(str(geometry['coordinates']))
            issue_index.append(create_geo_json_feature(issue, geometry['coordinates']))
print("index contains %d issues with coordinates" % (len(issue_index)))


print("Writing index to 'issue_index.json'...")
with open(output, 'w') as outfile:
    json.dump(geo_json, outfile)
print("updating database")
cur = conn.cursor()
cur.execute("""DELETE FROM app_issue""")
cur.executemany("""INSERT INTO app_issue(id, title, summary,category_name, modified_time, last_decision_time) VALUES (%(id)s, %(subject)s, %(summary)s, %(category_name)s, %(last_modified_time)s, %(latest_decision_date)s)""", issues)
conn.commit()
cur.close()
conn.close()
print("DONE!")



