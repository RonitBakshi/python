import subprocess

def append_upstream_endpoint(conf_file, new_endpoint):
    try:
        # Read the current content of the .conf file
        with open(conf_file, 'r') as file:
            lines = file.readlines()

        # Find the position where the new server should be added
        upstream_found = False
        insert_position = -1

        for i, line in enumerate(lines):
            if line.strip().startswith('upstream'):
                upstream_found = True
            if upstream_found and line.strip().startswith('}'):
                insert_position = i
                break

        if insert_position == -1:
            raise Exception("Upstream block not found in the configuration file")

        # Insert the new server endpoint before the closing bracket
        lines.insert(insert_position, f'    server {new_endpoint};\n')

        # Write the updated content back to the file
        with open(conf_file, 'w') as file:
            file.writelines(lines)

        print(f"Successfully added {new_endpoint} to the upstream configuration.")
        
        # Reload NGINX to apply the new configuration
        reload_nginx()

    except Exception as e:
        print(f"An error occurred: {e}")

def reload_nginx():
    try:
        # Run the command to reload NGINX
        subprocess.run(['systemctl', 'reload', 'nginx'], check=True)
        print("NGINX reloaded successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Failed to reload NGINX: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
conf_file_path = '/home/tisuper/Desktop/workspace/new_upstream.conf'
new_server = 'localhost:8006'

append_upstream_endpoint(conf_file_path, new_server)
