import requests
import sys
import re

baseUrl = "https://api.instatus.com"
bearer_token = "8d16333936e72e705980878e18c95976"

def process_pages():
    url = f"{baseUrl}/v1/pages"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        data = response.json()

        # Check if the JSON data is empty or null
        if not data:
            print("JSON data is empty or null")
            sys.exit(1)
        else:
            # Extract the value of "page_id"
            page_id = data[0].get("id")

            if page_id is not None:
                print("Page ID:", page_id)
                return page_id
            else:
                print("Unable to find 'page_id' in JSON data")
                sys.exit(1)
    else:
        print(f"Request failed with status code {response.status_code}")
        sys.exit(1)

def validate_email(email):
    # Regular expression pattern for email validation
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if re.match(pattern, email):
        print("Valid email:", email)
    else:
        print("Invalid email:", email)
        sys.exit(1)

def process_components(page_id):
    url = f"{baseUrl}/v1/{page_id}/components"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        data = response.json()

        # Process the components data
        if not data:
            print("Components data is empty or null")
            sys.exit(1)
        else:
            # Extract information for the first component
            component_id = data[0].get("id")
            component_name = data[0].get("name")
            component_order = data[0].get("order")
            component_unique_email = data[0].get("uniqueEmail")

            if component_id is not None:
                print("Component ID:", component_id)
            else:
                print("Unable to find 'id' in component data")
                sys.exit(1)

            if component_name is not None:
                print("Component Name:", component_name)
            else:
                print("Unable to find 'name' in component data")
                sys.exit(1)

            if component_order is not None:
                print("Component Order:", component_order)
            else:
                print("Unable to find 'order' in component data")
                sys.exit(1)

            if component_unique_email is not None:
                print("Component Unique Email:", component_unique_email)
                validate_email(component_unique_email)
            else:
                print("Unable to find 'uniqueEmail' in component data")
                sys.exit(1)

            return component_id, component_name, component_order, component_unique_email
    else:
        print(f"Request failed with status code {response.status_code}")
        sys.exit(1)

def process_components_info(page_id, component_id, component_name, component_order, component_unique_email):
    url = f"{baseUrl}/v1/{page_id}/components/{component_id}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        data = response.json()

        # Process the components info data
        if not data:
            print("Components info data is empty or null")
            sys.exit(1)
        else:
            # Extract information for the component
            comp_id = data.get("id")
            comp_name = data.get("name")
            comp_order = data.get("order")
            comp_unique_email = data.get("uniqueEmail")

            if comp_id is not None:
                print("Component ID:", comp_id)
                if comp_id == component_id:
                    print("Component ID matches the previous call")
                else:
                    print("Component ID does not match the previous call")
                    sys.exit(1)
            else:
                print("Unable to find 'id' in component info data")
                sys.exit(1)

            if comp_name is not None:
                print("Component Name:", comp_name)
                if comp_name == component_name:
                    print("Component Name matches the previous call")
                else:
                    print("Component Name does not match the previous call")
                    sys.exit(1)
            else:
                print("Unable to find 'name' in component info data")
                sys.exit(1)

            if comp_order is not None:
                print("Component Order:", comp_order)
                if comp_order == component_order:
                    print("Component Order matches the previous call")
                else:
                    print("Component Order does not match the previous call")
                    sys.exit(1)
            else:
                print("Unable to find 'order' in component info data")
                sys.exit(1)

            if comp_unique_email is not None:
                print("Component Unique Email:", comp_unique_email)
                if comp_unique_email == component_unique_email:
                    print("Component Unique Email matches the previous call")
                else:
                    print("Component Unique Email does not match the previous call")
                    sys.exit(1)
                validate_email(comp_unique_email)
            else:
                print("Unable to find 'uniqueEmail' in component info data")
                sys.exit(1)
    else:
        print(f"Request failed with status code {response.status_code}")
        sys.exit(1)

def validate_updates(update):
    update_id = update.get("id")
    created_at = update.get("createdAt")
    incident_id = update.get("incidentId")

    if update_id is not None and created_at is not None and incident_id is not None:
        print("Valid update:")
        print("Update ID:", update_id)
        print("Created At:", created_at)
        print("Incident ID:", incident_id)
    else:
        print("Invalid update:")
        print("Update ID:", update_id)
        print("Created At:", created_at)
        print("Incident ID:", incident_id)
        sys.exit(1)

def process_incidents(page_id):
    url = f"{baseUrl}/v1/{page_id}/incidents"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    response = requests.get(url, headers=headers)

    # Check the response
    if response.status_code == 200:
        data = response.json()

        # Check if the JSON data is empty or null
        if not data:
            print("Incidents data is empty or null")
            sys.exit(1)
        else:
            # Process each incident
            for incident in data:
                updates = incident.get("updates")

                if updates:
                    print("Processing updates for Incident ID:", incident.get("id"))
                    for update in updates:
                        validate_updates(update)
                else:
                    print("No updates found for Incident ID:", incident.get("id"))
                    sys.exit(1)
    else:
        print(f"Request failed with status code {response.status_code}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        page_id = process_pages()
        component_id, component_name, component_order, component_unique_email = process_components(page_id)
        process_components_info(page_id, component_id, component_name, component_order, component_unique_email)
        process_incidents(page_id)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)  # Exit the script with a non-zero status code
