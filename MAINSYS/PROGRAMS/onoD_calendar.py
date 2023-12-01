from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from googleapiclient.discovery import build
from google.auth import load_credentials_from_file
import datetime
import japanize_kivy

class CalendarApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        label = Label(text='一日の予定:')
        layout.add_widget(label)

        SCOPES = ['https://www.googleapis.com/auth/calendar']
        calendar_id = 'j5gr4sa@gmail.com'
        gapi_creds = load_credentials_from_file(
            'MAINSYS\JSON\j5g-p-403802-f6d11f806041.json',
            SCOPES
        )
        service = build('calendar', 'v3', credentials=gapi_creds[0])

        today = datetime.date.today()
        start_of_day = datetime.datetime(today.year, today.month, today.day, 0, 0, 0).isoformat() + 'Z'
        end_of_day = datetime.datetime(today.year, today.month, today.day, 23, 59, 59).isoformat() + 'Z'

        event_list = service.events().list(
            calendarId=calendar_id, timeMin=start_of_day, timeMax=end_of_day,
            maxResults=10, singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = event_list.get('items', [])
        schedule = "[今日の予定]\n"

        for event in events:
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            end_time = event['end'].get('dateTime', event['end'].get('date'))
            summary = event['summary']

            if 'date' in start_time:
                schedule += f'{start_time}: {summary} (終日)\n'
            else:
                schedule += f'{start_time} ～ {end_time}: {summary}\n'

        schedule_label = Label(text=schedule)
        layout.add_widget(schedule_label)

        return layout

if __name__ == '__main__':
    CalendarApp().run()