import argparse
import docker

def run_docker_command(docker_image, output_file=None):
    client = docker.from_env()
    volume_mapping = {"/Users/muskan/scanpiper/src": {"bind": "/home", "mode": "rw"}}
    entrypoint = "bash"
    command = "/home/docan.sh"  

    container = client.containers.run(
        docker_image,
        entrypoint=entrypoint,
        command=command,
        volumes=volume_mapping,
        remove=True,
        detach=True,
    )

    if output_file:
        with open(output_file, "w") as f:
            for line in container.logs(stream=True):
                f.write(line.decode("utf-8").strip() + "\n")
    else:
        for line in container.logs(stream=True):
            print(line.decode("utf-8").strip())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Docker command")
    parser.add_argument("-i", "--image", help="Name of the Docker image: `$docker images`", required=True)
    parser.add_argument("-o", "--output", help="Output file to write the Docker logs")
    args = parser.parse_args()

    run_docker_command(args.image, args.output)
