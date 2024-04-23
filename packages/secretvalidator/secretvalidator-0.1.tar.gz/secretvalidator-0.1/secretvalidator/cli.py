import click
import requests
import json

@click.command()
@click.argument('secret', nargs=1)
@click.argument('service', nargs=1, type=click.Choice(['sonarcloud', 'snyk']))
def validate(secret, service):
    """Run secret validation checks."""
    click.echo("Running secret validation checks...")
    
    # Load URL from url.txt based on service
    with open('urls.txt', 'r') as f:
        urls = json.load(f)
    
    service_url = urls.get(service)
    
    if not service_url:
        click.echo(f"Error: URL for service {service} not found.")
        return
    
    # Make HTTP request to the service
    payload = {
        'secret': secret,
    }
    
    response = requests.post(service_url, data=json.dumps(payload))
    
    if response.status_code == 200:
        click.echo("Secret validation successful!")
        # Export the secret (Optional)
        click.echo(f"export SECRET={secret}")
    else:
        click.echo("Secret validation failed!")
        click.echo(f"Error: {response.text}")

if __name__ == '__main__':
    validate()
