from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):

    page_size = 4
    # page_size_query_param = 'page_size'
    max_page_size = 10000
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return {
            'status':'success',
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'currentPage': self.page.number
            },
            'count': self.page.paginator.count,
            'total_page': self.page.paginator.num_pages,
            'current_data': len(data),
            'data': data
        }
    

def merge_variant(data):
    unique_options = {}

# Iterate through the data
    for item in data:
        option = item["option"]
        tags = item["tags"]
        
        # Check if the option already exists in the dictionary
        if option in unique_options:
            # If it exists, append the tags to the existing list
            unique_options[option]["tags"].extend(tags)
        else:
            # If it doesn't exist, create a new entry for the option
            unique_options[option] = {"option": option, "tags": tags}

    # Extract the unique options from the dictionary
    unique_data = list(unique_options.values())
    return unique_data