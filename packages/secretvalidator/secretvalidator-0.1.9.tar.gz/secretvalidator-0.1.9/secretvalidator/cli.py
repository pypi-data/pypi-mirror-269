import click
import requests
import json
import os

@click.command()
@click.argument('service', nargs=1, type=click.Choice(['sonarcloud', 'snyk']))
@click.argument('secret', nargs=1)
@click.option('-r', '--response', is_flag=True, help='Print simple response (status/true/false).')
def validate(service, secret, response):
    """Run secret validation checks."""
    click.echo("Running secret validation checks...")
         # Get absolute path to urls.txt
    current_dir = os.path.abspath(os.path.dirname(__file__))
    urls_path = os.path.join(current_dir, 'urls.txt')
    
    # Check if urls.txt exists
    if not os.path.exists(urls_path):
        click.echo("Error: 'urls.txt' file not found.")
        return

    # Read file content
    with open(urls_path, 'r') as f:
        urls_content = f.read()
    
    urls = json.loads(urls_content)
    
    service_url = urls.get(service)

    if not service_url:
        click.echo(f"Error: URL for service {service} not found.")
        return
    
    headers = {}
    
    # Set headers for Snyk or SonarCloud
    if service == 'snyk':
        headers['Authorization'] = f'token {secret}'
    elif service == 'sonarcloud':
        headers['Authorization'] = f'Bearer {secret}'
    
    # Make HTTP request to the service
    response_data = requests.get(service_url, headers=headers)
            
    click.echo(f"Response status: {response_data.status_code}")
    
    if response_data.status_code == 200:
        click.echo(f"{service.capitalize()} secret validation successful!")
        
        # Check if -r option is specified
        if response:
            click.echo(f"Response status: {response_data.status_code == 200}")
        else:
            # Print JSON response
            try:
                json_response = response_data.json()
                click.echo("Response:")
                click.echo(json.dumps(json_response, indent=4))
            except json.JSONDecodeError:
                click.echo("Response is not a valid JSON.")
    else:
        click.echo(f"{service.capitalize()} secret validation failed!")
        
        # Check if -r option is specified
        if response:
            click.echo(f"Response status: {response_data.status_code == 200}")
        else:
            click.echo(f"Error: {response_data.text}")

if __name__ == '__main__':
    validate()
