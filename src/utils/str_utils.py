import re

def remove_duplicates(domains: list, domain_type=None, list_of_dicts=False):
    '''
    Removes duplicates in a list or dictionary
    '''
    done = set()
    unique_list = []
    for domain in domains:
        if list_of_dicts:
            domain = domain[domain_type]
        if domain not in done:
            done.add(domain)
            unique_list.append(domain)
    return unique_list

def strip_domains(domains: list, domain_type: str):
    '''
    Strips domain name if it has http(s) and/or www. in front
    - Removes duplicates
    '''
    stripped_domains = []
    for domain in domains:
        domain[domain_type] = re.sub('^(http|https)://|/', '', domain[domain_type])
        domain[domain_type] = re.sub('^(www\.)', '', domain[domain_type])
        stripped_domains.append(domain[domain_type])
    unique_stripped_domains = remove_duplicates(domains=stripped_domains)
    return unique_stripped_domains

def combine_domain_lists(file_paths):
    combined_list = []
    for file in file_paths:
        with open(file, 'r') as f:
            l = [line.rstrip() for line in f.readlines()]
            combined_list.extend(l)
    unique_list = list(set(combined_list))
    return unique_list