import requests
import icalendar


class OnlineICalendar:
    def __init__(self, icalendar_url: str):
        self.icalendar_url = icalendar_url
        self.icalendar_parser = icalendar.Calendar

    def make_calendar_request(self) -> requests.Response:
        return requests.get(self.icalendar_url)

    def get_calendar_data(self) -> str:
        requested_calendar = self.make_calendar_request()
        # Not a response we were expecting
        if requested_calendar.status_code != 200:
            raise requests.HTTPError(f'Error Status Code -> {requested_calendar.status_code}')

        return requested_calendar.text

    def get_events(self) -> list[dict]:
        calendar = self.icalendar_parser.from_ical(self.get_calendar_data())
        return calendar.walk("VEVENT")


if __name__ == '__main__':
    online_calendar = OnlineICalendar("https://bbhosted.cuny.edu/webapps/calendar/calendarFeed"
                                      "/3021d6b8993e4af2a3e71f9805b27fd1/learn.ics")
    for event in online_calendar.get_events():
        print(event.get('SUMMARY'))
