import json
import requests

API_COUNTER = 0
REQUESTS = 0


def get_author_info(api_key, author_id):
    global API_COUNTER
    base_url = "https://api.elsevier.com/content/search/author?"
    url = (base_url + "query=au-id(" + author_id + ")&apiKey=" + api_key)  # URL para la consulta al API SCOPUS

    print("\nRequest to:", url.upper())
    print("Count: ", API_COUNTER)
    resp = requests.get(url,
                        headers={'Accept': 'application/json', 'X-ELS-APIKey': api_key})  # Configuración de headers"
    API_COUNTER += 1
    return json.loads(resp.text.encode('utf-8'))


def scopus_id_from_file():
    file = open("IdScopusRUPA.txt", "r")
    authors_list = file.read().split("|")
    return authors_list


def main():
    global REQUESTS
    api_keys = ["dd2748a194ea17342057a709890fcb9a",
                "f584c9b504c17728720bfb878ac29965"]
    output_file = open("scopus_y_orcid.txt", "a")
    for api in api_keys:
        authors_ids = scopus_id_from_file()
        for field in authors_ids:
            info = field.split(",")
            id = info[0]
            worker_number = info[1]
            data = get_author_info(api, id)
            entry = data['search-results']['entry'][0]
            try:
                orcid = entry['orcid']
                output_file.write(id + "|" + orcid + "|" + worker_number + "\n")
            except KeyError:
                print(id + " no tiene orcid")
        break


if __name__ == '__main__':
    main()
