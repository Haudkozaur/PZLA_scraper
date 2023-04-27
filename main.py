from Find_event import Links_Generator
import PySimpleGUI as sg
from Fav_athls import Favourite
from PZLA_stats import PZLA
from Start_lists import Start_Lists
from GUI_run_class import GUI_run
from sub_GUI_run_class import sub_GUI_run
from Third_searching import Third_Searching
from input_encoding_func import encode_input
from Add_To_Favourites import Add_To_Fav

sg.theme('DarkTeal10')

last_ten_events = Links_Generator()
last_ten_events.get_events_links('https://domtel-sport.pl/wyniki,index,1,all,all,11')
last_ten_events.get_events_results_links()
last_ten_events.get_competitions_urls()

temp = Favourite()
temp.get_empty_table()

stats = PZLA('https://statystyka.pzla.pl/spis_imprez.php?Sezon=',
             'https://statystyka.pzla.pl/spis_imprez.php?Sezon=2023Z&FiltrM=&FiltrWoj=')
stats.create_basic_layout()
stats.create_basic_layout_domtel()

startlisty = Start_Lists('https://starter.pzla.pl/?Typ=888')
startlisty.produce_basic_layout()

third_searching = Third_Searching()
third_searching.create_basic_layout()

GUI_events = GUI_run()


class MainWindow:
    def __init__(self, events_names_list, competitions_lists_list):
        self.events_names_list = events_names_list
        self.competitions_lists_list = competitions_lists_list
        self.first_tab_layout = GUI_events.create_first_tab_layout(self.events_names_list)

        self.layout = [
            [sg.TabGroup([[sg.Tab('Events', self.first_tab_layout, key='-tab1-')],

                          [sg.Tab('Check recent results', stats.fourth_tab_layout, key='-tab3-')],
                          [sg.Tab('Athletes', temp.second_tab_layout, key='-tab2-')],
                          [sg.Tab('Advanced searching', stats.third_tab_layout, key='-tab4-')],
                          [sg.Tab('Check startlists', startlisty.fifth_tab_layout, key='-tab5-')],
                          [sg.Tab('Recent results', third_searching.sixth_tab_layout, key='-tab6-')],
                          ],
                         tab_location='topleft', enable_events=True, key='-tabgroup-')]]

        self.sub_windows = {}

        self.window = sg.Window('Domtel scraper 1.0', self.layout, size=(800, 600), resizable=False,
                                grab_anywhere=False,
                                grab_anywhere_using_control=False, keep_on_top=False)

    def run(self):
        # Main loop
        while True:

            event, values = self.window.read()
            print(event)
            match event:
                case sg.WIN_CLOSED:
                    self.window.close()
                    break
                case 'Submit':
                    GUI_events.get_atlete_PRs(values, temp, self.window)
                case 'Outdoor':
                    GUI_events.choose_outdoor(temp, self.window)
                case 'Indoor':
                    GUI_events.choose_indoor(temp, self.window)
                case 'Find events':
                    GUI_events.advanced_events_searching(values, stats, self.window)
                case 'find_events_PZLA_domtel':
                    GUI_events.find_season_results(values, self.window, stats)
                case 'Outdoor_season':
                    GUI_events.change_season_to_outdoor(self.window, stats)
                case 'Indoor_season':
                    GUI_events.change_season_to_indoor(self.window, stats)
                case 'Choose':
                    GUI_events.change_year(values, self.window, stats)
                case 'find_events_startlist':
                    GUI_events.get_startlists(values, startlisty, self.window)
                case 'See all':
                    GUI_events.show_all_startlists(startlisty, self.window)
                case 'find_events_recent':
                    GUI_events.find_and_display_recent_results(third_searching, last_ten_events, values, self.window)
                case '-add_athl1-' | '-add_athl2-' | '-add_athl3-' | '-add_athl4-' | '-add_athl5-':
                    favourite = Add_To_Fav()
                    favourite.get_active_tab_and_add_to_fav(self.window['-tabgroup-'].get(), values)
                case '-TABLE-':
                    print(self.window['-TABLE-'].get())
                case int():
                    self.event = event
                    sub_window = SubWindow(event, self.competitions_lists_list, self.events_names_list[self.event])
                    self.sub_windows[event] = sub_window


class SubWindow:
    def __init__(self, title, competitions_lists_list, events_names_list):
        self.events_names_list = events_names_list
        self.competitions_lists_list = competitions_lists_list
        self.title = title
        sub_GUI_events_temp = sub_GUI_run()
        sub_GUI_events_temp.create_sub_layout(self.competitions_lists_list, GUI, self.events_names_list)
        self.window = sub_GUI_events_temp.window
        # sub Loop
        while True:
            event, values = self.window.read()
            match event:
                case int():
                    sub_GUI_events_temp.chose_event(event, last_ten_events, GUI)
                case sg.WIN_CLOSED | 'back':
                    self.window.close()
                    break


GUI = MainWindow(last_ten_events.events_names_list, last_ten_events.competitions_lists_list)
GUI.run()
