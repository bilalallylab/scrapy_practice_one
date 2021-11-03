import betamax
from betamax_serializers import pretty_json
import requests
import os

CASSETTE_LIBRARY_DIR = 'cassettes_result'
if not os.path.exists(CASSETTE_LIBRARY_DIR):
    os.mkdir(CASSETTE_LIBRARY_DIR)


def main():
    session = requests.Session()
    betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
    recorder = betamax.Betamax(
        session, cassette_library_dir=CASSETTE_LIBRARY_DIR
    )

    with recorder.use_cassette('cassettes_output',
                               serialize_with='prettyjson',
                           match_requests_on=['method', 'uri', 'body'],
                           record='all'):
        session.get('https://httpbin.org/get')
        session.post('https://httpbin.org/post',
                     params={'id': '20'},
                     json={'some-attribute': 'some-value'})
        session.get('https://httpbin.org/get', params={'id': '20'})
        session.post('https://httpbin.org/post',
                     params={'id': '20'},
                     json={'some-other-attribute': 'some-other-value'})


if __name__ == '__main__':
    main()
