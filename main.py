import requests
from Table_class import Table
from Find_event import Links_Generator

last_ten_events = Links_Generator()
last_ten_events.get_events_links('https://domtel-sport.pl/wyniki,index,1,all,all,11')
last_ten_events.get_events_results_links()

print(last_ten_events.events_results_links_list)



# requested_html = requests.get(
#     'https://wmaci2023.domtel-sport.pl/?seria=0&runda=3&konkurencja=MTJ_35&dzien=&impreza=6')
#
# event_results = Table(requested_html)
# event_results.get_headers()
# event_results.get_rows()
# event_results.display_table()
